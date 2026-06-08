# -*- coding: utf-8 -*-
import logging
from odoo import _, api, fields, models
from odoo.exceptions import ValidationError, UserError

_logger = logging.getLogger(__name__)


class Attachment(models.Model):
    _name = 'ir.attachment'
    _inherit = ['ir.attachment', 'mail.thread', 'rk.document.mixin']

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
            if not val.get('matter_id') and val.get('res_model') == 'rk.matter':
                val['matter_id'] = val.get('res_id')
                # val = self._prepare_values(vals)
        return super().create(vals)

    def write(self, vals):
        if not vals.get('matter_id'):
            need_prepare = self.filtered(lambda r: hasattr(r, 'matter_id') and not r.matter_id)
            if need_prepare:
                vals = self._prepare_values(vals)
        return super().write(vals)

    def unlink(self):
        for record in self:
            if not self.env.user.has_group('record_keeping.group_rk_manager') and record.document_id.matter_id:
                raise UserError(_("You are not authorized to delete a document linked to a matter"))
        return super(Attachment, self).unlink()

