# -*- coding: utf-8 -*-

from odoo import _, api, fields, models


class RecordKeepingSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    matter_default_classification_id = fields.Many2one(
        comodel_name='rk.classification',
        config_parameter=(
            'record_keeping.rk_matter_default_classification_id'),
        help='Default classification used for matters',
        string='Classification',
    )
    matter_default_date = fields.Date(
        compute="_compute_matter_default_date",
        inverse="_inverse_matter_default_date_str",
        help='Default date used for filtering matters not done',
        string='Date',
    )
    matter_default_date_str = fields.Char(
        config_parameter='record_keeping.rk_matter_default_date',
        help='Default date used for filtering matters not done',    
        string='Date (str)', 
    )
    matter_default_sorting_out_days = fields.Integer(
        config_parameter=(
            'record_keeping.rk_matter_default_sorting_out_days'),
        help='Default number of sorting out days',
        string='Sorting out days',
    )


    @api.depends('matter_default_date_str')
    def _compute_matter_default_date(self):
        to_date = fields.Date.to_date
        for setting in self:
            if not (default_date := setting.matter_default_date_str):
                setting.matter_default_date = to_date(fields.Date.today())
            else:
                try:
                    setting.matter_default_date = to_date(default_date)
                except ValueError:
                    setting.matter_default_date = to_date(fields.Date.today())

    def _inverse_matter_default_date_str(self):
        xmlid = 'record_keeping.filter_matters_not_done_before_default_date'
        for setting in self:
            if setting.matter_default_date:
                new_date = fields.Date.to_string(setting.matter_default_date)
                if new_date != setting.matter_default_date_str:
                    setting.matter_default_date_str = new_date
                    domain = (f"['&', '&', ('state', '!=', 'done'), '|', "
                              f"('receive_date', '<', '{new_date}'), "
                              f"('receive_date', '=', False), "
                              f"'|', ('draw_up_date', '<', '{new_date}'), "
                              f"('draw_up_date', '=', False)]")
                    name = _('Matters not done before %s') % new_date
                    self.env.ref(xmlid).write(dict(domain=domain, name=name))
