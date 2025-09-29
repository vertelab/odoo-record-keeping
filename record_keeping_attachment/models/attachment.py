# -*- coding: utf-8 -*-
from odoo import _, api, fields, models


class Attachment(models.Model):
    _name = 'ir.attachment'
    _inherit = ['ir.attachment', 'mail.thread']  # 'rk.document.mixin'

    # Add document_id directly without the mixin
    document_id = fields.Many2one(
        'rk.document',
        string='Document',
        help='The record-keeping document id',
        ondelete='restrict',
        auto_join=True,
        copy=False,
        index=True
    )
    
    # Related fields from document
    classification_id = fields.Many2one(
        'rk.classification',
        related='document_id.classification_id',
        store=True,
        readonly=False
    )
    
    document_type_id = fields.Many2one(
        'rk.document.type',
        related='document_id.document_type_id',
        store=True,
        readonly=False
    )
    
    matter_id = fields.Many2one(
        'rk.matter',
        related='document_id.matter_id',
        store=True,
        readonly=False
    )
    
    is_official = fields.Boolean(
        related='document_id.is_official',
        store=True,
        readonly=False
    )

    rk_file_name = fields.Char(string="Original file Name", readonly=True)

    def _find_matter(self, values):
        _model = values.get('active_model') or values.get('res_model')
        _id = values.get('active_id') or values.get('res_id')
        if _model and _id and (record := self.env[_model].browse(_id)):
            if hasattr(record, 'matter_id'):
                return record.matter_id.id

    def _prepare_values(self, vals):
        matter_id = self.env.context.get('active_matter')

        for v in [self.env.context, vals]:
            if not matter_id:
                matter_id = self._find_matter(v)

        if matter_id:
            vals['matter_id'] = matter_id
            vals['is_official'] = True

        return vals


    @api.model_create_multi
    def create(self, vals):
        for val in vals:
            if not val.get('matter_id'):
                val.update(**self._prepare_values(val))
                # val = self._prepare_values(vals)
        return super().create(vals)


    def write(self, vals):
        for rec in self:
            if hasattr(rec, 'matter_id') and not rec.matter_id and not vals.get('matter_id'):
                vals = self._prepare_values(vals)
            return super().write(vals)
