odoo.define('custom_helpdesk_website.change_domain_dr_metier_open', function (require) {
    "use strict";
    
    const publicWidget = require('web.public.widget');
    const rpc = require('web.rpc');

    publicWidget.registry.MetierSelectionOpen = publicWidget.Widget.extend({
        selector: '#demande_recrutement_form_open', // Adjust the selector accordingly

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
                this._loadMetiers(direction); // Load jobs if a métier is selected
            }
        },

        _onDirectionChange: function(event) {
            const direction = $(event.currentTarget).val();
            this._loadMetiers(direction); // Load jobs based on selected métier
        },

        _get_ticket_metier_a_choisir_id_value: function() {
            const demande_recrutement_id = this.$el.find('input[name="demande_recrutement_id"]').val();
            if (demande_recrutement_id) {
                // Perform RPC search
                rpc.query({
                    model: 'helpdesk.ticket',
                    method: 'search_read',
                    args: [[['id', '=', parseInt(demande_recrutement_id)]], ['id', 'metier_a_choisir_id']],
                }).then(function(tickets) {
                    console.log("Tickets found:", tickets);
                    if (tickets.length > 0) {
                        return tickets[0].metier_a_choisir_id[0]; // Return the ID of the first found ticket
                    } else {
                        console.log("No tickets found.");
                        return null; // Handle the case where no tickets are found
                    }
                }).catch(function(error) {
                    console.error("RPC error:", error);
                    // Handle error appropriately
                });
            } else {
                console.log("demande_recrutement_id is empty.");
                return null; // Handle empty ID case
            }
        },

        _loadMetiers: function(direction) {
            const $metierSelect = $('#metier_a_choisir_id');
            $metierSelect.empty().append('<option value=""></option>'); // Clear current options

            rpc.query({
                model: 'dr.metier',
                method: 'get_metiers_by_direction',
                args: [direction],
            }).then((metierRecords) => {
                const test = parseInt(this.$el.find('input[name="demande_recrutement_metier_a_choisir_id"]').val());
                metierRecords.forEach((record) => {
                    $metierSelect.append(`<option value="${record.id}" ${test == record.id ? 'selected' : ''}>${record.name}</option>`);
                });
            });
        },
    });
});
