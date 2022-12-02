# -*- coding: utf-8 -*-
from odoo import _, api, fields, models
import logging
_logger = logging.getLogger(__name__)


class DocumentMixin(models.AbstractModel):
    _name = 'rk.document.mixin'
    _description = 'Document Mixin'
    _inherits = {'rk.document': 'document_id'}

    document_id = fields.Many2one(
        auto_join=True,
        comodel_name='rk.document',
        copy=False,
        help='The record-keeping document id',
        ondelete='restrict',
        required=True,
        string='Document',
        index=True
    )
    document_ref = fields.Reference(
        compute='_compute_document_ref',
        copy=False,
        help='The record-keeping document reference',
        selection='_selection_target_model',
        string='Document Reference',
    )

    @api.depends('document_id')
    def _compute_document_ref(self):
        for record in self:
            record.document_ref = f"rk.document,{record.document_id.id or 0}"
            record._get_document_link()

    def _get_default_param(self, field):
        param = f"record_keeping.{self._name.replace('.', '_')}_default_{field}"
        if (res := self.env['ir.config_parameter'].sudo().get_param(param)):
            res = int(res)
        return res

    def _get_document_link(self):
        self.ensure_one()
        vals = dict(res_model=self._name, res_id=self.id)
        if (document := self.document_id):
            if document.res_model != self._name or document.res_id != self.id:
                document.write(vals)
        else:
            return vals

    @api.model
    def _selection_target_model(self):
        models = self.env['ir.model'].search([('model', '=', 'rk.document')])
        return [(model.model, model.name) for model in models]

    @api.model
    def create(self, vals):
        for field in ['classification_id', 'document_type_id']:
            if not field in vals:
                vals[field] = self._get_default_param(field)
        record = super().create(vals)
        record._get_document_link()
        return record

    def create_matter(self):
        self.ensure_one()
        if not self.matter_id:
            self.is_official = True
            self.matter_id = self.env['rk.matter'].create({})

    def write(self, vals):
        for record in self:
            if (document_vals := record._get_document_link()):
                vals['document_id'] = self.env['rk.document'].create(
                    document_vals)
            # if (name := vals.get('name')):
            #     record.document_id._compute_name(name)
        result = super().write(vals)
        return result
