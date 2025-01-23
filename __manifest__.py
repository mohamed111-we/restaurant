{
    'name': 'Restaurant Management',
    'version': '17.0',
    'summary': 'Manage restaurant menu, orders, and reservations',
    'description': """
        This module helps in managing a restaurant's operations including menu management, 
        table reservations, and order processing.
    """,
    'category': 'Restaurant',
    'author': 'Mohamed',
    'website': 'http://www.example.com',
    'depends': ['base', 'product', 'mail','sale_management','sale_stock'],
    'data': [
        'security/ir.model.access.csv',

        'data/sequence.xml',

        'views/food_views.xml',
        'views/restaurant_views.xml',
        'views/inherit_id.xml',

        'reports/restaurant_report.xml',


    ],
    'demo': [],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
