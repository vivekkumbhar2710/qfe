// Copyright (c) 2024, Quantbit Technologies Pvt ltd and contributors
// For license information, please see license.txt

frappe.ui.form.on('Material Conversion', {
	// refresh: function(frm) {

	// } 
});

frappe.ui.form.on('Input Material For Material Conversion', {
	item_code:function(frm)
	{
		frm.call({
				method:'get_value_per_unit_for_input',
				doc: frm.doc
		});
	},
	
	quantity:function(frm)
	{
		frm.call({
				method:'total_weight_on_input_material',
				doc: frm.doc
		});
	},
});

frappe.ui.form.on('Input Material For Material Conversion', {
	quantity:function(frm)
	{
		frm.call({
				method:'call_method',
				doc: frm.doc
		});
	}
});

frappe.ui.form.on('Output Material For Material Conversion', {
	quantity:function(frm)
	{
		frm.call({
				method:'call_method_output',
				doc: frm.doc
		});
	}
});

frappe.ui.form.on('Output Material For Material Conversion', {
	quantity:function(frm)
	{
		frm.call({
				method:'total_weight_on_output_material',
				doc: frm.doc
		});
	},
	item_code:function(frm)
	{
		frm.call({
				method:'get_value_per_unit_for_output',
				doc: frm.doc
		});
	},
});

frappe.ui.form.on('Material Conversion', {
    setup: function(frm) {
        frm.set_query("item_code", "input_material", function (doc, cdt, cdn) {
            let d = locals[cdt][cdn];
            return {
                filters:{
					'item_group' :  d.item_group,
				}
            };
        });
    }
});

frappe.ui.form.on('Material Conversion', {
    setup: function(frm) {
        frm.set_query("item_code", "output_material", function (doc, cdt, cdn) {
            let d = locals[cdt][cdn];
            return {
                filters:{
					'item_group' :  d.item_group,
				}
            };
        });
    }
});
 
frappe.ui.form.on('Input Material For Material Conversion', {
	warehouse:function(frm)
	{
		frm.call({
				method:'get_available_quantity_input_material',
				doc: frm.doc
		});
	}
});

frappe.ui.form.on('Output Material For Material Conversion', {
	warehouse:function(frm)
	{
		frm.call({
				method:'get_available_quantity_output_material',
				doc: frm.doc
		});
	}
});

frappe.ui.form.on('Material Conversion', {
	setup: function (frm) {
	  var company_field = 'company';
        // frm.set_query("operator_id", function(doc) {
        //     return {
        //         filters: [
        //             ["Operator Master", company_field, '=', frm.doc.company],
        //          ]
        //     };
        // });
        
        frm.set_query("warehouse", "input_material", function(doc, cdt, cdn) {
		let d = locals[cdt][cdn];
		return {
			filters: [
        		  ["Warehouse", company_field, '=', frm.doc.company]
				]
			};
    	});
    	
    	frm.set_query("warehouse", "output_material", function(doc, cdt, cdn) {
		let d = locals[cdt][cdn];
		return {
			filters: [
        		  ["Warehouse", company_field, '=', frm.doc.company]
				]
			};
    	});
	}
});