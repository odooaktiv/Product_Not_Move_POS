# -*- coding: utf-8 -*-
{
    'name': "Product Not Move POS",
    'summary': """
        Display that products which are not sold in selected period.""",
    'description': """
        This reports will display all stockable products which are not\
        sold in selected period.
        User can also filter products by warehouse.
    """,
    'author': 'Aktiv Software',
    'website': 'http://www.aktivsoftware.com',
    'category': 'Stock',
    'version': '12.0.1.0.0',
    'license': "OPL-1",
    'price': 7.00,
    'currency': "EUR",
    'depends': ['stock', 'point_of_sale'],
    'data': [
        'reports/product_not_move_report.xml',
        'wizard/product_not_moving.xml',
    ],
    'images': ['static/description/banner.jpg'],
    'installable': True,
    'application': False,
    'auto_install': False,
}
