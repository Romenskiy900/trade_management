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
        'views/doctor_history_views.xml',
        'views/doctor_category_views.xml',
        'views/menu.xml',
        'wizard/mass_reassign_doctor_wizard_views.xml',
        'views/patient_actions.xml',
        'wizard/visit_report_wizard_views.xml',
        'views/visit_report_actions.xml',


        'data/doctor_category_data.xml',
        'demo/demo_doctor.xml',
        'demo/demo_patient.xml',
        'demo/demo_visit.xml',
        'demo/demo_disease.xml',

    ],


    'installable': True,
    'auto_install': False,

}