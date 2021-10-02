# -*- coding: utf-8 -*-

import logging

from odoo import _, api, fields, models

_logger = logging.getLogger(__name__)


class ProjectProject(models.Model):
    _name = 'project.project'
    _inherit = ['project.project', 'rk.mixin', 'mail.thread']
    _description = "Extend Project with Record-keeping Mixin"


class ProjectTask(models.Model):
    _name = 'project.task'
    _inherit = ['project.task', 'rk.mixin']
    _description = "Extend Project Task with Record-keeping Mixin"
