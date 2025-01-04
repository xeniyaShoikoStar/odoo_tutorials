from odoo.tools import SQL

import logging

def property_match_sql(property_id):
    """
    Generates the SQL query that finds all similar properties, and scores their "match percentage"
    """
    logger = logging.getLogger("match_sql")

    # if you modify this, you also must change the SELECT statement
    attributes = {
        "postcode": 2.0,
        "bedrooms": 1.0,
        "living_area": 0.5,
    }

    # part of the WHERE clause
    #   any match: A.postcode = B.postcode OR A.bedrooms = B.bedrooms OR A.living_area = B.living_area
    any_match = " OR ".join([f"A.{field} = B.{field}" for field in attributes.keys()])
    logger.info(f"\nany match: {any_match}")

    def attr_score(attributes, name):
        return f"({attributes[name]} * (CASE WHEN a.{name} = b.{name} THEN 1 ELSE 0 END))"

    def attr_1(name):
        return f"(CASE WHEN a.{name} = b.{name} THEN 1 ELSE 0 END)"

    factor_total = sum(attributes.values())

    # (2.0 * (CASE WHEN a.postcode = b.postcode THEN 1 ELSE 0 END)) + (1.0 * (CASE WHEN a.bedrooms = b.bedrooms THEN 1 ELSE 0 END)) + ...
    score_plus = " + ".join([f"{attr_score(attributes, name)}" for name in attributes.keys()])
    logger.info(f"\nscore plus: {score_plus}")

    score = f"({score_plus}) * 100 / {factor_total}"
    logger.info(f"\nscore: {score}")

    attr_count = " + ".join([f"{attr_1(name)}" for name in attributes.keys()])
    logger.info(f"\nattr count: {attr_count}")

    # score = """
    # (
    #   (2.0 * (CASE WHEN a.postcode = b.postcode THEN 1 ELSE 0 END))
    #   + (1.0 * (CASE WHEN a.bedrooms = b.bedrooms THEN 1 ELSE 0 END))
    #   + (0.5 * (CASE WHEN a.living_area = b.living_area THEN 1 ELSE 0 END))
    # ) * 100 / 3.5
    # """

    return SQL(f"""
            SELECT B.id, B.name, B.postcode, B.bedrooms, B.living_area, B.description,
            CAST({score} as INT) as percent_match, {attr_count} as match_count

            FROM estate_property AS A
            INNER JOIN estate_property AS B
            ON A.id != B.id AND ({any_match})

            WHERE {score} > 25 AND a.id = %s

            ORDER BY percent_match DESC;
            """, property_id)