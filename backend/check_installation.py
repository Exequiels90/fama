"""
Script para verificar que la instalación esté completa y correcta.
Ejecutar: python backend/check_installation.py
"""

import os
import sys


def check_file(path, description):
    """Verifica que un archivo exista."""
    if os.path.exists(path):
        print(f"✓ {description}")
        return True
    else:
        print(f"✗ {description} - FALTA: {path}")
        return False


def check_database():
    """Verifica que la base de datos tenga las tablas necesarias."""
    try:
        from app import create_app
        from models import (
            db, Product, Category, Order, AdminUser, Setting,
            SocialLink, TopbarLink, CarouselSlide, FeatureBox,
            OfferBanner, FooterSection, VendorLogo
        )
        
        app = create_app()
        with app.app_context():
            # Verificar que las tablas existan
            tables = [
                ('products', Product),
                ('categories', Category),
                ('orders', Order),
                ('admin_users', AdminUser),
                ('settings', Setting),
                ('social_links', SocialLink),
                ('topbar_links', TopbarLink),
                ('carousel_slides', CarouselSlide),
                ('feature_boxes', FeatureBox),
                ('offer_banners', OfferBanner),
                ('footer_sections', FooterSection),
                ('vendor_logos', VendorLogo),
            ]
            
            all_ok = True
            for table_name, model in tables:
                try:
                    count = model.query.count()
                    print(f"✓ Tabla '{table_name}' existe ({count} registros)")
                except Exception as e:
                    print(f"✗ Tabla '{table_name}' tiene problemas: {e}")
                    all_ok = False
            
            return all_ok
    except Exception as e:
        print(f"✗ Error al verificar base de datos: {e}")
        return False


def check_admin_user():
    """Verifica que exista el usuario admin."""
    try:
        from app import create_app
        from models import AdminUser
        
        app = create_app()
        with app.app_context():
            admin = AdminUser.query.filter_by(username='admin').first()
            if admin:
                print("✓ Usuario admin existe")
                return True
            else:
                print("✗ Usuario admin NO existe")
                return False
    except Exception as e:
        print(f"✗ Error al verificar usuario admin: {e}")
        return False


def check_content():
    """Verifica que exista contenido de ejemplo."""
    try:
        from app import create_app
        from models import SocialLink, CarouselSlide, FeatureBox
        
        app = create_app()
        with app.app_context():
            social_count = SocialLink.query.count()
            carousel_count = CarouselSlide.query.count()
            feature_count = FeatureBox.query.count()
            
            if social_count > 0 and carousel_count > 0 and feature_count > 0:
                print(f"✓ Contenido de ejemplo existe")
                print(f"  - {social_count} redes sociales")
                print(f"  - {carousel_count} slides")
                print(f"  - {feature_count} características")
                return True
            else:
                print("✗ Falta contenido de ejemplo")
                print("  Ejecuta: python backend/init_content.py")
                return False
    except Exception as e:
        print(f"✗ Error al verificar contenido: {e}")
        return False


def main():
    print("=" * 60)
    print("VERIFICACIÓN DE INSTALACIÓN - FaMa Shop CMS")
    print("=" * 60)
    print()
    
    all_checks = []
    
    # Verificar archivos principales
    print("📁 Verificando archivos principales...")
    all_checks.append(check_file("backend/app.py", "app.py"))
    all_checks.append(check_file("backend/models.py", "models.py"))
    all_checks.append(check_file("backend/config.py", "config.py"))
    all_checks.append(check_file("backend/init_content.py", "init_content.py"))
    all_checks.append(check_file("backend/requirements.txt", "requirements.txt"))
    print()
    
    # Verificar templates del admin
    print("📄 Verificando templates del admin...")
    templates = [
        "admin_content.html",
        "admin_social_links.html",
        "admin_topbar_links.html",
        "admin_carousel.html",
        "admin_features.html",
        "admin_offers.html",
        "admin_vendors.html",
        "admin_footer.html",
    ]
    for template in templates:
        all_checks.append(check_file(f"bootstrap-shop-template/{template}", template))
    print()
    
    # Verificar documentación
    print("📚 Verificando documentación...")
    docs = [
        ("CMS_USAGE.md", "Guía de uso"),
        ("INSTRUCCIONES_RAPIDAS.md", "Instrucciones rápidas"),
        ("DATABASE_SCHEMA.md", "Esquema de BD"),
        ("RESUMEN_IMPLEMENTACION.md", "Resumen técnico"),
    ]
    for doc_file, doc_name in docs:
        all_checks.append(check_file(doc_file, doc_name))
    print()
    
    # Verificar base de datos
    print("🗄️ Verificando base de datos...")
    all_checks.append(check_database())
    print()
    
    # Verificar usuario admin
    print("👤 Verificando usuario admin...")
    all_checks.append(check_admin_user())
    print()
    
    # Verificar contenido
    print("🎨 Verificando contenido de ejemplo...")
    all_checks.append(check_content())
    print()
    
    # Resumen
    print("=" * 60)
    passed = sum(all_checks)
    total = len(all_checks)
    percentage = (passed / total) * 100 if total > 0 else 0
    
    print(f"RESULTADO: {passed}/{total} checks pasaron ({percentage:.1f}%)")
    print("=" * 60)
    print()
    
    if percentage == 100:
        print("✅ ¡INSTALACIÓN COMPLETA Y CORRECTA!")
        print()
        print("Próximos pasos:")
        print("1. Ejecutar: python backend/app.py")
        print("2. Abrir: http://localhost:5000")
        print("3. Admin: http://localhost:5000/admin/login")
        print("   Usuario: admin")
        print("   Contraseña: admin123")
    elif percentage >= 80:
        print("⚠️ INSTALACIÓN CASI COMPLETA")
        print("Algunos elementos opcionales faltan, pero el sistema debería funcionar.")
    else:
        print("❌ INSTALACIÓN INCOMPLETA")
        print("Faltan elementos importantes. Revisa los errores arriba.")
        print()
        print("Soluciones comunes:")
        print("- Ejecutar: python backend/init_content.py")
        print("- Verificar que todos los archivos estén presentes")
        print("- Reinstalar dependencias: pip install -r backend/requirements.txt")
    
    print()
    return 0 if percentage == 100 else 1


if __name__ == "__main__":
    sys.exit(main())
