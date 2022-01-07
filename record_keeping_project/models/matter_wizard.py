import logging

from odoo import models, fields, api

_logger = logging.getLogger(__name__)


class ProjectMatterWizard(models.TransientModel):
    _name = "rk.wizard.project"

    _inherit = ["rk.wizard"]

    def _get_model(self):
        project_project = self.env["project.project"].browse(self.env.context.get('active_ids'))
        return project_project

    model = fields.Many2one(
        comodel_name="project.project",
        default=_get_model,
        readonly=True,
    )


class ProjectTaskMatterWizard(models.TransientModel):
    _name = "rk.wizard.project.task"

    _inherit = ["rk.wizard"]

    def _get_model(self):
        project_project = self.env["project.task"].browse(self.env.context.get('active_ids'))
        return project_project

    model = fields.Many2one(
        comodel_name="project.task",
        default=_get_model,
        readonly=True,
    )
