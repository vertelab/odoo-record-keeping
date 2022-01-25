# -*- coding: utf-8 -*-

from odoo import _, fields, models


class DocumentType(models.Model):
    _name = 'rk.document.type'
    _description = 'Document Type'

    name = fields.Char(
        required=True,
        string='Name',
    )
    description = fields.Char(
        string='Description',
    )
    classification_id = fields.Many2one(
        comodel_name='rk.classification',
        domain=[('has_types', '=', True)],
        string='Classification',
    )
