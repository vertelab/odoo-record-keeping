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

    @api.model
    def create(self, vals):
        record = super(Order, self).create(vals)
        record.document_id = self.env['rk.document'].create(
            {'res_model': record._name, 'res_id': record.id})
        return record

    def write(self, vals):
        for record in self:
            if vals.get('is_official') and not record.document_id:
                vals['document_id'] = self.env['rk.document'].create(
                    {'res_model': record._name, 'res_id': record.id})
        result = super(Order, self).write(vals)
        return result
