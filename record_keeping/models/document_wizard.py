# -*- coding: utf-8 -*-

import logging
from odoo import _, api, fields, models

_logger = logging.getLogger(__name__)


class DocumentWizard(models.TransientModel):
    _name = "rk.document.wizard"
    _description = 'Wizard for attaching an attachment to a document'

    name = fields.Char(
        required=True,
        string='Name',
    )
    datas = fields.Binary(
        string='File Content (base64)',
    )
    description = fields.Text(
        string='Description',
    )
    type = fields.Selection(
        [('url', 'URL'), ('binary', 'File')],
        change_default=True,
        default='binary',
        help="You can either upload a file from your computer or copy/paste an internet link to your file.",
        required=True,
        string='Type',
    )
    url = fields.Char(
        index=True,
        size=1024,
        string='Url',
    )

    def save_button(self):
        Attachment = self.env['ir.attachment']
        attachment_vals = {
            'name': self.name,
            'description': self.description,
            'datas': self.datas,
            'type': self.type,
            'url': self.url,
        }
        attachment = Attachment.create(attachment_vals)

        ctx = self.env.context
        if attachment and 'rk.matter' in ctx['active_model']:
            Document = self.env['rk.document']
            document_vals = {
                'matter_id': ctx.get('active_id', 0),
                'res_id': attachment.id,
                'res_model': 'ir.attachment',
            }
            document = Document.create(document_vals)
