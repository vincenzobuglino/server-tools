#   @author Sébastien BEAU @ Akretion
#   @author Florian DA COSTA @ Akretion
#   @author Benoit GUILLOT @ Akretion
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "File Email",
    "version": "12.0.1.0.0",
    "author": "Akretion,Odoo Community Association (OCA)",
    "category": "Generic Modules",
    "license": "AGPL-3",
    "website": "http://www.akretion.com/",
    "maintainers": ["florian-dacosta", "sebastienbeau", "bealdav"],
    "depends": ["attachment_queue", "fetchmail", "test_mail"],
    "demo": [],
    "data": ["security/ir.model.access.csv", "views/fetchmail_views.xml"],
    "installable": True,
    "images": [],
}
