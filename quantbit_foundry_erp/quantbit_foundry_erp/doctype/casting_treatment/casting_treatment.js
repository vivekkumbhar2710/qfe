// Copyright (c) 2023, Quantbit Technologies Pvt ltd and contributors
// For license information, please see license.txt

frappe.ui.form.on('Casting Treatment', {
	// refresh: function(frm) {

	// }
});

// ============================================================= Casting Treatment ================================================= 
frappe.ui.form.on('Casting Treatment', {
    casting_treatment: function(frm) {
		var pouring_list=[];
        frm.call({
			method:'get_pouring_id',
			doc:frm.doc,
			callback: function(response) {
				if (!response.exc) {
					pouring_list=response.message
					if(pouring_list==null)
					{
						frappe.throw("Pouring entry is not available for this 'Casting Treatment'");
					}
			}}
		})
		frm.set_query("select_pouring", function(doc) {
			return {
				filters: [
					['Pouring', 'name','in', pouring_list],  
				]
			};
		});
    }
});

frappe.ui.form.on('Casting Treatment', {
    select_pouring: function(frm) {
		frm.clear_table("casting_item");
		frm.refresh_field('casting_item');
		frm.clear_table("quantity_details");
		frm.refresh_field('quantity_details');
		frm.clear_table("raw_item");
		frm.refresh_field('raw_item');

        frm.call({
			method:'get_pouring',
			doc:frm.doc,
		})
    }
});


frappe.ui.form.on('Casting Treatment', {
    casting_treatment: function(frm) {

		if (frm.doc.select_pouring && frm.doc.select_pouring.length > 0) {

		frm.clear_table("casting_item");
		frm.refresh_field('casting_item');
		frm.clear_table("quantity_details");
		frm.refresh_field('quantity_details');
		frm.clear_table("raw_item");
		frm.refresh_field('raw_item');

        frm.call({
			method:'get_pouring',
			doc:frm.doc,
		})
	}

    }
});


frappe.ui.form.on('Casting Treatment', {
    get_rejection: function(frm) {
		frm.clear_table("rejected_items_reasons");
		frm.refresh_field('rejected_items_reasons');

        frm.call({
			method:'get_rejections',
			doc:frm.doc,
		})
    }
});






// ============================================================= Casting Treatment Quantity Details =================================================  

frappe.ui.form.on('Casting Treatment Quantity Details', {
    ok_quantity: function(frm) {
        frm.call({
			method:'rejection_addition',
			doc:frm.doc,
		})
    }
});

frappe.ui.form.on('Casting Treatment Quantity Details', {
    cr_quantity: function(frm) {
        frm.call({
			method:'rejection_addition',
			doc:frm.doc,
		});

	
    },
	
});

frappe.ui.form.on('Casting Treatment Quantity Details', {
    cr_quantity: function(frm) {

		frm.clear_table("rejected_items_reasons");
		frm.refresh_field('rejected_items_reasons');

        frm.call({
			method:'get_rejections',
			doc:frm.doc,
		})

    },
	
});

frappe.ui.form.on('Casting Treatment Quantity Details', {
    rw_quantity: function(frm) {
        frm.call({
			method:'rejection_addition',
			doc:frm.doc,
		});

    }
});

frappe.ui.form.on('Casting Treatment Quantity Details', {
    rw_quantity: function(frm) {


		frm.clear_table("rejected_items_reasons");
		frm.refresh_field('rejected_items_reasons');

        frm.call({
			method:'get_rejections',
			doc:frm.doc,
		})
    }
});


// ============================================================= Casting Treatment Casting Item ================================================= 

frappe.ui.form.on('Casting Treatment Casting Item', {
    source_warehouse: function(frm) {

		var args = {
            table_name: 'casting_item',
            item_code: 'item_code',
			warehouse: 'source_warehouse',
            field_name: 'available_quantity',
        };

        frm.call({
			method:'set_available_qty',
			args: args,
			doc:frm.doc,
		})
    }
});

frappe.ui.form.on('Casting Treatment Casting Item', {
    quantity: function(frm) {
        frm.call({
			method:'calculate_total_weight_quentity',
			doc:frm.doc,
		})
    }
});

frappe.ui.form.on('Casting Treatment Casting Item', {
    quantity: function(frm) {
        frm.call({
			method:'update_raw',
			doc:frm.doc,
		})
    }
});

frappe.ui.form.on('Casting Treatment Casting Item', {
    quantity: function(frm) {
        frm.call({
			method:'validate_casting_quantity',
			doc:frm.doc,
		})
    }
});

// ============================================================= Casting Treatment Raw Item ================================================= 

frappe.ui.form.on('Casting Treatment Raw Item', {
    source_warehouse: function(frm) {
		var args = {
            table_name: 'raw_item',
            item_code: 'raw_item_code',
			warehouse: 'source_warehouse',
            field_name: 'available_quantity',
        };

        frm.call({
			method:'set_available_qty',
			args: args,
			doc:frm.doc,
		})
    }
});