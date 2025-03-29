odoo.define('custom_helpdesk_website.delete_attachment', function (require) {
    "use strict";
    
    var ajax = require('web.ajax');
    var core = require('web.core');

    $(document).on('click', '.btn-delete-attachment', function (e) {
        e.preventDefault();
        var attachment_id = $(this).data('id');
        var $attachmentDiv = $('#attachment-div-oe-att-' + attachment_id);
        //console.log(attachment_id);

        // Call the controller via AJAX
        ajax.jsonRpc('/delete/attachment', 'call', {
            'attachment_id': attachment_id
        }).then(function (response) {
            if (response.status === 'success') {
                // Remove the attachment div from the DOM
                //console.log("c bon delete")
                //console.log(attachment_id);
                //console.log($attachmentDiv)
                $attachmentDiv.remove();
                //console.log("end")

            } else {
                alert('Error: ' + response.message);
            }
        });
    });
});
