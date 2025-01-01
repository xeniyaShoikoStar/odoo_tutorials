from odoo import models, fields, api

class PropertyMatchPart2(models.TransientModel):
    _name = "estate.property.match.part2"
    _description = "SQL query result list wizard"

    match_res = fields.Char()

    # manual deletion. Manually del. old records b4 adding new ones, but this gets a warning printed in logs:
    # if WARNING odoodb py.warnings: /home/xeniya_star/source_code/odoo/odoo/api.py:466: DeprecationWarning: The model odoo.addons.estate.wizard.estate_calc_part2 is not overriding the create method in batch
    # change to @api.model to @api.model_create_multi
    @api.model_create_multi
    def create(self, vals):
        # del old records
        old_records = self.search([('create_uid', '=', self.env.uid)])
        old_records.unlink()
        # create new record
        return super(PropertyMatchPart2, self).create(vals)