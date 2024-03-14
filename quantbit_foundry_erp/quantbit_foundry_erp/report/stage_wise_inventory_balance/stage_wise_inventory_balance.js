// Copyright (c) 2024, Quantbit Technologies Pvt ltd and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Stage Wise Inventory Balance"] = {
	"filters": [
		{
			fieldname: "company",
			fieldtype: "Link",
			label: "Company",
			options: "Company",
			default: frappe.defaults.get_user_default('company'),
			reqd: 1
		},
		{
			fieldname: "from_date",
			fieldtype: "Date",
			label: "From Date",
			default:frappe.datetime.add_days(frappe.datetime.get_today(), -30),
			reqd: 1
		},
		{
			fieldname: "to_date",
			fieldtype: "Date",
			label: "To Date",
			default:frappe.datetime.get_today(),
			reqd: 1
		},
		{
            fieldname: "item_group",
            fieldtype: "Link",
            label: "Item Group",
            options: "Item Group",
			get_query: function() {
				const company = frappe.query_report.get_filter_value('company');
				return {
					filters: { 'custom_company': company }
				}
			}
        },
		{
			fieldname: "item_code",
			fieldtype: "Link",
			label: "Item Code",
			options: "Item",
			get_query: function() {
				const company = frappe.query_report.get_filter_value('company');
				const item_group=frappe.query_report.get_filter_value('item_group');
				if(item_group)
				{
					return {
						filters: {'custom_company': company ,'item_group': item_group},
					}
				}
				else
				{
					return {
						filters: {'custom_company': company},
					}
				}
			}
			
		},
		{
			fieldname: "warehouse_group",
			fieldtype: "Link",
			label: "Warehouse Group",
			options: "Warehouse",
			default: "",
			get_query: function() {
				const company = frappe.query_report.get_filter_value('company');
				return {
					filters: { 'company': company ,"is_group":1},
				}
			}
		},
		{
			fieldname: "warehouse",
			label: __("Warehouse"),
			fieldtype: "Link",
			options: "Warehouse",
			default: "",
			get_query: function() {
				const company = frappe.query_report.get_filter_value('company');
				const parent_warehouse = frappe.query_report.get_filter_value('warehouse_group');
				if(parent_warehouse)
				{
					return {
						filters:{'company':company ,'parent_warehouse': parent_warehouse, "is_group":0},
					}
				}
				else
				{
					return {
						filters: { 'company': company, "is_group":0},
					}
				}
			}
		},
		{
			fieldname: "include_uom",
			fieldtype: "Link",
			label: "Include UOM",
			default:"",
			options:"UOM"
		},
	]
};

