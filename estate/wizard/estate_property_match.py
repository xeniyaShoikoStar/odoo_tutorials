import logging
from odoo import api, models, fields, _
from odoo.tools import SQL

from . import match_sql


class PropertyMatch(models.TransientModel):
    _name = "estate.property.match"
    _description = "Match property with a Custom Query"

    to_match = fields.Char(readonly=True) # Display a property identifier or name passed from another view to this wizard for context.

    @api.model
    def default_get(self, fields):
        """
        When opening this wizard from a Property form, the property_id context ensures the wizard is pre-loaded with
        that specific property's ID. The user sees a readonly field displaying the property_id
        """
        rec = super(PropertyMatch, self).default_get(fields)

        logger = logging.getLogger("PropertyMatch")
        # self.env.context.get() method used to check if key is present in context. Make sure that context has this field&val.
        # Retrieves the property_id from the context (a dictionary-like structure passed between views or methods in Odoo)
        property_id = self._context.get("property_id")
        logger.info(f"in wizard default_get(); current property id: {property_id}")

        #rec["to_match"] = self.env["PropertyMatch"].
        rec["to_match"] = property_id
        return rec

    # this method name, "action_button_next1" must match the name="" attribute of the <button> tag
    def action_button_next2(self):
        """
        Sequence:
        - on property form, press [Wizard Match] to launch estate_property_match
        - on estate_property_match wizard, press [Next2] to launch estate_property_match_part2

        In theory, estate_calc_part2 shows the results of a query.

        This function is called when the [Next2] button is pressed.  It:
        1. runs a sql py wrapped custom query
        2. populates the estate_property_match_part2 model with the results of the query (for now fully implemented in raw SQL)
        3. triggers an action to show the estate_property_match_part2 wizard, which shows a list of the results.
        """
        # sql = SQL("UPDATE TABLE foo SET a = %s, b = %s", "hello", 42)

        logger = logging.getLogger("PropertyMatch")
        property_id = self._context.get("property_id")

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
            "name": _("Result of Properties Match query"),  # window title?
            "res_model": "estate.property.match.part2",
            "target": "new",  # open in new tab or window
            "view_mode": "list",
            "view_type": "list",
            "context": {
                # "default_user_id": self.id,
                "property_id": self.id,
            },
        }