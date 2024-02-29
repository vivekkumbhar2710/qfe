// Copyright (c) 2024, Quantbit Technologies Pvt ltd and contributors
// For license information, please see license.txt

frappe.ui.form.on('Cupola Pouring', {
	// refresh: function(frm) {

	// }
});

// ================================================= coloring Field on Cupola Pouring============================================================================


frappe.ui.form.on('Cupola Pouring', {
    refresh: function(frm) {
        frm.fields_dict['furnece'].$input.css('background-color', '#D2E9FB');
        frm.fields_dict['supervisor'].$input.css('background-color', '#D2E9FB');
        frm.fields_dict['operator'].$input.css('background-color', '#D2E9FB');
        frm.fields_dict['contractor'].$input.css('background-color', '#D2E9FB');
        frm.fields_dict['shift'].$input.css('background-color', '#D2E9FB');
		// frm.fields_dict['pattern_details'].grid.get_field('pattern_code').$input.each(function(i, element) {
        //     $(element).css('background-color', '#D2E9FB'); });
    }
});


//================================================================ filters on fields=============================================================================


frappe.ui.form.on("Cupola Pouring", {
	setup: function(frm) {
			frm.set_query("furnece", function() { // Replace with the name of the link field
				return {
					filters: [
						["Furnece Master", "company", '=', frm.doc.company],// Replace with your actual filter criteria
					]
				};
			});

		}
	});
	

//================================================================ filters on fields============================================================================

var item_group="CASTING"

var company_field ='company'

frappe.ui.form.on('Cupola Pouring', {
	setup: function(frm) {
    	frm.set_query("contractor", function(doc, cdt, cdn) {
		let d = locals[cdt][cdn];
		return {
			filters: [
        			["Supplier", "company", '=', frm.doc.company]
				]
			};
    	});
    	
    	
    	frm.set_query("pattern_code","pattern_details", function(doc, cdt, cdn) {
		let d = locals[cdt][cdn];
		return {
			filters: [
        			["Pattern Master", "company", '=', frm.doc.company],
        			['Pattern Master', 'enable', '=', 1]
				]
			};
    	});
    	
    	frm.set_query("sales_order","pattern_details", function(doc, cdt, cdn) {
		let d = locals[cdt][cdn];
		return {
			filters: [
			        ['Sales Order', 'docstatus', '=', '1'],
        			["Sales Order", "company", '=', frm.doc.company]
				]
			};
    	});
    	
    	frm.set_query("item_code","change_mix_details", function(doc) {
		return {
			filters: [
    			["Item", company_field, '=', frm.doc.company]
			]   
		};
    	});
    	
    	frm.set_query("warehouse","change_mix_details", function(doc) {
		return {
			filters: [
    			["Warehouse", "company", '=', frm.doc.company]
			]   
		};
    	});
    	
    	
    	frm.set_query("warehouse","molding_sand_details", function(doc) {
		return {
			filters: [
    			["Warehouse", "company", '=', frm.doc.company]
			]   
		};
    	});
    	
    	frm.set_query("item_code","molding_sand_details", function(doc) {
		return {
			filters: [
    			["Item", company_field, '=', frm.doc.company]
			]   
		};
    	});
    	
    	frm.set_query("casting_item_code","core_details", function(doc) {
		return {
			filters: [
			    ['Item', 'custom_is_finished_foundry_casting_items', '=',1],
    			["Item", company_field, '=', frm.doc.company]
			]   
		};
    	});
    	
    	
    	frm.set_query("item_code","core_details", function(doc) {
		return {
			filters: [
    			["Item", company_field, '=', frm.doc.company]
			]   
		};
    	});
    	
    	frm.set_query("item_code","retained_items", function(doc) {
		return {
			filters: [
    			["Item", company_field, '=', frm.doc.company]
			]   
		};
    	});
    	
    	frm.set_query("target_warehouse","retained_items", function(doc) {
		return {
			filters: [
    			["Warehouse", "company", '=', frm.doc.company]
			]   
		};
    	});
    	
    	frm.set_query("downtime_reason","downtime_reasons_details", function(doc) {
		return {
			filters: [
    			["Rejection Reason Master", "company", '=', frm.doc.company]
			]   
		};
    	});
    	
    		frm.set_query("target_warehouse","casting_details", function(doc) {
		return {
			filters: [
    			["Warehouse", "company", '=', frm.doc.company]
			]   
		};
    	});
    	
    	frm.set_query("warehouse","core_details", function(doc) {
		return {
			filters: [
    			["Warehouse", "company", '=', frm.doc.company]
			]   
		};
    	});
    	
    		frm.set_query("pattern","core_details", function(doc) {
		return {
			filters: [
    			["Pattern Master", "company", '=', frm.doc.company]
			]   
		};
    	});
    	
    		frm.set_query("expense_head_account","additional_cost_details", function(doc) {
		return {
			filters: [
    			["Account", "company", '=', frm.doc.company]
			]   
		};
    	});
	}
});



frappe.ui.form.on('Cupola Pouring', {
    grade: function(frm) {

		frm.clear_table("change_mix_details");
		frm.refresh_field('change_mix_details');
            frm.call({
			method:'get_details_grade_master',
			doc:frm.doc,
		});
    }
});


//  To fetch child entries from template
frappe.ui.form.on('Cupola Pouring', {
    select_cupola_template: function(frm) {
		frm.clear_table("cupola_heat_details");
		frm.refresh_field('cupola_heat_details');
            frm.call({
			method:'get_template_entries',
			doc:frm.doc,
		});
    }
});



frappe.ui.form.on('Cupola Pouring', {
    furnece: function(frm) {
			frm.clear_table("casting_details");
			frm.refresh_field('casting_details');
	
			frm.clear_table("core_details");
			frm.refresh_field('core_details');


			frm.clear_table("molding_sand_details");
			frm.refresh_field('molding_sand_details');
	
			// 	frm.call({
			// 	method:'get_details_pattern_master',
			// 	doc:frm.doc,
			// });
	}
    
});

frappe.ui.form.on('Cupola Pouring', {
    power_reading_final: function(frm) {

            frm.call({
			method:'calculating_power_consumption',
			doc:frm.doc,
		});
    }
});

frappe.ui.form.on('Cupola Pouring', {
    power_reading_initial: function(frm) {

            frm.call({
			method:'calculating_power_consumption',
			doc:frm.doc,
		});
    }
});

frappe.ui.form.on('Cupola Pouring', {
    refresh: function(frm) {

            frm.call({
			method:'set_last_power_consumption',
			doc:frm.doc,
		});
    }
});



frappe.ui.form.on('Cupola Pouring', {
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

	frappe.ui.form.on("Cupola Pouring", {
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

	frappe.ui.form.on("Cupola Pouring", {
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



frappe.ui.form.on('Cupola Pattern Details', {
    poured_boxes: function(frm) {

		frm.clear_table("casting_details");
		frm.refresh_field('casting_details');

		frm.clear_table("core_details");
		frm.refresh_field('core_details');


		frm.clear_table("molding_sand_details");
			frm.refresh_field('molding_sand_details');

            frm.call({
			method:'get_details_pattern_master',
			doc:frm.doc,
		});
    }
});


frappe.ui.form.on('Cupola Pattern Details', {
    pattern_code: function(frm ,cdt, cdn) {

		var child = locals[cdt][cdn];

		// if (child.doc.poured_boxes) {

			frm.clear_table("casting_details");
			frm.refresh_field('casting_details');
	
			frm.clear_table("core_details");
			frm.refresh_field('core_details');



			frm.clear_table("molding_sand_details");
			frm.refresh_field('molding_sand_details');
	
				frm.call({
				method:'get_details_pattern_master',
				doc:frm.doc,
			});
	}

    // }
});

frappe.ui.form.on('Cupola Pattern Details', {
    sales_order: function(frm) {

		if (frm.doc.poured_boxes) {

			frm.clear_table("casting_details");
			frm.refresh_field('casting_details');
	
			frm.clear_table("core_details");
			frm.refresh_field('core_details');



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

frappe.ui.form.on('Cupola Change Mix Details', {
    warehouse: function(frm) {

            frm.call({
			method:'get_stock_change_mix_details',
			doc:frm.doc,
		});
    }
});

frappe.ui.form.on('Cupola Change Mix Details', {
    quantity: function(frm) {

            frm.call({
			method:'calculate_total_weight_after_charge_mix_filling',
			doc:frm.doc,
		});
    }
});

// ============================================================= Core  Details =================================================

frappe.ui.form.on('Cupola Core  Details', {
    warehouse: function(frm) {

            frm.call({
			method:'get_stock_core_details',
			doc:frm.doc,
		});
    }
});
// ============================================================= Casting Details =================================================

frappe.ui.form.on('Cupola Casting Details', {
    short_quantity: function(frm) {


            frm.call({
			method:'calculation_after_short_quentity',
			doc:frm.doc,
		});
		frm.refresh_field('casting_details');

    }
});

