# -*- coding: utf-8 -*-
from odoo import _, api, fields, models


class SaleOrder(models.Model):
    _name = 'sale.order'
    _inherit = ['sale.order', 'rk.document.mixin']

    def _create_invoices(self, grouped=False, final=False, date=None):
        invoices = super()._create_invoices(grouped, final, date)
        # If record_keeping_account is installed,
        # link invoice(s) to same matter as in sale order.
        if hasattr(invoices, 'matter_id'):
            for order in self:
                for invoice in invoices:
                    if not invoice.matter_id and order.matter_id:
                        invoice.matter_id = order.matter_id
        return invoices
