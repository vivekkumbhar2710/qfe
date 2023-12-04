// Copyright (c) 2023, Quantbit Technologies Pvt ltd and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Pouring Rejection Report With Date Range"] = {
	"filters": [

		{
			"fieldname": "name",
			"fieldtype": "Link",
			"label": "Pouring",
			"options": "Pouring",
			
		},
		{
			"fieldname": "from_heat_date",
			"fieldtype": "Date",
			"label": " From Heat Date",
			
		},
		{
			"fieldname": "to_heat_date",
			"fieldtype": "Date",
			"label": " To Heat Date",
			
		},

	]
};
