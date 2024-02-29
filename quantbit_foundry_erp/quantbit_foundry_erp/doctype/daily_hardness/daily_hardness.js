// Copyright (c) 2024, Quantbit Technologies Pvt ltd and contributors
// For license information, please see license.txt

frappe.ui.form.on('Daily Hardness', {
	part_code:function(frm)
	{
		frm.call({
				method:'part_hardness',
				doc: frm.doc
		});
	}
});
 

frappe.ui.form.on('Daily Hardness', {
    refresh: function(frm) {
        frappe.call({
            method: 'set_filters_for_items',
            doc: frm.doc,
            callback: function(r) {
                if (r.message) {
                    var k = r.message;
                    frm.set_query("part_code", function(doc, cdt, cdn) {
                        return {
                            filters: [
                                ['Item', 'name', 'in', k],
                                ['Item', 'company', '=', doc.company]
                            ]
                        };
                    });
                }
            }
        });
    }
});
