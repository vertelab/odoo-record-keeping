# -*- coding: utf-8 -*-

from odoo import _, api, fields, models
from odoo.exceptions import UserError
import logging

_logger = logging.getLogger(__name__)

IMPORT = '__import__'

class Attachment(models.Model):
    _inherit = ['ir.attachment']
    
    @api.model
    def migrate_from_xlsx(self, path, count=0, start=0, end=0):
        import base64
        import openpyxl
        import pytz
        from datetime import datetime
        from datetime import timedelta
        from pathlib import Path
        from . import mapping

        new_context = {
            'mail_create_nosubscribe': True,
            'mail_create_nolog': True,
            'mail_notrack': True,
            'tracking_disable': True,
            'tz': 'UTC',
        }

        path_to_file = Path(path)
        file_name = path_to_file.stem
        count = count or int(self.env['ir.config_parameter'].get_param('/migration/count', '0'))
        start = start or int(self.env['ir.config_parameter'].get_param(path, '0'))
        _logger.info(f"Initializing migration: {path=}, {start=}")
        if start < 0:
            return

        def compare_values(record, model_fields, vals):
            for key in list(vals):
                value = getattr(record, key)
                field_type = model_fields.get(key).get('type')
                if field_type in ['many2one']:
                    value = value.id
                elif field_type in ['one2many', 'many2many']:    
                    value = value.ids
                    if type(vals[key]) is list:
                        for command in vals[key]:
                            if type(command) is list or tuple:
                                if command[0] == 4 and command[1] in value:
                                    vals.pop(key)
                        continue
                if value == vals[key]:
                    vals.pop(key)
            return vals

        def create_record_and_xmlid_or_update(model, params, vals, xmlid):
            model_fields = get_model_fields(model, params)
            if 'skip' in vals:
               _logger.warning(f"skip {vals=}, {xmlid=}")
               return 0
            res_id = get_res_id(xmlid)
            if res_id:
                record = self.env.ref(xmlid).with_context(new_context)
                vals = compare_values(record, model_fields, vals)
                if vals:
                    record.write(vals)
                    _logger.info(f"write({vals=})")
                    _logger.info(f"write: {res_id=}, {xmlid=}")
            else:
                res_id = self.env[model].with_context(new_context).create(vals).id
                create_xmlid(model, res_id, xmlid)
                _logger.info(f"create_record_and_xmlid_or_update({model=}, {vals=}, {xmlid=})")
                _logger.info(f"create_xmlid({model=}, {res_id=}, {xmlid=})")
            if vals:
                if '_counter' in params:
                    params['_counter'] += 1
                else:
                    params['_counter'] = 1
            return res_id
            
        def create_xmlid(model, res_id, xmlid):
            module = xmlid.split('.')[0]
            vals = {'model': model,
                    'module': module,
                    'name': xmlid.split('.')[1],
                    'res_id': res_id}
            if module != IMPORT:
                vals['noupdate'] = True
            self.env['ir.model.data'].with_context(new_context).create(vals)

        def get_model_fields(model, params):
            model_fields = f"{model.replace('.', '_')}_fields_get"
            if model_fields not in params:
                params[model_fields] = self.env[model].fields_get()
            return params[model_fields]

        def get_res_id(xmlid):
            return self.env['ir.model.data'].xmlid_to_res_id(xmlid)

        def get_xmlid(name, ext_id):
            return f"{IMPORT}.{name.replace('.', '_')}_{ext_id}"
        
        def vals_builder(row, cols, fields):
            vals = {}
            for key in fields:
                if fields[key] in cols:
                    i = cols.index(fields[key])
                    vals[key] = row[i].value
            return vals

        sheet = openpyxl.load_workbook(path_to_file, data_only=True).active
        cols = [col.value for col in sheet[1]]

        params = getattr(mapping, file_name)
        model = params.get('model')
        fields = params.get('fields')
        before = params.get('before', '')
        after = params.get('after', '')
        params['_counter'] = 0
        
        for row in sheet.iter_rows(min_row=start or 2, max_row=end or None):
            vals = vals_builder(row, cols, fields)
            xmlid = get_xmlid(file_name, row[0].value)
            row_number = row[0].row
            if row_number % 1000 == 0:
                _logger.info(f"{row_number=}")
            try:
                exec(before)
                create_record_and_xmlid_or_update(model, params, vals, xmlid)
                exec(after)

            except Exception as e:
                _logger.error(f"{e=}")
                _logger.info(f"{[r.value for r in row]=}")
                _logger.warning(f"{vals=}")
                _logger.info(f"{xmlid=}")
                params['_counter'] = 1
                break

            else:
                if count and params['_counter'] >= count:
                    break

        _logger.info(f"{file_name=}, {row_number=}, {params['_counter']=}")
        
        self.env['ir.config_parameter'].set_param(path, str(row_number) if params['_counter'] else '-1')
