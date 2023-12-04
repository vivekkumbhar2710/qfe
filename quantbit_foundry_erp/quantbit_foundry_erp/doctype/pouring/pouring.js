// Copyright (c) 2023, Quantbit Technologies Pvt ltd and contributors
// For license information, please see license.txt

frappe.ui.form.on('Pouring', {
	// refresh: function(frm) {

	// }
});
// ============================================================= Pouring =================================================
frappe.ui.form.on('Pouring', {
    refresh: function(frm) {
        frm.fields_dict['furnece'].$input.css('background-color', '#8FC5FF');
        frm.fields_dict['supervisor'].$input.css('background-color', '#8FC5FF');
        frm.fields_dict['operator'].$input.css('background-color', '#8FC5FF');
        frm.fields_dict['contractor'].$input.css('background-color', '#8FC5FF');
        frm.fields_dict['shift'].$input.css('background-color', '#8FC5FF');
    }
});

frappe.ui.form.on('Pouring', {
    grade: function(frm) {

		frm.clear_table("change_mix_details");
		frm.refresh_field('change_mix_details');
            frm.call({
			method:'get_details_grade_master',
			doc:frm.doc,
		});
    }
});

frappe.ui.form.on('Pouring', {
    furnece: function(frm) {

		

			frm.clear_table("casting_details");
			frm.refresh_field('casting_details');
	
			frm.clear_table("core_details");
			frm.refresh_field('core_details');

			frm.clear_table("change_mix_details");
			frm.refresh_field('change_mix_details');

			frm.clear_table("molding_sand_details");
			frm.refresh_field('molding_sand_details');
	
			// 	frm.call({
			// 	method:'get_details_pattern_master',
			// 	doc:frm.doc,
			// });
	}
    
});

frappe.ui.form.on('Pouring', {
    power_reading_final: function(frm) {

            frm.call({
			method:'calculating_power_consumption',
			doc:frm.doc,
		});
    }
});

frappe.ui.form.on('Pouring', {
    power_reading_initial: function(frm) {

            frm.call({
			method:'calculating_power_consumption',
			doc:frm.doc,
		});
    }
});

frappe.ui.form.on('Pouring', {
    refresh: function(frm) {

            frm.call({
			method:'set_last_power_consumption',
			doc:frm.doc,
		});
    }
});



frappe.ui.form.on('Pouring', {
	setup: function(frm) {
		frm.set_query("pattern_code", "pattern_details", function(doc, cdt, cdn) {
			let d = locals[cdt][cdn];
			return {

				filters: [
				['Pattern Master', 'enable', '=', 1],
				]
			};
		});
	},
});

	frappe.ui.form.on("Pouring", {
		setup: function(frm) {
				frm.set_query("supervisor", function() { // Replace with the name of the link field
					return {
						filters: [
							["Employee", "company", '=', frm.doc.company],// Replace with your actual filter criteria
							["Employee", "designation", '=', 'Supervisor'],
						]
					};
				});
	
			}
		});

	frappe.ui.form.on("Pouring", {
		setup: function(frm) {
				frm.set_query("operator", function() { // Replace with the name of the link field
					return {
						filters: [
							["Employee", "company", '=', frm.doc.company],// Replace with your actual filter criteria
							["Employee", "designation", '=', 'Operator'],
						]
					};
				});
	
			}
		});

// ============================================================= Pattern Details =================================================



frappe.ui.form.on('Pattern Details', {
    poured_boxes: function(frm) {

		frm.clear_table("casting_details");
		frm.refresh_field('casting_details');

		frm.clear_table("core_details");
		frm.refresh_field('core_details');

		frm.clear_table("change_mix_details");
		frm.refresh_field('change_mix_details');

		frm.clear_table("molding_sand_details");
			frm.refresh_field('molding_sand_details');

            frm.call({
			method:'get_details_pattern_master',
			doc:frm.doc,
		});
    }
});


frappe.ui.form.on('Pattern Details', {
    pattern_code: function(frm ,cdt, cdn) {

		var child = locals[cdt][cdn];

		// if (child.doc.poured_boxes) {

			frm.clear_table("casting_details");
			frm.refresh_field('casting_details');
	
			frm.clear_table("core_details");
			frm.refresh_field('core_details');

			frm.clear_table("change_mix_details");
			frm.refresh_field('change_mix_details');

			frm.clear_table("molding_sand_details");
			frm.refresh_field('molding_sand_details');
	
				frm.call({
				method:'get_details_pattern_master',
				doc:frm.doc,
			});
	}

    // }
});

frappe.ui.form.on('Pattern Details', {
    sales_order: function(frm) {

		if (frm.doc.poured_boxes) {

			frm.clear_table("casting_details");
			frm.refresh_field('casting_details');
	
			frm.clear_table("core_details");
			frm.refresh_field('core_details');

			frm.clear_table("change_mix_details");
			frm.refresh_field('change_mix_details');

			frm.clear_table("molding_sand_details");
			frm.refresh_field('molding_sand_details');
	
				frm.call({
				method:'get_details_pattern_master',
				doc:frm.doc,
			});
	}

    }
});


// ============================================================= Change Mix Details =================================================

frappe.ui.form.on('Change Mix Details', {
    warehouse: function(frm) {

            frm.call({
			method:'get_stock_change_mix_details',
			doc:frm.doc,
		});
    }
});


// ============================================================= Core  Details =================================================

frappe.ui.form.on('Core  Details', {
    warehouse: function(frm) {

            frm.call({
			method:'get_stock_core_details',
			doc:frm.doc,
		});
    }
});
// ============================================================= Casting Details =================================================

frappe.ui.form.on('Casting Details', {
    short_quantity: function(frm) {

		frm.clear_table("change_mix_details");
		frm.refresh_field('change_mix_details');

            frm.call({
			method:'calculation_after_short_quentity',
			doc:frm.doc,
		});
		frm.refresh_field('casting_details');

    }
});