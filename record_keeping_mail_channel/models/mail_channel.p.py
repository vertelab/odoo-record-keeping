from odoo import _, api, fields, models

class MailChannel(models.Model):
    # #if VERSION  <= "16.0"
    _name = 'mail.channel'
    _inherit = ['mail.channel', 'rk.document.mixin']
    # #elif VERSION >= "17.0"
    _name = 'discuss.channel'
    _inherit = ['discuss.channel', 'rk.document.mixin']
    # #endif