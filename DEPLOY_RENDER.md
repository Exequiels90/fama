# 🚀 Desplegar en Render (Más Fácil que Fly.io)

## ¿Por qué Render?
- ✅ No requiere CLI (todo desde el navegador)
- ✅ Conecta directo con GitHub
- ✅ Plan gratuito generoso
- ✅ Configuración super simple

---

## 📋 Pasos para Desplegar

### 1. Subir a GitHub

```bash
# Inicializar git (si no lo hiciste)
git init
git add .
git commit -m "Tienda FaMa lista para desplegar"

# Crear repo en GitHub y subir
git remote add origin https://github.com/TU_USUARIO/fama-shop.git
git branch -M main
git push -u origin main
```

### 2. Crear Cuenta en Render
1. Ve a https://render.com
2. Regístrate con GitHub (más fácil)
3. Autoriza Render a acceder a tus repos

### 3. Crear Web Service
1. Click en "New +" → "Web Service"
2. Conecta tu repositorio `fama-shop`
3. Configurar:

**Name:** `fama-shop` (o el que quieras)

**Environment:** `Python 3`

**Build Command:**
```bash
pip install -r backend/requirements.txt
```

**Start Command:**
```bash
gunicorn -w 4 -b 0.0.0.0:$PORT --chdir backend app:app
```

**Plan:** `Free`

### 4. Variables de Entorno
En la sección "Environment":

```
SECRET_KEY = tu-clave-secreta-muy-larga-y-segura-123456789
FLASK_ENV = production
```

### 5. Deploy!
Click en "Create Web Service"

Render automáticamente:
- Clona tu repo
- Instala dependencias
- Inicia el servidor
- Te da una URL: `https://fama-shop.onrender.com`

---

## ⏱️ Tiempo de Despliegue
- Primera vez: 5-10 minutos
- Siguientes: 2-3 minutos

---

## 🔄 Actualizar el Sitio

Cada vez que hagas `git push`, Render redespliega automáticamente:

```bash
git add .
git commit -m "Actualización"
git push
```

---

## 🗄️ Base de Datos

### Opción 1: SQLite (Actual)
- Funciona out-of-the-box
- **Nota:** Se pierde al redesplegar

### Opción 2: PostgreSQL Gratis en Render
1. En Render: New + → PostgreSQL
2. Plan: Free
3. Copiar "Internal Database URL"
4. En tu Web Service → Environment:
   ```
   DATABASE_URL = postgresql://...
   ```
5. Actualizar `requirements.txt`:
   ```
   psycopg2-binary==2.9.9
   ```
6. Commit y push

### Opción 3: Neon (Recomendado)
1. Crear cuenta en https://neon.tech
2. Crear proyecto
3. Copiar connection string
4. Agregar a Environment en Render:
   ```
   DATABASE_URL = postgresql://...
   ```

---

## 🔒 Post-Despliegue

### 1. Cambiar Contraseña de Admin
Desde Render Shell (en el dashboard):
```python
from backend.app import create_app
from backend.models import db, AdminUser

app = create_app()
with app.app_context():
    admin = AdminUser.query.filter_by(username='admin').first()
    admin.set_password('TuNuevaContraseñaSegura!')
    db.session.commit()
```

### 2. Cargar Contenido
1. Accede a tu sitio: `https://tu-app.onrender.com/admin/login`
2. Login con la nueva contraseña
3. Carga tu contenido desde el admin

---

## 💰 Costos

**Plan Gratuito incluye:**
- 750 horas/mes (suficiente para 1 sitio)
- Se duerme después de 15 min sin uso
- Despierta automáticamente al visitarlo (tarda ~30 seg)

**Plan Paid ($7/mes):**
- Siempre activo
- Más rápido
- Sin límite de horas

---

## 🐛 Troubleshooting

### "Build failed"
Verifica que `requirements.txt` esté en `backend/`

### "Application failed to start"
Revisa los logs en Render Dashboard

### "Database not found"
Inicializa la BD desde Render Shell

---

## 📊 Ventajas vs Fly.io

| Feature | Render | Fly.io |
|---------|--------|--------|
| Setup | ✅ Navegador | ❌ CLI |
| GitHub | ✅ Auto-deploy | ⚠️ Manual |
| Free Tier | ✅ 750h/mes | ✅ 3 VMs |
| Facilidad | ✅✅✅ | ⚠️⚠️ |

---

## 🎯 Resumen

1. Sube a GitHub
2. Conecta con Render
3. Configura variables
4. Deploy automático
5. ¡Listo!

**Tiempo total: 10-15 minutos** ⏱️

---

¿Prefieres Render? Es mucho más simple que Fly.io 😊
