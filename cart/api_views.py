from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Cart, CartItem
from products.models import Product
from .serializers import CartSerializer, AddToCartSerializer
from .telegram import send_telegram_message


def get_active_cart(user):
    cart, _ = Cart.objects.get_or_create(user=user, is_active=True)
    return cart


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_to_cart(request):
    serializer = AddToCartSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=400)
    product = Product.objects.filter(pk=serializer.validated_data['product_id']).first()
    if not product:
        return Response({'error': 'Product not found'}, status=404)
    cart = get_active_cart(request.user)
    item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        defaults={'price': product.price, 'quantity': serializer.validated_data['quantity']}
    )
    if not created:
        item.quantity += serializer.validated_data['quantity']
        item.save()
    return Response(CartSerializer(cart).data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_cart(request):
    cart = get_active_cart(request.user)
    return Response(CartSerializer(cart).data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def buy_cart(request):
    cart = get_active_cart(request.user)
    if not cart.items.exists():
        return Response({'error': 'Cart is empty'}, status=400)
    fio = request.data.get('fio', '').strip()
    phone = request.data.get('phone', '').strip()
    address = request.data.get('address', '').strip()
    telegram = request.data.get('telegram', '').strip()
    if not fio or not phone or not address:
        return Response({'error': 'FIO, Telefon va Manzil majburiy'}, status=400)
    order_num = Cart.objects.filter(is_active=False, user=request.user).count() + 1
    items_text = []
    for i, item in enumerate(cart.items.all(), 1):
        items_text.append(f"{i}) {item.product.name} — {item.quantity} dona = {item.total:,.0f} $")
    total = sum(item.total for item in cart.items.all())
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
    return Response({'status': 'success', 'message': 'Buyurtma yuborildi!'})


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_cart_item(request, item_id):
    cart = get_active_cart(request.user)
    item = CartItem.objects.filter(pk=item_id, cart=cart).first()
    if not item:
        return Response({'error': 'Item not found'}, status=404)
    item.delete()
    return Response({'status': 'deleted'})
