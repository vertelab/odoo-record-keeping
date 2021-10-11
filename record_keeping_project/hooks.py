from odoo import SUPERUSER_ID, api, fields
import logging


_logger = logging.getLogger(__name__)


def post_init_hook(cr, registry):
    """
    This post-init-hook will create rk.document records for each existing project.
    """
    env = api.Environment(cr, SUPERUSER_ID, dict())
    projects = env['project.project'].search([], order='id')
    for project in projects:
        if not project.rk_id:
            project.rk_id = env['rk.document'].create({})
