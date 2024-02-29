frappe.ui.form.on('Daily Spectro Analysis', {
	// refresh: function(frm) {

	// }
});
frappe.ui.form.on('Daily Spectro Details', {
	pouring_id: function(frm,cdt,cdn) {
		var child = locals[cdt][cdn]
		frm.call({
			method: 'part',//function name defined in python
			doc: frm.doc, //current document
			args:{
				child_index:child.idx,
				pouring_id:child.pouring_id
			}
		});
		// frm.refresh();
		// frm.reload()
	}
});

