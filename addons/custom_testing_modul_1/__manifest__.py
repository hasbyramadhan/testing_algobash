{
    'name': 'Custom Manufacturing Schedule',
    'version': '1.0',
    'summary': 'Automatically schedules production based on estimated production time',
    'description': """
        This module adds a custom field for estimated production time and a button to plan production automatically.
    """,
    'author': 'Company Hasby',
    'depends': ['mrp'],
    'data': [
        'views/mrp_production_views.xml',
    ],
    'installable': True,
    'application': False,
}
