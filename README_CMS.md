# 🛍️ FaMa Shop - Sistema de Gestión de Contenido

Sistema completo de e-commerce con panel de administración y CMS integrado para gestionar todo el contenido visual del sitio.

## 🌟 Características Principales

### ✅ Tienda Online
- Catálogo de productos con categorías
- Carrito de compras
- Sistema de checkout
- Gestión de pedidos

### ✅ Panel de Administración
- CRUD completo de productos
- CRUD completo de categorías
- Gestión de pedidos
- Configuración de apariencia (colores, nombre)
- **Sistema CMS para gestionar TODO el contenido**

### ✅ Sistema CMS (Nuevo)
Gestiona desde el admin:
- 🔗 Redes sociales
- 📌 Enlaces del topbar
- 🎠 Carousel/Slider principal
- ⭐ Cajas de características
- 🏷️ Banners de ofertas
- 🏢 Logos de marcas
- 👣 Footer completo

## 🚀 Inicio Rápido

### 1. Requisitos
- Python 3.8+
- pip

### 2. Instalación
```bash
# Instalar dependencias
pip install -r backend/requirements.txt

# Inicializar contenido de ejemplo
python backend/init_content.py
```

### 3. Ejecutar
```bash
# Iniciar servidor
python backend/app.py

# Abrir en navegador
http://localhost:5000
```

### 4. Acceder al Admin
```
URL: http://localhost:5000/admin/login
Usuario: admin
Contraseña: admin123
```

## 📁 Estructura del Proyecto

```
shoponline/
├── backend/
│   ├── app.py              # Aplicación Flask principal
│   ├── models.py           # Modelos de base de datos
│   ├── config.py           # Configuración
│   ├── init_content.py     # Script de inicialización
│   ├── requirements.txt    # Dependencias Python
│   └── shop.db            # Base de datos SQLite
│
├── bootstrap-shop-template/
│   ├── admin_*.html       # Plantillas del admin
│   ├── index.html         # Home del sitio
│   ├── shop.html          # Catálogo
│   ├── cart.html          # Carrito
│   ├── checkout.html      # Checkout
│   ├── css/               # Estilos
│   ├── js/                # JavaScript
│   └── img/               # Imágenes
│
└── docs/
    ├── CMS_USAGE.md                    # Guía de uso del CMS
    ├── INSTRUCCIONES_RAPIDAS.md        # Inicio rápido
    ├── DATABASE_SCHEMA.md              # Esquema de BD
    ├── RESUMEN_IMPLEMENTACION.md       # Resumen técnico
    ├── CHECKLIST_VERIFICACION.md       # Checklist de pruebas
    └── SHOPONLINE_PLAN.md              # Plan del proyecto
```

## 📚 Documentación

### Para Usuarios
- **[Instrucciones Rápidas](INSTRUCCIONES_RAPIDAS.md)** - Cómo empezar en 5 minutos
- **[Guía de Uso del CMS](CMS_USAGE.md)** - Guía completa con ejemplos

### Para Desarrolladores
- **[Esquema de Base de Datos](DATABASE_SCHEMA.md)** - Estructura de tablas
- **[Resumen de Implementación](RESUMEN_IMPLEMENTACION.md)** - Detalles técnicos
- **[Checklist de Verificación](CHECKLIST_VERIFICACION.md)** - Pruebas completas

### Plan del Proyecto
- **[Plan General](SHOPONLINE_PLAN.md)** - Estado y próximos pasos

## 🎨 Personalización

### Cambiar Colores y Nombre
1. Admin → Configuración
2. Editar:
   - Nombre de la tienda
   - Iniciales (logo)
   - Color primario
   - Color secundario
3. Guardar

### Editar Contenido Visual
1. Admin → Contenido
2. Seleccionar sección a editar
3. Crear/Editar/Eliminar elementos
4. Los cambios se reflejan inmediatamente

## 🔧 Tecnologías

### Backend
- **Flask** - Framework web
- **SQLAlchemy** - ORM
- **SQLite** - Base de datos (desarrollo)
- **Werkzeug** - Seguridad y utilidades

### Frontend
- **Bootstrap 4** - Framework CSS
- **jQuery** - JavaScript
- **Font Awesome 5** - Iconos
- **Owl Carousel** - Carruseles

## 📊 Base de Datos

### Tablas Principales
- `products` - Productos
- `categories` - Categorías
- `orders` - Pedidos
- `order_items` - Items de pedidos
- `admin_users` - Usuarios admin
- `settings` - Configuración

### Tablas CMS (Nuevas)
- `social_links` - Redes sociales
- `topbar_links` - Enlaces topbar
- `carousel_slides` - Slides del carousel
- `feature_boxes` - Características
- `offer_banners` - Banners de ofertas
- `footer_sections` - Secciones del footer
- `footer_links` - Enlaces del footer
- `vendor_logos` - Logos de marcas

## 🔐 Seguridad

- Autenticación con hash de contraseñas
- Protección de rutas admin con `@login_required`
- Validación de datos en backend
- Sanitización de HTML en templates

## 🚧 Próximos Pasos

### Fase 1 (Actual)
- ✅ Sistema CMS completo
- ⏳ Adaptar páginas restantes (detail, cart, checkout)
- ⏳ Sistema de upload de imágenes

### Fase 2
- ⏳ Integración con Mercado Pago
- ⏳ Webhooks para notificaciones
- ⏳ Reportes de ventas

### Mejoras Futuras
- Editor WYSIWYG
- Múltiples imágenes por producto
- Sistema de roles y permisos
- API REST
- Cache de contenido

## 🐛 Solución de Problemas

### El servidor no inicia
```bash
# Verificar que las dependencias estén instaladas
pip install -r backend/requirements.txt

# Verificar que el puerto 5000 esté libre
netstat -ano | findstr :5000
```

### No veo mis cambios
- Refrescar con Ctrl+F5 (limpia caché)
- Verificar que el elemento esté marcado como "Activo"
- Revisar logs del servidor

### Imágenes no cargan
- Verificar que la URL sea correcta
- Para imágenes locales, usar: `img/nombre.jpg`
- Para imágenes externas, usar URL completa

### Iconos no se muestran
- Usar formato Font Awesome v5
- Ejemplos: `fa fa-check`, `fas fa-star`, `fab fa-facebook-f`

## 📞 Soporte

Para problemas o preguntas:
1. Revisar la documentación en `/docs`
2. Verificar el checklist de pruebas
3. Revisar logs del servidor

## 📄 Licencia

Este proyecto es privado y propietario.

## 👥 Créditos

- **Template:** Bootstrap E-Shopper
- **Framework:** Flask
- **Iconos:** Font Awesome
- **Desarrollo:** FaMa Team

---

## 🎉 ¡Listo para Usar!

El sistema está completamente funcional y listo para gestionar tu tienda online.

**¿Necesitas ayuda?** Consulta la [Guía de Uso del CMS](CMS_USAGE.md)

---

**Versión:** 1.0.0  
**Última actualización:** Diciembre 2024
