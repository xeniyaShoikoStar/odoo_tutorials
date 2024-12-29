{
    'name': 'Estate',
    'author': 'Xeniya',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_property_type_views.xml',
        'wizard/estate_calc_views.xml',
        'views/estate_menus.xml',
        # 'data/test.xml' # !!! if this file is empty or WIP turn it off it breaks the module
    ],
    'installable': True,
    'application': True,
}