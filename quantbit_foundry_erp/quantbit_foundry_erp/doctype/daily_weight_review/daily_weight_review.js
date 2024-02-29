// Copyright (c) 2024, Quantbit Technologies Pvt ltd and contributors
// For license information, please see license.txt

frappe.ui.form.on('Daily Weight Review', {
    refresh: function(frm) {
            frappe.call({
                method: 'set_filters_for_items',
                doc: frm.doc,
                callback: function(r) {
                    if (r.message) {
                        var k = r.message;
                        frm.set_query("part_code", "weight_details", function(doc, cdt, cdn) {
                            let d = locals[cdt][cdn];
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

frappe.ui.form.on('Pouring Details', {
	part_code:function(frm)
	{
		frm.call({
				method:'cavity_standard',
				doc: frm.doc
		});
	}
});

frappe.ui.form.on('Pouring Details', {
    reading_1: function (frm) {
        frm.call({
			method:'average_weight_calculation',
			doc:frm.doc,
		})

    }
});

frappe.ui.form.on('Pouring Details', {
    reading_2: function (frm) {
        frm.call({
			method:'average_weight_calculation',
			doc:frm.doc,
		})

    }
});

frappe.ui.form.on('Pouring Details', {
    reading_3: function (frm) {
        frm.call({
			method:'average_weight_calculation',
			doc:frm.doc,
		})

    }
});


frappe.ui.form.on('Pouring Details', {
    reading_4: function (frm) {
        frm.call({
			method:'average_weight_calculation',
			doc:frm.doc,
		})

    }
});

frappe.ui.form.on('Pouring Details', {
    reading_5: function (frm) {
        frm.call({
			method:'average_weight_calculation',
			doc:frm.doc,
		})

    }
});