# -*- coding: utf-8 -*-

from odoo import _, api, fields, models

import logging
_logger = logging.getLogger(__name__)


class Document(models.Model):
    _name = 'rk.document'
    _description = 'Document'
    _inherit = ['mail.activity.mixin', 'mail.thread', 'rk.mixin']

    name = fields.Char(
        help='The format is [current year]/[sequence] if this document is '
             'belongs to a matter',
        readonly=True,
        string='Name',
        tracking=True,
    )
    classification_id = fields.Many2one(
        comodel_name='rk.classification',
        string='Classification',
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
        tracking=True,
    )
    document_type_id = fields.Many2one(
        comodel_name='rk.document.type',
        string='Document Type',
        tracking=True,
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

    @api.depends('name', 'res_model', 'res_id')
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

    def _message_log(self, **kwargs):
        if kwargs:
            res = super(Document, self)._message_log(**kwargs)
        if self.matter_id:
            kwargs['body'] = _(
                '<p>Document (%s):</p>') % self.name.split(' ')[0]
            self.matter_id._message_log(**kwargs)
        return res

    def _message_log_batch(self, bodies, author_id=None, email_from=None,
                           subject=False, message_type='notification'):
        res = super()._message_log_batch(bodies, author_id=None,
                                         email_from=None, subject=False,
                                         message_type='notification')
        if res and self.matter_id and message_type in ['notification']:
            self._next_document_no()
            for b in bodies.values():
                name = f"{self.matter_id.reg_no}-{self.document_no}"
                body = _('<p>Document (%s) created</p>') % name
                self.matter_id._message_log(body=body)

        return res

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
        document = super().create(vals)
        _logger.warning(f"{vals=}")
        document._next_document_no()
        return document

    @api.model
    def search(self, args, offset=0, limit=80, order='id', count=False):
        self = self.sudo()
        search_res = super().search(args, offset=offset,
                                    limit=limit, order=order, count=count)
        return search_res

    def write(self, vals):
        if vals.get('matter_id'):
            vals['document_no'] = ''
        res = super().write(vals)
        for document in self:
            document._next_document_no()
        return res
