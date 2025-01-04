from email.policy import default
import logging
from odoo import models, fields, _

from ..wizard import match_sql


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
        logger = logging.getLogger("EstateProperty")
        logger.info("******* action_start_wizard() called *******")
        return {
            "type": "ir.actions.act_window",
            "name": _("Start Wizard"),  # window title?
            "res_model": "estate.calc",
            "target": "new",  # open in new tab or window
            "view_mode": "form",
            "view_type": "form",
            "context": {"default_user_id": self.id},
        }

    def action_start_property_match(self):
        """
        handler for a button: Match Property. When the wizard is opened,
        .default_get() populates 'to_match' with the property_id from the context.
        ! The method handles multiple records in a single call by default after odoo13,
        no need of api decorator.
        """
        # This is how you can access the fields of the active record in a form
        current_id = self.id
        property_name = self.name

        logger = logging.getLogger("EstateProperty")
        logger.info(f"current property id: {current_id} name={property_name}")
        return {
            "type": "ir.actions.act_window",
            "name": _("Match Wizard"),  # window title?
            "res_model": "estate.property.match", # MUST match model's _name on model
            "target": "new",  # open in new tab or window
            "view_mode": "form",
            "view_type": "form",
            "context": {
                # "property_id": self.id,
                "property_id": current_id,
            }, # possibly to pass a current property
        }

    def action_button_similar_property(self):
        logger = logging.getLogger("EstateProperty")
        property_id = self.id
        logger.info(f"finding properties similar to property id: {property_id}")

        sql = match_sql.property_match_sql(property_id)

        logger.info(f"SQL: {sql}")

        self.env.cr.execute(sql)
        # fetch all res as list of dicts
        results = self.env.cr.dictfetchall()

        # clear the search results
        self.env['estate.property.match.part2'].search([]).update({
            "active": False
        })

        # these lines simulate creating records from the SQL query
        for result in results:
            self.env["estate.property.match.part2"].create({
                "property_id": result['id'],
                "name": result['name'],
                'postcode': result['postcode'],
                'description': result['description'],
                'bedrooms': result['bedrooms'],
                'living_area': result['living_area'],
                'match_count': result['match_count'],
                'match_percent': result['percent_match'],
            })

        return {
            "type": "ir.actions.act_window",
            "name": _("Similar Properties"),  # window title?
            "res_model": "estate.property.match.part2",
            "target": "new",  # open in new tab or window
            "view_mode": "list",
            "view_type": "list",
            "context": {
                "property_id": self.id,
                "create": 0,  # disallow "new" button on the list view
                "edit": 0,
            },
        }
