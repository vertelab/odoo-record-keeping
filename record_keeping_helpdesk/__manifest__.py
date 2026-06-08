# -*- coding: utf-8 -*-
##############################################################################
#
#    Odoo SA, Open Source Management Solution, third party addon
#    Copyright (C) 2024- Vertel AB (<https://vertel.se>).
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
    'name': 'Record-keeping: Helpdesk',
    'version': '2.1.1',
    # Version ledger: 14.0 = Odoo version. 1 = Major. Non regressionable code. 2 = Minor. New features that are regressionable. 3 = Bug fixes
    'summary': 'Record-keeping Helpdesk for Odoo',
    'category': 'Government',
    'description': """
This module extends Helpdesk with record-keeping fields
""",
    #'sequence': '1',
    'author': 'Vertel AB',
    'website': 'https://vertel.se/apps/odoo-record-keeping/record_keeping_helpdesk',
    'images': ['static/description/banner.png'], # 560x280 px.
    'license': 'AGPL-3',
    'contributor': '',
    'maintainer': 'Vertel AB',
    'repository': 'https://github.com/vertelab/odoo-record-keeping',
    'depends': ['helpdesk_mgmt', 'record_keeping', 'record_keeping_wizard'],
    'data': [
        'views/helpdesk.xml',
        #'security/ir.model.access.csv',
    ],
    # 'post_init_hook': 'post_init_hook',
}
# vim:expandtab:smartindent:tabstop=4s:softtabstop=4:shiftwidth=4:
