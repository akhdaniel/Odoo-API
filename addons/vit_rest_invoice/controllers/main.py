# Copyright 2018 ACSONE SA/NV
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo.addons.base_rest.controllers import main


class VitInvoicePrivateApiController(main.RestController):
    _root_path = "/vit_rest_invoice/private/"
    _collection_name = "vit.rest.api.private.services"
    _default_auth = "user"


