# -*- coding: utf-8 -*-

import logging

from odoo import _, api, fields, models

_logger = logging.getLogger(__name__)


class ProjectProject(models.Model):
    _name = 'project.project'
    _inherit = ['mail.thread', 'project.project']
    _inherits = {'rk.document': 'rk_id'}

    rk_id = fields.Many2one(
        comodel_name='rk.document',
        help='The record-keeping document of this project',
        ondelete='restrict',
        required=True,
        readonly=True,
        string='Record-keeping Document',
    )


class ProjectTask(models.Model):
    _name = 'project.task'
    _inherit = ['project.task']
    _inherits = {'rk.document': 'rk_id'}

    rk_id = fields.Many2one(
        comodel_name='rk.document',
        help='The record-keeping document of this task',
        ondelete='restrict',
        required=True,
        readonly=True,
        string='Record-keeping Document',
    )
