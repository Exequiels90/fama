# 🚀 Desplegar en Fly.io

## 📋 Pre-requisitos

1. Cuenta en Fly.io (gratis): https://fly.io/
2. Instalar flyctl:
   ```bash
   # Windows (PowerShell)
   iwr https://fly.io/install.ps1 -useb | iex
   ```

3. Login:
   ```bash
   flyctl auth login
   ```

---

## 📁 Archivos Necesarios

### 1. Crear `Procfile`
```bash
web: gunicorn -w 4 -b 0.0.0.0:$PORT backend.app:app
```

### 2. Crear `runtime.txt`
```
python-3.11
```

### 3. Actualizar `requirements.txt`
Agregar:
```
gunicorn==21.2.0
```

### 4. Crear `fly.toml`
```toml
app = "fama-shop"  # Cambiar por tu nombre único

[build]
  builder = "paketobuildpacks/builder:base"

[env]
  PORT = "8080"
  FLASK_ENV = "production"

[[services]]
  internal_port = 8080
  protocol = "tcp"

  [[services.ports]]
    handlers = ["http"]
    port = 80

  [[services.ports]]
    handlers = ["tls", "http"]
    port = 443

[[services.http_checks]]
  interval = 10000
  grace_period = "5s"
  method = "get"
  path = "/"
  protocol = "http"
  timeout = 2000
```

---

## 🔧 Preparar el Proyecto

### 1. Actualizar `backend/config.py`
```python
import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///shop.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevConfig(Config):
    DEBUG = True

class ProdConfig(Config):
    DEBUG = False
```

### 2. Actualizar `backend/app.py`
Cambiar:
```python
def create_app(config_object=DevConfig) -> Flask:
```

Por:
```python
def create_app(config_object=None) -> Flask:
    if config_object is None:
        if os.environ.get('FLASK_ENV') == 'production':
            config_object = ProdConfig
        else:
            config_object = DevConfig
```

---

## 🚀 Desplegar

### 1. Inicializar Fly.io
```bash
flyctl launch
```

Responder:
- App name: `fama-shop` (o el que quieras)
- Region: `gru` (São Paulo - más cercano a Argentina)
- PostgreSQL: `No` (usaremos SQLite por ahora)
- Redis: `No`

### 2. Configurar Variables de Entorno
```bash
flyctl secrets set SECRET_KEY="tu-clave-secreta-muy-larga-y-segura"
```

### 3. Desplegar
```bash
flyctl deploy
```

### 4. Abrir la App
```bash
flyctl open
```

---

## 📊 Comandos Útiles

### Ver Logs
```bash
flyctl logs
```

### Ver Estado
```bash
flyctl status
```

### SSH a la App
```bash
flyctl ssh console
```

### Escalar (si necesitas más recursos)
```bash
flyctl scale vm shared-cpu-1x --memory 512
```

---

## 🗄️ Base de Datos

### Opción 1: SQLite (Actual)
**Pros:**
- Simple
- Sin configuración
- Gratis

**Contras:**
- Se pierde al redesplegar
- No escalable

### Opción 2: PostgreSQL en Fly.io
```bash
flyctl postgres create
flyctl postgres attach <postgres-app-name>
```

Luego actualizar `requirements.txt`:
```
psycopg2-binary==2.9.9
```

Y `config.py`:
```python
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
```

### Opción 3: Neon (PostgreSQL Gratis)
1. Crear cuenta en https://neon.tech
2. Crear base de datos
3. Copiar connection string
4. Configurar:
```bash
flyctl secrets set DATABASE_URL="postgresql://..."
```

---

## 🔒 Seguridad

### 1. Cambiar Contraseña de Admin
Después del primer despliegue:
```bash
flyctl ssh console
python
>>> from backend.app import create_app
>>> from backend.models import db, AdminUser
>>> app = create_app()
>>> with app.app_context():
...     admin = AdminUser.query.filter_by(username='admin').first()
...     admin.set_password('nueva-contraseña-segura')
...     db.session.commit()
```

### 2. Configurar HTTPS
Fly.io lo hace automáticamente ✅

---

## 📝 Checklist Pre-Despliegue

- [ ] `requirements.txt` actualizado con gunicorn
- [ ] `Procfile` creado
- [ ] `fly.toml` creado
- [ ] Variables de entorno configuradas
- [ ] Base de datos inicializada
- [ ] Contenido de ejemplo cargado
- [ ] Contraseña de admin cambiada

---

## 🐛 Troubleshooting

### Error: "No module named 'config'"
Asegúrate de que el `Procfile` use:
```
web: gunicorn -w 4 -b 0.0.0.0:$PORT --chdir backend app:app
```

### Error: "Database not found"
Inicializar la BD:
```bash
flyctl ssh console
cd backend
python
>>> from app import create_app
>>> app = create_app()
>>> with app.app_context():
...     from models import db
...     db.create_all()
```

### Error: "Port already in use"
Fly.io maneja esto automáticamente, no te preocupes.

---

## 💰 Costos

**Plan Gratuito de Fly.io incluye:**
- 3 VMs compartidas
- 160GB de tráfico
- Suficiente para desarrollo y pruebas

**Si necesitas más:**
- ~$5/mes por VM adicional
- PostgreSQL: ~$2/mes

---

## 🎯 Después del Despliegue

1. Probar todas las funcionalidades
2. Cargar contenido real desde el admin
3. Configurar dominio personalizado (opcional)
4. Integrar Mercado Pago
5. Configurar backups de BD

---

## 📞 Soporte

- Docs de Fly.io: https://fly.io/docs/
- Community: https://community.fly.io/
- Status: https://status.fly.io/

---

¡Listo para desplegar! 🚀
