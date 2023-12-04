// Copyright (c) 2023, Quantbit Technologies Pvt ltd and contributors
// For license information, please see license.txt

frappe.ui.form.on('Pattern Master', {
	// refresh: function(frm) {

	// }
});


// ============================================================= Pattern Master =================================================
frappe.ui.form.on('Pattern Master', {
    box_weight: function(frm) {

		// frm.clear_table("casting_details");
		// frm.refresh_field('casting_details');
            frm.call({
			method:'calculating_casting_weight',
			doc:frm.doc,
		});
    }
});


// frappe.ui.form.on('Pattern Master', {
// 	setup: function(frm) {
// 		frm.set_query("casting_item_code", "core_material_details", function(doc, cdt, cdn) {
// 			let d = locals[cdt][cdn];
// 			return {

// 				filters: [
// 				['Item', 'item_type', '=', "Raw Item"],
// 				]
// 			};
// 		});
// 	},
// });


frappe.ui.form.on('Pattern Master', {
    refresh: function(frm) {
            frappe.call({
                method: 'set_filters_for_items',
                doc: frm.doc,
                callback: function(r) {
                    if (r.message) {
                        var k = r.message;
                        frm.set_query("casting_item_code", "core_material_details", function(doc, cdt, cdn) {
                            let d = locals[cdt][cdn];
                            return {
                                filters: [
                                    ['Item', 'name', 'in', k],
                                ]
                            };
                        });
                    }
                }
			});
        
    }
});


frappe.ui.form.on('Pattern Master', {
    refresh: function(frm) {
            frappe.call({
                method: 'set_filters_for_items',
                doc: frm.doc,
                callback: function(r) {
                    if (r.message) {
                        var k = r.message;
                        frm.set_query("casting_items_code", "casting_treatment_details", function(doc, cdt, cdn) {
                            let d = locals[cdt][cdn];
                            return {
                                filters: [
                                    ['Item', 'name', 'in', k],
                                ]
                            };
                        });
                    }
                }
			});
        
    }
});


// ============================================================= Casting Material Details =================================================


frappe.ui.form.on('Casting Material Details', {
    weight: function(frm) {

		// frm.clear_table("casting_details");
		// frm.refresh_field('casting_details');
            frm.call({
			method:'calculating_casting_weight',
			doc:frm.doc,
		});
    }
});

frappe.ui.form.on('Casting Material Details', {
    qty: function(frm) {

		// frm.clear_table("casting_details");
		// frm.refresh_field('casting_details');
            frm.call({
			method:'calculating_cavities',
			doc:frm.doc,
		});
    }
});



frappe.ui.form.on('Casting Material Details', {
    item_code: function(frm) {
            frappe.call({
                method: 'set_filters_for_items',
                doc: frm.doc,
                callback: function(r) {
                    if (r.message) {
                        var k = r.message;
                        frm.set_query("casting_item_code", "core_material_details", function(doc, cdt, cdn) {
                            let d = locals[cdt][cdn];
                            return {
                                filters: [
                                    ['Item', 'name', 'in', k],
                                ]
                            };
                        });
                    }
                }
			});
        
    }
});



frappe.ui.form.on('Casting Material Details', {
    item_code: function(frm) {
            frappe.call({
                method: 'set_filters_for_items',
                doc: frm.doc,
                callback: function(r) {
                    if (r.message) {
                        var k = r.message;
                        frm.set_query("casting_items_code", "casting_treatment_details", function(doc, cdt, cdn) {
                            let d = locals[cdt][cdn];
                            return {
                                filters: [
                                    ['Item', 'name', 'in', k],
                                ]
                            };
                        });
                    }
                }
			});
        
    }
});
