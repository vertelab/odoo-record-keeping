# -*- coding: utf-8 -*-
 
from odoo import SUPERUSER_ID, api


def post_init_hook(cr, registry):
    """
    This post-init-hook will create rk.document records for each existing sale order.
    """
    env = api.Environment(cr, SUPERUSER_ID, dict())
    models = ['sale.order']

    for model in models:
        records = env[model].search([], order='id')
        for record in records:
            if not record.rk_id:
                vals = {'rk_res_model': model, 'rk_res_id': record.id}
                record.rk_id = env['rk.document'].create(vals)
                record.rk_ref = f'{record.rk_id._name},{record.rk_id.id}'