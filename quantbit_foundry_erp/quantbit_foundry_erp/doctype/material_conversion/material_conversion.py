# Copyright (c) 2024, Quantbit Technologies Pvt ltd and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

def getVal(val):
	return val if val is not None else 0

class MaterialConversion(Document):
	@frappe.whitelist()
	def get_available_quantity_input_material(self):
		input_material = self.get("input_material")
		for row in input_material : 
			if row.warehouse :
				actual_qty = frappe.get_value('Bin',{'item_code':row.item_code,"warehouse":row.warehouse},'actual_qty')
				if actual_qty :
					row.available_quantity = actual_qty
				else :
					frappe.msgprint("The Available Quantity for this item in the warehouse is not available.")
					row.warehouse = None 
      
	@frappe.whitelist()
	def get_available_quantity_output_material(self):
		output_material = self.get("output_material")
		for row in output_material : 
			if row.warehouse :
				actual_qty = frappe.get_value('Bin',{'item_code':row.item_code,"warehouse":row.warehouse},'actual_qty')
				if actual_qty :
					row.available_quantity = actual_qty
				
	@frappe.whitelist()
	def get_value_per_unit_for_input(self):
		input_material = self.get("input_material")
		for i in input_material:
			if i.item_code:
				value = frappe.get_value('Production UOM Definition',{'parent': i.item_code ,'uom':'Kg'}, "value_per_unit")
				i.weight_per_unit = value if value else 0

	@frappe.whitelist()
	def get_value_per_unit_for_output(self):
		output_material = self.get("output_material")
		for i in output_material:
			if i.item_code:
				value = frappe.get_value('Production UOM Definition',{'parent': i.item_code ,'uom':'Kg'}, "value_per_unit")
				i.weight_per_unit = value if value else 0

	@frappe.whitelist()  
	def total_weight_on_input_material(self):
		input_material = self.get("input_material") 
		for row in input_material:
			total_weight = getVal(row.quantity) * getVal(row.weight_per_unit)
			row.total_weight = total_weight
	
	@frappe.whitelist()  
	def total_weight_on_output_material(self):
		output_material = self.get("output_material") 
		for row in output_material:
			total_weight = getVal(row.quantity) * getVal(row.weight_per_unit)
			row.total_weight = total_weight
		
	@frappe.whitelist()
	def call_method(self):
		self.input_total_quantity = self.calculating_total('input_material','quantity')	

	@frappe.whitelist()
	def call_method_output(self):
		#frappe.msgprint("Hii in Output Material")
		self.output_total_quantity = self.calculating_total('output_material','quantity')	

	@frappe.whitelist()
	def calculating_total(self,child_table ,total_field):
		casting_details = self.get(child_table)
		total_pouring_weight = 0
		for i in casting_details:
			field_data = getVal(i.get(total_field))
			total_pouring_weight = total_pouring_weight + field_data
		return total_pouring_weight
	

	def on_submit(self):
		self.Manufacturing_stock_entry()

	# After Submitting Component Work Order Manufacturing Stock Entry will be created 
	@frappe.whitelist()
	def Manufacturing_stock_entry(self):
		doc = frappe.new_doc("Stock Entry")
		doc.stock_entry_type = "Manufacture"
		doc.company = self.company
		doc.posting_date =self.posting_date

		for i in self.get("input_material"):
			doc.append("items", {
				"s_warehouse": i.warehouse,
				"item_code": i.item_code,
				"qty": i.quantity ,
			})
		
		for i in self.get("output_material"):
			doc.append("items", {
				"t_warehouse": i.warehouse,
				"item_code": i.item_code,
				"qty": i.quantity,
				"is_finished_item": True,
			})
		
		# doc.custom_component_work_order = self.name
		doc.insert()
		doc.save()
		doc.submit()
		