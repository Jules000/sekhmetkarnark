from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import TemplateView, View
from django.contrib import messages
from apps.shop.models import Product
from .models import Cart, CartItem


def _cart_data(request):
    items = []
    total = 0
    try:
        if request.user.is_authenticated:
            cart = Cart.objects.filter(user=request.user).first()
        else:
            sk = request.session.session_key
            cart = Cart.objects.filter(session_key=sk).first() if sk else None
        if cart:
            for item in cart.items.all().select_related("product__category"):
                if item.product:
                    items.append({
                        "id": item.id,
                        "product_id": item.product.id,
                        "name": item.product.name,
                        "price": str(item.product.price),
                        "quantity": item.quantity,
                        "total": str(item.product.price * item.quantity),
                        "image_url": item.product.main_image.url if item.product.main_image else "",
                        "category": item.product.category.name if item.product.category else "",
                    })
                    total += item.product.price * item.quantity
    except Exception:
        pass
    cart_product_ids = [i["product_id"] for i in items]
    suggested_qs = Product.objects.filter(is_active=True)
    if cart_product_ids:
        suggested_qs = suggested_qs.exclude(id__in=cart_product_ids)
    suggested = [
        {
            "id": p.id,
            "name": p.name,
            "price": str(p.price),
            "slug": p.slug,
            "image_url": p.main_image_thumb.url if p.main_image else "",
            "category": p.category.name if p.category else "",
        }
        for p in suggested_qs[:3]
    ]
    return {
        "success": True,
        "cart_count": sum(i["quantity"] for i in items),
        "cart_total": str(total),
        "items": items,
        "suggested": suggested,
    }


class CartDetailView(TemplateView):
    template_name = "cart/cart_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = self._get_cart()
        items = cart.items.all().select_related("product") if cart else []
        context["cart"] = cart
        context["cart_items"] = items
        context["cart_total"] = sum(
            item.product.price * item.quantity for item in items if item.product
        )
        context["suggested_products"] = Product.objects.filter(is_active=True)[:3]
        return context

    def _get_cart(self):
        if self.request.user.is_authenticated:
            cart, _ = Cart.objects.get_or_create(user=self.request.user)
        else:
            session_key = self.request.session.session_key
            if not session_key:
                self.request.session.save()
                session_key = self.request.session.session_key
            cart, _ = Cart.objects.get_or_create(session_key=session_key)
        return cart


class CartAddView(View):
    def post(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        quantity = int(request.POST.get("quantity", 1))
        if request.user.is_authenticated:
            cart, _ = Cart.objects.get_or_create(user=request.user)
        else:
            session_key = request.session.session_key
            if not session_key:
                request.session.save()
                session_key = request.session.session_key
            cart, _ = Cart.objects.get_or_create(session_key=session_key)

        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if not created:
            cart_item.quantity += quantity
        else:
            cart_item.quantity = quantity
        cart_item.save()

        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return JsonResponse(_cart_data(request))

        messages.success(request, "Produit ajouté au panier")
        return redirect(request.META.get("HTTP_REFERER", "cart:cart_detail"))


class CartRemoveView(View):
    def post(self, request, item_id):
        get_object_or_404(CartItem, id=item_id).delete()
        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return JsonResponse(_cart_data(request))
        return redirect("cart:cart_detail")


class CartUpdateView(View):
    def post(self, request, item_id):
        cart_item = get_object_or_404(CartItem, id=item_id)
        quantity = int(request.POST.get("quantity", 1))
        if quantity > 0:
            cart_item.quantity = quantity
            cart_item.save()
        else:
            cart_item.delete()
        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return JsonResponse(_cart_data(request))
        return redirect("cart:cart_detail")


class CartDataView(View):
    def get(self, request, *args, **kwargs):
        return JsonResponse(_cart_data(request))
