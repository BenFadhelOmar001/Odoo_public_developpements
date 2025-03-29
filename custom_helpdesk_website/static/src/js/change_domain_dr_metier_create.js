odoo.define('custom_helpdesk_website.change_domain_dr_metier_create', function (require) {
    "use strict";
    
    const publicWidget = require('web.public.widget');
    const rpc = require('web.rpc');

    publicWidget.registry.MetierSelectionCreate = publicWidget.Widget.extend({
        selector: '#demande_recrutement_form_create', // Adjust the selector accordingly

        events: {
            'change #direction_a_choisir_id': '_onDirectionChange',
        },

        start: function() {
            this._super.apply(this, arguments);
            this._initializeMetierSelection();
        },

        _initializeMetierSelection: function() {
            const direction = $('#direction_a_choisir_id').val(); // Get the current value of metier_a_choisir
            if (direction) {
                this._loadMetiers(direction); // Load Metiers if a direction is selected
            }
        },

        _onDirectionChange: function(event) {
            const direction = $(event.currentTarget).val();
            this._loadMetiers(direction); // Load metiers based on selected direction
        },

        _loadMetiers: function(direction) {
            const $metierSelect = $('#metier_a_choisir_id');
            $metierSelect.empty().append('<option value=""></option>'); // Clear current options


            rpc.query({
                model: 'dr.metier',
                method: 'get_metiers_by_direction',
                args: [direction],
                    
                
            }).then((metierRecords) => {
                // Populate new job records
                metierRecords.forEach((record) => {
                    $metierSelect.append(`<option value="${record.id}">${record.name}</option>`);
                });
            });
        },
    });
});

