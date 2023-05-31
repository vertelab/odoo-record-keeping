
import json
import logging
import requests
from datetime import timedelta

from odoo import api, fields, models
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class MailChannel(models.Model):
    _name = "mail.channel"
    _inherit = ['mail.channel', 'mail.thread', 'mail.activity.mixin']
