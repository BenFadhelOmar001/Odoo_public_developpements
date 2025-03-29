odoo.define('custom_helpdesk_website.change_domain_hr_jobs_create', function (require) {
    "use strict";
    
    const publicWidget = require('web.public.widget');
    const rpc = require('web.rpc');

    publicWidget.registry.JobSelectionCreate = publicWidget.Widget.extend({
        selector: '#demande_recrutement_form_create', // Adjust the selector accordingly

        events: {
            'change #metier_a_choisir_id': '_onMetierChange',
        },

        start: function() {
            this._super.apply(this, arguments);
            this._initializeJobSelection();
        },

        _initializeJobSelection: function() {
            const metier = $('#metier_a_choisir_id').val(); // Get the current value of metier_a_choisir
            //console.log("const metier from _initializeJobSelection")
            //console.log(metier)
            if (metier) {
                this._loadJobs(metier); // Load jobs if a métier is selected
            }
        },

        _onMetierChange: function(event) {
            const metier = $(event.currentTarget).val();
            //console.log("const metier from _onMetierChange")
            //console.log(metier)
            this._loadJobs(metier); // Load jobs based on selected métier
        },

        _loadJobs: function(metier) {
            const $posteSelect = $('#poste_a_choisir');
            $posteSelect.empty().append('<option value=""></option>'); // Clear current options

            //console.log("_loadJobs")

            rpc.query({
                model: 'hr.job',
                method: 'get_jobs_by_metier',
                args: [metier],
                    
                
            }).then((jobRecords) => {
                // Populate new job records
                jobRecords.forEach((record) => {
                    $posteSelect.append(`<option value="${record.id}">${record.name}</option>`);
                });
            });
        },
    });
});

