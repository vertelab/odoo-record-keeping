# -*- coding: utf-8 -*-

from odoo import _, fields, models


class MatterDocumentWizard(models.TransientModel):
    _name = 'rk.matter.document.wizard'
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
        [
            ('binary', 'File'),
            ('url', 'URL'), 
        ],
        change_default=True,
        default='binary',
        help='You can either upload a file from your computer or copy/paste '
             'an internet link to your file.',
        required=True,
        string='Type',
    )
    url = fields.Char(
        index=True,
        size=1024,
        string='Url',
    )

    def save_button(self):
        attachment_vals = {
            'name': self.name,
            'description': self.description,
            'datas': self.datas,
            'type': self.type,
            'url': self.url,
        }
        attachment = self.env['ir.attachment'].create(attachment_vals)

        ctx = self.env.context.get
        if attachment and 'rk.matter' in ctx('active_model'):
            document_vals = {
                'matter_id': ctx('active_id', 0),
                'res_id': attachment.id,
                'res_model': 'ir.attachment',
            }
            self.env['rk.document'].create(document_vals)
