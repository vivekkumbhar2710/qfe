# Copyright (c) 2024, Quantbit Technologies Pvt ltd and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class DailySpectroAnalysis(Document):
    @frappe.whitelist()
    def part(self, child_index, pouring_id): 
       
        casting_details = frappe.db.get_all("Casting Details", {"parent": pouring_id}, ['parent', 'item_code', 'item_name'])
        if casting_details:
            status = 0 
            for i in casting_details:
                p = frappe.get_value('Chemical Composition Item Master', i.item_code,'name')
                sccr = lambda: None  
                sccr.c , sccr.si, sccr.mn, sccr.s, sccr.p, sccr.cu, sccr.mg, sccr.cr =  None,None,None,None,None,None,None,None
                if p:
                    sccr = frappe.get_doc('Chemical Composition Item Master', i.item_code)
                if len(casting_details) >= 1 and status == 0:
                    self.get("daily_spectro_details")[child_index - 1].item_code = i.item_code
                    self.get("daily_spectro_details")[child_index - 1].item_name = i.item_name
                    self.get("daily_spectro_details")[child_index - 1].standard_chemical_composition_range = i.item_name
                    self.get("daily_spectro_details")[child_index - 1].c_ = sccr.c
                    self.get("daily_spectro_details")[child_index - 1].si_ = sccr.si
                    self.get("daily_spectro_details")[child_index - 1].mn_ = sccr.mn
                    self.get("daily_spectro_details")[child_index - 1].s_ = sccr.s
                    self.get("daily_spectro_details")[child_index - 1].p_ = sccr.p
                    self.get("daily_spectro_details")[child_index - 1].cu_ = sccr.cu
                    self.get("daily_spectro_details")[child_index - 1].mg_ = sccr.mg
                    self.get("daily_spectro_details")[child_index - 1].cr_ = sccr.cr
                    
                    status += 1
                    continue
                if len(casting_details) >= 1 and status > 0:
                    self.append("daily_spectro_details", {
                        "pouring_id":i.parent,
                        "item_code": i.item_code,
                        "item_name": i.item_name,
                        "standard_chemical_composition_range" :i.item_code,
                        'c_':sccr.c,
                        'si_':sccr.si,
                        'mn_':sccr.mn,
                        's_':sccr.s,
                        'p_':sccr.p,
                        'cu_':sccr.cu,
                        'mg_':sccr.mg,
                        'cr_':sccr.cr,
                    })


    