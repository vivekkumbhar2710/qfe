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

frappe.ui.form.on('Daily Hardness', {
    refresh: function(frm) {
        // Trigger calculation on any of the five fields change
        ['reading_11', 'reading_12', 'reading_13', 'reading_14', 'reading_15'].forEach(field => {
            frm.fields_dict[field].$input.on('change', function() {
                calculateMinMax(frm);
            });
        });
    }
});

function calculateMinMax(frm) {
    var values = [];
    
    ['reading_11', 'reading_12', 'reading_13', 'reading_14', 'reading_15'].forEach(field => {
        var value = frm.doc[field] || 0;
        values.push(value);
    });

    var nonZeroValues = values.filter(val => val !== 0);

    nonZeroValues.sort((a, b) => a - b);

    var concatenated_val = '';

    if (nonZeroValues.length > 0) {
      
        var min_val = nonZeroValues[0];
        var max_val = nonZeroValues[nonZeroValues.length - 1];

        concatenated_val = min_val.toString() + '-' + max_val.toString();
    } else {
        concatenated_val = '0-0';
    }

    frm.set_value('actual_hardness', concatenated_val);
}

