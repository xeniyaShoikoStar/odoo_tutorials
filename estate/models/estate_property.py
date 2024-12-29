from email.policy import default

from odoo import models, fields, _



def three_months(mymodel):
    """
    :param mymodel: is an instance of <class 'odoo.api.estate.property'>
    :return:
    """
    return fields.Date.add(
        fields.Date.today(),
        months=3,
    )






class EstateProperty(models.Model):
    _name = "estate.property" # the model name (in dot-notation, module namespace)
    _description = "Estate Property Tutorial" # the model’s informal name

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(copy=False,default=three_months)
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        selection=[('north', 'North'), ('south', 'South'), ('east', 'East'),  ('west', 'West')]
    )
    state = fields.Selection(
        selection=[('new', 'New'), ('offer_received', 'Offer Received'), ('offer_accepted', 'Offer Accepted'), ('sold', 'Sold'), ('canceled', 'Cancelled')],
        default='new'
    )

    # this is special, when false the thing disappears from the UI: and needs to be
    # searched with filters
    active = fields.Boolean(default=True)

    def action_start_wizard(self):
        """
        handler for a button
        """
        return {
            "type": "ir.actions.act_window",
            "name": _("Start Wizard"),  # window title?
            "res_model": "estate.calc",
            "target": "new",  # open in new tab or window
            "view_mode": "form",
            "view_type": "form",
            "context": {"default_user_id": self.id},
        }