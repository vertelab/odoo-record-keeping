# -*- coding: utf-8 -*-

from odoo import _, api, fields, models


class Order(models.Model):
    _name = 'sale.order'
    _inherit = ['sale.order']
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

    @api.depends('document_id')
    def _compute_document_ref(self):
        for record in self:
            record.document_ref = f'rk.document,{record.document_id.id or 0}'

    @api.model
    def _selection_target_model(self):
        models = self.env['ir.model'].search([('model', '=', 'rk.document')])
        return [(model.model, model.name) for model in models]

    def _set_document_link(self):
        self.ensure_one()
        document = self.document_id
        if not document.res_model or not document.res_id:
            return {'res_model': self._name, 'res_id': self.id}

    @api.model
    def create(self, vals):
        record = super(Order, self).create(vals)
        document_vals = record._set_document_link()
        if document_vals:
            record.document_id.write(document_vals)
        return record

    def write(self, vals):
        for record in self:
            document_vals = record._set_document_link()
            if document_vals:
                Document = self.env['rk.document']
                if record.document_id:
                    Document.write(record.document_id.id, document_vals)
                    vals.update(document_vals)
                else:
                    vals['document_id'] = Document.create(document_vals)
        result = super(Order, self).write(vals)
        return result
