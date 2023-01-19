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
    datas_name = fields.Char(
        required=True,
        string='Matter Name',
    )

    def save_button(self):
        ctx = self.env.context.get

        attachment_vals = {
            'datas': self.datas,
            'description': self.description,
            'name': self.datas_name,
            'type': 'binary',
            'rk_file_name': self.name
        }

        if 'rk.matter' in ctx('active_model') and (
                matter_id := ctx('active_id')):
            attachment_vals['matter_id'] = matter_id
            attachment_vals['is_official'] = True

        self.env['ir.attachment'].create(attachment_vals)
