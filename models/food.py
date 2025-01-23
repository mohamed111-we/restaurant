from odoo import models, fields, api
from odoo.exceptions import ValidationError


class RestaurantFood(models.Model):
    _name = 'restaurant.food'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Restaurant Food'

    name = fields.Char(string="Food Name", required=True)
    category = fields.Selection([
        ('appetizer', 'Appetizer'),  # المقبلات
        ('entree', 'Entrée'),  # الطبق الرئيسي:.
        ('dessert', 'Dessert'),  # الحلوي.
        ('drinks', 'Drinks')  # المشروبات.
    ], string="Category", required=True)
    sizes = fields.Selection([
        ('large_size', 'Large Size'),
        ('medium_size', 'Medium Size'),
        ('small_size', 'Small Size'),
    ], string="Sizes", required=True, default='medium_size')
    price = fields.Float(string='Price')
    ingredients = fields.Text('Ingredients', tracking=True)
    is_available = fields.Boolean(string="Available", default=True)
    rating = fields.Float(string="Rating", digits=(2, 1), default=0.0)
    image = fields.Binary(string="Image")
    restaurant_id = fields.Many2one('restaurant.restaurant', string="Restaurant")
    ingredient_ids = fields.One2many('restaurant.ingredient','food_id',string='Ingredient')


    @api.constrains('price')
    def _check_price(self):
        for rec in self:
            if rec.price < 0:
                raise ValidationError("Price must be a positive number.")

    @api.constrains('rating')
    def _check_rating(self):
        for rec in self:
            if rec.rating < 0 or rec.rating > 5:
                raise ValidationError("Rating must be between 0 and 5.")

    def action_large_size(self):
        self.sizes = "large_size"

    def action_medium_size(self):
        self.sizes = "medium_size"

    def action_small_size(self):
        self.sizes = "small_size"


class RestaurantIngredient(models.Model):
    _name = 'restaurant.ingredient'
    _description = 'Restaurant Ingredient'

    name = fields.Char(string='Name of Ingredient', required=True)
    quantity = fields.Integer(string='Quantity Available')
    food_id = fields.Many2one('restaurant.food', string='Food')
