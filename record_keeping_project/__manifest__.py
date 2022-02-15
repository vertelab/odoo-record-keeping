# -*- coding: utf-8 -*-
################################################################################
#
#    Odoo, Open Source Management Solution, third party addon
#    Copyright (C) 2004-2017 Vertel AB (<https://vertel.se>).
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
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
################################################################################

{
    'name': 'Record-keeping Project',
    'summary': 'Record-keeping Project for Odoo',
    'author': 'Vertel AB',
    'contributor': '',
    'maintainer': 'Vertel AB',
    'repository': 'https://github.com/vertelab/odoo-record-keeping.git',
    'category': 'Administration',
    'version': '14.0.2.2.0',
    # Version ledger: 14.0 = Odoo version. 1 = Major. Non regressionable code. 2 = Minor. New features that are regressionable. 3 = Bug fixes
    'license': 'AGPL-3',
    'website': 'https://vertel.se/record-keeping',
    'description': """
This module extends projects with record-keeping fields\n
v14.1.1.0 added new version number.   \n
v14.0.2.1.0 added wizard to link to record
v14.0.2.2.0 refactored classes
""",
    'depends': ['mail', 'project', 'record_keeping', 'record_keeping_wizard'],
    'data': [
        'views/project_views.xml',
        'views/task_views.xml',
        'views/res_config_settings_views.xml',
    ],
}
