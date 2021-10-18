from datetime import datetime
from odoo import _, api, fields, models
from odoo.exceptions import ValidationError
import logging

from werkzeug.exceptions import default_exceptions

_logger = logging.getLogger(__name__)


TYPES = [
    ('drawn_up', 'Drawn up'),
    ('received', 'Received'),
]


class Document(models.Model):
    _name = 'rk.document'
    _description = 'Record-keeping Document'
    _inherit = ['mail.activity.mixin', 'mail.thread']

    name = fields.Char(
        help="The format is [current year]/[sequence] and is set when document is official",
        readonly=True,
        string="Registration number"
    )
    draw_up_date = fields.Date(
        default=False,
        help='The date when the document is ready to be used or sent',
        string='Drawn up',
        tracking=True,
    )
    is_official = fields.Boolean(
        default=False,
        help='Check this option if this document is an official document',
        string='Official document',
        tracking=True,
    )
    is_secret = fields.Boolean(
        default=False,
        help='Check this option if it can be assumed that information contained '
             'in this document should not be disclosed on grounds of secrecy.',
        string='Secrecy marker',
        tracking=True,
    )
    law_section_id = fields.Many2one(
        comodel_name='rk.law.section',
        help='The specified secrecy provision when the document has a secrecy marker',
        string='Secrecy provision',
        tracking=True,
    )
    receive_date = fields.Date(
        default=False,
        help='The date when the document has been received by a competent person.',
        string='Received',
        tracking=True,
    )
    receiver_id = fields.Many2one(
        comodel_name='res.partner',
        string='Receiver',
        tracking=True,
    )
    rk_name = fields.Char(
        help="The format is [current year]/[sequence] and is set when document is official",
        readonly=True,
        string="Registration number",
    )
    rk_res_id = fields.Integer(
        help="The record id this document is attached to.",
        readonly=True,
        string='Resource ID',
    )
    rk_res_model = fields.Char(
        help="The record model this attachment is attached to.",
        readonly=True,
        string='Resource Model',
    )
    rk_res_ref = fields.Reference(
        compute='_compute_res_ref',
        help="The record this document is attached to.",
        readonly=True,
        selection='_selection_target_model',
        string='Resource Reference',
    )
    rk_type = fields.Selection(TYPES)
    secrecy_grounds = fields.Char(
        default=False,
        help='If marked as secret, please provide more information',
        string='Secrecy grounds',
        tracking=True,
    )
    sender_id = fields.Many2one(
        comodel_name='res.partner',
        help='A partner designated as sender',
        string='Sender',
        tracking=True,
    )

    _sql_constraints = [
        ('is_secret_require_grounds',
         "CHECK(is_secret IS NOT TRUE OR (law_section_id IS NOT NULL AND secrecy_grounds IS NOT NULL))",
         'Please provide legal grounds')]

    def _compute_url(self):
        base_url = self.env['ir.config_parameter'].sudo().get_param(
            'web.base.url')
        action = self.env.ref('record_keeping.action_document_view',
                              raise_if_not_found=False)
        for record in self:
            record.rk_url = (
                f'{base_url}/web#id={record.id}&view_type=form&model='
                f'{record._name}&action={action.id}')

    @api.depends('rk_res_model', 'rk_res_id')
    def _compute_res_ref(self):
        for record in self:
            record.rk_res_ref = f'{record.rk_res_model},{record.rk_res_id}'

    @api.onchange('is_official')
    def _onchange_is_official(self):
        if not self.is_official:
            self.is_secret = False

    @api.onchange('is_secret')
    def _onchange_is_secret(self):
        if not self.is_secret:
            self.law_section_id = False
            self.secrecy_grounds = False

    @api.model
    def _selection_target_model(self):
        models = self.env['ir.model'].search([])
        return [(model.model, model.name) for model in models]

    @api.model
    def create(self, vals):
        if vals.get('is_official'):
            vals.update(
                {'name': self.env['ir.sequence'].next_by_code('rk.document')})
        return super().create(vals)

    def write(self, vals):
        for rec in self:
            if not rec.name and vals.get('is_official'):
                rec.name = self.env['ir.sequence'].next_by_code('rk.document')
                rec.rk_name = rec.name
        return super(Document, self).write(vals)


class Classification(models.Model):
    _name = 'rk.classification'
    _description = 'Record-keeping Classification'

    name = fields.Char()
    parent_id = fields.Many2one('rk.classification')
