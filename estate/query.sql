-- todo: might need to deal with null if considered !=
-- todo: link the found matches results
SELECT B.id, B.name, B.postcode, B.bedrooms, B.living_area, B.description,

-- calculating % on matching fields, where:
-- 2, 1, 0.5 are the weights to give the 'postcode' a greater effect on match.
-- Use '/x', where x-has to be all weights add together
(
  (2.0 * (CASE WHEN a.postcode = b.postcode THEN 1 ELSE 0 END))
  + (1.0 * (CASE WHEN a.bedrooms = b.bedrooms THEN 1 ELSE 0 END))
  + (0.5 * (CASE WHEN a.living_area = b.living_area THEN 1 ELSE 0 END))
) * 100 / 3.5 as percent_match

-- join on itself, to make pairs of matches on all attr that match
FROM estate_property AS A
INNER JOIN estate_property AS B
ON A.id != B.id
AND (A.postcode = B.postcode OR A.bedrooms = B.bedrooms OR A.living_area = B.living_area)

-- % > 25, for WHERE MUST repeat the case above, bc the 'percent_match' doesn't exist yet
WHERE (
  (2.0 * (CASE WHEN a.postcode = b.postcode THEN 1 ELSE 0 END))
  + (1.0 * (CASE WHEN a.bedrooms = b.bedrooms THEN 1 ELSE 0 END))
  + (0.5 * (CASE WHEN a.living_area = b.living_area THEN 1 ELSE 0 END))
) * 100 / 3.5 > 25

-- order in DESC
ORDER BY percent_match DESC;