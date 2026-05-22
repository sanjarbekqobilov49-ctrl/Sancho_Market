from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from products.api_views import ProductViewSet, CategoryViewSet
from cart.api_views import add_to_cart, get_cart, buy_cart, delete_cart_item

router = DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'categories', CategoryViewSet)

urlpatterns = [
    path('', include('products.urls')),
    path('cart/', include('cart.urls')),
    path('', include('accounts.urls')),
    path('admin/products/', include('products.admin_urls')),
    path('api/', include(router.urls)),
    path('api/cart/add/', add_to_cart, name='api_cart_add'),
    path('api/cart/', get_cart, name='api_cart'),
    path('api/cart/buy/', buy_cart, name='api_cart_buy'),
    path('api/cart/delete/<int:item_id>/', delete_cart_item, name='api_cart_delete'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
