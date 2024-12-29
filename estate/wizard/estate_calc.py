from odoo import models, fields

class Calc(models.TransientModel):
    _name = "estate.calc"
    _description = "Calculator tester"

    x = fields.Integer()