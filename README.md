# Mini Shop

Online shop with Telegram order notifications.

## Project haqida

Mini Shop - bu Django + Bootstrap + DRF + Telegram Bot yordamida qurilgan mini ecommerce loyiha. Foydalanuvchilar mahsulotlarni ko'radi, savatchaga qo'shadi va buyurtma beradi. Admin maxsus UI orqali mahsulotlarni boshqaradi.

## Features

- User authentication (Register/Login/Logout) with role-based UI
- Product listing with category filter and search
- Product detail page with image gallery (carousel)
- Shopping cart (add, update, delete items)
- Checkout form (FIO, Phone, Address, Telegram)
- Order placement via Telegram bot
- Admin panel (custom UI, no Django admin)
- REST API (DRF + JWT Authentication)

## Installation

```bash
pip install -r requirements.txt
cp .env.example .env  # .env faylini sozlash
python manage.py migrate
python manage.py runserver
```

## API Endpoints

| Method | URL | Description | Auth |
|--------|-----|-------------|------|
| POST | /api/token/ | Get JWT token | - |
| POST | /api/token/refresh/ | Refresh JWT token | - |
| GET | /api/products/ | Product list | Token |
| POST | /api/products/ | Create product (admin) | Token (admin) |
| GET | /api/products/<id>/ | Product detail | Token |
| PUT/PATCH | /api/products/<id>/ | Update product (admin) | Token (admin) |
| DELETE | /api/products/<id>/ | Delete product (admin) | Token (admin) |
| POST | /api/cart/add/ | Add to cart | Token |
| GET | /api/cart/ | View cart | Token |
| DELETE | /api/cart/delete/<id>/ | Delete cart item | Token |
| POST | /api/cart/buy/ | Place order (Telegram) | Token |
| GET | /api/categories/ | Category list | Token |

## Telegram Setup

Create `.env` file in project root:

```
SECRET_KEY=your-secret-key
BOT_TOKEN=your_bot_token
CHAT_ID=your_chat_id
```

Bot tokenini [@BotFather](https://t.me/BotFather) dan oling. CHAT_ID ni [@userinfobot](https://t.me/userinfobot) dan oling.

## Screenshots

(UI rasmlari qo'shilishi kerak)
