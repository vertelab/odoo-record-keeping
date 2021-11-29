# -*- coding: utf-8 -*-

from odoo import _, api, fields, models


class Classification(models.Model):
    _name = 'rk.classification'
    _description = 'Classification Structure'
    _parent_name = 'parent_id'
    _parent_store = True

    child_ids = fields.One2many(
        comodel_name='rk.classification',
        inverse_name='parent_id',
        string='Child Structures',
    )
    classification_name = fields.Char(
        index=True,
        required=True,
        string='Name'
    )
    description = fields.Char(
        string='Description',
    )
    has_types = fields.Boolean(
        string='Has Types',
    )
    name = fields.Char(
        compute='_compute_name',
        recursive=True,
        store=True,
        string='Name',
    )
    parent_id = fields.Many2one(
        comodel_name='rk.classification',
        index=True,
        string='Parent Structure',
    )
    parent_path = fields.Char(
        index=True,
    )
    sequence = fields.Integer(
        string='Sequence',
    )
    type_ids = fields.One2many(
        comodel_name='rk.document.type',
        inverse_name='classification_id',
        string='Document Types',
    )

    @api.depends('classification_name', 'parent_id.name')
    def _compute_name(self):
        for record in self:
            if record.parent_id:
                parent_seq = record.parent_id.name.split(' ')[0]
                record.name = (f'{parent_seq}.{record.sequence} '
                               f'{record.classification_name}')
            else:
                record.name = (f'{record.sequence} '
                               f'{record.classification_name}')
