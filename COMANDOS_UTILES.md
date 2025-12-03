# 🛠️ Comandos Útiles - FaMa Shop CMS

## 🚀 Comandos Básicos

### Iniciar el Servidor
```bash
python backend/app.py
```

### Verificar Instalación
```bash
python backend/check_installation.py
```

### Inicializar Contenido de Ejemplo
```bash
python backend/init_content.py
```

---

## 🗄️ Base de Datos

### Backup de la Base de Datos
```bash
# Windows
copy backend\shop.db backend\shop_backup_%date:~-4,4%%date:~-10,2%%date:~-7,2%.db

# Linux/Mac
cp backend/shop.db backend/shop_backup_$(date +%Y%m%d).db
```

### Restaurar Backup
```bash
# Windows
copy backend\shop_backup.db backend\shop.db

# Linux/Mac
cp backend/shop_backup.db backend/shop.db
```

### Resetear Base de Datos (¡CUIDADO!)
```bash
# Windows
del backend\shop.db
python backend/app.py

# Linux/Mac
rm backend/shop.db
python backend/app.py
```

### Ver Contenido de la Base de Datos
```bash
# Instalar sqlite3 si no lo tienes
sqlite3 backend/shop.db

# Dentro de sqlite3:
.tables                    # Ver todas las tablas
.schema social_links       # Ver estructura de una tabla
SELECT * FROM social_links; # Ver datos de una tabla
.quit                      # Salir
```

---

## 📦 Dependencias

### Instalar Dependencias
```bash
pip install -r backend/requirements.txt
```

### Actualizar Dependencias
```bash
pip install --upgrade -r backend/requirements.txt
```

### Ver Dependencias Instaladas
```bash
pip list
```

### Crear requirements.txt Actualizado
```bash
pip freeze > backend/requirements.txt
```

---

## 🧪 Testing

### Verificar Sintaxis Python
```bash
python -m py_compile backend/app.py
python -m py_compile backend/models.py
```

### Ejecutar Checklist Completo
```bash
python backend/check_installation.py
```

### Probar Conexión a Base de Datos
```bash
python -c "from backend.app import create_app; from backend.models import db; app = create_app(); app.app_context().push(); print('Conexión OK')"
```

---

## 🔍 Debugging

### Ver Logs del Servidor
El servidor muestra logs en la consola donde se ejecuta.

### Modo Debug
Ya está activado por defecto en `backend/app.py`:
```python
if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
```

### Ver Variables de Entorno
```bash
# Windows
set

# Linux/Mac
env
```

---

## 📊 Consultas Útiles

### Contar Registros
```python
# En Python shell
from backend.app import create_app
from backend.models import *

app = create_app()
with app.app_context():
    print(f"Productos: {Product.query.count()}")
    print(f"Categorías: {Category.query.count()}")
    print(f"Redes Sociales: {SocialLink.query.count()}")
    print(f"Slides: {CarouselSlide.query.count()}")
```

### Ver Todos los Elementos Activos
```python
from backend.app import create_app
from backend.models import SocialLink

app = create_app()
with app.app_context():
    links = SocialLink.query.filter_by(is_active=True).order_by(SocialLink.order).all()
    for link in links:
        print(f"{link.order}. {link.name} - {link.url}")
```

---

## 🎨 Gestión de Contenido

### Exportar Contenido a JSON
```python
import json
from backend.app import create_app
from backend.models import SocialLink

app = create_app()
with app.app_context():
    links = SocialLink.query.all()
    data = [{"name": l.name, "icon": l.icon, "url": l.url} for l in links]
    with open("social_links_backup.json", "w") as f:
        json.dump(data, f, indent=2)
```

### Importar Contenido desde JSON
```python
import json
from backend.app import create_app
from backend.models import db, SocialLink

app = create_app()
with app.app_context():
    with open("social_links_backup.json", "r") as f:
        data = json.load(f)
    
    for item in data:
        link = SocialLink(**item)
        db.session.add(link)
    
    db.session.commit()
```

---

## 🔐 Seguridad

### Cambiar Contraseña de Admin
```python
from backend.app import create_app
from backend.models import db, AdminUser

app = create_app()
with app.app_context():
    admin = AdminUser.query.filter_by(username='admin').first()
    admin.set_password('nueva_contraseña_segura')
    db.session.commit()
    print("Contraseña actualizada")
```

### Crear Nuevo Usuario Admin
```python
from backend.app import create_app
from backend.models import db, AdminUser

app = create_app()
with app.app_context():
    nuevo_admin = AdminUser(username='nuevo_usuario')
    nuevo_admin.set_password('contraseña_segura')
    db.session.add(nuevo_admin)
    db.session.commit()
    print("Usuario creado")
```

---

## 🌐 Producción

### Ejecutar con Gunicorn (Linux/Mac)
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 backend.app:app
```

### Ejecutar con Waitress (Windows)
```bash
pip install waitress
waitress-serve --port=5000 backend.app:app
```

### Variables de Entorno para Producción
```bash
# Windows
set FLASK_ENV=production
set SECRET_KEY=tu_clave_secreta_muy_larga_y_segura

# Linux/Mac
export FLASK_ENV=production
export SECRET_KEY=tu_clave_secreta_muy_larga_y_segura
```

---

## 📁 Gestión de Archivos

### Limpiar Archivos Temporales
```bash
# Windows
del /s /q __pycache__
del /s /q *.pyc

# Linux/Mac
find . -type d -name __pycache__ -exec rm -rf {} +
find . -type f -name "*.pyc" -delete
```

### Ver Tamaño de la Base de Datos
```bash
# Windows
dir backend\shop.db

# Linux/Mac
ls -lh backend/shop.db
```

---

## 🔄 Git (Control de Versiones)

### Inicializar Repositorio
```bash
git init
git add .
git commit -m "Initial commit - CMS completo"
```

### Crear .gitignore
```bash
echo "__pycache__/" > .gitignore
echo "*.pyc" >> .gitignore
echo "*.db" >> .gitignore
echo ".env" >> .gitignore
```

### Guardar Cambios
```bash
git add .
git commit -m "Descripción de los cambios"
```

---

## 📊 Monitoreo

### Ver Uso de Memoria
```bash
# Windows
tasklist | findstr python

# Linux/Mac
ps aux | grep python
```

### Ver Puerto en Uso
```bash
# Windows
netstat -ano | findstr :5000

# Linux/Mac
lsof -i :5000
```

---

## 🆘 Solución Rápida de Problemas

### El servidor no inicia
```bash
# 1. Verificar dependencias
pip install -r backend/requirements.txt

# 2. Verificar puerto
netstat -ano | findstr :5000

# 3. Reiniciar
python backend/app.py
```

### Error de base de datos
```bash
# 1. Backup actual
copy backend\shop.db backend\shop_backup.db

# 2. Resetear
del backend\shop.db

# 3. Reinicializar
python backend/app.py
python backend/init_content.py
```

### No veo cambios en el sitio
```bash
# 1. Limpiar caché del navegador (Ctrl+F5)
# 2. Verificar que el elemento esté activo en el admin
# 3. Reiniciar el servidor
```

---

## 📚 Recursos Adicionales

### Documentación
- `CMS_USAGE.md` - Guía completa
- `INSTRUCCIONES_RAPIDAS.md` - Inicio rápido
- `DATABASE_SCHEMA.md` - Esquema de BD

### URLs Importantes
- Sitio: http://localhost:5000
- Admin: http://localhost:5000/admin/login
- Contenido: http://localhost:5000/admin/content

### Credenciales por Defecto
- Usuario: `admin`
- Contraseña: `admin123`

---

## 💡 Tips

### Desarrollo Rápido
```bash
# Terminal 1: Servidor
python backend/app.py

# Terminal 2: Comandos
python backend/check_installation.py
```

### Backup Automático
Crear un script `backup.bat` (Windows) o `backup.sh` (Linux/Mac):
```bash
@echo off
set fecha=%date:~-4,4%%date:~-10,2%%date:~-7,2%
copy backend\shop.db backups\shop_%fecha%.db
echo Backup creado: shop_%fecha%.db
```

### Alias Útiles (Linux/Mac)
Agregar a `.bashrc` o `.zshrc`:
```bash
alias shop-start="python backend/app.py"
alias shop-check="python backend/check_installation.py"
alias shop-init="python backend/init_content.py"
alias shop-backup="cp backend/shop.db backend/shop_backup_$(date +%Y%m%d).db"
```

---

¡Guarda este archivo para referencia rápida! 📌
