{
    'name': 'Estate',
    'author': 'Xeniya',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        # 'data/test.xml' # !!! if this file is empty or WIP turn it off it breaks the module
    ],
    'installable': True,
    'application': True,
}