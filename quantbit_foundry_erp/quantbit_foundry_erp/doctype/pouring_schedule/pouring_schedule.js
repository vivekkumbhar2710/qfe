// Copyright (c) 2024, Quantbit Technologies Pvt ltd and contributors
// For license information, please see license.txt

frappe.ui.form.on('Pouring Schedule', {
	// refresh: function(frm) {

	// }
});

// ============================================================= Pouring Schedule =================================================


frappe.ui.form.on('Pouring Schedule', {
    item_group: function(frm) {
		frm.clear_table("item_pouring_schedule");
		frm.refresh_field('item_pouring_schedule');
            frm.call({
			method:'set_items_in_IPS',
			doc:frm.doc,
		});
    }
});

frappe.ui.form.on('Pouring Schedule', {
	setup: function(frm) {
		frm.set_query("item_code", "item_pouring_schedule", function(doc, cdt, cdn) {
			let d = locals[cdt][cdn];
			let filters = {};
            filters["custom_company"] = frm.doc.company;
            if (frm.doc.item_group != 'All Item Groups') {
                filters["item_group"] = frm.doc.item_group;
            }

            return {
                filters: filters
            };
		});
	},
});

frappe.ui.form.on('Pouring Schedule', {
    refresh: function(frm) {
            frm.call({
			method:'method_after_refresh_call',
			doc:frm.doc,
		});
    }
});

frappe.ui.form.on('Pouring Schedule', {
    refresh_button: function(frm) {

            frm.call({
			method:'method_after_refresh_call',
			doc:frm.doc,
		});
    }
});
// ============================================================= Item Pouring Schedule =================================================

frappe.ui.form.on('Item Pouring Schedule', {
    weight_per_unit_quantity: function(frm) {

            frm.call({
			method:'calculate_total_weight',
			doc:frm.doc,
		});
    }
});
frappe.ui.form.on('Item Pouring Schedule', {
    schedule_quantity: function(frm) {

            frm.call({
			method:'calculate_total_weight',
			doc:frm.doc,
		});
    }
});