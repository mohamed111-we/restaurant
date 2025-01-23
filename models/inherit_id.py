from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    res_id = fields.Many2one('restaurant.restaurant', string='Restaurant')
    is_restaurant = fields.Boolean()
    test = fields.Char()


class ResPartner(models.Model):
    _inherit = 'res.partner'

    company_type = fields.Selection(selection_add=[
        ('employees', 'Authenticated Employees'),
    ],)