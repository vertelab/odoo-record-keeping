# -*- coding: utf-8 -*-

from odoo import _, api, fields, models


class Task(models.Model):
    _name = 'project.task'
    _inherit = ['project.task', 'rk.document.mixin']
    _inherits = {'rk.document': 'document_id'}

    def create_matter(self):
        self.is_official = True
        self.matter_id = self.env['rk.matter'].create({})
        return self.matter_id
