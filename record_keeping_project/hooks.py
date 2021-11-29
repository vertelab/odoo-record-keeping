# -*- coding: utf-8 -*-

from odoo import SUPERUSER_ID, api


def post_init_hook(cr, registry):
    """
    This post-init-hook will create a rk.document for existing projects and tasks.
    """
    env = api.Environment(cr, SUPERUSER_ID, dict())
    models = ['project.project', 'project.task']

    for model in models:
        records = env[model].search([], order='id')
        for record in records:
            if not record.document_id:
                vals = {'res_model': model, 'res_id': record.id}
                record.document_id = env['rk.document'].create(vals)
