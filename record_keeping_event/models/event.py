# -*- coding: utf-8 -*-

import logging
from odoo import _, api, fields, models

_logger = logging.getLogger(__name__)


class Event(models.Model):
    _name = 'event.event'
    _inherit = ['event.event']
    _inherits = {'rk.document': 'document_id'}

    document_id = fields.Many2one(
        comodel_name='rk.document',
        help='The record-keeping document id',
        ondelete='restrict',
        required=True,
        string='Document',
    )
    document_ref = fields.Reference(
        compute='_compute_document_ref',
        help='The record-keeping document reference',
        selection='_selection_target_model',
        string='Document Reference',
    )

    @api.depends('document_id', 'res_model', 'res_id')
    def _compute_document_ref(self):
        for record in self:
            if record.document_id:
                record.document_id.res_model = record._name
                record.document_id.res_id = record.id
            record.document_ref = f"rk.document,{record.document_id.id or 0}"

    @api.model
    def _selection_target_model(self):
        models = self.env['ir.model'].search([('model', '=', 'rk.document')])
        return [(model.model, model.name) for model in models]

    def create_matter(self):
        self = self.sudo()
        self.is_official = True
        self.matter_id = self.env['rk.matter'].create({})
