{
    'name': 'Inventory Adjustment Approval',
    'version': '1.0',
    'category': 'Inventory',
    'summary': 'Add approval workflow for Inventory Adjustment',
    'description': 'This module adds an approval workflow for stock adjustments with approval by Warehouse Manager.',
    'depends': ['stock'],
    'data': [
        'views/stock_inventory_views.xml',
        'security/security.xml', 
        'security/ir.model.access.csv', 
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
