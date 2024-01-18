# Copyright (c) 2023, Quantbit Technologies Pvt ltd and contributors
# For license information, please see license.txt

import frappe


def execute(filters=None):
	columns, data = [], []
	columns = get_columns()
	data = get_data()

	return columns, data

def get_columns():
	return [
		{
			"fieldname": "name",
			"fieldtype": "Link",
			"label": "Pouring",
			"options": "Pouring",
		},
		{
			"fieldname": "heat_date",
			"fieldtype": "Date",
			"label": " From Heat Date",
		},
		{
			"fieldname": "supervisor",
			"fieldtype": "Link",
			"label": "Supervisor ID",
			"options": "Employee",
		},
		{
			"fieldname": "operator",
			"fieldtype": "Link",
			"label": "Operator ID",
			"options": "Employee",
		},
		{
			"fieldname": "shift",
			"fieldtype": "Link",
			"label": "Shift",
			"options": "Shift Master",
		},
	]

def get_data():
	data = frappe.get_all("Pouring", fields =['name','heat_date','supervisor','operator','shift'])
	return data