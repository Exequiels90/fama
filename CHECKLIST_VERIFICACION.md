# ✅ Checklist de Verificación - Sistema CMS

## Pre-requisitos
- [ ] Python 3.8+ instalado
- [ ] Dependencias instaladas (`pip install -r backend/requirements.txt`)
- [ ] Base de datos inicializada

## Instalación y Configuración

### 1. Inicializar Contenido
```bash
python backend/init_content.py
```
**Verificar:**
- [ ] Script ejecuta sin errores
- [ ] Muestra mensajes de confirmación (✓)
- [ ] Archivo `backend/shop.db` existe

### 2. Iniciar Servidor
```bash
python backend/app.py
```
**Verificar:**
- [ ] Servidor inicia en http://127.0.0.1:5000
- [ ] No hay errores en consola
- [ ] Muestra "Debug mode: on"

## Verificación del Admin

### 3. Login
**URL:** http://localhost:5000/admin/login

**Verificar:**
- [ ] Página de login carga correctamente
- [ ] Formulario tiene campos username y password
- [ ] Login con `admin` / `admin123` funciona
- [ ] Redirecciona a dashboard

### 4. Dashboard
**URL:** http://localhost:5000/admin

**Verificar:**
- [ ] Muestra contadores de productos y pedidos
- [ ] Menú superior tiene: Productos, Categorías, Pedidos, **Contenido**, Configuración
- [ ] Botón "Salir" funciona

### 5. Hub de Contenido
**URL:** http://localhost:5000/admin/content

**Verificar:**
- [ ] Muestra 7 tarjetas de secciones
- [ ] Cada tarjeta tiene botón "Administrar"
- [ ] Iconos se muestran correctamente

## Verificación de Cada Sección

### 6. Redes Sociales
**URL:** http://localhost:5000/admin/content/social-links

**Verificar:**
- [ ] Lista muestra 4 redes sociales de ejemplo
- [ ] Tabla tiene columnas: Orden, Nombre, Icono, URL, Estado, Acciones
- [ ] Botón "Agregar Red Social" funciona
- [ ] Botón editar (lápiz) funciona
- [ ] Botón eliminar (basura) pide confirmación
- [ ] Formulario de creación/edición tiene todos los campos
- [ ] Guardar funciona y redirecciona

### 7. Enlaces Topbar
**URL:** http://localhost:5000/admin/content/topbar-links

**Verificar:**
- [ ] Lista muestra 3 enlaces de ejemplo
- [ ] CRUD completo funciona
- [ ] Formularios validan campos requeridos

### 8. Carousel
**URL:** http://localhost:5000/admin/content/carousel

**Verificar:**
- [ ] Lista muestra 2 slides de ejemplo
- [ ] Imágenes se muestran en miniatura
- [ ] CRUD completo funciona
- [ ] Formulario tiene todos los campos (título, subtítulo, imagen, botón)

### 9. Características
**URL:** http://localhost:5000/admin/content/features

**Verificar:**
- [ ] Lista muestra 4 características de ejemplo
- [ ] Iconos se renderizan correctamente
- [ ] CRUD completo funciona

### 10. Ofertas
**URL:** http://localhost:5000/admin/content/offers

**Verificar:**
- [ ] Lista muestra 2 ofertas de ejemplo
- [ ] Imágenes se muestran en miniatura
- [ ] CRUD completo funciona
- [ ] Selector de color funciona
- [ ] Selector de alineación funciona

### 11. Vendors
**URL:** http://localhost:5000/admin/content/vendors

**Verificar:**
- [ ] Lista muestra 6 logos de ejemplo
- [ ] Imágenes se muestran en miniatura
- [ ] CRUD completo funciona

### 12. Footer
**URL:** http://localhost:5000/admin/content/footer

**Verificar:**
- [ ] Lista muestra 3 secciones de ejemplo
- [ ] Tipos de sección se muestran correctamente
- [ ] CRUD completo funciona
- [ ] Selector de tipo de sección funciona

## Verificación del Sitio Público

### 13. Página Principal
**URL:** http://localhost:5000/

**Verificar Topbar:**
- [ ] Enlaces superiores izquierda (FAQs, Ayuda, Soporte)
- [ ] Iconos de redes sociales derecha
- [ ] Nombre de la tienda (FaMa)

**Verificar Carousel:**
- [ ] Muestra 2 slides
- [ ] Imágenes cargan correctamente
- [ ] Títulos y subtítulos se muestran
- [ ] Botones funcionan
- [ ] Controles prev/next funcionan

**Verificar Características:**
- [ ] Muestra 4 cajas de características
- [ ] Iconos se renderizan
- [ ] Textos se muestran

**Verificar Ofertas:**
- [ ] Muestra 2 banners de ofertas
- [ ] Imágenes cargan
- [ ] Textos se muestran
- [ ] Botones funcionan

**Verificar Vendors:**
- [ ] Carrusel de logos funciona
- [ ] Logos se muestran
- [ ] Auto-scroll funciona

**Verificar Footer:**
- [ ] Sección "Acerca de" se muestra
- [ ] Sección "Enlaces Rápidos" se muestra
- [ ] Sección "Contacto" se muestra
- [ ] Iconos de contacto se renderizan
- [ ] Copyright muestra nombre de la tienda

## Pruebas de Funcionalidad

### 14. Crear Nuevo Contenido
**Probar con Redes Sociales:**
- [ ] Ir a Redes Sociales → Agregar
- [ ] Llenar formulario:
  - Nombre: TikTok
  - Icono: fab fa-tiktok
  - URL: https://tiktok.com/@mitienda
  - Orden: 5
  - Activo: ✓
- [ ] Guardar
- [ ] Verificar que aparece en la lista
- [ ] Verificar que aparece en el sitio público

### 15. Editar Contenido
**Probar con Carousel:**
- [ ] Ir a Carousel → Editar primer slide
- [ ] Cambiar título a "Nueva Colección 2024"
- [ ] Guardar
- [ ] Verificar cambio en el sitio público

### 16. Desactivar Contenido
**Probar con Características:**
- [ ] Ir a Características → Editar "Envío Gratis"
- [ ] Desmarcar "Activo"
- [ ] Guardar
- [ ] Verificar que NO aparece en el sitio público
- [ ] Verificar que SÍ aparece en la lista del admin (como inactivo)

### 17. Eliminar Contenido
**Probar con Vendors:**
- [ ] Ir a Vendors → Eliminar último logo
- [ ] Confirmar eliminación
- [ ] Verificar que desaparece de la lista
- [ ] Verificar que desaparece del sitio público

### 18. Ordenar Contenido
**Probar con Enlaces Topbar:**
- [ ] Editar "FAQs" → cambiar orden a 30
- [ ] Editar "Ayuda" → cambiar orden a 10
- [ ] Editar "Soporte" → cambiar orden a 20
- [ ] Verificar que el orden en el sitio es: Ayuda, Soporte, FAQs

## Pruebas de Validación

### 19. Campos Requeridos
- [ ] Intentar crear red social sin nombre → debe mostrar error
- [ ] Intentar crear slide sin título → debe mostrar error
- [ ] Intentar crear característica sin icono → debe mostrar error

### 20. URLs
- [ ] Probar URL relativa: `img/test.jpg`
- [ ] Probar URL absoluta: `https://ejemplo.com/imagen.jpg`
- [ ] Ambas deben funcionar

### 21. HTML en Footer
- [ ] Editar sección de contacto
- [ ] Agregar HTML: `<p><strong>Nuevo</strong> texto</p>`
- [ ] Verificar que se renderiza correctamente en el sitio

## Pruebas de Integración

### 22. Configuración General
**URL:** http://localhost:5000/admin/settings

**Verificar:**
- [ ] Cambiar nombre de tienda a "Mi Tienda"
- [ ] Cambiar iniciales a "MT"
- [ ] Cambiar color primario
- [ ] Guardar
- [ ] Verificar cambios en topbar del sitio
- [ ] Verificar cambios en footer del sitio

### 23. Productos y Categorías
**Verificar que el CMS no afecta funcionalidad existente:**
- [ ] Crear categoría funciona
- [ ] Crear producto funciona
- [ ] Productos se muestran en el home
- [ ] Categorías se muestran en el menú

### 24. Carrito y Checkout
**Verificar que el CMS no afecta funcionalidad existente:**
- [ ] Agregar producto al carrito funciona
- [ ] Ver carrito funciona
- [ ] Checkout funciona

## Pruebas de Rendimiento

### 25. Carga de Página
- [ ] Home carga en menos de 2 segundos
- [ ] Admin carga en menos de 1 segundo
- [ ] No hay errores en consola del navegador

### 26. Imágenes
- [ ] Todas las imágenes cargan correctamente
- [ ] No hay imágenes rotas (404)

## Pruebas de Seguridad

### 27. Autenticación
- [ ] Intentar acceder a `/admin/content` sin login → redirecciona a login
- [ ] Intentar acceder a `/admin/products` sin login → redirecciona a login
- [ ] Logout funciona correctamente

### 28. Validación de Datos
- [ ] No se puede inyectar HTML malicioso en campos de texto
- [ ] URLs se validan correctamente

## Documentación

### 29. Archivos de Documentación
- [ ] `CMS_USAGE.md` existe y es completo
- [ ] `INSTRUCCIONES_RAPIDAS.md` existe
- [ ] `DATABASE_SCHEMA.md` existe
- [ ] `RESUMEN_IMPLEMENTACION.md` existe
- [ ] `SHOPONLINE_PLAN.md` actualizado

### 30. Código
- [ ] Código está comentado donde es necesario
- [ ] No hay código duplicado
- [ ] Nombres de variables son descriptivos
- [ ] Estructura de archivos es clara

## Resultado Final

**Total de checks:** 150+

**Criterio de éxito:** 
- ✅ Todos los checks básicos (1-12) deben pasar
- ✅ Al menos 90% de checks de funcionalidad (13-24) deben pasar
- ✅ Al menos 80% de checks de integración (25-30) deben pasar

---

## 🎉 Si todos los checks pasan:

**¡El sistema CMS está completamente funcional y listo para producción!**

---

## 🐛 Si algún check falla:

1. Revisar logs del servidor
2. Verificar que la base de datos tiene datos
3. Limpiar caché del navegador
4. Reiniciar el servidor
5. Consultar documentación específica

---

**Fecha de verificación:** _____________

**Verificado por:** _____________

**Resultado:** ⬜ APROBADO  ⬜ REQUIERE AJUSTES

**Notas:**
_____________________________________________
_____________________________________________
_____________________________________________
