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
    'name': 'Record-keeping HR',
    'summary': 'Record-keeping HR for Odoo',
    'description': """
This module extends Employees with record-keeping features
""",
    'version': '14.0.1',
    'category': 'Administration',
    'license': 'AGPL-3',
    'website': 'https://vertel.se',
    'author': 'Vertel AB',
    'depends': ['attachment_notebook', 'hr', 'record_keeping_mixin', ],
    'data': [
        'views/hr_views.xml',
    ],
    'post_init_hook': 'post_init_hook',
}
