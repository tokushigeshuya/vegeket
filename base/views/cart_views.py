from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import redirect
from django.conf import settings
from django.views.generic import View, ListView
from base.models import Item
from collections import OrderedDict


class CartListView(ListView):
    model = Item
    template_name = 'pages/cart.html'
    # ListViewが持っているメソッド（上書きする※オーバーライド）
    def get_queryset(self):
        # cartのキー情報のチェック
        cart = self.request.session.get('cart',None)
        if cart is None or len(cart) == 0:
            # cartにitemがない場合はトップページへ
            return redirect('/')
        self.queryset = []
        self.total = 0
        # item_pkにはキー、quantityにはvalue
        for item_pk, quantity in cart['items'].items():
            obj = Item.objects.get(pk=item_pk)
            # quantityとsubtotalは画面に表示するために一時的に表示（データベース内には入らない）
            obj.quantity = quantity
            # itemの価格*量
            obj.subtotal = int(obj.price * quantity)
            self.queryset.append(obj)
            self.total += obj.subtotal
        # 合計金額（消費税*1.1）
        self.tax_included_total = int(self.total * (settings.TAX_RATE + 1))
        # cartの中にtotalを構築
        cart['total'] = self.total
        cart['tax_included_total'] = self.tax_included_total
        self.request.session['cart'] = cart
        return super().get_queryset()
        

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