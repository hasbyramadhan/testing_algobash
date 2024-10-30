{
    'name': 'Sales Order Cancel Reason',
    'version': '1.0',
    'depends': ['sale'],
    'data': [
        'security/ir.model.access.csv',
        'views/cancel_reason_views.xml',
        'views/sale_order_views.xml',
        'data/cancel_reason_data.xml',
    ],
    'installable': True,
    'application': False,
}