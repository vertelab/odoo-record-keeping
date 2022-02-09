# -*- coding: utf-8 -*-

from odoo import _, api, fields, models


class RecordKeepingMail(models.Model):
    _name = 'rk.mail'
    _description = 'Saves mail for Record-Keeping'
    _inherit = ['rk.document.mixin']

    attachment_ids = fields.Many2many(
        comodel_name='ir.attachment',
        readonly=1,
    )
    author_id = fields.Many2one(
        comodel_name='res.partner',
        readonly=1,
    )
    auto_delete = fields.Boolean(
        readonly=1,
        string='Auto Delete',
    )
    body_html = fields.Text(
        readonly=1,
        string='Rich-text Contents',
    )
    date = fields.Datetime(
        default=fields.Datetime.now,
        readonly=1,
    )
    email_cc = fields.Char(
        readonly=1,
        string='Cc',
    )
    email_from = fields.Char(
        readonly=1,
        string='From',
    )
    email_to = fields.Text(
        readonly=1,
        string='To',
    )
    headers = fields.Text(
        readonly=1,
    )
    mail_message_id = fields.Many2one(
        comodel_name='mail.message',
        readonly=1,
        string='Message',
    )
    mail_server_id = fields.Many2one(
        comodel_name='ir.mail_server',
        readonly=1,
        string='Outgoing mail server',
    )
    message_id = fields.Char(
        readonly=1,
        string='Message-Id',
    )
    message_type = fields.Selection([
        ('email', 'Email'),
        ('comment', 'Comment'),
        ('notification', 'System notification'),
        ('user_notification', 'User Specific Notification')],
        default='email',
        readonly=1,
        string='Type',
    )
    model = fields.Char(
        readonly=1,
        string='Related Document Model',
    )
    name = fields.Char(
        readonly=1,
        string='Subject'
    )
    notification = fields.Boolean(
        readonly=1,
        string='Is Notification',
    )
    recipient_ids = fields.Many2many(
        comodel_name='res.partner',
        context={'active_test': False},
        readonly=1,
        string='To (Partners)',
    )
    record_name = fields.Char(
        readonly=1,
        string='Message Record Name',
    )
    references = fields.Text(
        readonly=1,
    )
    reply_to = fields.Char(
        readonly=1,
        string='Reply-To',
    )
    res_id = fields.Many2oneReference(
        model_field='model',
        readonly=1,
        string='Related Document ID',
    )
    scheduled_date = fields.Char(
        readonly=1,
        string='Scheduled Send Date',
    )
    subject = fields.Char(
        readonly=1,
    )


class Mail(models.Model):
    _inherit = 'mail.mail'

    @api.model
    def create(self, vals):
        res = super().create(vals)
        fields = self.env['rk.mail'].fields_get()
        for mail in res.mail_ids:
            values = {'name': mail['subject']}
            for key in fields.keys():
                if hasattr(mail, key):
                    if fields[key]['type'] in ['many2many']:
                        values[key] = mail[key].ids
                    elif fields[key]['type'] in ['many2one']:
                        values[key] = mail[key].id
                    else:
                        values[key] = mail[key]
            if (model := mail.model) and (res_id := mail.res_id):
                if (matter_id := self.env[model].browse(res_id).matter_id):
                    values['matter_id'] = matter_id.id
                    values['is_official'] = True
            self.env['rk.mail'].create(values)
        return res
