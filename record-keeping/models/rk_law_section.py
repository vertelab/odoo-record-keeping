import base64
import hashlib
import json
import logging
from collections import defaultdict

from odoo import _, api, fields, models, tools
from odoo.exceptions import ValidationError
from odoo.osv import expression
from odoo.tools import consteq, human_size
from odoo.tools.mimetypes import guess_mimetype

_logger = logging.getLogger(__name__)

class RecordKeepingLawSection(models.Model):
    _name = "rk.law_section"
    _description = "Law section"
    
    _inherit = [
        "mail.thread",
    ]

    _order = "name asc"
    
    description = fields.Char()