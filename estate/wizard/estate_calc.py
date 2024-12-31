import logging
from odoo import models, fields, _

class Calc(models.TransientModel):
    _name = "estate.calc"
    _description = "Calculator tester"
    # Auto Purging transient models' table to delete rec-s more frequently
    # _transient_max_hours = 1 # records will be auto-purged after 1h

    x = fields.Integer()
    text_field = fields.Char()

    # this method name, "action_button_next1" must match the name="" attribute of the <button> tag
    def action_button_next1(self):
        """
        Sequence:
        - on propery form, press [Wizard Button] to launch estate_calc
        - on estate_calc wizard, press [Next1] to launch estate_calc_part2

        In theory, estate_calc_part2 shows the results of a query.

        This function is called when the [Next1] button is pressed.  It:
        1. runs a sql query
        2. populates the estate_calc_part2 model with the results of the query (not fully implemented)
        3. triggers an action to show the estate_calc_part2 wizard, which shows a list of the results.
        """
        logger = logging.getLogger("Calc")
        logger.info("******* Calc.action_button_next1() called *******")

        # ######
        # PART 1:  THE QUERY
        # #####
        sql = """
        SELECT * FROM estate_property;
        """
        self.env.cr.execute(sql)
        row = str(self.env.cr.fetchone())
        logger.info(f"GOT ROW: {row}")
        # 2024-12-30 03:46:02,837 41696 INFO odoodb Calc: GOT ROW: (2, 2, 0, 0, 0, 2, 2, 'Beach house2', '1234', None, datetime.date(2025, 3, 26), 'Long Beach, NY', True, datetime.datetime(2024, 12, 26, 1, 5, 23, 712516), datetime.datetime(2024, 12, 27, 2, 5, 58, 104258), 0.0, None, True, 'offer_received', None)
        # TODO better sql, use odoo.tools.SQL
        # sql = SQL("UPDATE TABLE foo SET a = %s, b = %s", "hello", 42)
        # cr.execute(sql)
        # TODO also may need to flush models before reading with ea. sql query
        # e.g. with Environment.flush_all() # flush all pending computations & updates to db ... maybe self.env.flush_all() ?
        # or self.flush_model() ? #given fields flushed to db model
        # TODO look into self.env.cr.dictfetchall() # fetch all results as a list of dict-s
        # ex. execure query
        self.env.cr.execute("SELECT * FROM estate_property;")
        # fetch all res as list of dicts
        results = self.env.cr.dictfetchall()
        # SAMPLE OUTPUT of dicts, ea. dict is a row, where key is col, val is date
        logger.info(f"\n***** GOT RESULTS FROM estate_property: {str(results)} ******\n")
        # ! data integrity: must flush b4 execute query
        # !! Security: must sanitize input to avoid sql injections attack
        # !!! Performance: Direct query may be fast - it bypasses ORM security & validation layer,
        # use .dictfetchtall() for particularly complex query when ORM can't express or to optimize perform.


        # ######
        # PART 2:  copying the results to the next wizard
        # #####

        # *** This is the line that gets rid of old records!  (by setting active to false) ***
        # There is a problem with the transient model -- every time I call create() it just adds new
        # records.  I can't delete them.   Instead, I use the following line to mark all of the
        # existing records as "inactive" before adding new ones.  The list in the next wizard
        # will automatically hide records with active=False.
        self.env["estate.calc.part2"].search([]).update({"math_result": "0", "active": False})

        # these lines simulate creating records from the SQL query
        # TODO instead of hardcoding these, they should be created from the results of the sql query
        # X: I modified the .create() to remove the previous record -> basically overide every time
        self.env["estate.calc.part2"].create({"math_result": "42"})
        self.env["estate.calc.part2"].create({"math_result": "10"})
        self.env["estate.calc.part2"].create({"math_result": "11"})
        self.env["estate.calc.part2"].create({"math_result": "12"})

        # WORKS: The argument [] is an empty list, which means no filter is applied, -> it will return all records of the model estate.calc.part2.
        # The update method is used to update fields in the retrieved records.
        # {"math_result": 2} is the dictionary passed to update, which indicates that the field math_result will be
        # updated with the value 2 for all records returned by the search.
        self.env["estate.calc.part2"].search([]).update({"math_result": 2})
        # WORKS: self.env["estate.calc.part2"].search([]).write({"math_result": 3})

        # V2, now it manually deletes old record b4 writing a new
        # self.env["estate.calc.part2"].create({"math_result": "4242"}) # works


        # ######
        # PART 3:  trigger going to the next wizard; show a list of estate_calc_part2 records (the results of the query)
        # #####
        return {
            "type": "ir.actions.act_window",
            "name": _("Wizard Next"),  # window title?
            "res_model": "estate.calc.part2",
            "target": "new",  # open in new tab or window
            "view_mode": "list",
            "view_type": "list",
            "context": {
                "default_user_id": self.id,
            },
        }