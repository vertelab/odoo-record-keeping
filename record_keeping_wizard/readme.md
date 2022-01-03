#How to add to new record_keeping_module

* Create _matter_wizard_ model, inheriting from _matter_wizard_ in this module.
  * Implement function _\_get_module_ and field _model_, (see _record_keeping_sale_)
  * Add to \_\_init__.py
* Copy security/ir.model.access.csv, add to \_\_manifest__.py
* Add record_keeping_wizard to dependencies in \_\_manifest__.py
* Add definition of wizard creation in commented part in views/matter_wizard.xml
* Add button to trigger wizard creation in appropriate view.