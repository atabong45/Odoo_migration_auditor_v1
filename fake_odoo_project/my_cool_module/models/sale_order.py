# fake_odoo_project/my_cool_module/models/sale_order.py

from odoo import models, fields, api

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def some_old_function(self):
        # This is a comment
        pass

    @api.one # <-- C'est cette ligne que notre agent doit trouver !
    def another_function(self):
        # Do something here
        self.ensure_one()
        return True
    
    def risky_sql_function(self):
        # Direct SQL execution
        self.env.cr.execute('SELECT * FROM sale_order')  # <-- Et c'est cette ligne aussi !  