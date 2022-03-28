# -*- coding: utf-8 -*-
from odoo import _, fields, models


class AddFileWizard(models.TransientModel):
    _name = 'rk.add.file.wizard'
    _description = 'Wizard for adding a file to a matter'

    name = fields.Char(
        required=True,
        string='Name',
    )
    datas = fields.Binary(
        string='File Content',
    )
    description = fields.Text(
        string='Description',
    )
    file_type = fields.Selection(
        [('binary', 'File')],
        default='binary',
        required=True,
        string='Type',
    )

    def save_button(self):
        attachment_vals = {
            'datas': self.datas,
            'description': self.description,
            'name': self.name,
            'type': self.file_type,
        }
        attachment = self.env['ir.attachment'].create(attachment_vals)

        ctx = self.env.context.get
        if attachment and 'rk.matter' in ctx('active_model'):
            document_vals = {
                'description': self.description,
                'is_official': True,
                'matter_id': ctx('active_id', 0),
                'res_id': attachment.id,
                'res_model': 'ir.attachment',
            }
            self.env['rk.document'].create(document_vals)
