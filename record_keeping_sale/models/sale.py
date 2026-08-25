# -*- coding: utf-8 -*-
from odoo import _, api, fields, models
from odoo.sql_db import SQL


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


class CrmTeam(models.Model):
    """Override av sale/core crm_team._compute_quotations_to_invoice.

    Odoo SA:s implementation använder hårdkodad "FROM sale_order" som inte
    inkluderar query.from_clause. När en modul lägger en _inherits-delegation
    på sale.order (här: rk.document via document_id) genererar _where_calc
    ett "sale_order__document_id"-alias i WHERE (active-filter) som saknar
    JOIN → psycopg2 UndefinedTable.

    Fix: använd query.from_clause i SELECT så JOIN:en följer med. Detta är
    en kopia av core-metoden med from_clause — vi ändrar aldrig Odoo SA-kod.
    """

    _inherit = 'crm.team'

    def _compute_quotations_to_invoice(self):
        query = self.env['sale.order']._where_calc([
            ('team_id', 'in', self.ids),
            ('state', 'in', ['draft', 'sent']),
        ])
        self.env['sale.order']._apply_ir_rules(query, 'read')
        select_sql = SQL("""
            SELECT team_id, count(*), sum(amount_total /
                CASE COALESCE(currency_rate, 0)
                WHEN 0 THEN 1.0
                ELSE currency_rate
                END
            ) as amount_total
            FROM %s
            WHERE %s
            GROUP BY team_id
        """, query.from_clause, query.where_clause or SQL("TRUE"))
        self.env.cr.execute(select_sql)
        quotation_data = self.env.cr.dictfetchall()
        teams = self.browse()
        for datum in quotation_data:
            team = self.browse(datum['team_id'])
            team.quotations_amount = datum['amount_total']
            team.quotations_count = datum['count']
            teams |= team
        remaining = (self - teams)
        remaining.quotations_amount = 0
        remaining.quotations_count = 0
