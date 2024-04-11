from django.shortcuts import redirect
from django.conf import settings
from django.views.generic import View, ListView
from base.models import Item
from collections import OrderedDict


class CartListView(ListView):
    model = Item
    template_name = 'pages/cart.html'

class AddCartView(View):
    # postされた時に処理
    def post(self, request):
        item_pk = request.POST.get('item.pk')
        quantity = int(request.POST.get('quantity'))
        cart = request.session.get('cart',None)
        # cartが空の場合
        if cart is None or len(cart) == 0:
            items = OrderedDict()
            # 順序付きの辞書をcartに格納
            cart = {'items':items}
        # cartがからでない時（item_pkがcartのitemの中にあるか）
        if item_pk in cart['items']:
            cart['items'][item_pk] += quantity
        else:
            cart['items'][item_pk] = quantity
        request.session['cart'] = cart
        return redirect('/cart/')