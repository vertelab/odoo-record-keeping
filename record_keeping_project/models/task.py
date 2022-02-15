# -*- coding: utf-8 -*-

import logging
from odoo import _, api, fields, models


_logger = logging.getLogger(__name__)

class Task(models.Model):
    _name = 'project.task'
    _inherit = ['project.task', 'rk.document.mixin']
    _inherits = {'rk.document': 'document_id'}

    def create_matter(self):
        self.ensure_one()
        if not self.matter_id:
            self.is_official = True
            self.matter_id = self.env['rk.matter'].create({})
