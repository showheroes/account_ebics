# Copyright 2020-2023 Noviat.
# License LGPL-3 or later (http://www.gnu.org/licenses/lgpl).

{
    "name": "account_ebics with OCA Bank Statement Imoort",
    "summary": "Use OCA Bank Statement Import with account_ebics",
    "version": "16.0.1.0.0",
    "author": "Noviat",
    "website": "https://www.noviat.com",
    "category": "Hidden",
    "license": "LGPL-3",
    "depends": [
        "account_ebics",
        "account_statement_import",
    ],
    # installable False unit OCA statement import becomes
    # available for 16.0
    "installable": False,
    "auto_install": True,
    "images": ["static/description/cover.png"],
}
