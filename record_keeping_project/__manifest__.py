# -*- coding: utf-8 -*-
##############################################################################
#
#    Odoo SA, Open Source Management Solution, third party addon
#    Copyright (C) 2021- Vertel AB (<https://vertel.se>).
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
    'name': 'Record-keeping: Project',
    'version': '14.0.2.2.0',
    # Version ledger: 14.0 = Odoo version. 1 = Major. Non regressionable code. 2 = Minor. New features that are regressionable. 3 = Bug fixes
    'summary': 'Record-keeping Project for Odoo',
    'category': 'Government',
    'description': """
This module extends projects with record-keeping fields\n
v14.1.1.0 added new version number.   \n
v14.0.2.1.0 added wizard to link to record
v14.0.2.2.0 refactored classes
""",
    #'sequence': '1',
    'author': 'Vertel AB',
    'website': 'https://vertel.se/apps/odoo-record-keeping/record_keeping_project',
    'images': ['static/description/banner.png'], # 560x280 px.
    'license': 'AGPL-3',
    'contributor': '',
    'maintainer': 'Vertel AB',
    'repository': 'https://github.com/vertelab/odoo-record-keeping',
    'depends': ['mail', 'project', 'record_keeping', 'record_keeping_wizard'],
    'data': [
        'views/project_views.xml',
        'views/task_views.xml',
        'views/res_config_settings_views.xml',
    ],
}
# vim:expandtab:smartindent:tabstop=4s:softtabstop=4:shiftwidth=4:
