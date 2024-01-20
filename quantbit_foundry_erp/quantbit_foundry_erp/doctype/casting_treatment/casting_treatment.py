# Copyright (c) 2023, Quantbit Technologies Pvt ltd and contributors
# For license information, please see license.txt y

import frappe
from frappe.model.document import Document
from quantbit_foundry_erp.quantbit_foundry_erp.doctype.pattern_master.pattern_master import (
	item_weight_per_unit,
)

class CastingTreatment(Document):


	def before_save(self):
		self.update_raw()
		self.validate_total_quentity()
		self.validate_rejections()
		self.validate_casting_quantity()

	def before_submit(self):
		self.manifacturing_stock_entry()
		self.transfer_stock_entry()
		self.updating_treatment_analysis()

	def before_cancel(self):
		self.updating_treatment_analysis_on_cancle()

	@frappe.whitelist()
	def get_pouring (self):
		if self.select_pouring and self.casting_treatment:

			cttwcasting = frappe.get_value("Foundry Setting",self.company,"ct_tw_casting") 
			ctswraw = frappe.get_value("Foundry Setting",self.company,"ct_sw_raw")
 

			for d in self.get("select_pouring"):
				items_doc= frappe.get_all("Casting Details" ,
													filters = {"parent": str(d.pouring)},
													fields = ["name","item_code","item_name","total_quantity","target_warehouse","casting_weight","pattern","sales_order","casting_treatment_quantity"])
				for i in items_doc:
					casting_treatment_analysis = frappe.get_all("Casting Treatment Analysis" ,
													filters = {"parent": str(d.pouring), "casting_treatment": self.casting_treatment,'reference_id':i.name ,"casting_item_code": i.item_code,"pattern":i.pattern},
													fields = ["treatment_remaining_quantity",'name','treatment_no','source_warehouse','target_warehouse'])
					treatmentable_quantity = 0
					name_reference=''
					next_treatment=''
					for k in casting_treatment_analysis:
						treatmentable_quantity = k.treatment_remaining_quantity
						name_reference = str(k.name)
						source_warehouse = k.source_warehouse
						target_warehouse = k.target_warehouse
						c_t_a = frappe.get_all("Casting Treatment Analysis" ,
													filters = {"parent": str(d.pouring), "treatment_no": (k.treatment_no +1),'reference_id':i.name ,"casting_item_code": i.item_code,"pattern":i.pattern},
													fields = ["treatment_remaining_quantity",'name',])
						if c_t_a:
							for n in c_t_a:
								next_treatment =n.name

					if treatmentable_quantity != 0:
						self.append("casting_item",{
								'item_code': i.item_code ,
								'item_name': i.item_name,
								'pouring': d.pouring,
								'source_warehouse':source_warehouse if source_warehouse else i.target_warehouse ,
								'available_quantity': self.get_available_quantity(i.item_code , i.target_warehouse ),
								'treatmentable_quantity':treatmentable_quantity,
								'quantity': treatmentable_quantity  ,
								'weight': i.casting_weight * i.total_quantity ,
								'target_warehouse':target_warehouse if target_warehouse else cttwcasting,
								"casting_weight": i.casting_weight,
								"sales_order":i.sales_order,
								"reference_id": i.name,
								"name_reference":name_reference,
								"next_treatment_id": next_treatment
							},),


						self.append("quantity_details",{
								'item_code': i.item_code ,
								'item_name': i.item_name,
								'pouring': d.pouring,
								'sales_order' : i.sales_order,
								'reference_id':i.name,
								'casting_weight':i.casting_weight ,
				
							},),

						casting_treatment = frappe.get_all("Casting Treatment Details" ,
														filters = {"parent": i.pattern , 'casting_items_code': i.item_code , 'casting_treatment' : self.casting_treatment },
														fields = ["casting_treatment","casting_items_code","casting_item_name","raw_item_code","raw_item_name","required_quantity"])
			
						
						for ct in casting_treatment:
							total_quantity = 0
							raw_uom = frappe.get_value("Item",ct.raw_item_code,"stock_uom")
							if raw_uom:
								if raw_uom =='Nos':
									temp_total_quantity = ct.required_quantity * (i.total_quantity)
									total_quantity = int(temp_total_quantity) + (1 if temp_total_quantity % 1 != 0 else 0)
								else:
									total_quantity = ct.required_quantity * (i.total_quantity)
							if ct.raw_item_code:
								self.append("raw_item",{
										'item_code': ct.casting_items_code ,
										'item_name': ct.casting_item_name,
										'pouring': d.pouring,
										'raw_item_code':ct.raw_item_code,
										"raw_item_name": ct.raw_item_name,
										'required_quantity_per_unit':ct.required_quantity,
										"total_quantity": total_quantity,
										"source_warehouse" : ctswraw ,
										"available_quantity": self.get_available_quantity(ct.raw_item_code ,ctswraw),
										'reference_id':i.name,

						
									},),


			self.calculate_total_weight_quentity()

		else:
			frappe.throw("Please select Both Pouring and Casting Treatment")


	@frappe.whitelist()
	def default_warehouse(self, casting_treatment):
		pass
		
		





	@frappe.whitelist()
	def updating_treatment_analysis(self):
		casting = self.get("casting_item")
		for g in casting:
			quantity_to_treatment = frappe.get_value("Casting Treatment Analysis",g.name_reference ,"quantity_to_treatment")
			treatment_done_quantity = frappe.get_value("Casting Treatment Analysis",g.name_reference ,"treatment_done_quantity")
			treatment_remaining_quantity = frappe.get_value("Casting Treatment Analysis",g.name_reference ,"treatment_remaining_quantity")
			casting_treatment_ok = frappe.get_value("Casting Treatment Analysis",g.name_reference ,"casting_treatment_ok")
			casting_treatment_cr = frappe.get_value("Casting Treatment Analysis",g.name_reference ,"casting_treatment_cr")
			casting_treatment_rw = frappe.get_value("Casting Treatment Analysis",g.name_reference ,"casting_treatment_rw")

			update_done_qty = treatment_done_quantity + g.quantity
			update_remaining_qty = treatment_remaining_quantity - g.quantity

			for p in self.get("quantity_details" , filters = {"reference_id":g.reference_id}):
				update_treatment_ok = casting_treatment_ok + p.ok_quantity
				update_treatment_cr = casting_treatment_cr + p.cr_quantity
				update_treatment_rw = casting_treatment_rw + p.rw_quantity

			frappe.set_value("Casting Treatment Analysis",g.name_reference ,"treatment_done_quantity",update_done_qty)
			frappe.set_value("Casting Treatment Analysis",g.name_reference ,"treatment_remaining_quantity",update_remaining_qty)

			frappe.set_value("Casting Treatment Analysis",g.name_reference ,"casting_treatment_ok",update_treatment_ok)
			frappe.set_value("Casting Treatment Analysis",g.name_reference ,"casting_treatment_cr",update_treatment_cr)
			frappe.set_value("Casting Treatment Analysis",g.name_reference ,"casting_treatment_rw",update_treatment_rw)

			if quantity_to_treatment == update_done_qty:
				frappe.set_value("Casting Treatment Analysis",g.name_reference ,"status",'Completed')
			elif quantity_to_treatment > update_done_qty and quantity_to_treatment != update_remaining_qty:
				frappe.set_value("Casting Treatment Analysis",g.name_reference ,"status",'Partially Done')
			elif quantity_to_treatment == update_remaining_qty:
				frappe.set_value("Casting Treatment Analysis",g.name_reference ,"status",'In Process')
			elif quantity_to_treatment < update_done_qty:
				frappe.throw(f"Casting Treatment Is Done For Pouring '{g.pouring}' , You Can Not Update")


			for k in self.get("quantity_details" , filters = {"reference_id":g.reference_id}):
				next_reference_remaining = frappe.get_value("Casting Treatment Analysis",g.next_treatment_id ,"treatment_remaining_quantity")
				if next_reference_remaining or next_reference_remaining == 0:
					updated_next_remaining = next_reference_remaining + k.ok_quantity
					frappe.set_value("Casting Treatment Analysis",g.next_treatment_id ,"treatment_remaining_quantity",updated_next_remaining)

			

	@frappe.whitelist()
	def updating_treatment_analysis_on_cancle(self):
		casting = self.get("casting_item")
		for g in casting:
			quantity_to_treatment = frappe.get_value("Casting Treatment Analysis",g.name_reference ,"quantity_to_treatment")

			treatment_done_quantity = frappe.get_value("Casting Treatment Analysis",g.name_reference ,"treatment_done_quantity")
			treatment_remaining_quantity = frappe.get_value("Casting Treatment Analysis",g.name_reference ,"treatment_remaining_quantity")
			casting_treatment_ok = frappe.get_value("Casting Treatment Analysis",g.name_reference ,"casting_treatment_ok")
			casting_treatment_cr = frappe.get_value("Casting Treatment Analysis",g.name_reference ,"casting_treatment_cr")
			casting_treatment_rw = frappe.get_value("Casting Treatment Analysis",g.name_reference ,"casting_treatment_rw")

			update_done_qty = treatment_done_quantity - g.quantity
			update_remaining_qty = treatment_remaining_quantity + g.quantity

			for p in self.get("quantity_details" , filters = {"reference_id":g.reference_id}):
				update_treatment_ok = casting_treatment_ok - p.ok_quantity
				update_treatment_cr = casting_treatment_cr - p.cr_quantity
				update_treatment_rw = casting_treatment_rw - p.rw_quantity
 
			frappe.set_value("Casting Treatment Analysis",g.name_reference ,"treatment_done_quantity",update_done_qty)
			frappe.set_value("Casting Treatment Analysis",g.name_reference ,"treatment_remaining_quantity",update_remaining_qty)

			frappe.set_value("Casting Treatment Analysis",g.name_reference ,"casting_treatment_ok",update_treatment_ok)
			frappe.set_value("Casting Treatment Analysis",g.name_reference ,"casting_treatment_cr",update_treatment_cr)
			frappe.set_value("Casting Treatment Analysis",g.name_reference ,"casting_treatment_rw",update_treatment_rw)


			if quantity_to_treatment == update_done_qty:
				frappe.set_value("Casting Treatment Analysis",g.name_reference ,"status",'Completed')
			elif quantity_to_treatment > update_done_qty and quantity_to_treatment != update_remaining_qty:
				frappe.set_value("Casting Treatment Analysis",g.name_reference ,"status",'Partially Done')
			elif quantity_to_treatment == update_remaining_qty:
				frappe.set_value("Casting Treatment Analysis",g.name_reference ,"status",'In Process')
			elif quantity_to_treatment < update_done_qty:
				frappe.throw(f"Casting Treatment Is Done For Pouring '{g.pouring}' , You Can Not Update")

			# next_reference_remaining = frappe.get_value("Casting Treatment Analysis",g.next_treatment_id ,"treatment_remaining_quantity")
			# if next_reference_remaining or next_reference_remaining == 0:
			# 	updated_next_remaining = next_reference_remaining - g.quantity
			# 	frappe.set_value("Casting Treatment Analysis",g.next_treatment_id ,"treatment_remaining_quantity",updated_next_remaining)

			for k in self.get("quantity_details" , filters = {"reference_id":g.reference_id}):
				next_reference_remaining = frappe.get_value("Casting Treatment Analysis",g.next_treatment_id ,"treatment_remaining_quantity")
				if next_reference_remaining or next_reference_remaining == 0:
					updated_next_remaining = next_reference_remaining - k.ok_quantity
					frappe.set_value("Casting Treatment Analysis",g.next_treatment_id ,"treatment_remaining_quantity",updated_next_remaining)

	@frappe.whitelist()
	def update_raw(self):
		casting_item = self.get("casting_item")
		for d in casting_item :
			if d.quantity:
				total_quantity = frappe.get_value("Casting Details", d.reference_id ,'total_quantity')
				if d.quantity > total_quantity:
					frappe.throw(f"You Can Not Set 'Quantity' More Than {total_quantity} ")
				if d.casting_weight:
					d.weight = d.quantity * d.casting_weight
				if d.pouring and d.reference_id:
					raw_item = self.get("raw_item" , filters = {'reference_id': d.reference_id})
					for r in raw_item:
						raw_uom = frappe.get_value("Item",r.raw_item_code,"stock_uom")
						if raw_uom:
							if raw_uom =='Nos':
								temp_total_quantity = r.required_quantity_per_unit * d.quantity
								total_quantity = int(temp_total_quantity) + (1 if temp_total_quantity % 1 != 0 else 0)
							else:
								total_quantity = r.required_quantity_per_unit * d.quantity



						r.total_quantity = total_quantity



		self.calculate_total_weight_quentity()
			

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
			qd.ok_quantity_weight = qd.casting_weight * qd.ok_quantity
			qd.cr_quantity_weight = qd.casting_weight * qd.cr_quantity
			qd.rw_quantiry_weight = qd.casting_weight * qd.rw_quantity
			qd.weight             = qd.casting_weight * qd.total_quantity
			
			# for ci in (self.get("casting_item" , filters= {"pouring" : qd.pouring , "item_code" : qd.item_code })):
			# 	qd.weight = qd.total_quantity * (ci.weight/ci.quantity)

		self.sum_of_total_quantity =  self.calculating_total_weight("quantity_details" ,"total_quantity")
		self.sum_of_total_weight = self.calculating_total_weight("quantity_details" ,"weight")
		self.sum_of_ok_quantity = self.calculating_total_weight("quantity_details" ,"ok_quantity")
		self.sum_of_cr_quantity = self.calculating_total_weight("quantity_details" ,"cr_quantity")
		self.sum_of_rw_quantity = self.calculating_total_weight("quantity_details" ,"rw_quantity")

		self.get_rejections()

	@frappe.whitelist()
	def validate_total_quentity(self):
		for qd in self.get('quantity_details'):

			for ci in (self.get("casting_item" , filters= {"pouring" : qd.pouring , "item_code" : qd.item_code , "reference_id" : qd.reference_id})):
				if qd.total_quantity != ci.quantity:
					frappe.throw(f'The "Total Quantity" in table "Quantity Details" must be equal to "Quantity" from "Casting Item" for Item "{qd.item_code}"-"{qd.item_name}" and Pouring ID "{qd.pouring}"')

			for i in (self.get("pattern_casting_item" , filters= {"reference_id" : qd.reference_id})):
				if qd.total_quantity != i.quantity:
					frappe.throw(f'The "Total Quantity" in table "Quantity Details" must be equal to "Quantity" from "Casting Item" for Item "{qd.item_code}"-"{qd.item_name}"')



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
		CR_rejections = frappe.get_value("Casting Treatment Master",self.casting_treatment,"crt_warehouse")
		RW_rejections = frappe.get_value("Casting Treatment Master",self.casting_treatment,"rwt_warehouse")

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
									"target_warehouse" :CR_rejections if CR_rejections else  cttwrejected,
									"reference_id":qty_d.reference_id,
								},),
			if qty_d.rw_quantity:
				self.append("rejected_items_reasons",
							{
									'item_code': qty_d.item_code ,
									'item_name': qty_d.item_name,
									'pouring': qty_d.pouring,
									'rejection_type':"RW",
									"qty": qty_d.rw_quantity,
									"target_warehouse":RW_rejections if RW_rejections else cttwrejected,
									"reference_id":qty_d.reference_id,		
								},),
	@frappe.whitelist()
	def validate_rejections(self):
		for qnt_dtls in self.get('quantity_details'):
			if qnt_dtls.cr_quantity:
				cr_quantity = 0
				for rir in self.get('rejected_items_reasons' , filters={"item_code": qnt_dtls.item_code , "pouring": qnt_dtls.pouring ,"rejection_type" : "CR" , "reference_id":qnt_dtls.reference_id}):
					cr_quantity = cr_quantity + rir.qty

				if cr_quantity !=  qnt_dtls.cr_quantity :
					frappe.throw(f'Please define Correct Qty of rejection of Item {qnt_dtls.item_code}-{qnt_dtls.item_name} off Pouring ID {qnt_dtls.pouring} in table "Rejected Items Reasons"')

			if qnt_dtls.rw_quantity :
				rw_quantity = 0 
				for rir in self.get('rejected_items_reasons' , filters={"item_code": qnt_dtls.item_code , "pouring": qnt_dtls.pouring , "rejection_type" : "RW" , "reference_id":qnt_dtls.reference_id}):
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
		if self.get('pattern_casting_item'):
			self.total_quantity = self.calculating_total_weight("pattern_casting_item" ,"quantity")
			self.total_weight = self.calculating_total_weight("pattern_casting_item" ,"weight")

	@frappe.whitelist()
	def validate_casting_quantity(self):
		castingitem = self.get("casting_item")
		for j in castingitem :
			if j.treatmentable_quantity < j.quantity :
				frappe.throw(f"You can not select value more than 'Remaining Treatment Quantity' which is '{j.treatmentable_quantity}' ")

	@frappe.whitelist()
	def manifacturing_stock_entry(self):
		if self.casting_treatment_without_pouring:
			table = 'pattern_casting_item'
		else:
			table = 'casting_item'

		for cd in self.get(table):      
			se = frappe.new_doc("Stock Entry")
			se.stock_entry_type = "Manufacture"
			se.company = self.company
			se.posting_date = self.treatment_date
			
			all_core = self.get("quantity_details" ,  filters={"item_code": cd.item_code ,"ok_quantity" : ["!=",0],"reference_id" : cd.reference_id})
			for core in all_core:
				for g in self.get("raw_item" , filters={"item_code": cd.item_code  ,"reference_id" : cd.reference_id}):
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
		if self.casting_treatment_without_pouring:
			for y in self.get("pattern_casting_item"):
				for z in self.get("rejected_items_reasons" ,filters={"item_code": y.item_code ,"reference_id":y.reference_id}):
					count = count + 1
					se.append(
							"items",
							{
								"item_code": y.item_code,
								"qty": z.qty,
								"s_warehouse": y.source_warehouse,
								"t_warehouse": z.target_warehouse,
							},)

						
			se.custom_casting_treatment = self.name	
			if count !=0:
				se.insert()
				se.save()
				se.submit()
		else:
			for i in self.get("casting_item"):
				for j in self.get("rejected_items_reasons" ,filters={"item_code": i.item_code , "pouring": i.pouring ,"reference_id":i.reference_id}):
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


	#This method used to get filter for getting pouring doctype name
	@frappe.whitelist()
	def get_pouring_id(self):
		document_list=[]
		doc=frappe.db.sql("""select distinct parent from `tabCasting Treatment Analysis` where casting_treatment='{0}' and docstatus='1' 
                    and status <> 'Completed'
                    """.format(self.casting_treatment),as_dict="True")
		for i in doc:
			document_list.append(i.parent)
		return document_list
	
	#This method used to get filter for getting Items which are present in taht perticular Pattern
	@frappe.whitelist()
	def get_item_id_from_pattern(self):
		document_list=[]
		if self.select_pattern:
			doc = frappe.get_all("Casting Material Details" , filters = {'parent': self.select_pattern} ,fields = ['item_code'])
			for i in doc:
				document_list.append(i.item_code)
			return document_list
		
	#This method used to set data in table 'Pattern Casting Item'
	@frappe.whitelist()
	def pcidetails(self):
		
		if self.select_pattern and self.select_item:
			if not self.casting_treatment:
				frappe.throw("Please Select 'Casting Treatment'")

			source_warehouse = frappe.get_value('Casting Treatment Details',{'parent':self.select_pattern , 'casting_treatment': self.casting_treatment},'finished_source_warehouse')
			self.append("pattern_casting_item",
							{
							'item_code': self.select_item ,
							'item_name': frappe.get_value("Item" , self.select_item ,"item_name"),
							'pattern_id': self.select_pattern,
							'casting_weight':item_weight_per_unit(self.select_item),
							'reference_id': self.select_pattern,
							'available_quantity' : self.get_available_quantity(self.select_item ,source_warehouse),
							'source_warehouse':source_warehouse,
							'target_warehouse':frappe.get_value('Casting Treatment Details',{'parent':self.select_pattern , 'casting_treatment': self.casting_treatment},'finished_target_warehouse'),
							},),

	@frappe.whitelist()
	def pattern_set_raw_item(self):

		ctswraw = frappe.get_value("Foundry Setting",self.company,"ct_sw_raw")
		pattern_casting_item = self.get('pattern_casting_item')

		for j in pattern_casting_item:
			if j.quantity:
				self.validate_pattern_casting_item( j.source_warehouse , j.available_quantity ,j.quantity)
				j.weight = j.casting_weight * j.quantity

				casting_treatment = frappe.get_all("Casting Treatment Details" ,
												filters = {"parent": self.select_pattern , 'casting_items_code': self.select_item, 'casting_treatment' : self.casting_treatment },
												fields = ["casting_treatment","casting_items_code","casting_item_name","raw_item_code","raw_item_name","required_quantity"])

				
				for ct in casting_treatment:
					total_quantity = 0
					raw_uom = frappe.get_value("Item",ct.raw_item_code,"stock_uom")
					if raw_uom:
						if raw_uom =='Nos':
							temp_total_quantity = ct.required_quantity * (j.quantity)
							total_quantity = int(temp_total_quantity) + (1 if temp_total_quantity % 1 != 0 else 0)
						else:
							total_quantity = ct.required_quantity * (j.quantity)
					if ct.raw_item_code:
						self.append("raw_item",{
								'item_code': ct.casting_items_code ,
								'item_name': ct.casting_item_name,
								'pouring': None,
								'raw_item_code':ct.raw_item_code,
								"raw_item_name": ct.raw_item_name,
								'required_quantity_per_unit':ct.required_quantity,
								"total_quantity": total_quantity,
								"source_warehouse" : ctswraw ,
								"available_quantity": self.get_available_quantity(ct.raw_item_code ,ctswraw),
								'reference_id':self.select_pattern,

				
							},),
		self.pattern_set_quantity_details()

	@frappe.whitelist()
	def pattern_set_quantity_details(self):
		pattern_casting_item = self.get('pattern_casting_item')
		for k in pattern_casting_item:
			self.append("quantity_details",{
									'item_code': k.item_code ,
									'item_name': k.item_name,
									'pouring': None,
									'sales_order' : None,
									'reference_id':self.select_pattern,
									'casting_weight': k.casting_weight,
					
								},),

		self.calculate_total_weight_quentity()

	
	@frappe.whitelist()
	def validate_pattern_casting_item(self , source_warehouse , available_quantity , quantity):
		if not source_warehouse:
			frappe.throw("please select source_warehouse") 
		if available_quantity < quantity:
			frappe.throw("You can not select 'Quantity' more than 'Quantity Available In Warehouse'   ")

	#set available qty in child table
	# @frappe.whitelist()
	# def set_available_qty_in_pcidetails(self):
	# 	pattern_casting_item = self.get("pattern_casting_item")
	# 	for d in pattern_casting_item:
	# 		if d.source_warehouse and d.item_code:
	# 			d.available_quantity = self.get_available_quantity(d.item_code , d.source_warehouse)
			

	# @frappe.whitelist()
	# def item_weight_per_unit(self , item_code ):
	# 	item_uom = frappe.get_value("Item",item_code,"stock_uom")
	# 	if item_uom == 'Kg':
	# 		item_weight = frappe.get_all("Item",item_code,"weight")
	# 	else:
	# 		production_uom_definition = frappe.get_all("Production UOM Definition",
	# 																			filters = {"parent":item_code,"uom": 'Kg'},
	# 																			fields = ["value_per_unit"])
	# 		if production_uom_definition:
	# 			for k in production_uom_definition:
	# 				item_weight= k.value_per_unit
	# 		else:
	# 			frappe.throw(f'Please Set "Production UOM Definition" For Item {get_link_to_form("Item",item_code)} of UOM "Kg" ')
	# 	if item_weight:
	# 		return  item_weight
	# 	else:
	# 		return 0
 