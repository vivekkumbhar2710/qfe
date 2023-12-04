# Copyright (c) 2023, Quantbit Technologies Pvt ltd and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class PatternMaster(Document):


	def before_save(self):
		self.calculating_casting_weight()
		self.calculating_cavities()
		self.validate_grade()
		# self. = self.box_weight - self.casting_weight
		# self.box_weight = (self.no_of_cavities * self.casting_weight )+ self.rr_weight
	
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
		
	