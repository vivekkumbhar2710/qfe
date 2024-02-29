# Copyright (c) 2024, Quantbit Technologies Pvt ltd and contributors
# For license information, please see license.txt
import frappe
from datetime import datetime,timedelta
def execute(filters=None):
	if not filters: filters={}
	columns, data =[],[]
	columns=get_column(filters)
	data=get_data(filters)
	if not data:
		frappe.msgprint('NO RECORD FOUND')
		return columns, data
	return columns, data


def get_warehouse_filters(filters):
	company=filters.get('company')
	warehouse=filters.get('warehouse')
	warehouse_group=filters.get('warehouse_group')
	warehouse_filter={}
	if(company):
		warehouse_filter.update({"company":company})
	if(warehouse_group):
		warehouse_filter.update({"parent_warehouse":warehouse_group})
	if(warehouse):
		warehouse_filter.update({"name":warehouse})
	warehouse_filter.update({"disabled":0})
	return warehouse_filter


def get_column(filters):
	warehouse_filter=get_warehouse_filters(filters)
	warehouse_list=frappe.get_all("Warehouse",filters=warehouse_filter,fields=["name"])
	warehouse_dict_list = []  
	warehouse_dict_list.append(
		{
			"fieldname": "item_code",
			"fieldtype": "Link",
			"label": "Item Code",
			"options": "Item",
			}
	)
	warehouse_dict_list.append(
		{
			"fieldname": "item_name",
			"fieldtype": "Data",
			"label": "Item Name",
			}
	)
	warehouse_dict_list.append(
		{
			"fieldname": "item_group",
			"fieldtype": "Link",
			"label": "Item Group",
			"options": "Item Group",
			}
	)
	for i in warehouse_list:
		warehouse_dict ={
			"fieldname": i.name,
			"fieldtype": "Float",
			"label": i.name,
		}
		warehouse_dict_list.append(warehouse_dict) 
	return warehouse_dict_list
	

def get_data(filters):
	company=filters.get('company')
	item_code=filters.get('item_code')
	item_group=filters.get('item_group')
	from_date=filters.get('from_date')
	to_date=filters.get('to_date')
	if to_date and from_date:
		to_date = datetime.strptime(to_date, "%Y-%m-%d")
		from_date = datetime.strptime(from_date, "%Y-%m-%d")
		if from_date > to_date:
			frappe.throw("From date cannot be greater than To Date")
  
	report_data_li=[]
	item_filter_dict={}
	if(company):
		item_filter_dict["custom_company"]=company
	if(item_code):
		item_filter_dict["name"]=item_code
	if(item_group):
		item_filter_dict["item_group"]=item_group
 
	item_list=frappe.get_all("Item",filters=item_filter_dict,fields=["name","item_name","item_group"])
	if(item_list):
		for i in item_list:
			doc_elemet_item={}
			doc_elemet_item["item_code"]=i.name
			doc_elemet_item["item_name"]=i.item_name
			doc_elemet_item["item_group"]=i.item_group
			warehouse_filter=get_warehouse_filters(filters)
			warehouse_list=frappe.get_all("Warehouse",filters=warehouse_filter,fields=["name"])
			if(warehouse_list):
				for j in warehouse_list:
					doc_elemet_item[str(j.name)]=get_item_qty_for_warehouse(j.name,to_date,company,i.name)
			report_data_li.append(doc_elemet_item)	
	return report_data_li


def get_item_qty_for_warehouse(warehouse,to_date,company,item_code):
	fiscal_year =frappe.db.sql("""
		SELECT name 
		FROM `tabFiscal Year`
		ORDER BY creation ASC
		LIMIT 1
	""", as_dict=True)

	opening_balance=frappe.db.sql("""
							SELECT qty_after_transaction 
							FROM `tabStock Ledger Entry` 
							WHERE posting_date <= '{0}' 
								AND warehouse = '{1}' 
								AND item_code = '{2}' 
								AND fiscal_year = '{3}' 
								AND company = '{4}' 
								AND is_cancelled='{5}'
							ORDER BY creation DESC 
							LIMIT 1
							""".format(to_date,warehouse,item_code,fiscal_year[0].name,company,False),as_dict=True)
	if(opening_balance):
		return opening_balance[0].qty_after_transaction
	return 0