# -*- coding: utf-8 -*-
from odoo import _, api, fields, models
import logging
_logger = logging.getLogger(__name__)


class Attachment(models.Model):
    _name = 'ir.attachment'
    _inherit = ['ir.attachment', 'mail.thread', 'rk.document.mixin']

    @api.model
    def create(self, vals):
        ctx = self.env.context.get
        val = vals.get
        if not val('matter_id'):
            matter_id = ctx('active_matter')
            rec = None
            if not matter_id and (
                    active_id := ctx('active_id')) and (
                    active_model := ctx('active_model')):
                rec = self.env[active_model].browse(active_id)
                
            if not matter_id and (
                    res_id := val('res_id')) and (
                    res_model := val('res_model')):
                rec = self.env[res_model].browse(res_id)

            if not matter_id and rec and hasattr(rec, 'matter_id'):
                matter_id = rec.matter_id.id
                
            if matter_id:
                vals['matter_id'] = matter_id
                vals['is_official'] = True

        return super().create(vals)
