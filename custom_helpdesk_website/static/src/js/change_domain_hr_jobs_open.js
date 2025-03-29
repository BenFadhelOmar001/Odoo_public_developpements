odoo.define('custom_helpdesk_website.change_domain_hr_jobs_open', function (require) {
    "use strict";
    
    const publicWidget = require('web.public.widget');
    const rpc = require('web.rpc');

    publicWidget.registry.JobSelectionOpen = publicWidget.Widget.extend({
        selector: '#demande_recrutement_form_open', // Adjust the selector accordingly

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

        _get_ticket_poste_a_choisir_id_value: function() {
            const demande_recrutement_id = this.$el.find('input[name="demande_recrutement_id"]').val();
            //console.log("demande_recrutement_id");
            //console.log(demande_recrutement_id);
            if (demande_recrutement_id) {
                //console.log("enter in if condition");
                const rpc = require('web.rpc');
                
                // Perform RPC search
                rpc.query({
                    model: 'helpdesk.ticket',
                    method: 'search_read',
                    args: [[['id', '=', parseInt(demande_recrutement_id)]], ['id', 'poste_a_choisir']], // Add other fields as needed
                }).then(function(tickets) {
                    //console.log("Tickets found:", tickets);
                    // Do something with the tickets (e.g., return the first ticket ID)
                    if (tickets.length > 0) {
                        //console.log("-----------");
                        //console.log(tickets[0].poste_a_choisir[0]);
                        return tickets[0].poste_a_choisir[0]; // Return the ID of the first found ticket
                    } else {
                        //console.log("No tickets found.");
                        return null; // Or handle the case where no tickets are found
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

        _loadJobs: function(metier) {
            const $posteSelect = $('#poste_a_choisir');
            $posteSelect.empty().append('<option value=""></option>'); // Clear current options

            //console.log("_loadJobs")
            //console.log('Domain:', [['metier', '=', metier]]);

            rpc.query({
                model: 'hr.job',
                method: 'get_jobs_by_metier',
                args: [metier],
                    
                
            }).then((jobRecords) => {
                // Populate new job records
                //const test = this._get_ticket_poste_a_choisir_id_value();
                const test = parseInt(this.$el.find('input[name="demande_recrutement_poste_a_choisir_id"]').val());
                //console.log("test");
                //console.log(test);
                jobRecords.forEach((record) => {
                    $posteSelect.append(`<option value="${record.id}" ${test == record.id ? 'selected' : ''}>${record.name}</option>`);
                });
            });
        },
    });
});

