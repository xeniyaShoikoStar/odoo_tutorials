import logging
from odoo import models, fields

class Calc(models.TransientModel):
    _name = "estate.calc"
    _description = "Calculator tester"

    x = fields.Integer()
    text_field = fields.Char()

    # this method name, "action_button_next1" must match the name="" attribute of the <button> tag
    def action_button_next1(self):
        logger = logging.getLogger("Calc")
        logger.info("******* Calc.action_button_next1() called *******")