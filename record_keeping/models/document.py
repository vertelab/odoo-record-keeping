# -*- coding: utf-8 -*-

from datetime import datetime
from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class Document(models.Model):
    _name = 'rk.document'
    _description = 'Document'
    _inherit = ['mail.activity.mixin', 'mail.thread', 'rk.mixin']

    name = fields.Char(
        compute='_compute_name',
        help='The format is [current year]/[sequence] if this document is belongs to a matter',
        string='Name',
        store=True,
    )
    document_name = fields.Char(
        help='Name of this document',
        string='Document Name',
        store=True,
    )
    document_no = fields.Char(
        help='The number assigned to this document',
        readonly=True,
        string='Document number',
    )
    matter_id = fields.Many2one(
        comodel_name='rk.matter',
        help='The matter this document belongs to',
        string='Matter',
        tracking=True,
    )
    res_id = fields.Integer(
        help='The record id this document is attached to.',
        readonly=True,
        string='Resource ID',
    )
    res_model = fields.Char(
        help='The record model this attachment is attached to.',
        readonly=True,
        string='Resource Model',
    )
    resource_ref = fields.Reference(
        compute='_compute_resource_ref',
        help='The record this document is attached to.',
        selection='_selection_target_model',
        string='Resource Reference',
    )

    @api.depends('document_name', 'document_no', 'matter_id')
    def _compute_name(self):
        for rec in self:
            if rec.matter_id:
                rec.name = f"{rec.matter_id.registration_no}-{rec.document_no or ''} {rec.document_name}"
            else:
                rec.name = rec.document_name or ''

    @api.depends('res_model', 'res_id')
    def _compute_resource_ref(self):
        for document in self:
            if document.res_model and document.res_id in self.env:
                document.resource_ref = f"{document.rk_res_model},{document.rk_res_id or 0}"
            else:
                document.resource_ref = None

    def _next_document_no(self):
        self.ensure_one()
        if self.matter_id and not self.document_no:
            self.document_no = str(self.matter_id.document_no_next)
            self.matter_id.document_no_next += 1

    @api.model
    def _selection_target_model(self):
        models = self.env['ir.model'].search([])
        return [(model.model, model.name) for model in models]

    @api.model
    def create(self, vals):
        document = super().create(vals)
        if 'matter_id' in vals:
            document._next_document_no()
        return document

    def write(self, vals):
        res = super(Document, self).write(vals)
        for document in self:
            document._next_document_no()
        return res
