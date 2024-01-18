# Copyright (c) 2024, Quantbit Technologies Pvt ltd and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import get_link_to_form
import calendar
from datetime import datetime


class PouringSchedule(Document):
	@frappe.whitelist()
	def set_items_in_IPS(self):
		if self.item_group:
			if self.item_group == 'All Item Groups':
				filters = {}
			else:
				filters ={ "item_group" : self.item_group }

			doc = frappe.get_all( "Item" , 
											filters = filters ,
											fields = ["name" , "item_name"])
			for d in doc:
				self.append("item_pouring_schedule",{
													'item_code': d.name,
													'item_name': d.item_name,
													'weight_per_unit_quantity': self.get_weight_of_item(d.name)
													},),


	@frappe.whitelist()
	def calculate_total_weight(self):
		item_pouring_schedule = self.get("item_pouring_schedule")
		total_qty = 0
		total_weight = 0
		for d in item_pouring_schedule:
			if d.weight_per_unit_quantity and d.schedule_quantity:
				d.total_weight =  d.weight_per_unit_quantity * d.schedule_quantity

		self.total_quantity = self.calculating_total_weight('item_pouring_schedule','schedule_quantity')
		self.total_weight = self.calculating_total_weight('item_pouring_schedule','total_weight')



	@frappe.whitelist()
	def get_weight_of_item(self , item_code ):
		item_uom = frappe.get_value("Item",item_code,"stock_uom")
		if item_uom == 'Kg':
			item_weight = frappe.get_value("Item",item_code,"weight")
		else:
			item_weight = frappe.get_value("Production UOM Definition",{"parent":item_code,"uom": 'Kg'},"value_per_unit")
		return  item_weight if item_weight else 0
	
	@frappe.whitelist()
	def calculating_total_weight(self,child_table ,total_field):
		casting_details = self.get(child_table)
		total_pouring_weight = 0
		for i in casting_details:
			field_data = i.get(total_field)
			if field_data:
				total_pouring_weight = total_pouring_weight + field_data
		return total_pouring_weight



	@frappe.whitelist()
	def method_after_refresh_call(self):
		if self.year and self.month:
			self.from_date , self.to_date = self.get_month_dates( int(self.year),self.month)
		self.refresh_calculate_total_weight()
		self.refresh_get_pouring_data()

	@frappe.whitelist()
	def refresh_calculate_total_weight(self):
		item_pouring_schedule = self.get("item_pouring_schedule")
		for d in item_pouring_schedule:
			if d.item_code:
				d.weight_per_unit_quantity = self.get_weight_of_item(d.item_code)
				d.total_weight = d.weight_per_unit_quantity * d.schedule_quantity

	@frappe.whitelist()
	def refresh_get_pouring_data(self):
		item_pouring_schedule = self.get("item_pouring_schedule")
		for d in item_pouring_schedule:
			if d.item_code:
				total_qty_of_items = frappe.db.sql("""
														SELECT b.item_code, SUM(b.total_quantity) 
														FROM `tabPouring` a
														LEFT JOIN `tabCasting Details` b ON a.name = b.parent
														WHERE a.heat_date BETWEEN %s AND %s AND b.item_code = %s
													""",(self.from_date ,self.to_date ,d.item_code),as_dict="True")
				d.actual_poured_quantity = total_qty_of_items[0]['SUM(b.total_quantity)']
				if d.actual_poured_quantity:
					d.actual_total_poured_weight = d.actual_poured_quantity * d.weight_per_unit_quantity
			
		self.total_quantity = self.calculating_total_weight('item_pouring_schedule','schedule_quantity')
		self.total_weight = self.calculating_total_weight('item_pouring_schedule','total_weight')
		self.total_actual_quantity = self.calculating_total_weight('item_pouring_schedule','actual_poured_quantity')
		self.total_actual_weight = self.calculating_total_weight('item_pouring_schedule','actual_total_poured_weight')

	def get_month_dates(self ,year, month_name):
		month_number = datetime.strptime(month_name, "%B").month
		_, last_day = calendar.monthrange(year, month_number)

		start_date = datetime(year, month_number, 1)
		end_date = datetime(year, month_number, last_day)

		return start_date, end_date

		# """	select a.heat_date , b.item_code , b.total_quantity from `tabPouring` a
		# 													Left join `tabCasting Details` b on a.name = b.parent
		# 													where a.heat_date between %({0})$ and %({1})$ and b.item_code = {2}
		# 												"""