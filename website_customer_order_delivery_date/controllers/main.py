# -*- coding: utf-8 -*-
# Part of AppJetty. See LICENSE file for full copyright and licensing details.

from datetime import datetime
from leewise import http
from leewise.http import request
from leewise.addons.website_sale.controllers.main import WebsiteSale


class WebsiteSaleDeliveryDate(WebsiteSale):

    """Add Customer Order Delivery functions to the website_sale controller."""

    @http.route(['/shop/customer_order_delivery'], type='json', auth="public", methods=['POST'], website=True)
    def customer_order_delivery(self, **post):
        """ Json method that used to add a
        delivery date and/or comment when the user clicks on 'pay now' button.
        """

        if post.get('delivery_date') or post.get('delivery_comment'):
            order = request.website.sale_get_order().sudo()
            redirection = self.checkout_redirection(order)
            if redirection:
                return redirection

            if order and order.id:
                values = {}
                if post.get('delivery_comment'):
                    values.update(
                        {'customer_order_delivery_comment': post.get('delivery_comment')})
                else:
                    values.update(
                        {'customer_order_delivery_comment': 'No Comment'})
                p_date = datetime.strptime(
                    post.get('delivery_date'), '%Y-%m-%d')
                if order and order.id:
                    values.update({
                        'customer_order_delivery_date': p_date
                    })

                order.write(values)
        return True
