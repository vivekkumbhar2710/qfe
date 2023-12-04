# Copyright (c) 2023, Quantbit Technologies Pvt ltd and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class GradeMaster(Document):
	
	def before_save(self):
		self.validate_percentage()
		# self.calculating_cavities()
	
	@frappe.whitelist()
	def validate_percentage(self):
		grade_items_details = self.get("grade_items_details")
		total_percentage = 0
		for i in grade_items_details:
			if i.percentage :
				total_percentage = total_percentage + i.percentage

		if total_percentage !=100 :
			frappe.throw(f'The addition of toal percentage must equal to 100 % the difference is {100- total_percentage}')