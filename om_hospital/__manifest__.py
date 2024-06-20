# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


{
    'name': 'Hospital Management',
    'version': '1.0.0',
    'category': 'Hospital',
    'summary': 'Hospital management system',
    'description': """Hospital management system""",
    'depends': ['mail','product'],
    'data': [
        'security/ir.model.access.csv',
        # 'data/patient.tag.csv',
        'data/sequence_data.xml',
        'views/Patient_view.xml',
        'views/menu.xml',
        'wizard/Cancel_appointement_view.xml',
        'views/Female_Patient_View.xml',
        'views/Appointement_Patient_view.xml',
        'views/patient_tag_view.xml'



    ],
    'demo': [],
    'application': True,
    'sequence': -100,
    'installable': True,
    'auto_install': False,
    'license': 'LGPL-3',
    'assets': {},

}
