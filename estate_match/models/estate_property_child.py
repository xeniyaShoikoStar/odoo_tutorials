import logging
from odoo import models, fields, _

class EstatePropertyChild(models.Model):

    # using both _name & _inherit:  create new model from existing one
    # https://www.odoo.com/documentation/master/developer/reference/backend/orm.html#reference-orm-inheritance
    _name = "estate.property.child"
    _inherit = ["estate.property"]

    _description = "Child of Estate Property"
