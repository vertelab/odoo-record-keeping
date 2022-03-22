# -*- coding: utf-8 -*-
from odoo import _, api, fields, models


class Task(models.Model):
    _name = 'project.task'
    _inherit = ['project.task', 'rk.document.mixin']

    def create_matter(self):
        self.ensure_one()
        if not self.matter_id:
            self.is_official = True
            self.matter_id = self.env['rk.matter'].create({})
