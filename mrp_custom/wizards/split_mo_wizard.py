from odoo import fields, models, api, _
from odoo.exceptions import UserError, ValidationError

from odoo import models, fields, api


class SplitManufacturingOrders(models.TransientModel):
    _name = "split.mo.wizard"

    # Fields for user input
    split_mo_by = fields.Selection([
        ('by_no', 'Nombre de Divisions'),
        ('by_qty', 'Diviser par Quantité')],
        required=True)
    split_mo_no = fields.Integer('Split Quantity/Number', required=True)

    def btn_split(self):
        mrp_obj = self.env['mrp.production']
        active_id = self.env.context.get('active_id')
        current_mrp_data = mrp_obj.browse(active_id)

        if self.split_mo_by == 'by_no':
            split_mo_no = self.split_mo_no
            for _ in range(split_mo_no):
                # Prepare values for the new manufacturing order
                mrp_vals = {
                    'product_id': current_mrp_data.product_id.id,
                    'product_qty': current_mrp_data.product_qty / split_mo_no,
                    'date_planned_start': current_mrp_data.date_planned_start,
                    'company_id': current_mrp_data.company_id.id,
                    'origin': current_mrp_data.name,
                    'bom_id': current_mrp_data.bom_id.id,
                    'product_uom_id': current_mrp_data.product_uom_id.id,
                }

                # Prepare component line values for the new manufacturing order
                mrp_line_data = []
                for mo_line in current_mrp_data.bom_id.bom_line_ids:
                    line_vals = {
                        'product_id': mo_line.product_id.id,
                        'name': mo_line.product_id.name,
                        'product_uom_qty': (
                                mo_line.product_qty * (current_mrp_data.product_qty / split_mo_no)),
                        'location_id': current_mrp_data.location_src_id.id,
                        'location_dest_id': current_mrp_data.location_dest_id.id,
                        'product_uom': current_mrp_data.product_uom_id.id,
                    }
                    mrp_line_data.append((0, 0, line_vals))
                mrp_vals['move_raw_ids'] = mrp_line_data

                # Create the new manufacturing order
                mrp_obj.create(mrp_vals)

            # Unreserve the original manufacturing order and set state to 'cancel'
            current_mrp_data.do_unreserve()
            current_mrp_data.state = 'cancel'

        elif self.split_mo_by == 'by_qty':
            split_mo_qty = self.split_mo_no
            qty = current_mrp_data.product_qty - split_mo_qty

            # Adjust the product quantity using a wizard
            change_production_qty_wizard = self.env['change.production.qty'].create({'product_qty': qty})
            change_production_qty_wizard.change_prod_qty()

            # Prepare values for the new manufacturing order
            mrp_vals = {
                'product_id': current_mrp_data.product_id.id,
                'product_qty': split_mo_qty,
                'date_planned_start': current_mrp_data.date_planned_start,
                'company_id': current_mrp_data.company_id.id,
                'origin': current_mrp_data.name,
                'bom_id': current_mrp_data.bom_id.id,
                'product_uom_id': current_mrp_data.product_uom_id.id,
            }

            # Prepare component line values for the new manufacturing order
            mrp_line_data = []
            for mo_line in current_mrp_data.bom_id.bom_line_ids:
                line_vals = {
                    'product_id': mo_line.product_id.id,
                    'name': mo_line.product_id.name,
                    'product_uom_qty': (mo_line.product_qty * split_mo_qty),
                    'location_id': current_mrp_data.location_src_id.id,
                    'location_dest_id': current_mrp_data.location_dest_id.id,
                    'product_uom': current_mrp_data.product_uom_id.id,
                }
                mrp_line_data.append((0, 0, line_vals))
            mrp_vals['move_raw_ids'] = mrp_line_data

            # Create the new manufacturing order
            mrp_obj.create(mrp_vals)
