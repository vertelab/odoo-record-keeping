from odoo import _, api, fields, models

class RecordKeepingMail(models.Model):
    _name = 'rk.mail'
    _description = 'Saves mail for Record-Keeping'
    _inherit = ['rk.document.mixin']

    attachment_ids = fields.Many2many(
        comodel_name='ir.attachment',
        readonly=True,
    )
    author_id = fields.Many2one(
        comodel_name='res.partner',
         readonly=True,
    )
    auto_delete = fields.Boolean(
         readonly=True,
        string='Auto Delete',
    )
    body_html = fields.Text(
         readonly=True,
        string='Rich-text Contents',
    )
    date = fields.Datetime(
        default=fields.Datetime.now,
         readonly=True,
    )
    email_cc = fields.Char(
         readonly=True,
        string='Cc',
    )
    email_from = fields.Char(
         readonly=True,
        string='From',
    )
    email_to = fields.Text(
         readonly=True,
        string='To',
    )
    headers = fields.Text(
         readonly=True,
    )
    mail_server_id = fields.Many2one(
        comodel_name='ir.mail_server',
         readonly=True,
        string='Outgoing mail server',
    )
    message_id = fields.Char(
         readonly=True,
        string='Message-Id',
    )
    message_type = fields.Selection([
        ('email', 'Email'),
        ('comment', 'Comment'),
        ('auto_comment', 'Comment'), # added this instead of replacing the above (reason: it might affect data that already uses comment)
        ('notification', 'System notification'),
         ('user_notification', 'User Specific Notification'),
         ('email_outgoing', 'Outgoing Email')],
        default='email',
         readonly=True,
        string='Type',
    )
    model = fields.Char(
         readonly=True,
        string='Related Document Model',
    )
    name = fields.Char(
         readonly=True,
        string='Name'
    )
    notification = fields.Boolean(
         readonly=True,
        string='Is Notification',
    )
    recipient_ids = fields.Many2many(
        comodel_name='res.partner',
        context={'active_test': False},
         readonly=True,
        string='To (Partners)',
    )
    record_name = fields.Char(
         readonly=True,
        string='Message Record Name',
    )
    references = fields.Text(
         readonly=True,
    )
    reply_to = fields.Char(
         readonly=True,
        string='Reply-To',
    )
    res_id = fields.Many2oneReference(
        model_field='model',
         readonly=True,
        string='Related Document ID',
    )
    scheduled_date = fields.Char(
         readonly=True,
        string='Scheduled Send Date',
    )
    subject = fields.Char(
         readonly=True,
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
            values['sender'] = mail.email_from
            receivers = [mail.email_to] if mail.email_to else []
            recipients = [recipient_id.email_formatted for recipient_id in mail.recipient_ids]
            values['receiver'] = ', '.join(receivers + recipients)

            if (model := mail.model) and (res_id := mail.res_id):
                if rec := self.env[model].browse(res_id):
                    if hasattr(rec, 'matter_id'):
                        values['matter_id'] = rec.matter_id.id
                        values['is_official'] = True
            self.env['rk.mail'].create(values)
        return res
