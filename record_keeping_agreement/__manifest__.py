{
    'website': 'https://vertel.se/apps/odoo-record-keeping/record_keeping_agreement',
    "name": "Record Keeping - Agreement",
    'summary': "Adds agreements to record keeping.",
    'description': '''
Record Keeping - Agreement
==========================

    Adds agreements to record keeping.

    Features:

        - UI Integration: Extends 1 view(s) in the Odoo interface.
        - Extends Odoo: Builds on agreement.
    ''',
    "version": "18.0.1.0.0",
    "license": "LGPL-3",
    "depends": [
        "record_keeping",
        "agreement",
    ],
    "data": [
        "views/agreement_form_inherit.xml",
    ],
    "installable": True,

}
