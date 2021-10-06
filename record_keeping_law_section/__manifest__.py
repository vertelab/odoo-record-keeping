# -*- coding: utf-8 -*-
##############################################################################
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
##############################################################################

{
    'name': 'Record-keeping Law Section',
    'summary': 'Adds Law section to Record-keeping',
    'description': """
Record-keeping Law Section
==========================

------------------------------------------------------
    * Link an official document to a secrecy provision
""",
    'version': '14.0.1',
    'category': 'Administration',
    'license': 'AGPL-3',
    'website': 'https://vertel.se',
    'author': 'Vertel AB',
    'depends': ['record_keeping',],
    'data': [
        'data/rk_law_section_data.xml',
        'security/rk_law_section_security.xml',
        'security/ir.model.access.csv',
        'views/rk_law_section_views.xml',
    ],
    'demo': [],
    'application': True,
}
