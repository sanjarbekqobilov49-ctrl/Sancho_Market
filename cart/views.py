from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Cart, CartItem
from .telegram import send_telegram_message


@login_required
def cart_view(request):
    cart, _ = Cart.objects.get_or_create(user=request.user, is_active=True)
    items = cart.items.all()
    total = sum(item.total for item in items)
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'update':
            item_id = request.POST.get('item_id')
            qty = int(request.POST.get('quantity', 1))
            item = get_object_or_404(CartItem, pk=item_id, cart=cart)
            if qty <= 0:
                item.delete()
            else:
                item.quantity = qty
                item.save()
        elif action == 'delete':
            item_id = request.POST.get('item_id')
            CartItem.objects.filter(pk=item_id, cart=cart).delete()
        elif action == 'buy':
            fio = request.POST.get('fio', '').strip()
            phone = request.POST.get('phone', '').strip()
            address = request.POST.get('address', '').strip()
            telegram = request.POST.get('telegram', '').strip()
            if not fio or not phone or not address:
                return render(request, 'cart/cart.html', {
                    'cart': cart, 'items': items, 'total': total,
                    'error': 'Iltimos, FIO, Telefon va Manzilni to\'ldiring!',
                    'fio': fio, 'phone': phone, 'address': address, 'telegram': telegram,
                })
            if not items.exists():
                return redirect('cart')
            order_num = Cart.objects.filter(is_active=False, user=request.user).count() + 1
            items_text = []
            for i, item in enumerate(items, 1):
                items_text.append(f"{i}) {item.product.name} — {item.quantity} dona = {item.total:,.0f} $")
            tg_info = f"\n✈️ Telegram: @{telegram}" if telegram else ""
            message = f"""📦 Yangi Buyurtma #{order_num}

👤 FIO: {fio}
📞 Phone: {phone}
📍 Address: {address}{tg_info}

🛍 Mahsulotlar:
{chr(10).join(items_text)}
💳 Umumiy: {total:,.0f} $"""
            send_telegram_message(message)
            cart.fio = fio
            cart.phone = phone
            cart.address = address
            cart.telegram = telegram
            cart.is_active = False
            cart.save()
            Cart.objects.create(user=request.user, is_active=True)
            return redirect('cart')
        return redirect('cart')
    return render(request, 'cart/cart.html', {
        'cart': cart,
        'items': items,
        'total': total,
        'fio': '', 'phone': '', 'address': '', 'telegram': '',
    })
