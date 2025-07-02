# -*- coding: utf-8 -*-
from odoo import _, api, fields, models


class Event(models.Model):
    _name = 'event.event'
    _inherit = ['event.event', 'rk.document.mixin']


    def create_matter(self):
        self.ensure_one()
        super().create_matter()
        self.matter_id.matter_name = f"{self.event_type_id.name} i {self.address_id.name} med startdatum {self.date_begin.date()}"

