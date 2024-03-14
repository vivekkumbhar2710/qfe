// Copyright (c) 2024, Quantbit Technologies Pvt ltd and contributors
// For license information, please see license.txt

frappe.ui.form.on('Moulding Sand Testing', {
	// refresh: function(frm) {

	// }
});

frappe.ui.form.on("Moulding Sand Testing", {
	dry_mix: function(frm) {
	  let sum = flt(frm.doc.dry_mix) + flt(frm.doc.wet_mix);
	  frm.set_value("total_mixture_time", sum);
	},
	wet_mix: function(frm) {
	  let sum = flt(frm.doc.dry_mix) + flt(frm.doc.wet_mix);
	  frm.set_value("total_mixture_time", sum);
	}
  });

  frappe.ui.form.on('Moulding Sand Testing', {
    setup: function(frm) {
        frm.set_query("work_sup", function(doc) {
            return {
                filters: [
                    ["Lab Supervisor Master", "company", '=', frm.doc.company],
                ]
            };
        });
        frm.set_query("shift", function(doc) {
		return {
			filters: [
        			["Shift Master", "company", '=', frm.doc.company]
				]
			};
    	});
    }
});
