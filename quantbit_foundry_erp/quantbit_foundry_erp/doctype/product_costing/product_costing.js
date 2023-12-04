// Copyright (c) 2023, Quantbit Technologies Pvt ltd and contributors
// For license information, please see license.txt

frappe.ui.form.on('Product Costing', {
	// refresh: function(frm) {

	// }
});

// ============================================================= Product Costing =================================================

frappe.ui.form.on('Product Costing', {
    select_grade: function(frm) {

		frm.clear_table("grade_mix");
		frm.refresh_field('grade_mix');
            frm.call({
			method:'grade_mix_data',
			doc:frm.doc,
		});

		
		
    }
});




// ============================================================= Product Costing Casting Details =================================================

frappe.ui.form.on('Product Costing Casting Details', {
    quantity_to_manufacture: function(frm) {


            frm.call({
			method:'calculating_total_weight',
			doc:frm.doc,
		});

		
		
    }
});


frappe.ui.form.on('Product Costing Casting Details', { 
	casting_details_remove: function(frm, cdt, cdn) {

		var d = locals[cdt][cdn];
		frm.call({
			method:'calculating_total_weight',
			doc:frm.doc,
		});
	  }
	})

	// ============================================================= Product Costing Overheads =================================================


	frappe.ui.form.on('Product Costing Overheads', {
		quantity: function(frm) {

				frm.call({
				method:'overhead_amount_calculation',
				doc:frm.doc,
			});
	
			
			
		}
	});

	frappe.ui.form.on('Product Costing Overheads', {
		rate: function(frm) {

				frm.call({
				method:'overhead_amount_calculation',
				doc:frm.doc,
			});
	
			
			
		}
	});
	frappe.ui.form.on('Product Costing Overheads', {
		amount: function(frm) {

				frm.call({
				method:'overhead_amount_calculation',
				doc:frm.doc,
			});
	
			
			
		}
	});

	frappe.ui.form.on('Product Costing Overheads', { 
		total_overheads_remove: function(frm, cdt, cdn) {
	
			var d = locals[cdt][cdn];
			frm.call({
				method:'overhead_amount_calculation',
				doc:frm.doc,
			});
		  }
		})