import logging
from odoo import models, fields, _

class PropertyMatch(models.TransientModel):
    _name = "estate.property.match"
    _description = "Match property with a Custom Query"

    to_match = fields.Char()


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
        pass

        return {
            "type": "ir.actions.act_window",
            "name": _("Wizard of Next2"),  # window title?
            "res_model": "estate.property.match.part2",
            "target": "new",  # open in new tab or window
            "view_mode": "list",
            "view_type": "list",
            "context": {
                "default_user_id": self.id,
            },
        }