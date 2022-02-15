# -*- coding: utf-8 -*-

import logging
from odoo import _, api, fields, models


_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _name = 'sale.order'
    _inherit = ['sale.order', 'rk.document.mixin']
    _inherits = {'rk.document': 'document_id'}

    
    # def message_post(self, **kwargs):
    #     self = self.sudo()
    #     _logger.warning(f"{self._description=}")
    #     res = super().message_post(**kwargs)
    #     matter_id = self.matter_id.id or False
    #     fields = self.env['rk.mail'].fields_get()
    #     _logger.warning(f"{res=}")
    #     _logger.warning(f"{res.mail_ids=}")
    #     for mail in res.mail_ids:
    #         vals = {'name': mail['subject']}
    #         for key in fields.keys():
    #             if hasattr(mail, key):
    #                 if fields[key]['type'] in ['many2many']:
    #                     vals[key] = mail[key].ids
    #                 elif fields[key]['type'] in ['many2one']:
    #                     vals[key] = mail[key].id
    #                 else:
    #                     vals[key] = mail[key]
    #         if matter_id:
    #             vals['matter_id'] = matter_id
    #             vals['is_official'] = True
    #         _logger.warning(f"{vals=}")
    #         mail = self.env['rk.mail'].create(vals)
    #         # mail.document_id.matter_id = matter_id
    #     return res
