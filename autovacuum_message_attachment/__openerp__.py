# -*- coding: utf-8 -*-

# Copyright (C) 2018 Akretion
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

{
    "name": "AutoVacuum Mail Message and Attachment",
    "version": "8.0.1.1.1",
    "category": "Tools",
    "website": "https://github.com/OCA/server-tools",
    "author": "Akretion, Odoo Community Association (OCA)",
    "license": "LGPL-3",
    "installable": True,
    "summary": "Automatically delete old mail messages and attachments",
    "depends": [
        "mail",
    ],
    "data": [
        "data/data.xml",
        "views/rule_vacuum.xml",
        "security/ir.model.access.csv",
    ],
}
