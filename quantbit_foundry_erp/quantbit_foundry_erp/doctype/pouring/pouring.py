# Copyright (c) 2023, Quantbit Technologies Pvt ltd and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class Pouring(Document):
	def before_save(self):
		self.validate_poring_weight()
		self.calculating_power_consumption()
		self.validate_stock()
		# self.validate_retained_items()
		self.calculating_power_consumption_amount()
		self.set_datd_in_naming_fields()
		self.validate_pattern()
		self.validate_pattern_equality()
		self.create_rr_item_retain_items()
		self.validate_total_charge_mix()
		self.calculate_normal_loss()
		if int(self.power_reading_initial) == 0:
			frappe.throw('Please Fill Power Reading')
		if int(self.power_reading_final) == 0:
			frappe.throw('Please Fill Power Reading')

		self.charge_mix = str(self.grade)

	def before_submit(self):
		self.validate_last_power_consumption()
		self.manifacturing_stock_entry()
		self.manifacturing_retained_items()
		self.calculating_power_consumption_amount()
		self.casting_treatment_analysis_details()



	@frappe.whitelist()
	def get_details_pattern_master(self):

		pattern_details = self.get("pattern_details")
	
		self.validate_pattern()
		
		for i in pattern_details:
			if self.furnece :
				if i.pattern_code and i.poured_boxes :
					swcore = frappe.get_value("Foundry Setting",self.company,"sw_core")
					twcasting = frappe.get_value("Foundry Setting",self.company,"tw_casting")
					swsand = frappe.get_value("Foundry Setting",self.company,"sw_sand")
					pm_rr_weight =frappe.get_value('Pattern Master',i.pattern_code ,'rr_weight')
					casting_weight =frappe.get_value('Pattern Master',i.pattern_code ,'casting_weight')
					
					pm_doc = frappe.get_all("Casting Material Details", 
													filters = {"parent": i.pattern_code},
													fields = ["item_code","item_name","weight","qty","uom","name"])
					
					
					for d in pm_doc:

						rr_weight=((pm_rr_weight/casting_weight)*(d.weight))
						total_weight = ((d.weight)+ rr_weight ) * (i.poured_boxes * d.qty)


						self.append("casting_details",{
							'item_code': d.item_code ,
							'item_name': d.item_name,
							'pattern': i.pattern_code,
							'quantitybox': d.qty ,
							'total_quantity':i.poured_boxes * d.qty,
							'casting_weight' : d.weight,
							'rr_weight' : rr_weight,
							'rr_weight_total' : rr_weight * i.poured_boxes * d.qty,
							'total_weight' : total_weight ,
							'target_warehouse' : twcasting ,
							'sales_order' : i.sales_order,
							'reference_id' : d.name,
						},),


						cmd_doc = frappe.get_all("Core Material Details", 
														filters = {"parent": i.pattern_code, "casting_item_code" : d.item_code},
														fields = ["casting_item_code","item_code","item_name","qty","uom"])
						# rr_weight =frappe.get_value('Pattern Master',i.pattern_code ,'rr_weight')
						for cmd in cmd_doc:
							


							self.append("core_details",{
								"casting_item_code" : cmd.casting_item_code,
								'item_code': cmd.item_code ,
								'item_name': cmd.item_name,
								'pattern': i.pattern_code ,
								'qty': cmd.qty * i.poured_boxes  ,
								'uom':cmd.uom,
								"warehouse" : swcore ,
								'stock' : self.get_available_quantity(cmd.item_code , swcore),
								'required_quantity':cmd.qty * i.poured_boxes,
								'reference_id' :  d.name,

							},),
			
					sand_doc = frappe.get_all("Molding Sand Details", 
													filters = {"parent": i.pattern_code, },
													fields = ["sand_item_code","sand_item_name","quantity_in_kg",])
					# rr_weight =frappe.get_value('Pattern Master',i.pattern_code ,'rr_weight')
					for sand in sand_doc:
						
						sand_qty = sand.quantity_in_kg * i.poured_boxes


						self.append("molding_sand_details",{
							"pattern_id" : i.pattern_code,
							'item_code': sand.sand_item_code ,
							'item_name': sand.sand_item_name,
							'warehouse':swsand,
							'stock' : self.get_available_quantity(sand.sand_item_code , swsand),
							'required_quantity':sand_qty,
							"quantity" : sand_qty ,
							"reference_id": i.pattern_code,

						},),
			else:
				frappe.msgprint("Please Select Furnace")
				i.pattern_code = None 
				i.poured_boxes = None
				i.pattern_name = None

		self.total_pouring_weight = self.calculating_total_weight("casting_details","total_weight")
		self.totals_calculation()
		self.get_details_grade_master()

		# self.validate_poring_weight_without_interupt()

	@frappe.whitelist()
	def calculating_total_weight(self,child_table ,total_field):
		casting_details = self.get(child_table)
		total_pouring_weight = 0
		for i in casting_details:
			field_data = i.get(total_field)
			if field_data:
				total_pouring_weight = total_pouring_weight + field_data
		return total_pouring_weight
	
		# self.total_pouring_weight= total_pouring_weight


	@frappe.whitelist()
	def get_details_grade_master(self):

		pattern_details = self.get("pattern_details")
		for t in pattern_details:
			cmt_data = frappe.get_value("Pattern Master", t.pattern_code,'grade')
		self.grade = cmt_data

		if self.grade:
			if self.furnece:
				change_mix_details = self.get('change_mix_details',)
				if not change_mix_details:
					swcharge = frappe.get_value("Foundry Setting",self.company,"sw_charge")
					total_furnece_kg = frappe.get_value("Furnece Master",self.furnece,"furnece_capcity")
					gid_doc = frappe.get_all("Grade Items Details", 
														filters = {"parent": self.grade},
														fields = ["item_code","item_name","item_group","percentage"] , order_by='idx ASC')

					for gid in gid_doc:
							calculated_qty = (gid.percentage * total_furnece_kg)/100

							self.append("change_mix_details",{
								'item_code': gid.item_code ,
								'item_name': gid.item_name,
								'item_group': gid.item_group,
								'quantity': 0,
								'required_quantity' : calculated_qty,
								'warehouse': swcharge,
								'stock' : self.get_available_quantity(gid.item_code , swcharge) ,
							
							},),
			else:
				frappe.throw("Please select Furnece")

		self.calculate_total_weight_after_charge_mix_filling()		

	@frappe.whitelist()
	def calculate_total_weight_after_charge_mix_filling(self):
			
			self.total_consumed_weight = self.calculating_total_weight("change_mix_details","quantity")
			self.totals_calculation()


	@frappe.whitelist()
	def validate_poring_weight(self):
		if self.total_consumed_weight < self.total_pouring_weight:
			frappe.throw(f'"Total Pouring Weight" must be less than "Total Consumed Weight"')

	# @frappe.whitelist()
	# def validate_poring_weight_without_interupt(self):
	# 	pattern_details = self.get("pattern_details")
	# 	for t in pattern_details:
	# 		cmt_data = frappe.get_value("Pattern Master", t.pattern_code,'grade')
	# 	self.grade = cmt_data

	# 	self.get_details_grade_master()

	# 	if self.total_consumed_weight:
	# 			if self.total_consumed_weight < self.total_pouring_weight:
	# 				frappe.msgprint(f'"Total Pouring Weight" must be less than "Total Consumed Weight"')
		# else:
		# 	frappe.msgprint("Please select Grade")


	@frappe.whitelist()
	def calculating_power_consumption(self):
		if self.power_reading_initial and  self.power_reading_final:
			self.power_consumed = self.power_reading_final - self.power_reading_initial
			if self.power_consumed < 0 :
				frappe.throw("The 'Power Consumed' should not be negatine")

			self.calculating_power_consumption_amount()
		

	@frappe.whitelist()
	def get_stock_change_mix_details(self):
		for cmd in self.get("change_mix_details"):
			if cmd.item_code and cmd.warehouse:
				cmd.stock = self.get_available_quantity(cmd.item_code , cmd.warehouse)
	
	@frappe.whitelist()
	def get_stock_core_details(self):
		for cd in self.get("core_details"):
			if cd.item_code and cd.warehouse:
				cd.stock = self.get_available_quantity(cd.item_code , cd.warehouse)


	def get_available_quantity(self,item_code, warehouse):
		filters = 	{"item_code": item_code,"warehouse": warehouse}
		fields = ["actual_qty"]
		result = frappe.get_all("Bin", filters=filters, fields=fields)
		if result and result[0].get("actual_qty"):
			return result[0].get("actual_qty")
		else:
			return 0
		

	@frappe.whitelist()
	def validate_stock(self):
		for vsk in self.get("change_mix_details",filters = {"quantity" :['!=',0]}):
			if vsk.quantity > vsk.stock :
				frappe.throw(f'There is not enough stock present in warehouse "{vsk.warehouse}" of item "{vsk.item_name}" to proceed with pouring entry')

		for stk in self.get("core_details"):
			if stk.qty > stk.stock :
				frappe.throw(f'There is not enough stock present in warehouse "{stk.warehouse}" of item "{stk.item_name}" to proceed with pouring entry')

	# @frappe.whitelist()
	# def validate_retained_items(self):
	# 	total_sum =0
	# 	for ri in self.get("retained_items" , filters={"rr_item":0}):
	# 		if ri.total_quantity:
	# 			total_sum = total_sum + ri.total_quantity

	# 	total =int(self.total_pouring_weight) + int(total_sum)
	# 	total_furnece_kg = frappe.get_value("Furnece Master",self.furnece,"furnece_capcity")

	# 	if int(total_furnece_kg) != int(total):
	# 		frappe.throw(f"Please Enter Valid Retain Item Quentity the difference is{total_furnece_kg - total} ")
				
		
	@frappe.whitelist()
	def calculating_power_consumption_amount(self):
		power_consumption = frappe.get_all("Power Consumption Details",
									 				filters = {"parent": self.company , "from_date" : ['<=',self.heat_date]},
													fields = ["from_date","amount_per_unit",] , order_by = "from_date DESC",limit =1)
		expense_head_account = frappe.get_value("Power Consumption",self.company,"expense_head_account")

		if power_consumption:
			additional_cost_details = self.get("additional_cost_details")
			rows_to_remove = [d for d in self.get("additional_cost_details") if d.is_electricity_expense]
			for d in rows_to_remove:
				additional_cost_details.remove(d)




			if power_consumption:
				self.append("additional_cost_details",{
								'discription': "Electricity Expense" ,
								'expense_head_account': expense_head_account,
								'amount': self.power_consumed * power_consumption[0].amount_per_unit,
								'is_electricity_expense': True,
							},),
		else:
			frappe.msgprint("Please set 'Power Consumption'")


	def set_datd_in_naming_fields(self):
		list_data =[]
		for d in self.get('casting_details'):
			all_data = 'Item = '+str(d.item_name) + ',' + 'Total Quantity = ' +str(d.total_quantity) 
			list_data.append(all_data)
		self.naming_fields = str(list_data)

		
	@frappe.whitelist()
	def manifacturing_stock_entry(self):
		for cd in self.get("casting_details"):      
			se = frappe.new_doc("Stock Entry")
			se.stock_entry_type = "Manufacture"
			se.company = self.company
			se.posting_date = self.heat_date
			for g in self.get("change_mix_details" , filters = {"quantity" :['!=',0]}):
				se.append(
						"items",
						{
							"item_code": g.item_code,
							"qty":  ((cd.total_quantity * cd.casting_weight) * g.quantity) / self.total_consumed_weight,
							"s_warehouse": g.warehouse,
						},)
				
			for sand in self.get("molding_sand_details", filters = {"pattern_id": cd.pattern}):
				se.append(
						"items",
						{
							"item_code": sand.item_code,
							"qty":  ((cd.total_quantity * cd.casting_weight) * sand.quantity) / self.total_sand_weight,
							"s_warehouse": sand.warehouse,
						},)

			for core in self.get("core_details" , filters = {"pattern": cd.pattern ,'reference_id': cd.reference_id ,"casting_item_code": cd.item_code}):
					se.append(
							"items",
							{
								"item_code": core.item_code,
								"qty": core.qty,
								"s_warehouse": core.warehouse,
							},)

			se.append(
						"items",
						{
							"item_code": cd.item_code,
							"qty": cd.total_quantity ,
							"t_warehouse": cd.target_warehouse,
							'is_finished_item':True
						},) 
			for acd in self.get("additional_cost_details"):
				se.append(
						"additional_costs",
						{
							"expense_account":acd.expense_head_account,
							"description": acd.discription,
							"amount": (acd.amount* cd.total_weight) / self.total_pouring_weight,

						},)
			

			se.custom_pouring = self.name	
			se.insert()
			se.save()
			se.submit()

	@frappe.whitelist()
	def manifacturing_retained_items(self):
		for ri in self.get("retained_items"):      
			se = frappe.new_doc("Stock Entry")
			se.stock_entry_type = "Manufacture"
			se.company = self.company
			se.posting_date = self.heat_date
			for p in self.get("change_mix_details" , filters = {"quantity" :['!=',0]}):
				se.append(
						"items",
						{
							"item_code": p.item_code,
							"qty":  (ri.total_quantity * p.quantity) / self.total_consumed_weight,
							"s_warehouse": p.warehouse,
						},)

			for sand in self.get("molding_sand_details" ):
				se.append(
						"items",
						{
							"item_code": sand.item_code,
							"qty":  (ri.total_quantity * sand.quantity) / self.total_sand_weight,
							"s_warehouse": sand.warehouse,
						},)

			se.append(
						"items",
						{
							"item_code": ri.item_code,
							"qty": ri.total_quantity ,
							"t_warehouse": ri.target_warehouse,
							'is_finished_item':True
						},)

			se.custom_pouring = self.name	
			se.insert()
			se.save()
			se.submit()


	@frappe.whitelist()
	def calculation_after_short_quentity(self):
		for pd in self.get('pattern_details'):
			pm_rr_weight =frappe.get_value('Pattern Master',pd.pattern_code ,'rr_weight')
			casting_weight =frappe.get_value('Pattern Master',pd.pattern_code ,'casting_weight')

			for cd in self.get('casting_details'):
				if cd.short_quantity:
					total_quantity = pd.poured_boxes * cd.quantitybox


					cd.total_quantity = (total_quantity - int(cd.short_quantity) )
					cd.rr_weight_total = cd.rr_weight * cd.total_quantity
					cd.total_weight = (cd.casting_weight + cd.rr_weight) * (cd.total_quantity)

				

		self.total_pouring_weight = self.calculating_total_weight("casting_details","total_weight")
		self.totals_calculation()
		self.get_details_grade_master()


	def validate_pattern(self):
		pattern_details = self.get("pattern_details")
		for t in pattern_details:
			cmt_data = frappe.get_all("Casting Material Details", filters={"parent": t.pattern_code}, fields=['grade'])
			cmt_grades = set(cmt['grade'] for cmt in cmt_data)
			if len(cmt_grades) > 1:
				frappe.throw("❌ The pattern is faulty. Items in the pattern have different grades. Please ensure that all items have the same 'Grade'. Update the grade from the item master. ❌")

	def validate_pattern_equality(self):
		pattern_details = self.get("pattern_details")
		for  do in pattern_details:
			for so in pattern_details:
				if do.grade != so.grade:
					frappe.throw(" ❌ You Can Not select pattern with different grade ❌")
			break

	def create_rr_item_retain_items(self):
		rr_item = frappe.get_value("Grade Master",self.grade,"scrap_item_code")
		rr_item_warehouse = frappe.get_value("Grade Master",self.grade,"default_target_warehouse")
		if not rr_item:
			frappe.throw('Please Set RR item In Grade Master')

		retained_items = self.get("retained_items", filters={"rr_item":1})
		if not retained_items:
			self.append("retained_items",{
								'item_code': rr_item,
								'target_warehouse': rr_item_warehouse,
								'total_quantity': self.total_rr_weight,
								'rr_item' : True
							},),
		else:
			for g in retained_items:
				g.total_quantity = self.total_rr_weight

		heal_item = frappe.get_value("Grade Master",self.grade,"heal_item_code")
		heal_item_warehouse = frappe.get_value("Grade Master",self.grade,"default_target_warehouse_heal")
		if not heal_item:
			frappe.throw('Please Set Heal item In Grade Master')

		heal_metal = self.get("retained_items", filters={"item_code":heal_item})
		if not heal_metal:
			self.append("retained_items",{
								'item_code': heal_item,
								'target_warehouse': heal_item_warehouse,
								'total_quantity': 0,
								
							},),


	
	def totals_calculation(self):
		# if self.total_consumed_weight and self.total_pouring_weight:
		# 		self.total_weight_difference =  self.total_consumed_weight - self.total_pouring_weight

		self.total_rr_weight = self.calculating_total_weight("casting_details","rr_weight_total")
		self.total_sand_weight = self.calculating_total_weight("molding_sand_details","quantity")

	def calculate_normal_loss(self):
		total_sum =0
		for ri in self.get("retained_items" , filters={"rr_item":0}):
			if ri.total_quantity:
				total_sum = total_sum + ri.total_quantity

		self.normal_loss = self.total_consumed_weight - (self.total_pouring_weight + total_sum)
		

	def validate_total_charge_mix(self):
		total_furnece_kg = frappe.get_value("Furnece Master",self.furnece,"furnece_capcity")
		total_quantity = self.calculating_total_weight("change_mix_details","quantity")

		remit_value = ((total_furnece_kg*20)/100)
		total_valid_quantity = total_furnece_kg + remit_value

		if total_valid_quantity < total_quantity:
			frappe.throw(f'The Total Used Quantity of charge mix should be equal to {total_valid_quantity} which is Total Furnace Weight {total_furnece_kg} + 20% remit value {remit_value}' )

	@frappe.whitelist()
	def set_last_power_consumption(self):
		power_consumption = frappe.get_all('Pouring',
                                        filters ={'docstatus':1 ,},
                                        fields = ['name','power_reading_final'] ,order_by='creation DESC',limit=1)
		if power_consumption :
			for p in power_consumption:
				if not  self.power_reading_initial:
					self.power_reading_initial = p.power_reading_final
					
		doc = frappe.get_all("Laddle Master", filters = {'company':self.company})
		for d in doc:
			items = self.get("laddle_temperature", filters={"laddle":d.name})
			if 	not items:
				self.append("laddle_temperature",{
								'laddle': d.name,
							},),

	def validate_last_power_consumption(self):
		power_consumption = frappe.get_all('Pouring',
                                        filters ={'docstatus':1 ,},
                                        fields = ['name','power_reading_final'] ,order_by='creation DESC',limit=1)
		if power_consumption :
			for p in power_consumption:
					last_doc = p.power_reading_final

		if self.power_reading_initial and last_doc:
			if self.power_reading_initial < last_doc :
				frappe.msgprint("'Power Reading Initial' must be greater than last sumitted Pouring`s 'Power Reading Final'")

	def casting_treatment_analysis_details(self):
		casting_details = self.get("casting_details")
		casting_treatment_analysis = self.get("casting_treatment_analysis")
		casting_treatment_analysis.clear()

		for i in casting_details:
			casting_treatment_details = frappe.get_all("Casting Treatment Details",
																		filters = {"parent": i.pattern, "casting_items_code": i.item_code},
																		fields = ['casting_treatment','finished_target_warehouse','finished_source_warehouse'], order_by = 'idx ASC')
			p=0
			temp =0

			for j in casting_treatment_details:
				temp = temp + 1
				if p == 0:
					quantity_to_treatment = i.total_quantity
					p=1
				else:
					quantity_to_treatment = 0

				

				self.append("casting_treatment_analysis",{
								'pattern': i.pattern,
								'casting_item_code': i.item_code,
								'casting_treatment': j.casting_treatment,
								'quantity_to_treatment' : i.total_quantity,
								'treatment_done_quantity': 0,
								'casting_treatment_ok': 0,
								'casting_treatment_cr': 0,
								'casting_treatment_rw': 0,
								'treatment_remaining_quantity': quantity_to_treatment,
								'pouring_id' : self.name,
								'reference_id' : i.name,
								'status':'In Process',
								'treatment_no':temp,
								'source_warehouse':j.finished_source_warehouse if j.finished_source_warehouse else i.target_warehouse ,
								'target_warehouse':j.finished_target_warehouse ,
								
							},),



		






