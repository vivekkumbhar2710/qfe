# Copyright (c) 2023, Quantbit Technologies Pvt ltd and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import get_link_to_form


class PatternMaster(Document):


	def before_save(self):
		self.set_weight()
		self.calculating_casting_weight()
		self.calculating_cavities()
		self.validate_grade()
		self.warehouse_settings()
		self.velify_pattern_details()
		# self. = self.box_weight - self.casting_weight

		# self.box_weight = (self.no_of_cavities * self.casting_weight )+ self.rr_weight 


	@frappe.whitelist()
	def set_weight(self):
		for i in self.get('casting_material_details'):
			if i.item_code:
				i.weight = self.item_weight_per_unit( i.item_code)

	@frappe.whitelist()
	def item_weight_per_unit(self , item_code ):
		item_uom = frappe.get_value("Item",item_code,"stock_uom")
		if item_uom == 'Kg':
			item_weight = frappe.get_all("Item",item_code,"weight")
		else:
			production_uom_definition = frappe.get_all("Production UOM Definition",
																				filters = {"parent":item_code,"uom": 'Kg'},
																				fields = ["value_per_unit"])
			if production_uom_definition:
				for k in production_uom_definition:
					item_weight= k.value_per_unit
			else:
				frappe.throw(f'Please Set "Production UOM Definition" For Item {get_link_to_form("Item",item_code)} of UOM "Kg" ')
		if item_weight:
			return  item_weight
		else:
			return 0

	
	@frappe.whitelist()
	def calculating_casting_weight(self):
		pattern_details = self.get("casting_material_details")
		total_weight = 0
		
		for i in pattern_details:
			if i.item_code and i.weight and i.qty:
				total_weight = total_weight + (i.weight * i.qty)

		self.casting_weight = total_weight

		if self.box_weight:
			rr_weight = self.box_weight - self.casting_weight
			if rr_weight >=0:
				self.rr_weight = rr_weight
			else:
				frappe.throw("RR Weight should not be negative! 🛑")

	@frappe.whitelist()
	def calculating_cavities(self):
		pattern_details = self.get("casting_material_details")
		total_cavity = 0
		for i in pattern_details:
			if i.item_code :
				total_cavity = total_cavity + i.qty

		self.no_of_cavities = total_cavity

		if self.no_of_cavities == 0:
			frappe.throw("No. of Cavities should not be zero 🚫")

		self.calculating_casting_weight()

	@frappe.whitelist()
	def set_filters_for_items(self):
		final_listed =[]
		for d in self.get('casting_material_details'):
			final_listed.append(d.item_code)
		return final_listed
	
	@frappe.whitelist()
	def validate_grade(self):
		pogo = self.get('casting_material_details')
		for d in pogo:
			for m in pogo:
				if d.grade != m.grade:
					frappe.throw(f'Grade of Casting Items are not matching 🚨')
			break
		self.grade = d.grade

	@frappe.whitelist()
	def warehouse_settings(self):
		casting_material_details = self.get("casting_material_details")
		for i in casting_material_details:
			casting_treatment_details = self.get("casting_treatment_details" , filters = {"casting_items_code": i.item_code})
			
			source_warehouse = None
			for j in casting_treatment_details:
				Targer_warehouse = frappe.get_value('Casting Treatment Master',j.casting_treatment,'ft_warehouse')
				j.finished_target_warehouse = Targer_warehouse
				j.finished_source_warehouse = source_warehouse
				source_warehouse = Targer_warehouse
				# warehouse = frappe.get_value('Casting Treatment Master',j.casting_treatment,'ft_warehouse')


		# frappe.throw(str(len(casting_treatment_details)))
		
	def velify_pattern_details(self):
		casting_treatment_details = self.get('casting_treatment_details')
		core_material_details = self.get("core_material_details")
		casting_material_details = self.get("casting_material_details")

		td = set([i.casting_items_code for i in casting_treatment_details])
		cd = set([j.casting_item_code for j in core_material_details])
		castd = set([k.item_code for k in casting_material_details])

		missing_items = set()
		for code in td.union(cd):
			if code not in castd:
				missing_items.add(code)

		if missing_items:
			frappe.throw(f'{missing_items} are not present in "Casting Material Details"')