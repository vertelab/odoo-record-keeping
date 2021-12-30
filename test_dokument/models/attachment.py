# -*- coding: utf-8 -*-

import logging
from odoo import _, api, fields, models
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)
IMPORT = '__import__'

class Attachment(models.Model):
    _inherit = ['ir.attachment']
    
    def migrate_from_xlsx_files(self, paths, count=100):
        for path in paths:
            self.migrate_from_xlsx(path, count=count)

    @api.model
    def migrate_from_xlsx(self, path, count=1000, start=0, end=0):
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

        def compare_values(record, record_fields, vals):
            for key in list(vals):
                value = getattr(record, key)
                if 'relation' in record_fields.get(key):
                    if 'res.partner.category' in record_fields.get(key)['relation']:
                        _logger.info(f"{value=}")
                    value = list(value)
                    if 'res.partner.category' in record_fields.get(key)['relation']:
                        _logger.info(f"{value=}")
                    _logger.info(f"{value=}")
                    if type(vals[key]) is list:
                        for command in vals[key]:
                            if type(command) is list or tuple:
                                if command[0] == 4 and command[1] in value:
                                    vals.pop(key)
                        continue
                if value == vals[key]:
                    vals.pop(key)
            return vals

        def create_xmlid(model, res_id, xmlid):
            module = xmlid.split('.')[0]
            vals = {'model': model,
                    'module': module,
                    'name': xmlid.split('.')[1],
                    'res_id': res_id}
            if module != IMPORT:
                vals['noupdate'] = True
            self.env['ir.model.data'].with_context(new_context).create(vals)

        def create_record_and_xmlid_or_update(model, params, vals, xmlid):
            model_fields = get_model_fields(params, model)
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
            return res_id
            
        def get_model_fields(params, model):
            model_fields = f"{model.replace('.', '_')}_fields_get"
            if model_fields not in params:
                _logger.info(f"only once {model_fields=}")
                params[model_fields] = self.env[model].fields_get()
            return params[model_fields]

        def get_res_id(xmlid):
            return self.env['ir.model.data'].xmlid_to_res_id(xmlid)

        def get_xmlid(identifier, ext_id):
            return f"{IMPORT}.{identifier.replace('.', '_')}_{ext_id}"
        
        def vals_builder(row, cols, fields):
            vals = {}
            for key in fields:
                if fields[key] in cols:
                    i = cols.index(fields[key])
                    vals[key] = row[i].value
            return vals

        path_to_file = Path(path)
        file_name = path_to_file.stem
        
        sheet = openpyxl.load_workbook(path_to_file, data_only=True).active
        cols = [col.value for col in sheet[1]]

        params = getattr(mapping, file_name)
        model = params.get('model')
        fields = params.get('fields')
        before = params.get('before', '')
        after = params.get('after', '')
        counter = 0
        for row in sheet.iter_rows(min_row=start if start else 2, max_row=end if end else None):
            vals = vals_builder(row, cols, fields)
            xmlid = get_xmlid(file_name, row[0].value)
            
            try:
                exec(before)
                create_record_and_xmlid_or_update(model, params, vals, xmlid)
                exec(after)
                if vals:
                    counter += 1

            except Exception as e:
                _logger.error(f"{e=}")
                _logger.info(f"{[r.value for r in row]=}")
                _logger.warning(f"{vals=}")
                _logger.info(f"{xmlid=}")
                break

            else:
                if count and counter >= count:
                    _logger.info(f"{row[0].row=}")
                    break

        _logger.info(f"migrate_from_xlsx({path=}, {count=}, {start=}, {end=}): DONE!")
            