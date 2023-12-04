# Copyright (c) 2023, Quantbit Technologies Pvt ltd and contributors
# For license information, please see license.txt

import frappe


def execute(filters=None):
	if not filters: filters={}

	columns, data = [], []

	columns = get_columns()
	data = get_cs_data(filters)

	if not data:
		frappe.msgprint('🙄😵 NO RECORD FOUND 😵🙄')
		return columns, data
	
	# data = []
	# do 


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


def get_cs_data(filters):
	conditions = get_conditions(filters)
	data = frappe.get_all ("Pouring",
									fields = ['name','heat_date','supervisor','operator','shift'],
									filters = conditions,
									)
	return data


def get_conditions(filters):
	# conditions={}
	# for key , value in filters.items():
	# 	if filters.get(key):
	# 		conditions[key] = value
	from_heat_date = filters.get('from_heat_date')
	to_heat_date =  filters.get('to_heat_date')

	if from_heat_date or to_heat_date:
		
		data={'heat_date': ['between',[ filters.get('from_heat_date', '2001-01-01'), filters.get('to_heat_date', '2100-01-01')]]}
		filters.update(data)
		if from_heat_date:
			filters.pop('from_heat_date')
		if to_heat_date:
			filters.pop('to_heat_date')
			
	return filters
