# -*- coding: utf-8 -*-

from odoo import _, api, fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    matter_count = fields.Integer(
        compute='_compute_matter_count',
        string='Number of matters',
    )

    def _compute_matter_count(self):
        for partner in self:
            partner.matter_count = self.env['rk.matter'].search_count([
                ('partner_id', '=', partner.id),
            ])

    def matter_tree_view(self):
        # shows the tree view of rk.matter record linked to this res.partner
        action_xmlid = 'record_keeping.action_matter_view'
        action = self.env['ir.actions.act_window']._for_xml_id(action_xmlid)
        action['domain'] = str([('partner_id', 'in', self.ids)])
        action['context'] = "{'partner_id': '%d'}" % self.id
        return action

