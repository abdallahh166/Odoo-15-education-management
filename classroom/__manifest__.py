{
    'name': 'Future Classroom',
    'version': '15.0.0.0',
    'category': 'Education',
    "sequence": 3,
    'summary': 'Manage Classroom',
    'complexity': "easy",
    'author': 'Seven pictures',
    'website': 'https://www.futureacademyegypt.com/en/home',
    'depends': ['core'],
    'data': [
        'security/ir.model.access.csv',
        'views/classroom_view.xml',
        'menus/op_menu.xml',
    ],
    'demo': [
        'demo/classroom_demo.xml',
        'demo/facility_line_demo.xml'
    ],
    'images': [
        'static/description/openeducat_classroom_banner.jpg',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
