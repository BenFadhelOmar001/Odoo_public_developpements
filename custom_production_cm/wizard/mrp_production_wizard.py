from odoo import api, fields, models

class mrpproductionwizard(models.TransientModel):

    _name = 'mrp.production.wizard'

    def get_production_id(self):
        [run_data] = self.env['mrp.production'].browse(self._context.get("active_ids")).read(
            ['id'])
        return run_data.get('id')

    employee_id = fields.Many2one('hr.employee')
    production_id = fields.Many2one('mrp.production', default=get_production_id)

    def create_mrp_custom_report(self):
        data = {
            'model': 'mrp.production.wizard',
            'form': self.read()[0]
        }
        return self.env.ref('custom_production_cm.action_mrp_production_report_custom').report_action(self, data=data)