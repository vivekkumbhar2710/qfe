# Copyright (c) 2023, Quantbit Technologies Pvt ltd and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class ProductCosting(Document):

	@frappe.whitelist()
	def grade_mix_data(self):
		if self.select_grade and self.total_weight:
			doc = frappe.get_all("Grade Items Details",
				  									filters = {"parent": self.select_grade},
													fields = ["item_code","item_name","item_group","percentage"])
			
			for d in doc:
				last_purchase_rate = frappe.get_value("Item",d.item_code ,"last_purchase_rate") or 0
				required_quantity = ((d.percentage * self.total_weight)/100)
				self.append("grade_mix",{
							'item_code': d.item_code ,
							'item_name': d.item_name,
							'item_group': d.item_group,
							'required_quantity': required_quantity,
							'last_purchase_rate': last_purchase_rate,
							'amount' : last_purchase_rate * required_quantity,
							'percentage': d.percentage,
						
						},),
		else:
			frappe.throw(f'please select both "Grade" and "Quantity To Manufacture" from table "Casting Details"')
			
		self.calculation_of_EPC()
	@frappe.whitelist()
	def calculating_total_weight(self):
		for i in self.get("casting_details"):
			if i.weight and i.quantity_to_manufacture:
				i.total_weight = i.weight * i.quantity_to_manufacture

		self.total_weight = self.calculating_total("casting_details","total_weight")

		if self.select_grade and self.total_weight:
			grade_mix = self.get("grade_mix")
			grade_mix.clear()
			self.grade_mix_data()

	def calculating_total(self,child_table ,total_field):
		casting_details = self.get(child_table)
		total_pouring_weight = 0
		for i in casting_details:
			field_data = i.get(total_field)
			if field_data:
				total_pouring_weight = total_pouring_weight + field_data
		return total_pouring_weight
	

	@frappe.whitelist()
	def overhead_amount_calculation(self):
		for f in self.get('overheads'):
			if f.rate and f.quantity:
				f.amount = f.rate * f.quantity

		self.calculation_of_EPC()

	def calculation_of_EPC(self):
		self.total_grade_mixture_cost = self.calculating_total("grade_mix","amount")
		self.total_overheads = self.calculating_total("overheads","amount")
		self.estimated_product_costing = self.total_grade_mixture_cost + self.total_overheads
		if self.total_weight:
			self.cost_per_kg = self.estimated_product_costing/self.total_weight