{
    'name': 'Estate',
    'author': 'Xeniya',
    'depends': ['base'],
    # 'assets': {
    #     'web.assets_backend': [
    #         'estate/static/src/css/custom_styles.css',
    #     ],
    # },
    'data': [
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_property_type_views.xml',
        'wizard/estate_calc_views.xml',
        'wizard/estate_calc_part2_views.xml',
        'wizard/estate_property_match_views.xml',
        'wizard/estate_property_match_part2.xml',
        'views/estate_menus.xml',
        # 'data/test.xml' # !!! if this file is empty or WIP turn it off it breaks the module
    ],
    'installable': True,
    'application': True,
}