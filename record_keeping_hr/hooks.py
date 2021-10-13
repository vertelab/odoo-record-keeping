from odoo import SUPERUSER_ID, api, fields
import logging


_logger = logging.getLogger(__name__)


def post_init_hook(cr, registry):
    """
    This post-init-hook will create rk.document records for each existing employee.
    """
    env = api.Environment(cr, SUPERUSER_ID, dict())
    models = ['hr.employee']

    for model in models:
        records = env[model].search([], order='id')
        for record in records:
            if not record.rk_id:
                record.rk_id = env['rk.document'].create({})
