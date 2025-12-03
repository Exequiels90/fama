# 📊 Esquema de Base de Datos - Sistema CMS

## Tablas Existentes (Original)

### `admin_users`
- Usuarios administradores del sistema
- Campos: id, username, password_hash, created_at

### `categories`
- Categorías de productos
- Campos: id, name, description, created_at

### `products`
- Productos de la tienda
- Campos: id, name, description, price_ars, stock, image_url, is_active, category_id, created_at

### `orders`
- Pedidos de clientes
- Campos: id, customer_name, customer_email, customer_phone, customer_address, total_amount_ars, status, created_at, updated_at

### `order_items`
- Items individuales de cada pedido
- Campos: id, order_id, product_id, product_name, unit_price_ars, quantity, line_total_ars

### `settings`
- Configuración general del sitio
- Campos: id, key, value

---

## Nuevas Tablas (Sistema CMS)

### `social_links`
**Propósito:** Enlaces a redes sociales en el topbar

| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | Integer | PK |
| name | String(50) | Nombre de la red (Facebook, Twitter, etc.) |
| icon | String(50) | Clase de icono Font Awesome |
| url | String(255) | URL completa del perfil |
| is_active | Boolean | Si está visible o no |
| order | Integer | Orden de visualización |

**Ejemplo:**
```python
SocialLink(
    name="Facebook",
    icon="fab fa-facebook-f",
    url="https://facebook.com/mitienda",
    is_active=True,
    order=1
)
```

---

### `topbar_links`
**Propósito:** Enlaces superiores (FAQs, Help, Support)

| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | Integer | PK |
| text | String(100) | Texto del enlace |
| url | String(255) | URL del enlace |
| is_active | Boolean | Si está visible o no |
| order | Integer | Orden de visualización |

---

### `carousel_slides`
**Propósito:** Slides del carousel/banner principal

| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | Integer | PK |
| title | String(200) | Título principal |
| subtitle | String(200) | Subtítulo (opcional) |
| button_text | String(100) | Texto del botón (opcional) |
| button_url | String(255) | URL del botón (opcional) |
| image_url | String(255) | URL de la imagen de fondo |
| is_active | Boolean | Si está visible o no |
| order | Integer | Orden de visualización |

---

### `feature_boxes`
**Propósito:** Cajas de características (Quality, Shipping, etc.)

| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | Integer | PK |
| icon | String(50) | Clase de icono Font Awesome |
| title | String(100) | Título de la característica |
| is_active | Boolean | Si está visible o no |
| order | Integer | Orden de visualización |

---

### `offer_banners`
**Propósito:** Banners de ofertas especiales

| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | Integer | PK |
| title | String(200) | Título principal |
| subtitle | String(200) | Subtítulo (opcional) |
| button_text | String(100) | Texto del botón (opcional) |
| button_url | String(255) | URL del botón (opcional) |
| image_url | String(255) | URL de la imagen |
| background_color | String(20) | Color de fondo (hex) |
| text_align | String(20) | Alineación: left, center, right |
| is_active | Boolean | Si está visible o no |
| order | Integer | Orden de visualización |

---

### `footer_sections`
**Propósito:** Secciones del footer

| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | Integer | PK |
| section_type | String(50) | Tipo: about, contact, links |
| title | String(200) | Título de la sección |
| content | Text | Contenido (soporta HTML) |
| is_active | Boolean | Si está visible o no |
| order | Integer | Orden de visualización |

**Tipos de Sección:**
- `about`: Información de la empresa
- `contact`: Datos de contacto
- `links`: Sección de enlaces (los enlaces se agregan en otra tabla)

---

### `footer_links`
**Propósito:** Enlaces dentro de secciones del footer

| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | Integer | PK |
| section_id | Integer | FK a footer_sections |
| text | String(100) | Texto del enlace |
| url | String(255) | URL del enlace |
| icon | String(50) | Icono (opcional) |
| is_active | Boolean | Si está visible o no |
| order | Integer | Orden de visualización |

**Relación:** Muchos footer_links pertenecen a una footer_section

---

### `vendor_logos`
**Propósito:** Logos de marcas/vendors

| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | Integer | PK |
| name | String(100) | Nombre de la marca |
| image_url | String(255) | URL del logo |
| is_active | Boolean | Si está visible o no |
| order | Integer | Orden de visualización |

---

## Patrones Comunes

### Campo `order`
- Todas las tablas CMS tienen un campo `order`
- Permite ordenar elementos manualmente
- Recomendación: usar 10, 20, 30... para facilitar inserciones

### Campo `is_active`
- Permite ocultar elementos sin eliminarlos
- Útil para contenido estacional o temporal
- Los elementos inactivos no se muestran en el sitio público

### URLs de Imágenes
- Pueden ser rutas relativas: `img/mi-imagen.jpg`
- O URLs completas: `https://ejemplo.com/imagen.jpg`
- Las imágenes locales van en `bootstrap-shop-template/img/`

---

## Migraciones Futuras

Si necesitas agregar campos o tablas:

1. Modifica `backend/models.py`
2. Para SQLite (desarrollo), simplemente elimina `shop.db` y reinicia
3. Para producción (Postgres), usa Flask-Migrate o Alembic

---

## Consultas Útiles

### Ver todos los elementos activos ordenados
```python
items = ModelName.query.filter_by(is_active=True).order_by(ModelName.order).all()
```

### Obtener una sección específica del footer
```python
about = FooterSection.query.filter_by(section_type='about', is_active=True).first()
```

### Obtener enlaces de una sección
```python
section = FooterSection.query.get(section_id)
links = section.links  # Gracias a la relación definida
```

---

## Backup y Restauración

### Backup (SQLite)
```bash
cp backend/shop.db backend/shop_backup.db
```

### Restauración
```bash
cp backend/shop_backup.db backend/shop.db
```

### Exportar a SQL
```bash
sqlite3 backend/shop.db .dump > backup.sql
```

---

## Índices Recomendados (Futuro)

Para mejor performance en producción:
- `social_links.order`
- `carousel_slides.order`
- `feature_boxes.order`
- `footer_sections.section_type`
- `footer_links.section_id`

---

¡Esquema completo y documentado! 📚
