{
    'name': 'Custom Inventory Validation',
    'version': '1.0',
    'category': 'Inventory',
    'summary': 'Validation for specific product transfers to specific locations',
    'depends': ['stock'],
    'data': [
        'security/ir.model.access.csv',
        'views/location_product_rule_view.xml',
    ],
    'installable': True,
    'application': False,
}
