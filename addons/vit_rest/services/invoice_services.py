# Copyright 2018 ACSONE SA/NV
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
from odoo.addons.base_rest.components.service import to_bool, to_int
from odoo.addons.component.core import Component

import logging
_logger = logging.getLogger(__name__)

class InvoiceService(Component):
    _inherit = "base.rest.service"
    _name = "invoice.service"
    _usage = "invoice" #/vit_rest/private/invoice
    _collection = "vit.rest.api.private.services"
    _description = """
        Invoice Services
        Access to the invoice services is only allowed to authenticated users.
        If you are not authenticated go to <a href='/web/login'>Login</a>
    """

    def get(self, _id):
        """
        Get invoice's informations
        """
        return self._to_json(self._get(_id))

    def search(self, name):
        """
        Searh invoice by name
        """
        invoices = self.env["account.move"].name_search(name)
        invoices = self.env["account.move"].browse([i[0] for i in invoices])
        rows = []
        res = {"count": len(invoices), "rows": rows}
        for invoice in invoices:
            rows.append(self._to_json(invoice))
        return res

    # pylint:disable=method-required-super
    def create(self, **params):
        """
        Create a new invoice
        """
        p = self._prepare_params(params)
        invoice = self.env["account.move"].create(p)
        return self._to_json(invoice)

    def update(self, _id, **params):
        """
        Update invoice informations
        """
        invoice = self._get(_id)
        invoice.write(self._prepare_params(params))
        return self._to_json(invoice)
    
    def post(self, _id):
        """
        Post invoice informations
        """
        invoice = self._get(_id)
        invoice.action_post()
        return self._to_json(invoice)


    def complex_action(self, _id):
        invoice = self._get(_id)
        invoice.execute_complex_action()
        
        # create partne
        # create product
        # post journal
        # sedn email
        # send twitter
        pass


    def archive(self, _id, **params):
        """
        Archive the given invoice. This method is an empty method, IOW it
        don't update the invoice. This method is part of the demo data to
        illustrate that historically it's not mandatory to defined a schema
        describing the content of the response returned by a method.
        This kind of definition is DEPRECATED and will no more supported in
        the future.
        :param _id:
        :param params:
        :return:
        """
        return {"response": "Method archive called with id %s" % _id}

    # The following method are 'private' and should be never never NEVER call
    # from the controller.

    def _get(self, _id):
        return self.env["account.move"].browse(_id)

    def _prepare_params(self, params):
        _logger.info('_prepare_params....')
        for key in ["journal","currency","partner"]:
            if key in params:
                val = params.pop(key)
                if val.get("id"):
                    params["%s_id" % key] = val["id"]
                    
        for key in ["line_ids"]:
            if key in params:  # line_ids in param ? yes
                data = []
                for line in params[key]: # params['line_ids'] = [{},{}], line = {}
                    data.append((0,0,line))
                params[key] = data
                    
        return params

    # Validator
    def _validator_return_get(self):
        res = self._validator_get2()
        res.update({"id": {"type": "integer", "required": True, "empty": False}})
        return res

    def _validator_search(self):
        return {"name": {"type": "string", "nullable": False, "required": True}}

    def _validator_return_search(self):
        return {
            "count": {"type": "integer", "required": True},
            "rows": {
                "type": "list",
                "required": True,
                "schema": {"type": "dict", "schema": self._validator_return_get()},
            },
        }

    
    def _validator_create(self):
        _logger.info('_validator_create.....')
        res = {
            "name": {"type": "string", "required": True, "empty": False},
            "ref" : {"type": "string", "required": False, "empty": True},
            "date": {"type": "string", "nullable": True,},
            "move_type": {"type": "string", "nullable": False, "empty": False},
            "invoice_line_ids": { "type": "list", 
                          "schema": { "type":"dict", 
                                "schema":{
                                    "account_id" : {"type": "integer", },
                                    "product_id" : {"type": "integer", },
                                    "name"       : {"type": "string",},
                                    "price_unit" : {"type": "float",},
                                    "quantity"   : {"type": "float",},
                                    "price_subtotal"   : {"type": "float",},
                                    "tax_ids"    : {"type":"list","schema":{"type":"integer",}}
                                }
                            }
                         },
            "journal": {
                "type": "dict",
                "schema": {
                    "id": {
                        "type": "integer",
                        "coerce": to_int,
                        "required": True,
                        "nullable": False,
                    },
                    "name": {"type": "string"},
                },
            },            
            "currency": {
                "type": "dict",
                "schema": {
                    "id": {
                        "type": "integer",
                        "coerce": to_int,
                        "required": True,
                        "nullable": False,
                    },
                    "name": {"type": "string"},
                },
            },           
            "partner": {
                "type": "dict",
                "schema": {
                    "id": {
                        "type": "integer",
                        "coerce": to_int,
                        "required": True,
                        "nullable": False,
                    },
                    "name": {"type": "string"},
                },
            },
            "amount_untaxed":{"type": "float", "nullable": False, "empty": False},
        }
        return res
    
    def _validator_get2(self):
        _logger.info('_validator_get2.....')
        res = {
            "name": {"type": "string", },
            "ref" : {"type": "string", },
            "date": {"type": "date", },
            "invoice_line_ids": { 
                "type": "list", 
                "schema": { 
                    "type":"dict", 
                    "schema":{
                        "account_id" : {
                            "type": "dict", 
                            "schema":{ 
                                "id": {"type":"integer"},
                                "name": {"type":"string"}}},
                        "product_id" : {
                            "type": "dict", 
                            "required": False, "empty": True,
                            "schema":{ 
                                "id": {"type":"integer"}, 
                                "name": {"type":"string"}
                                }
                            },
                        "name"       : {"type": "string",},
                        "price_unit" : {"type": "float",},
                        "quantity"   : {"type": "float",},
                        "price_subtotal"   : {"type": "float",},
                        "tax_ids"    : {
                            "type"  :"list",
                            "schema":{
                                "type":"dict", 
                                "schema":{
                                    "id": {"type":"integer"}, 
                                    "name": {"type":"string"}
                                }
                            }
                        }
                    }
                }
                },
            "journal": {
                "type": "dict",
                "schema": {
                    "id": {
                        "type": "integer",
                    },
                    "name": {"type": "string"},
                },
            },            
            "currency": {
                "type": "dict",
                "schema": {
                    "id": {
                        "type": "integer",
                    },
                    "name": {"type": "string"},
                },
            },           
            "partner": {
                "type": "dict",
                "schema": {
                    "id": {
                        "type": "integer",
                    },
                    "name": {"type": "string"},
                },
            },
            "amount_untaxed":{"type": "float", "nullable": False, "empty": False},
        }
        return res

    def _validator_return_create(self):
        return self._validator_return_get()

    def _validator_update(self):
        res = self._validator_create()
        for key in res:
            if "required" in res[key]:
                del res[key]["required"]
        return res

    def _validator_return_update(self):
        return self._validator_return_get()

    def _validator_archive(self):
        return {}

    def _to_json(self, invoice):
        res = {
            "id": invoice.id,
            "name": invoice.name,
            "ref": invoice.ref or "",
            "date": invoice.date,
            "invoice_line_ids": [{
                'name':w.name, 
                'quantity':w.quantity,
                'price_unit':w.price_unit,
                'price_subtotal':w.price_subtotal,
                'product_id':{'id': w.product_id.id if w.product_id else 0, 'name': w.product_id.name if w.product_id else ''},
                'account_id':{'id': w.account_id.id, 'name': w.account_id.name},
                'partner_id':{'id': w.partner_id.id, 'name': w.partner_id.name},
                'tax_ids':[{'id': t.id, 'name': t.name} for t in w.tax_ids],
                } for w in invoice.invoice_line_ids],
            "amount_untaxed": invoice.amount_untaxed,
            "amount_by_group": invoice.amount_by_group,
            "amount_total": invoice.amount_total,
            "amount_residual": invoice.amount_residual,
            "narration": invoice.narration,
            "state": invoice.state,
            "move_type": invoice.move_type,
        }
        if invoice.journal_id:
            res["journal"] = {
                "id": invoice.journal_id.id,
                "name": invoice.journal_id.name,
            }
        
        if invoice.currency_id:
            res["currency"] = {
                "id": invoice.currency_id.id,
                "name": invoice.currency_id.name,
            }        
            
        if invoice.partner_id:
            res["partner"] = {
                "id": invoice.partner_id.id,
                "name": invoice.partner_id.name,
            }

        return res
