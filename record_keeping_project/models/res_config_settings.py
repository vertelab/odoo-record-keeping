# -*- coding: utf-8 -*-
from odoo import _, api, fields, models


class RecordKeepingSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    project_default_classification_id = fields.Many2one(
        comodel_name='rk.classification',
        config_parameter=(
            'record_keeping.project_project_default_classification_id'),
        help='Default classification used for projects',
        string='Project Classification',
    )
    project_default_document_type_id = fields.Many2one(
        comodel_name='rk.document.type',
        config_parameter=(
            'record_keeping.project_project_default_document_type_id'),
        help='Default document type used for projects',
        string='Project Document Type',
    )
    task_default_classification_id = fields.Many2one(
        comodel_name='rk.classification',
        config_parameter=(
            'record_keeping.project_task_default_classification_id'),
        help='Default classification used for tasks',
        string='Task Classification',
    )
    task_default_document_type_id = fields.Many2one(
        comodel_name='rk.document.type',
        config_parameter=(
            'record_keeping.project_task_default_document_type_id'),
        help='Default document type used for tasks',
        string='Task Document Type',
    )

    task_default_automatic_matter_connection = fields.Boolean(
        string="Automatic Matter Connection",
        config_parameter="record_keeping.project_task_default_automatic_matter_connection",
        help='Automaticly creates a connection to a sale order matter on a project.',
        )

