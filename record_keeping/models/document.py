# -*- coding: utf-8 -*-

from odoo import _, api, fields, models


class Document(models.Model):
    _name = 'rk.document'
    _description = 'Document'
    _inherit = ['mail.activity.mixin', 'mail.thread', 'rk.mixin']

    name = fields.Char(
        compute='_compute_name',
        help='The format is [current year]/[sequence] if this document is belongs to a matter',
        string='Name',
    )
    document_name = fields.Char(
        compute='_compute_document_name',
        default='Unknown',
        help='Name of this document',
        string='Document Name',
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
        help='The record model this document is attached to.',
        readonly=True,
        string='Resource Model',
    )
    res_ref = fields.Reference(
        compute='_compute_res_ref',
        help='The record this document is attached to.',
        selection='_selection_target_model',
        string='Resource Reference',
    )

    @api.depends('res_ref')
    def _compute_document_name(self):
        for rec in self:
            if rec.res_ref:
                rec.document_name = rec.res_ref.name
            else:
                rec.document_name = rec.document_name

    @api.depends('document_name', 'document_no', 'matter_id')
    def _compute_name(self):
        for rec in self:
            if rec.matter_id:
                rec.name = (f'{rec.matter_id.reg_no}-{rec.document_no or ""} '
                            f'{rec.document_name}')
            else:
                rec.name = rec.document_name or ''

    @api.depends('res_model', 'res_id')
    def _compute_res_ref(self):
        for rec in self:
            if rec.res_model and rec.res_id:
                rec.res_ref = f'{rec.res_model},{rec.res_id}'
            else:
                rec.res_ref = None

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
        document = super(Document, self).create(vals)
        if 'matter_id' in vals:
            document._next_document_no()
        return document

    def write(self, vals):
        res = super(Document, self).write(vals)
        for document in self:
            document._next_document_no()
        return res
