from odoo import SUPERUSER_ID, api, fields
import logging


_logger = logging.getLogger(__name__)


def post_init_hook(cr, registry):
    """
    This post-init-hook will create rk.document records for each existing employee.
    """
    env = api.Environment(cr, SUPERUSER_ID, dict())
    employees = env['hr.employee'].search([], order='id')
    for employee in employees:
        if not employee.rk_id:
            employee.rk_id = env['rk.document'].create({})
