{
    'name': 'Лікарняний облік',
    'version': '19.0.1.0.0',
    'category': 'Охорона здоров’я',
    'summary': 'Модуль для автоматизації лікарні',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'data/disease_data.xml',
        'views/doctor_views.xml',
        'views/disease_views.xml',
        'views/patient_views.xml',
        'views/visit_views.xml',
        'views/menu.xml',

    ],

    'installable': True,
    'auto_install': False,

}