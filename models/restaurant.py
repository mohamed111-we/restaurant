from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class Restaurant(models.Model):
    _name = 'restaurant.restaurant'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Restaurant Management'

    name = fields.Char(string="Restaurant Name", required=True)
    owner_id = fields.Many2one('res.partner', string='Owner', required=True)
    phone = fields.Char(string='Owner Phone', related='owner_id.phone', store=True)
    email = fields.Char(string='Owner Email', related='owner_id.email', store=True)
    location = fields.Char(string="Location", )
    zip_code = fields.Char(string='Zip Code')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('open', 'Open'),
        ('closed', 'Closed')
    ], string='Status', default='draft', required=True)
    cuisine_type = fields.Selection([
        ('italian', 'Italian'),
        ('chinese', 'Chinese'),
        ('indian', 'Indian'),
        ('american', 'American'),
        ('french', 'French'),
        ('other', 'Other')
    ], string='Cuisine Type')  # نوع المطبخ
    description = fields.Text(string="Description")
    rating = fields.Float(string="Rating", digits=(2, 1), default=0.0)
    reference = fields.Char(string='Reference', required=True, copy=False, readonly=True, index=True,
                            default=lambda self: _('New'))
    image = fields.Binary(string="Image")
    reservation_ids = fields.One2many('restaurant.reservation', "restaurant_id", string="Reservations")
    table_ids = fields.One2many('restaurant.table', "restaurant_id", string="Tables")
    review_ids = fields.One2many('restaurant.review', "restaurant_id", string="Reservations")
    employee_ids = fields.One2many('restaurant.employee', "restaurant_id", string="Employee")


    def action_draft(self):
        self.state = 'draft'
        return {
            'effect': {
                'fadeout': 'slow',
                'message': 'The action has been successfully completed.',
                'type': 'rainbow_man',
            }
        }

    def action_open(self):
        self.state = 'open'
        return {
            'effect': {
                'fadeout': 'slow',
                'message': 'The action has been successfully completed.',
                'type': 'rainbow_man',
            }
        }

    def action_closed(self):
        self.state = 'closed'
        return {
            'effect': {
                'fadeout': 'slow',
                'message': 'The action has been successfully completed.',
                'type': 'rainbow_man',
            }
        }

    api.constrains('rating')
    def _check_rating(self):
        for rec in self:
            if rec.rating < 0 or rec.rating > 5:
                raise ValidationError("Rating must be between 0 and 5.")

    @api.model
    def create(self, vals):
        if vals.get('reference', _('New')) == _('New'):
            vals['reference'] = self.env['ir.sequence'].next_by_code('restaurant.restaurant') or _('New')
        return super(Restaurant, self).create(vals)


class RestaurantReservation(models.Model):    # حجز
    _name = 'restaurant.reservation'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Restaurant Reservation'

    customer_name = fields.Char(string="Customer Name", required=True)
    number_of_people = fields.Integer(string="Number of People", required=True)
    reservation_date= fields.Date(string="Reservation Date & Time", required=True)
    status = fields.Selection(
        [('confirmed', 'Confirmed'),
         ('cancelled', 'Cancelled'),
         ('completed', 'Completed')],
        string="Status", default='confirmed')
    restaurant_id = fields.Many2one("restaurant.restaurant", string="Restaurant")

    @api.constrains('number_of_people')
    def _check_number_of_people(self):
        for record in self:
            if record.number_of_people <= 0:
                raise ValidationError("Number of people must be greater than zero.")



class RestaurantTable(models.Model):
    _name = 'restaurant.table'
    _description = 'Restaurant Table'


    table_number = fields.Integer(string="Table Number", required=True)
    availability = fields.Selection(
        [('available', 'Available'), # متاح
         ('occupied', 'Occupied'), # مشغول
         ('under_maintenance', 'Under Maintenance')] # تحت الصيانة
        , string="Availability", default='available')
    restaurant_id = fields.Many2one("restaurant.restaurant", string="Restaurant")



class Review(models.Model):
    _name = 'restaurant.review'
    _description = 'Customer Review'

    customer_name = fields.Char(string="Customer Name", required=True)
    rating = fields.Float(string="Rating", digits=(2, 1), default=0.0)
    comments = fields.Text(string="Comments")
    restaurant_id = fields.Many2one("restaurant.restaurant", string="Restaurant")

    api.constrains('rating')
    def _check_rating(self):
        for rec in self:
            if rec.rating < 0 or rec.rating > 5:
                raise ValidationError("Rating must be between 0 and 5.")



class RestaurantEmployee(models.Model):
    _name = 'restaurant.employee'
    _description = 'Restaurant Employee'

    employee_name = fields.Char(string="Employee Name", required=True)  # اسم الموظف
    role = fields.Selection(
        [('waiter', 'Waiter'),  # جرسون
         ('chef', 'Chef'),  # شيف
         ('supervisor', 'Supervisor')]  # مشرف
        , string="ٌRole", default='waiter')
    working_hours = fields.Float(string="Working Hours")
    restaurant_id = fields.Many2one("restaurant.restaurant", string="Restaurant")

    @api.constrains('working_hours')
    def _check_working_hours(self):
        for record in self:
            if record.working_hours < 5:
                raise ValidationError("Working hours must be at least 5 hours.")