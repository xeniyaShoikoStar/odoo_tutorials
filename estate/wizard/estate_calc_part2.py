import logging
from odoo import models, fields, api



class CalcPart2(models.TransientModel):
    _name = "estate.calc.part2"
    _description = "Calculator tester part 2"

    math_result = fields.Char()
    active = fields.Boolean(default=True)
    # related_model_id = fields.Many2one('related.model', ondelete='cascade') #

    # manual deletion. Manually del. old records b4 adding new ones, but this gets a warning printed in logs:
    # if WARNING odoodb py.warnings: /home/xeniya_star/source_code/odoo/odoo/api.py:466: DeprecationWarning: The model odoo.addons.estate.wizard.estate_calc_part2 is not overriding the create method in batch
    # change to @api.model to @api.model_create_multi
    @api.model_create_multi
    def create(self, vals):
        # del old records
        old_records = self.search([('create_uid', '=', self.env.uid)])
        old_records.unlink()
        # create new record
        return super(CalcPart2, self).create(vals)