# -*- coding: utf-8 -*-

from odoo import _, api, fields, models


class Document(models.Model):
    _name = 'rk.document'
    _description = 'Document'
    _inherit = ['mail.activity.mixin', 'mail.thread', 'rk.mixin']

    name = fields.Char(
        help='The format is [current year]/[sequence] if this document is '
             'belongs to a matter',
        string='Name',
        tracking=True,
    )
    description = fields.Char(
        help='The description of this document',
        string='Description',
        tracking=True,
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

    @api.depends('res_model', 'res_id')
    def _compute_res_ref(self):
        self = self.sudo()
        for document in self:
            if document.res_model and document.res_id:
                document.res_ref = f"{document.res_model},{document.res_id}"
                name = ''
                if document.matter_id:
                    name += document.matter_id.reg_no
                    if document.document_no:
                        name += '-' + document.document_no + ' '
                    else:
                        name += ' '
                if document.res_ref:
                    name += document.res_ref.name
                document.name = name
            else:
                document.res_ref = None

    def _next_document_no(self):
        self.ensure_one()
        if self.matter_id and not self.document_no:
            self.document_no = str(self.matter_id.document_no_next)
            self.matter_id.document_no_next += 1
            self._compute_res_ref()

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
        if vals.get('matter_id'):
            vals['document_no'] = ''
        res = super(Document, self).write(vals)
        for document in self:
            document._next_document_no()
        return res
