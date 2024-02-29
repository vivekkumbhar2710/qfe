# Copyright (c) 2024, Quantbit Technologies Pvt ltd and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

def GetVal(value):
    return value if value else 0

class DailyWeightReview(Document):
	@frappe.whitelist()
	def cavity_standard(self):
		weight_details = self.get("weight_details")
		for row in weight_details : 
			if row.part_code :
				pouring_id  = frappe.get_value('Casting Details',{'item_code':row.part_code}, "Parent")
				casting_weight = frappe.get_value('Casting Details',{'item_code':row.part_code},'casting_weight')
				quantitybox = frappe.get_value('Casting Details',{'item_code':row.part_code},'quantitybox')
				# frappe.throw(str(quantitybox))
				if pouring_id :
					row.pouring_id = pouring_id
					pouring = frappe.get_doc("Pouring", pouring_id)
					row.heat_no = pouring.heat_no
					row.heat_date = pouring.heat_date
					row.standard_weight = casting_weight
					row.cavity = quantitybox
				else :
					frappe.msgprint("This Item is not available in any pouring")
					row.part_code = None
     
	@frappe.whitelist()
	def average_weight_calculation(self):
		weight_details = self.get("weight_details")
		for row in weight_details :
			total = GetVal(row.reading_1) + GetVal(row.reading_2) + GetVal(row.reading_3) + GetVal(row.reading_4) + GetVal(row.reading_5)
			filtered_list = [x for x in [GetVal(row.reading_1), GetVal(row.reading_2), GetVal(row.reading_3), GetVal(row.reading_4), GetVal(row.reading_5)] if x is not None and x != 0]
			if len(filtered_list) != 0:
				avg_weight = total/len(filtered_list)
				row.average_weight = avg_weight	
	
				extra_weight = 	avg_weight - GetVal(row.standard_weight)
				row.extra_weight = extra_weight
				
	
				wt_value = (avg_weight / GetVal(row.standard_weight))*100
				row.wt_value = wt_value


	@frappe.whitelist()
	def set_filters_for_items(self):
		final_listed =[]
		doc = frappe.get_all("Casting Details", fields =['item_code'] , distinct = 'item_code' )
		for d in doc:
			final_listed.append(d.item_code)
		return final_listed			
	
		
	
