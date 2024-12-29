from odoo import models, fields


# NOTE: when adding a new model, must add an import to this packages' __init__.py
# NOTE: you also must added it to security/ir.model.access.csv
class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Type Tutorial"

    name = fields.Char(required=True)