# -*- coding: utf-8 -*-

import logging
from odoo import _, api, fields, models


_logger = logging.getLogger(__name__)


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
        _logger.warning(f"{vals=}")
        _logger.warning(f"{res=}")
        return res
