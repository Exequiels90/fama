"""
Script para inicializar contenido de ejemplo en la base de datos.
Ejecutar: python backend/init_content.py
"""

from app import create_app
from models import (
    db, SocialLink, TopbarLink, CarouselSlide, FeatureBox,
    OfferBanner, FooterSection, FooterLink, VendorLogo, NewsItem
)


def init_sample_content():
    app = create_app()
    with app.app_context():
        print("Inicializando contenido de ejemplo...")

        # Redes Sociales
        if not SocialLink.query.first():
            social_links = [
                SocialLink(name="Facebook", icon="fab fa-facebook-f", url="https://facebook.com", order=1, is_active=True),
                SocialLink(name="Twitter", icon="fab fa-twitter", url="https://twitter.com", order=2, is_active=True),
                SocialLink(name="Instagram", icon="fab fa-instagram", url="https://instagram.com", order=3, is_active=True),
                SocialLink(name="LinkedIn", icon="fab fa-linkedin-in", url="https://linkedin.com", order=4, is_active=True),
            ]
            db.session.add_all(social_links)
            print("✓ Redes sociales creadas")

        # Enlaces Topbar
        if not TopbarLink.query.first():
            topbar_links = [
                TopbarLink(text="FAQs", url="/faqs", order=1, is_active=True),
                TopbarLink(text="Ayuda", url="/help", order=2, is_active=True),
                TopbarLink(text="Soporte", url="/support", order=3, is_active=True),
            ]
            db.session.add_all(topbar_links)
            print("✓ Enlaces topbar creados")

        # Carousel
        if not CarouselSlide.query.first():
            slides = [
                CarouselSlide(
                    title="Colección Primavera",
                    subtitle="10% de descuento en tu primera compra",
                    button_text="Comprar Ahora",
                    button_url="/shop",
                    image_url="img/carousel-1.jpg",
                    order=1,
                    is_active=True
                ),
                CarouselSlide(
                    title="Precios Razonables",
                    subtitle="Calidad garantizada",
                    button_text="Ver Productos",
                    button_url="/shop",
                    image_url="img/carousel-2.jpg",
                    order=2,
                    is_active=True
                ),
            ]
            db.session.add_all(slides)
            print("✓ Slides del carousel creados")

        # Características
        if not FeatureBox.query.first():
            features = [
                FeatureBox(icon="fa fa-check", title="Productos de Calidad", order=1, is_active=True),
                FeatureBox(icon="fa fa-shipping-fast", title="Envío Gratis", order=2, is_active=True),
                FeatureBox(icon="fas fa-exchange-alt", title="Devolución 14 Días", order=3, is_active=True),
                FeatureBox(icon="fa fa-phone-volume", title="Soporte 24/7", order=4, is_active=True),
            ]
            db.session.add_all(features)
            print("✓ Características creadas")

        # Banners de Ofertas
        if not OfferBanner.query.first():
            offers = [
                OfferBanner(
                    title="Colección Primavera",
                    subtitle="20% de descuento en toda la orden",
                    button_text="Comprar Ahora",
                    button_url="/shop",
                    image_url="img/offer-1.png",
                    background_color="#6C757D",
                    text_align="right",
                    order=1,
                    is_active=True
                ),
                OfferBanner(
                    title="Colección Invierno",
                    subtitle="20% de descuento en toda la orden",
                    button_text="Comprar Ahora",
                    button_url="/shop",
                    image_url="img/offer-2.png",
                    background_color="#6C757D",
                    text_align="left",
                    order=2,
                    is_active=True
                ),
            ]
            db.session.add_all(offers)
            print("✓ Banners de ofertas creados")

        # Vendors
        if not VendorLogo.query.first():
            vendors = [
                VendorLogo(name="Vendor 1", image_url="img/vendor-1.jpg", order=1, is_active=True),
                VendorLogo(name="Vendor 2", image_url="img/vendor-2.jpg", order=2, is_active=True),
                VendorLogo(name="Vendor 3", image_url="img/vendor-3.jpg", order=3, is_active=True),
                VendorLogo(name="Vendor 4", image_url="img/vendor-4.jpg", order=4, is_active=True),
                VendorLogo(name="Vendor 5", image_url="img/vendor-5.jpg", order=5, is_active=True),
                VendorLogo(name="Vendor 6", image_url="img/vendor-6.jpg", order=6, is_active=True),
            ]
            db.session.add_all(vendors)
            print("✓ Logos de marcas creados")

        # Footer - Acerca de
        if not FooterSection.query.filter_by(section_type='about').first():
            about = FooterSection(
                section_type='about',
                title='Acerca de FaMa',
                content='<p>Tu tienda online de confianza. Ofrecemos productos de calidad con los mejores precios del mercado.</p>',
                order=1,
                is_active=True
            )
            db.session.add(about)
            print("✓ Sección 'Acerca de' creada")

        # Footer - Contacto
        if not FooterSection.query.filter_by(section_type='contact').first():
            contact = FooterSection(
                section_type='contact',
                title='Contacto',
                content='''<p class="mb-2"><i class="fa fa-map-marker-alt text-primary mr-3"></i>Calle Principal 123, Buenos Aires</p>
<p class="mb-2"><i class="fa fa-envelope text-primary mr-3"></i>info@fama.com</p>
<p class="mb-0"><i class="fa fa-phone-alt text-primary mr-3"></i>+54 11 1234-5678</p>''',
                order=3,
                is_active=True
            )
            db.session.add(contact)
            print("✓ Sección 'Contacto' creada")

        # Footer - Enlaces
        if not FooterSection.query.filter_by(section_type='links').first():
            links_section = FooterSection(
                section_type='links',
                title='Enlaces Rápidos',
                order=2,
                is_active=True
            )
            db.session.add(links_section)
            db.session.flush()

            footer_links = [
                FooterLink(section_id=links_section.id, text="Inicio", url="/", icon="fa fa-angle-right", order=1, is_active=True),
                FooterLink(section_id=links_section.id, text="Tienda", url="/shop", icon="fa fa-angle-right", order=2, is_active=True),
                FooterLink(section_id=links_section.id, text="Carrito", url="/cart", icon="fa fa-angle-right", order=3, is_active=True),
                FooterLink(section_id=links_section.id, text="Checkout", url="/checkout", icon="fa fa-angle-right", order=4, is_active=True),
            ]
            db.session.add_all(footer_links)
            print("✓ Sección 'Enlaces' creada")

        # Novedades
        if not NewsItem.query.first():
            news = [
                NewsItem(
                    title="Nueva Colección Primavera 2024",
                    description="Descubre nuestra nueva colección con los mejores diseños de la temporada.",
                    image_url="img/product-1.jpg",
                    link_url="/shop",
                    link_text="Ver Colección",
                    order=1,
                    is_active=True
                ),
                NewsItem(
                    title="Envío Gratis en Compras Mayores a $5000",
                    description="Aprovecha nuestro envío gratis en todas las compras superiores a $5000.",
                    image_url="img/product-2.jpg",
                    link_url="/shop",
                    link_text="Comprar Ahora",
                    order=2,
                    is_active=True
                ),
                NewsItem(
                    title="Descuentos Especiales para Clientes VIP",
                    description="Regístrate y obtén descuentos exclusivos en todos nuestros productos.",
                    image_url="img/product-3.jpg",
                    link_url="/shop",
                    link_text="Más Información",
                    order=3,
                    is_active=True
                ),
            ]
            db.session.add_all(news)
            print("✓ Novedades creadas")

        db.session.commit()
        print("\n✅ Contenido de ejemplo inicializado correctamente!")
        print("Ahora puedes editar todo desde el panel admin en: /admin/content")


if __name__ == "__main__":
    init_sample_content()
