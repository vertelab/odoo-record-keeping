# -*- coding: utf-8 -*-
##############################################################################
#
#    Odoo SA, Open Source Management Solution, third party addon
#    Copyright (C) 2022- Vertel AB (<https://vertel.se>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program. If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

{
    'name': 'Record-keeping: Record-keeping',
    'version': '14.0.2.4.0',
    # Version ledger: 14.0 = Odoo version. 1 = Major. Non regressionable code. 2 = Minor. New features that are regressionable. 3 = Bug fixes
    'summary': 'Record-keeping for Odoo',
    'category': 'Government',
    'description': """
    This module is the base module for Record-keeping \n 
    14.0.2.3.0 - Added new class for mails
    14.0.2.0.4 - Added relationship to ir.attachments
    14.0.2.0.4 - Added button to res.partner
    """,
    #'sequence': '1'
    'author': 'Vertel AB',
    'website': 'https://vertel.se/apps/record-keeping/record_keeping',
    'images': ['static/description/banner.png'], # 560x280 px.
    'license': 'AGPL-3',
    'contributor': '',
    'maintainer': 'Vertel AB',
    'repository': 'https://github.com/vertelab/odoo-record-keeping',
    'depends': ['base', 'hr', 'mail'],
    'data': [
        'data/rk.classification.csv',
        'data/rk.document.type.csv',
        'data/ir_sequence_data.xml',
        'data/law_section_data.xml',
        'security/rk_security.xml',
        'security/ir.model.access.csv',
        'wizard/add_record_wizard.xml',
        'views/classification_views.xml',
        'views/document_type_views.xml',
        'views/document_views.xml',
        'views/law_section_views.xml',
        'views/matter_views.xml',
        'views/mail_views.xml',
        'views/res_config_settings_views.xml',
        'views/res_partner_views.xml',
        'views/record_keeping_views.xml',
    ],
    'application': True,
}
# vim:expandtab:smartindent:tabstop=4s:softtabstop=4:shiftwidth=4:
