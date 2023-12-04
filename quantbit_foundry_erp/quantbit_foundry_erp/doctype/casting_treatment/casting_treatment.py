# Copyright (c) 2023, Quantbit Technologies Pvt ltd and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class CastingTreatment(Document):


	def before_save(self):
		self.validate_total_quentity()
		self.validate_rejections()

	def before_submit(self):
		self.manifacturing_stock_entry()
		self.transfer_stock_entry()

	@frappe.whitelist()
	def get_pouring (self):
		if self.select_pouring and self.casting_treatment:

			cttwcasting = frappe.get_value("Foundry Setting",self.company,"ct_tw_casting") 
			ctswraw = frappe.get_value("Foundry Setting",self.company,"ct_sw_raw")
			for d in self.get("select_pouring"):
				items_doc= frappe.get_all("Casting Details" ,
													filters = {"parent": str(d.pouring)},
													fields = ["item_code","item_name","total_quantity","total_weight","target_warehouse","casting_weight","pattern","sales_order","casting_treatment_quantity"])
				for i in items_doc:
					self.append("casting_item",{
							'item_code': i.item_code ,
							'item_name': i.item_name,
							'pouring': d.pouring,
							'source_warehouse': i.target_warehouse ,
							'available_quantity': self.get_available_quantity(i.item_code , i.target_warehouse ),
							'quantity': (i.total_quantity - i.casting_treatment_quantity) ,
							'weight': i.total_weight ,
							'target_warehouse':cttwcasting,
							"casting_weight": i.casting_weight,
							"sales_order":i.sales_order
						},),


					self.append("quantity_details",{
							'item_code': i.item_code ,
							'item_name': i.item_name,
							'pouring': d.pouring,
							'sales_order' : i.sales_order,
			
						},),

					casting_treatment = frappe.get_all("Casting Treatment Details" ,
													filters = {"parent": i.pattern , 'casting_items_code': i.item_code , 'casting_treatment' : self.casting_treatment },
													fields = ["casting_treatment","casting_items_code","casting_item_name","raw_item_code","raw_item_name","required_quantity"])
					for ct in casting_treatment:
						self.append("raw_item",{
								'item_code': ct.casting_items_code ,
								'item_name': ct.casting_item_name,
								'pouring': d.pouring,
								'raw_item_code':ct.raw_item_code,
								"raw_item_name": ct.raw_item_name,
								"total_quantity": ct.required_quantity * (i.total_quantity - i.casting_treatment_quantity),
								"source_warehouse" : ctswraw ,
								"available_quantity": self.get_available_quantity(ct.raw_item_code ,ctswraw),

				
							},),


			self.calculate_total_weight_quentity()

		else:
			frappe.throw("Please select Both Pouring and Casting Treatment")

	@frappe.whitelist()
	def set_available_qty(self ,table_name ,item_code , warehouse ,field_name):
		for tn in self.get(table_name):
			setattr(tn, field_name, self.get_available_quantity(tn.get(item_code), tn.get(warehouse)))
		

	def get_available_quantity(self,item_code, warehouse):
		filters = 	{"item_code": item_code,"warehouse": warehouse}
		fields = ["actual_qty"]
		result = frappe.get_all("Bin", filters=filters, fields=fields)
		if result and result[0].get("actual_qty"):
			return result[0].get("actual_qty")
		else:
			return 0
		
	@frappe.whitelist()
	def rejection_addition(self):
		for qd in self.get('quantity_details'):
			qd.total_quantity = qd.ok_quantity + qd.cr_quantity + qd.rw_quantity
			for ci in (self.get("casting_item" , filters= {"pouring" : qd.pouring , "item_code" : qd.item_code })):
				qd.weight = qd.total_quantity * (ci.weight/ci.quantity)

		self.sum_of_total_quantity =  self.calculating_total_weight("quantity_details" ,"total_quantity")
		self.sum_of_total_weight = self.calculating_total_weight("quantity_details" ,"weight")
		self.sum_of_ok_quantity = self.calculating_total_weight("quantity_details" ,"ok_quantity")
		self.sum_of_cr_quantity = self.calculating_total_weight("quantity_details" ,"cr_quantity")
		self.sum_of_rw_quantity = self.calculating_total_weight("quantity_details" ,"rw_quantity")

	@frappe.whitelist()
	def validate_total_quentity(self):
		for qd in self.get('quantity_details'):
			for ci in (self.get("casting_item" , filters= {"pouring" : qd.pouring , "item_code" : qd.item_code })):
				if qd.total_quantity != ci.quantity:
					frappe.throw(f'The "Total Quantity" in table "Quantity Details" must be equal to "Quantity" from "Casting Item" for Item "{qd.item_code}"-"{qd.item_name}" and Pouring ID "{qd.pouring}"')




	@frappe.whitelist()
	def calculating_total_weight(self,child_table ,total_field):
		casting_details = self.get(child_table)
		total_pouring_weight = 0
		for i in casting_details:
			field_data = i.get(total_field)
			total_pouring_weight = total_pouring_weight + field_data
		return total_pouring_weight


	@frappe.whitelist()
	def get_rejections(self):
		cttwrejected = frappe.get_value("Foundry Setting",self.company,"ct_tw_rejected")
		quantity_details = self.get('quantity_details')
		for qty_d in quantity_details:
			if qty_d.cr_quantity:
				self.append("rejected_items_reasons",
							{
									'item_code': qty_d.item_code ,
									'item_name': qty_d.item_name,
									'pouring': qty_d.pouring,
									'rejection_type':"CR",
									"qty": qty_d.cr_quantity,
									"target_warehouse" : cttwrejected,			
								},),
			if qty_d.rw_quantity:
				self.append("rejected_items_reasons",
							{
									'item_code': qty_d.item_code ,
									'item_name': qty_d.item_name,
									'pouring': qty_d.pouring,
									'rejection_type':"RW",
									"qty": qty_d.rw_quantity,
									"target_warehouse":cttwrejected,				
								},),
	@frappe.whitelist()
	def validate_rejections(self):
		for qnt_dtls in self.get('quantity_details'):
			if qnt_dtls.cr_quantity:
				cr_quantity = 0
				for rir in self.get('rejected_items_reasons' , filters={"item_code": qnt_dtls.item_code , "pouring": qnt_dtls.pouring ,"rejection_type" : "CR"}):
					cr_quantity = cr_quantity + rir.qty

				if cr_quantity !=  qnt_dtls.cr_quantity :
					frappe.throw(f'Please define Correct Qty of rejection of Item {qnt_dtls.item_code}-{qnt_dtls.item_name} off Pouring ID {qnt_dtls.pouring} in table "Rejected Items Reasons"')

			if qnt_dtls.rw_quantity :
				rw_quantity = 0 
				for rir in self.get('rejected_items_reasons' , filters={"item_code": qnt_dtls.item_code , "pouring": qnt_dtls.pouring , "rejection_type" : "RW"}):
					rw_quantity	= rw_quantity + rir.qty

				if rw_quantity != qnt_dtls.rw_quantity :
					frappe.throw(f'Please define Correct Qty of rejection of Item {qnt_dtls.item_code}-{qnt_dtls.item_name} off Pouring ID {qnt_dtls.pouring} in table "Rejected Items Reasons"')


	# @frappe.whitelist()
	# def update_quentities_at_pouring(self):
	# 	for o in self.get('quantity_details'):
	# 		if o.total_quantity:
	# 			frappe.get_all('Casting Details',
	# 			   						filters = {"parent" : o.pouring, "item_code": o.item_code, })
	@frappe.whitelist()
	def calculate_total_weight_quentity(self):
		self.total_quantity = self.calculating_total_weight("casting_item" ,"quantity")
		self.total_weight = self.calculating_total_weight("casting_item" ,"weight")


	@frappe.whitelist()
	def manifacturing_stock_entry(self):
		for cd in self.get("casting_item"):      
			se = frappe.new_doc("Stock Entry")
			se.stock_entry_type = "Manufacture"
			se.company = self.company
			se.posting_date = self.treatment_date
			
			all_core = self.get("quantity_details" ,  filters={"item_code": cd.item_code , "pouring": cd.pouring ,"ok_quantity" : ["!=",0]})
			for core in all_core:
				for g in self.get("raw_item" , filters={"item_code": cd.item_code , "pouring": cd.pouring}):
					se.append(
							"items",
							{
								"item_code": g.raw_item_code,
								"qty":  g.total_quantity,
								"s_warehouse": g.source_warehouse,
							},)
				se.append(
				"items",
					{
						"item_code": cd.item_code,
						"qty": core.ok_quantity,
						"s_warehouse": cd.source_warehouse,
					},)

				se.append(
						"items",
						{
							"item_code": core.item_code,
							"qty": core.ok_quantity,
							"t_warehouse": cd.target_warehouse,
							"is_finished_item": True
						},)
				additional_cost_details = self.get("additional_cost_details")
				if additional_cost_details:
					for acd in additional_cost_details:
						se.append(
								"additional_costs",
								{
									"expense_account":acd.expense_head_account,
									"description": acd.discription,
									"amount": (acd.amount* core.ok_quantity) / self.sum_of_ok_quantity,

								},)

			se.custom_casting_treatment = self.name	
			if all_core:
				se.insert()
				se.save()
				se.submit()


	@frappe.whitelist()
	def transfer_stock_entry(self):
		count = 0
		se = frappe.new_doc("Stock Entry")
		se.stock_entry_type = "Material Transfer"
		se.company = self.company
		se.posting_date = self.treatment_date
		for i in self.get("casting_item"):
			for j in self.get("rejected_items_reasons" ,filters={"item_code": i.item_code , "pouring": i.pouring}):
				count = count + 1
				se.append(
						"items",
						{
							"item_code": j.item_code,
							"qty": j.qty,
							"s_warehouse": i.source_warehouse,
							"t_warehouse": j.target_warehouse,
						},)

					
		se.custom_casting_treatment = self.name	
		if count !=0:
			se.insert()
			se.save()
			se.submit()
 