# Copyright (c) 2024, Quantbit Technologies Pvt ltd and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class DailyHardness(Document):
	@frappe.whitelist()
	def part_hardness(self):
		pouring_id  = frappe.get_value('Casting Details',{'item_code':self.part_code}, "Parent")
		heat_date,heat_no,grade  = frappe.get_value('Pouring',{'name':pouring_id}, ["heat_date","heat_no","grade"])
		self.pouring_id = pouring_id

		if pouring_id :
			self.heat_no=heat_no
			self.heat_date=heat_date
			self.grade=grade
		else :
			frappe.msgprint("This Item is not available in any pouring")
			self.part_code = None

	@frappe.whitelist()
	def set_filters_for_items(self):
		final_listed =[]
		doc = frappe.get_all("Casting Details", fields =['item_code'] , distinct = 'item_code' )
		for d in doc:
			final_listed.append(d.item_code)
		return final_listed	
		