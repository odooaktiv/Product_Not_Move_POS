from datetime import datetime
from datetime import date
from odoo import api, fields, models, _
from odoo.exceptions import UserError
from odoo.tools.float_utils import float_round


class ProductNotMovePOS(models.TransientModel):
    _name = "product.not.move.pos.report"
    _description = 'Product Not Move POS'

    @api.model
    def _get_end_date(self):
        return datetime.now().date()

    start_date = fields.Date(string="From Date", required=True)
    end_date = fields.Date(string="End Date", required=True,
                           default=_get_end_date)

    @api.multi
    def get_product_data(self):
        product_rec = self.env['product.product'].search(
            [('available_in_pos', '=', True)])
        move_list = []
        for product in product_rec:
            product_move_rec = self.env['stock.move.line'].search(
                [('state', '=', 'done'),
                 ('product_id', '=', product.id)])
            for move_line in product_move_rec:
                if move_line.date:
                    if move_line.date.date() >= self.start_date and move_line.date.date() <= self.end_date:
                        move_list.append(move_line.product_id.id)
        vals = []
        product_not_move_obj = self.env['product.product'].search(
            [('available_in_pos', '=', True), ('id', 'not in', move_list)])
        for product_not_move in product_not_move_obj:
            data_dict = {}
            duration = self.start_date - product_not_move.create_date.date()
            data_dict.update({
                'product_id':product_not_move,
                'available_qty': product_not_move.qty_available,
                'last_sale_date':product_not_move.create_date.date(),
                'duration_day': duration.days,
            })
            vals.append(data_dict)
        for product in product_rec:
            product_move_rec = self.env['stock.move.line'].search(
                [('state', '=', 'done'),
                 ('product_id', '=', product.id)], order='date DESC', limit=1)
        for move_line in product_move_rec:
            if move_line.date:
                if not move_line.date.date() >= self.start_date and move_line.date.date() <= self.end_date:
                    duration = self.start_date - move_line.date.date()
                    sale_date = move_line.date.date()
                    data_dict = {}
                    data_dict.update({
                        'product_id':product,
                        'available_qty': product.qty_available,
                        'last_sale_date':sale_date,
                        'duration_day': duration.days,
                    })
                    vals.append(data_dict)
        return vals

    @api.multi
    def print_product_report(self):
        if self.start_date > self.end_date:
            raise UserError(_("Period to should be greater than Period From"))
        return self.env.ref(
            'product_not_move_pos.report_product_move').report_action(self)
