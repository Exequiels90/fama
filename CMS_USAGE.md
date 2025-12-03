# Sistema de Gestión de Contenido (CMS) - Guía de Uso

## 🚀 Inicio Rápido

### 1. Inicializar la Base de Datos con Contenido de Ejemplo

```bash
python backend/init_content.py
```

Este script creará contenido de ejemplo para todas las secciones editables del sitio.

### 2. Acceder al Panel de Administración

1. Inicia el servidor: `python backend/app.py`
2. Abre tu navegador en: `http://localhost:5000/admin/login`
3. Credenciales por defecto:
   - Usuario: `admin`
   - Contraseña: `admin123`

### 3. Gestionar Contenido

Desde el panel admin, ve a **Contenido** en el menú superior.

---

## 📋 Secciones Editables

### 🔗 Redes Sociales
**Ubicación en el sitio:** Topbar superior derecha

**Campos:**
- Nombre (ej: Facebook, Instagram)
- Icono Font Awesome (ej: `fab fa-facebook-f`)
- URL completa
- Orden de visualización
- Estado (Activo/Inactivo)

**Ejemplo de iconos:**
- Facebook: `fab fa-facebook-f`
- Twitter: `fab fa-twitter`
- Instagram: `fab fa-instagram`
- LinkedIn: `fab fa-linkedin-in`
- YouTube: `fab fa-youtube`

---

### 📌 Enlaces Topbar
**Ubicación en el sitio:** Topbar superior izquierda

**Campos:**
- Texto del enlace
- URL
- Orden
- Estado

**Uso típico:** FAQs, Ayuda, Soporte, Contacto

---

### 🎠 Carousel / Slider
**Ubicación en el sitio:** Banner principal del home

**Campos:**
- Título principal
- Subtítulo (opcional)
- URL de imagen
- Texto del botón (opcional)
- URL del botón (opcional)
- Orden
- Estado

**Recomendaciones:**
- Imágenes: 1920x410px
- Máximo 3-4 slides para mejor UX
- Usa el campo "orden" para controlar la secuencia

---

### ⭐ Características (Features)
**Ubicación en el sitio:** Debajo del carousel

**Campos:**
- Icono Font Awesome
- Título
- Orden
- Estado

**Ejemplos de iconos:**
- `fa fa-check` - Calidad
- `fa fa-shipping-fast` - Envío rápido
- `fas fa-exchange-alt` - Devoluciones
- `fa fa-phone-volume` - Soporte
- `fa fa-shield-alt` - Seguridad
- `fa fa-credit-card` - Pagos seguros

---

### 🏷️ Banners de Ofertas
**Ubicación en el sitio:** Sección de ofertas en el home

**Campos:**
- Título
- Subtítulo (opcional)
- URL de imagen
- Texto del botón (opcional)
- URL del botón (opcional)
- Color de fondo (selector de color)
- Alineación de texto (izquierda/centro/derecha)
- Orden
- Estado

**Recomendaciones:**
- Máximo 2 banners para diseño óptimo
- Imágenes PNG con transparencia funcionan mejor

---

### 🏢 Logos de Marcas (Vendors)
**Ubicación en el sitio:** Carrusel de marcas al final del home

**Campos:**
- Nombre de la marca
- URL del logo
- Orden
- Estado

**Recomendaciones:**
- Logos en formato cuadrado o rectangular
- Fondo transparente (PNG)
- Tamaño recomendado: 200x100px

---

### 👣 Footer

El footer se divide en secciones configurables:

#### Tipos de Sección:

**1. Acerca de (About)**
- Información de la empresa
- Aparece en la columna izquierda
- Soporta HTML básico

**2. Contacto (Contact)**
- Información de contacto
- Soporta HTML con iconos
- Ejemplo:
```html
<p class="mb-2"><i class="fa fa-map-marker-alt text-primary mr-3"></i>Tu dirección</p>
<p class="mb-2"><i class="fa fa-envelope text-primary mr-3"></i>email@ejemplo.com</p>
<p class="mb-0"><i class="fa fa-phone-alt text-primary mr-3"></i>+54 11 1234-5678</p>
```

**3. Enlaces (Links)**
- Secciones de enlaces rápidos
- Puedes crear múltiples secciones
- Cada sección puede tener su propio título
- Los enlaces se agregan después de crear la sección

---

## 💡 Tips y Mejores Prácticas

### Orden de Elementos
- Usa números como 10, 20, 30... en lugar de 1, 2, 3
- Esto te permite insertar elementos entre otros sin renumerar todo

### Imágenes
- Sube las imágenes a la carpeta `bootstrap-shop-template/img/`
- Usa rutas relativas: `img/mi-imagen.jpg`
- O URLs completas: `https://ejemplo.com/imagen.jpg`

### Iconos Font Awesome
- Busca iconos en: https://fontawesome.com/v5/search
- Usa la versión 5.x (la que está incluida en el template)
- Formato: `fa fa-nombre` o `fas fa-nombre` o `fab fa-nombre`

### Estado Activo/Inactivo
- Desactiva elementos en lugar de eliminarlos
- Útil para contenido estacional o promociones temporales
- Los elementos inactivos no se muestran en el sitio público

### HTML en Contenido
- Las secciones de footer soportan HTML
- Puedes usar etiquetas básicas: `<p>`, `<strong>`, `<i>`, `<a>`, etc.
- Útil para formatear texto y agregar iconos

---

## 🔄 Flujo de Trabajo Recomendado

1. **Planifica tu contenido** antes de empezar a cargar
2. **Prepara tus imágenes** en los tamaños recomendados
3. **Carga el contenido** desde el panel admin
4. **Previsualiza** en el sitio público
5. **Ajusta el orden** si es necesario
6. **Activa/desactiva** según necesites

---

## 🆘 Solución de Problemas

### No veo mis cambios en el sitio
- Refresca la página con Ctrl+F5 (limpia caché)
- Verifica que el elemento esté marcado como "Activo"
- Revisa que la URL de la imagen sea correcta

### Los iconos no se muestran
- Verifica que uses el formato correcto: `fa fa-nombre`
- Busca el icono en Font Awesome v5
- Algunos iconos requieren `fas` o `fab` en lugar de `fa`

### El footer no se ve bien
- Asegúrate de usar HTML válido en el contenido
- Cierra todas las etiquetas correctamente
- Usa las clases de Bootstrap para mejor formato

---

## 🎨 Personalización Avanzada

### Colores del Sitio
Ve a **Configuración** en el admin para cambiar:
- Color primario
- Color secundario
- Nombre de la tienda
- Iniciales/logo corto

### Agregar Más Secciones
Si necesitas agregar más tipos de contenido editable:
1. Crea un nuevo modelo en `backend/models.py`
2. Agrega las rutas en `backend/app.py`
3. Crea las plantillas del admin
4. Actualiza `index.html` para usar los nuevos datos

---

## 📚 Recursos Adicionales

- **Font Awesome Icons:** https://fontawesome.com/v5/search
- **Bootstrap 4 Docs:** https://getbootstrap.com/docs/4.6/
- **Flask Docs:** https://flask.palletsprojects.com/

---

¡Ahora tienes control total sobre el contenido de tu tienda! 🎉
