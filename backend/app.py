from decimal import Decimal
from datetime import datetime

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    session,
    flash,
)

from config import DevConfig, ProdConfig
from models import (
    db, Product, Category, Order, OrderItem, AdminUser, Setting,
    SocialLink, TopbarLink, CarouselSlide, FeatureBox, OfferBanner,
    FooterSection, FooterLink, VendorLogo, NewsItem, Customer
)


def create_app(config_object=None) -> Flask:
    # Seleccionar configuración según entorno
    if config_object is None:
        import os
        if os.environ.get('FLASK_ENV') == 'production':
            config_object = ProdConfig
        else:
            config_object = DevConfig
    # static_url_path="" permite servir /css, /js, /img directamente desde la carpeta del template
    app = Flask(
        __name__,
        template_folder="../bootstrap-shop-template",
        static_folder="../bootstrap-shop-template",
        static_url_path="",
    )
    app.config.from_object(config_object)

    db.init_app(app)

    with app.app_context():
        db.create_all()
        _ensure_default_admin()
        _ensure_default_settings()

    @app.context_processor
    def inject_settings():
        """Variables globales disponibles en todas las plantillas."""
        site_name = Setting.get("site_name", "FaMa")
        site_short_name = Setting.get("site_short_name", "FM")
        primary_color = Setting.get("primary_color", "#D19C97")
        secondary_color = Setting.get("secondary_color", "#EDF1FF")
        return dict(
            SITE_NAME=site_name,
            SITE_SHORT_NAME=site_short_name,
            PRIMARY_COLOR=primary_color,
            SECONDARY_COLOR=secondary_color,
        )

    register_public_routes(app)
    register_admin_routes(app)

    return app


def _ensure_default_admin() -> None:
    """Crea un usuario admin por defecto si no existe."""
    if not AdminUser.query.filter_by(username="admin").first():
        admin = AdminUser(username="admin")
        admin.set_password("admin123")
        db.session.add(admin)
        db.session.commit()


def _ensure_default_settings() -> None:
    """Crea valores de configuración por defecto si no existen."""
    defaults = {
        "site_name": "FaMa",
        "site_short_name": "FM",
        "primary_color": "#D19C97",
        "secondary_color": "#EDF1FF",
    }
    changed = False
    for key, value in defaults.items():
        if Setting.query.filter_by(key=key).first() is None:
            db.session.add(Setting(key=key, value=value))
            changed = True
    if changed:
        db.session.commit()


def get_cart():
    """Devuelve el carrito guardado en sesión."""
    return session.get("cart", {})


def save_cart(cart):
    session["cart"] = cart
    session.modified = True


def register_public_routes(app: Flask) -> None:
    @app.route("/")
    def index():
        categories = Category.query.all()
        products = Product.query.filter_by(is_active=True).order_by(Product.created_at.desc()).limit(16).all()
        
        # Cargar contenido editable
        social_links = SocialLink.query.filter_by(is_active=True).order_by(SocialLink.order).all()
        topbar_links = TopbarLink.query.filter_by(is_active=True).order_by(TopbarLink.order).all()
        carousel_slides = CarouselSlide.query.filter_by(is_active=True).order_by(CarouselSlide.order).all()
        feature_boxes = FeatureBox.query.filter_by(is_active=True).order_by(FeatureBox.order).all()
        offer_banners = OfferBanner.query.filter_by(is_active=True).order_by(OfferBanner.order).all()
        vendor_logos = VendorLogo.query.filter_by(is_active=True).order_by(VendorLogo.order).all()
        news_items = NewsItem.query.filter_by(is_active=True).order_by(NewsItem.order).limit(3).all()
        
        footer_about = FooterSection.query.filter_by(section_type='about', is_active=True).first()
        footer_contact = FooterSection.query.filter_by(section_type='contact', is_active=True).first()
        footer_links_sections = FooterSection.query.filter_by(section_type='links', is_active=True).order_by(FooterSection.order).all()
        
        return render_template(
            "index.html",
            categories=categories,
            products=products,
            social_links=social_links,
            topbar_links=topbar_links,
            carousel_slides=carousel_slides,
            feature_boxes=feature_boxes,
            offer_banners=offer_banners,
            vendor_logos=vendor_logos,
            news_items=news_items,
            footer_about=footer_about,
            footer_contact=footer_contact,
            footer_links_sections=footer_links_sections,
        )

    @app.route("/search")
    def search():
        query_text = request.args.get("q", "").strip()
        categories = Category.query.all()
        
        if not query_text:
            flash("Por favor ingresa un término de búsqueda.", "warning")
            return redirect(url_for("shop"))
        
        # Buscar en nombre y descripción
        products = Product.query.filter(
            Product.is_active == True,
            (Product.name.ilike(f"%{query_text}%") | Product.description.ilike(f"%{query_text}%"))
        ).order_by(Product.created_at.desc()).all()
        
        return render_template(
            "shop.html",
            products=products,
            categories=categories,
            selected_category=None,
            sort_by="recent",
            search_query=query_text,
        )

    @app.route("/shop")
    def shop():
        category_id = request.args.get("category", type=int)
        sort_by = request.args.get("sort", default="recent")
        
        query = Product.query.filter_by(is_active=True)
        selected_category = None

        if category_id:
            query = query.filter_by(category_id=category_id)
            selected_category = Category.query.get(category_id)

        # Ordenamiento
        if sort_by == "price_asc":
            query = query.order_by(Product.price_ars.asc())
        elif sort_by == "price_desc":
            query = query.order_by(Product.price_ars.desc())
        elif sort_by == "name":
            query = query.order_by(Product.name.asc())
        else:  # recent (por defecto)
            query = query.order_by(Product.created_at.desc())

        products = query.all()
        categories = Category.query.all()
        return render_template(
            "shop.html",
            products=products,
            categories=categories,
            selected_category=selected_category,
            sort_by=sort_by,
        )

    @app.route("/product/<int:product_id>")
    def product_detail(product_id: int):
        product = Product.query.get_or_404(product_id)
        return render_template("detail.html", product=product)

    @app.route("/cart")
    def cart_view():
        cart = get_cart()
        product_ids = [int(pid) for pid in cart.keys()]
        products = Product.query.filter(Product.id.in_(product_ids)).all() if product_ids else []

        items = []
        total = Decimal("0.00")
        for product in products:
            quantity = cart.get(str(product.id), 0)
            line_total = Decimal(product.price_ars) * quantity
            total += line_total
            items.append(
                {
                    "product": product,
                    "quantity": quantity,
                    "line_total": line_total,
                }
            )

        # Cargar datos para el template
        categories = Category.query.all()
        social_links = SocialLink.query.filter_by(is_active=True).order_by(SocialLink.order).all()
        topbar_links = TopbarLink.query.filter_by(is_active=True).order_by(TopbarLink.order).all()
        footer_about = FooterSection.query.filter_by(section_type='about', is_active=True).first()
        footer_contact = FooterSection.query.filter_by(section_type='contact', is_active=True).first()
        footer_links_sections = FooterSection.query.filter_by(section_type='links', is_active=True).order_by(FooterSection.order).all()

        return render_template(
            "cart.html",
            items=items,
            total=total,
            categories=categories,
            social_links=social_links,
            topbar_links=topbar_links,
            footer_about=footer_about,
            footer_contact=footer_contact,
            footer_links_sections=footer_links_sections,
        )

    @app.route("/cart/add/<int:product_id>", methods=["POST"])
    def cart_add(product_id: int):
        from flask import jsonify
        product = Product.query.get_or_404(product_id)
        cart = get_cart()
        cart[str(product.id)] = cart.get(str(product.id), 0) + 1
        save_cart(cart)
        
        # Si es una petición AJAX, devolver JSON
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest' or request.is_json:
            cart_count = sum(cart.values())
            return jsonify({
                "success": True,
                "message": f"Se agregó {product.name} al carrito",
                "cart_count": cart_count
            })
        
        flash(f"Se agregó {product.name} al carrito.", "success")
        return redirect(request.referrer or url_for("shop"))

    @app.route("/cart/remove/<int:product_id>", methods=["POST"])
    def cart_remove(product_id: int):
        cart = get_cart()
        cart.pop(str(product_id), None)
        save_cart(cart)
        flash("Producto eliminado del carrito.", "info")
        return redirect(url_for("cart_view"))

    @app.route("/cart/update/<int:product_id>", methods=["POST"])
    def cart_update(product_id: int):
        from flask import jsonify
        data = request.get_json()
        quantity = data.get("quantity", 1)
        
        if quantity < 1:
            return jsonify({"success": False, "error": "Cantidad inválida"}), 400
        
        cart = get_cart()
        cart[str(product_id)] = quantity
        save_cart(cart)
        
        # Calcular totales
        product = Product.query.get_or_404(product_id)
        line_total = float(product.price_ars) * quantity
        
        # Calcular total del carrito
        product_ids = [int(pid) for pid in cart.keys()]
        products = Product.query.filter(Product.id.in_(product_ids)).all()
        cart_total = sum(float(p.price_ars) * cart.get(str(p.id), 0) for p in products)
        cart_count = sum(cart.values())
        
        return jsonify({
            "success": True,
            "line_total": line_total,
            "cart_total": cart_total,
            "cart_count": cart_count
        })

    @app.route("/cart/clear", methods=["POST"])
    def cart_clear():
        save_cart({})
        flash("Carrito vaciado.", "info")
        return redirect(url_for("cart_view"))

    @app.route("/checkout", methods=["GET", "POST"])
    def checkout():
        cart = get_cart()
        if not cart:
            flash("Tu carrito está vacío.", "warning")
            return redirect(url_for("shop"))

        product_ids = [int(pid) for pid in cart.keys()]
        products = Product.query.filter(Product.id.in_(product_ids)).all()

        items = []
        total = Decimal("0.00")
        for product in products:
            quantity = cart.get(str(product.id), 0)
            line_total = Decimal(product.price_ars) * quantity
            total += line_total
            items.append(
                {
                    "product": product,
                    "quantity": quantity,
                    "line_total": line_total,
                }
            )
        
        # Cargar datos para el template
        categories = Category.query.all()
        social_links = SocialLink.query.filter_by(is_active=True).order_by(SocialLink.order).all()
        topbar_links = TopbarLink.query.filter_by(is_active=True).order_by(TopbarLink.order).all()
        footer_about = FooterSection.query.filter_by(section_type='about', is_active=True).first()
        footer_contact = FooterSection.query.filter_by(section_type='contact', is_active=True).first()
        footer_links_sections = FooterSection.query.filter_by(section_type='links', is_active=True).order_by(FooterSection.order).all()

        if request.method == "POST":
            name = request.form.get("name")
            email = request.form.get("email")
            phone = request.form.get("phone")
            address = request.form.get("address")

            # Crear/actualizar cliente
            customer = None
            if email:
                customer = Customer.query.filter_by(email=email).first()
            elif phone:
                customer = Customer.query.filter_by(phone=phone).first()
            
            if customer:
                # Actualizar cliente existente
                customer.name = name
                customer.address = address or customer.address
                customer.total_orders += 1
                customer.total_spent += total
                customer.last_order_date = datetime.utcnow()
            else:
                # Crear nuevo cliente
                customer = Customer(
                    name=name,
                    email=email,
                    phone=phone,
                    address=address,
                    total_orders=1,
                    total_spent=total,
                    first_order_date=datetime.utcnow(),
                    last_order_date=datetime.utcnow(),
                )
                db.session.add(customer)

            order = Order(
                customer_name=name,
                customer_email=email,
                customer_phone=phone,
                customer_address=address,
                total_amount_ars=total,
                status="pendiente",
            )
            db.session.add(order)
            db.session.flush()  # para tener order.id

            for item in items:
                product = item["product"]
                quantity = item["quantity"]
                line_total = item["line_total"]

                order_item = OrderItem(
                    order_id=order.id,
                    product_id=product.id,
                    product_name=product.name,
                    unit_price_ars=product.price_ars,
                    quantity=quantity,
                    line_total_ars=line_total,
                )
                db.session.add(order_item)

                # Actualizar stock
                if product.stock is not None:
                    product.stock = max(product.stock - quantity, 0)

            db.session.commit()

            # Limpiar carrito
            save_cart({})

            flash("Pedido creado. El pago se completará cuando integremos Mercado Pago.", "success")
            return redirect(url_for("index"))

        return render_template(
            "checkout.html",
            items=items,
            total=total,
            categories=categories,
            social_links=social_links,
            topbar_links=topbar_links,
            footer_about=footer_about,
            footer_contact=footer_contact,
            footer_links_sections=footer_links_sections,
        )


def register_admin_routes(app: Flask) -> None:
    from functools import wraps

    def login_required(view):
        @wraps(view)
        def wrapped(*args, **kwargs):
            if not session.get("admin_user_id"):
                return redirect(url_for("admin_login"))
            return view(*args, **kwargs)

        return wrapped

    @app.route("/admin/login", methods=["GET", "POST"])
    def admin_login():
        if request.method == "POST":
            username = request.form.get("username")
            password = request.form.get("password")
            user = AdminUser.query.filter_by(username=username).first()
            if user and user.check_password(password):
                session["admin_user_id"] = user.id
                flash("Ingreso correcto.", "success")
                return redirect(url_for("admin_dashboard"))
            flash("Usuario o contraseña incorrectos.", "danger")
        return render_template("admin_login.html")

    @app.route("/admin/logout")
    def admin_logout():
        session.pop("admin_user_id", None)
        flash("Sesión cerrada.", "info")
        return redirect(url_for("admin_login"))

    @app.route("/admin")
    @login_required
    def admin_dashboard():
        from sqlalchemy import func
        from datetime import datetime, timedelta
        
        # Estadísticas generales
        total_products = Product.query.count()
        total_orders = Order.query.count()
        total_pending = Order.query.filter_by(status="pendiente").count()
        total_customers = Customer.query.count()
        
        # Ventas totales
        total_sales = db.session.query(func.sum(Order.total_amount_ars)).filter(
            Order.status == 'pagado'
        ).scalar() or 0
        
        # Pedidos recientes (últimos 5)
        recent_orders = Order.query.order_by(Order.created_at.desc()).limit(5).all()
        
        # Productos con bajo stock (menos de 5)
        low_stock_products = Product.query.filter(Product.stock < 5, Product.is_active == True).all()
        
        # Productos más vendidos
        top_products = db.session.query(
            Product.name,
            func.sum(OrderItem.quantity).label('total_sold')
        ).join(OrderItem).group_by(Product.id).order_by(func.sum(OrderItem.quantity).desc()).limit(5).all()
        
        # Ventas por mes (últimos 6 meses)
        six_months_ago = datetime.utcnow() - timedelta(days=180)
        monthly_sales = db.session.query(
            func.strftime('%Y-%m', Order.created_at).label('month'),
            func.sum(Order.total_amount_ars).label('total')
        ).filter(
            Order.created_at >= six_months_ago,
            Order.status == 'pagado'
        ).group_by('month').order_by('month').all()
        
        # Pedidos por estado
        orders_by_status = db.session.query(
            Order.status,
            func.count(Order.id).label('count')
        ).group_by(Order.status).all()
        
        return render_template(
            "admin_dashboard.html",
            total_products=total_products,
            total_orders=total_orders,
            total_pending=total_pending,
            total_customers=total_customers,
            total_sales=total_sales,
            recent_orders=recent_orders,
            low_stock_products=low_stock_products,
            top_products=top_products,
            monthly_sales=monthly_sales,
            orders_by_status=orders_by_status,
        )

    @app.route("/admin/products")
    @login_required
    def admin_products():
        products = Product.query.order_by(Product.created_at.desc()).all()
        categories = Category.query.all()
        return render_template(
            "admin_products.html",
            products=products,
            categories=categories,
        )

    @app.route("/admin/products/new", methods=["GET", "POST"])
    @login_required
    def admin_product_new():
        categories = Category.query.all()
        if request.method == "POST":
            name = request.form.get("name")
            description = request.form.get("description")
            price = request.form.get("price", type=float)
            stock = request.form.get("stock", type=int)
            image_url = request.form.get("image_url")
            category_id = request.form.get("category_id", type=int)
            is_active = bool(request.form.get("is_active"))

            product = Product(
                name=name,
                description=description,
                price_ars=price,
                stock=stock or 0,
                image_url=image_url,
                category_id=category_id or None,
                is_active=is_active,
            )
            db.session.add(product)
            db.session.commit()
            flash("Producto creado correctamente.", "success")
            return redirect(url_for("admin_products"))

        return render_template("admin_product_form.html", categories=categories, product=None)

    @app.route("/admin/products/<int:product_id>/edit", methods=["GET", "POST"])
    @login_required
    def admin_product_edit(product_id: int):
        product = Product.query.get_or_404(product_id)
        categories = Category.query.all()

        if request.method == "POST":
            product.name = request.form.get("name")
            product.description = request.form.get("description")
            product.price_ars = request.form.get("price", type=float)
            product.stock = request.form.get("stock", type=int) or 0
            product.image_url = request.form.get("image_url")
            category_id = request.form.get("category_id", type=int)
            product.category_id = category_id or None
            product.is_active = bool(request.form.get("is_active"))

            db.session.commit()
            flash("Producto actualizado correctamente.", "success")
            return redirect(url_for("admin_products"))

        return render_template(
            "admin_product_form.html",
            categories=categories,
            product=product,
        )

    @app.route("/admin/products/<int:product_id>/delete", methods=["POST"])
    @login_required
    def admin_product_delete(product_id: int):
        product = Product.query.get_or_404(product_id)
        db.session.delete(product)
        db.session.commit()
        flash("Producto eliminado.", "info")
        return redirect(url_for("admin_products"))

    # ----- Categorías -----

    @app.route("/admin/categories")
    @login_required
    def admin_categories():
        categories = Category.query.order_by(Category.name.asc()).all()
        return render_template("admin_categories.html", categories=categories)

    @app.route("/admin/categories/new", methods=["GET", "POST"])
    @login_required
    def admin_category_new():
        if request.method == "POST":
            name = request.form.get("name")
            description = request.form.get("description")
            if not name:
                flash("El nombre es obligatorio.", "danger")
            else:
                if Category.query.filter_by(name=name).first():
                    flash("Ya existe una categoría con ese nombre.", "warning")
                else:
                    category = Category(name=name, description=description)
                    db.session.add(category)
                    db.session.commit()
                    flash("Categoría creada correctamente.", "success")
                    return redirect(url_for("admin_categories"))
        return render_template("admin_category_form.html", category=None)

    @app.route("/admin/categories/<int:category_id>/edit", methods=["GET", "POST"])
    @login_required
    def admin_category_edit(category_id: int):
        category = Category.query.get_or_404(category_id)
        if request.method == "POST":
            name = request.form.get("name")
            description = request.form.get("description")
            if not name:
                flash("El nombre es obligatorio.", "danger")
            else:
                existing = Category.query.filter_by(name=name).first()
                if existing and existing.id != category.id:
                    flash("Ya existe otra categoría con ese nombre.", "warning")
                else:
                    category.name = name
                    category.description = description
                    db.session.commit()
                    flash("Categoría actualizada correctamente.", "success")
                    return redirect(url_for("admin_categories"))
        return render_template("admin_category_form.html", category=category)

    @app.route("/admin/categories/<int:category_id>/delete", methods=["POST"])
    @login_required
    def admin_category_delete(category_id: int):
        category = Category.query.get_or_404(category_id)
        db.session.delete(category)
        db.session.commit()
        flash("Categoría eliminada.", "info")
        return redirect(url_for("admin_categories"))

    # ----- Configuración / Apariencia -----

    @app.route("/admin/settings", methods=["GET", "POST"])
    @login_required
    def admin_settings():
        keys = ["site_name", "site_short_name", "primary_color", "secondary_color"]
        current = {k: Setting.get(k, "") or "" for k in keys}

        if request.method == "POST":
            site_name = request.form.get("site_name") or "FaMa"
            site_short_name = request.form.get("site_short_name") or "FM"
            primary_color = request.form.get("primary_color") or "#D19C97"
            secondary_color = request.form.get("secondary_color") or "#EDF1FF"

            new_values = {
                "site_name": site_name,
                "site_short_name": site_short_name,
                "primary_color": primary_color,
                "secondary_color": secondary_color,
            }

            for key, value in new_values.items():
                setting = Setting.query.filter_by(key=key).first()
                if setting is None:
                    setting = Setting(key=key, value=value)
                    db.session.add(setting)
                else:
                    setting.value = value

            db.session.commit()
            flash("Configuración actualizada correctamente.", "success")
            return redirect(url_for("admin_settings"))

        return render_template("admin_settings.html", settings=current)

    @app.route("/admin/orders")
    @login_required
    def admin_orders():
        status = request.args.get("status")
        query = Order.query.order_by(Order.created_at.desc())
        if status:
            query = query.filter_by(status=status)
        orders = query.all()
        return render_template("admin_orders.html", orders=orders)

    @app.route("/admin/orders/<int:order_id>")
    @login_required
    def admin_order_detail(order_id: int):
        order = Order.query.get_or_404(order_id)
        return render_template("admin_order_detail.html", order=order)

    # ----- Gestión de Contenido -----

    @app.route("/admin/content")
    @login_required
    def admin_content():
        return render_template("admin_content.html")

    # Social Links
    @app.route("/admin/content/social-links")
    @login_required
    def admin_social_links():
        links = SocialLink.query.order_by(SocialLink.order).all()
        return render_template("admin_social_links.html", links=links)

    @app.route("/admin/content/social-links/new", methods=["GET", "POST"])
    @login_required
    def admin_social_link_new():
        if request.method == "POST":
            link = SocialLink(
                name=request.form.get("name"),
                icon=request.form.get("icon"),
                url=request.form.get("url"),
                is_active=bool(request.form.get("is_active")),
                order=request.form.get("order", type=int) or 0,
            )
            db.session.add(link)
            db.session.commit()
            flash("Red social agregada.", "success")
            return redirect(url_for("admin_social_links"))
        return render_template("admin_social_link_form.html", link=None)

    @app.route("/admin/content/social-links/<int:link_id>/edit", methods=["GET", "POST"])
    @login_required
    def admin_social_link_edit(link_id: int):
        link = SocialLink.query.get_or_404(link_id)
        if request.method == "POST":
            link.name = request.form.get("name")
            link.icon = request.form.get("icon")
            link.url = request.form.get("url")
            link.is_active = bool(request.form.get("is_active"))
            link.order = request.form.get("order", type=int) or 0
            db.session.commit()
            flash("Red social actualizada.", "success")
            return redirect(url_for("admin_social_links"))
        return render_template("admin_social_link_form.html", link=link)

    @app.route("/admin/content/social-links/<int:link_id>/delete", methods=["POST"])
    @login_required
    def admin_social_link_delete(link_id: int):
        link = SocialLink.query.get_or_404(link_id)
        db.session.delete(link)
        db.session.commit()
        flash("Red social eliminada.", "info")
        return redirect(url_for("admin_social_links"))

    # Topbar Links
    @app.route("/admin/content/topbar-links")
    @login_required
    def admin_topbar_links():
        links = TopbarLink.query.order_by(TopbarLink.order).all()
        return render_template("admin_topbar_links.html", links=links)

    @app.route("/admin/content/topbar-links/new", methods=["GET", "POST"])
    @login_required
    def admin_topbar_link_new():
        if request.method == "POST":
            link = TopbarLink(
                text=request.form.get("text"),
                url=request.form.get("url"),
                is_active=bool(request.form.get("is_active")),
                order=request.form.get("order", type=int) or 0,
            )
            db.session.add(link)
            db.session.commit()
            flash("Enlace agregado.", "success")
            return redirect(url_for("admin_topbar_links"))
        return render_template("admin_topbar_link_form.html", link=None)

    @app.route("/admin/content/topbar-links/<int:link_id>/edit", methods=["GET", "POST"])
    @login_required
    def admin_topbar_link_edit(link_id: int):
        link = TopbarLink.query.get_or_404(link_id)
        if request.method == "POST":
            link.text = request.form.get("text")
            link.url = request.form.get("url")
            link.is_active = bool(request.form.get("is_active"))
            link.order = request.form.get("order", type=int) or 0
            db.session.commit()
            flash("Enlace actualizado.", "success")
            return redirect(url_for("admin_topbar_links"))
        return render_template("admin_topbar_link_form.html", link=link)

    @app.route("/admin/content/topbar-links/<int:link_id>/delete", methods=["POST"])
    @login_required
    def admin_topbar_link_delete(link_id: int):
        link = TopbarLink.query.get_or_404(link_id)
        db.session.delete(link)
        db.session.commit()
        flash("Enlace eliminado.", "info")
        return redirect(url_for("admin_topbar_links"))

    # Carousel Slides
    @app.route("/admin/content/carousel")
    @login_required
    def admin_carousel():
        slides = CarouselSlide.query.order_by(CarouselSlide.order).all()
        return render_template("admin_carousel.html", slides=slides)

    @app.route("/admin/content/carousel/new", methods=["GET", "POST"])
    @login_required
    def admin_carousel_new():
        if request.method == "POST":
            slide = CarouselSlide(
                title=request.form.get("title"),
                subtitle=request.form.get("subtitle"),
                button_text=request.form.get("button_text"),
                button_url=request.form.get("button_url"),
                image_url=request.form.get("image_url"),
                is_active=bool(request.form.get("is_active")),
                order=request.form.get("order", type=int) or 0,
            )
            db.session.add(slide)
            db.session.commit()
            flash("Slide agregado.", "success")
            return redirect(url_for("admin_carousel"))
        return render_template("admin_carousel_form.html", slide=None)

    @app.route("/admin/content/carousel/<int:slide_id>/edit", methods=["GET", "POST"])
    @login_required
    def admin_carousel_edit(slide_id: int):
        slide = CarouselSlide.query.get_or_404(slide_id)
        if request.method == "POST":
            slide.title = request.form.get("title")
            slide.subtitle = request.form.get("subtitle")
            slide.button_text = request.form.get("button_text")
            slide.button_url = request.form.get("button_url")
            slide.image_url = request.form.get("image_url")
            slide.is_active = bool(request.form.get("is_active"))
            slide.order = request.form.get("order", type=int) or 0
            db.session.commit()
            flash("Slide actualizado.", "success")
            return redirect(url_for("admin_carousel"))
        return render_template("admin_carousel_form.html", slide=slide)

    @app.route("/admin/content/carousel/<int:slide_id>/delete", methods=["POST"])
    @login_required
    def admin_carousel_delete(slide_id: int):
        slide = CarouselSlide.query.get_or_404(slide_id)
        db.session.delete(slide)
        db.session.commit()
        flash("Slide eliminado.", "info")
        return redirect(url_for("admin_carousel"))

    # Feature Boxes
    @app.route("/admin/content/features")
    @login_required
    def admin_features():
        features = FeatureBox.query.order_by(FeatureBox.order).all()
        return render_template("admin_features.html", features=features)

    @app.route("/admin/content/features/new", methods=["GET", "POST"])
    @login_required
    def admin_feature_new():
        if request.method == "POST":
            feature = FeatureBox(
                icon=request.form.get("icon"),
                title=request.form.get("title"),
                is_active=bool(request.form.get("is_active")),
                order=request.form.get("order", type=int) or 0,
            )
            db.session.add(feature)
            db.session.commit()
            flash("Característica agregada.", "success")
            return redirect(url_for("admin_features"))
        return render_template("admin_feature_form.html", feature=None)

    @app.route("/admin/content/features/<int:feature_id>/edit", methods=["GET", "POST"])
    @login_required
    def admin_feature_edit(feature_id: int):
        feature = FeatureBox.query.get_or_404(feature_id)
        if request.method == "POST":
            feature.icon = request.form.get("icon")
            feature.title = request.form.get("title")
            feature.is_active = bool(request.form.get("is_active"))
            feature.order = request.form.get("order", type=int) or 0
            db.session.commit()
            flash("Característica actualizada.", "success")
            return redirect(url_for("admin_features"))
        return render_template("admin_feature_form.html", feature=feature)

    @app.route("/admin/content/features/<int:feature_id>/delete", methods=["POST"])
    @login_required
    def admin_feature_delete(feature_id: int):
        feature = FeatureBox.query.get_or_404(feature_id)
        db.session.delete(feature)
        db.session.commit()
        flash("Característica eliminada.", "info")
        return redirect(url_for("admin_features"))

    # Offer Banners
    @app.route("/admin/content/offers")
    @login_required
    def admin_offers():
        offers = OfferBanner.query.order_by(OfferBanner.order).all()
        return render_template("admin_offers.html", offers=offers)

    @app.route("/admin/content/offers/new", methods=["GET", "POST"])
    @login_required
    def admin_offer_new():
        if request.method == "POST":
            offer = OfferBanner(
                title=request.form.get("title"),
                subtitle=request.form.get("subtitle"),
                button_text=request.form.get("button_text"),
                button_url=request.form.get("button_url"),
                image_url=request.form.get("image_url"),
                background_color=request.form.get("background_color") or "#6C757D",
                text_align=request.form.get("text_align") or "center",
                is_active=bool(request.form.get("is_active")),
                order=request.form.get("order", type=int) or 0,
            )
            db.session.add(offer)
            db.session.commit()
            flash("Banner de oferta agregado.", "success")
            return redirect(url_for("admin_offers"))
        return render_template("admin_offer_form.html", offer=None)

    @app.route("/admin/content/offers/<int:offer_id>/edit", methods=["GET", "POST"])
    @login_required
    def admin_offer_edit(offer_id: int):
        offer = OfferBanner.query.get_or_404(offer_id)
        if request.method == "POST":
            offer.title = request.form.get("title")
            offer.subtitle = request.form.get("subtitle")
            offer.button_text = request.form.get("button_text")
            offer.button_url = request.form.get("button_url")
            offer.image_url = request.form.get("image_url")
            offer.background_color = request.form.get("background_color") or "#6C757D"
            offer.text_align = request.form.get("text_align") or "center"
            offer.is_active = bool(request.form.get("is_active"))
            offer.order = request.form.get("order", type=int) or 0
            db.session.commit()
            flash("Banner de oferta actualizado.", "success")
            return redirect(url_for("admin_offers"))
        return render_template("admin_offer_form.html", offer=offer)

    @app.route("/admin/content/offers/<int:offer_id>/delete", methods=["POST"])
    @login_required
    def admin_offer_delete(offer_id: int):
        offer = OfferBanner.query.get_or_404(offer_id)
        db.session.delete(offer)
        db.session.commit()
        flash("Banner de oferta eliminado.", "info")
        return redirect(url_for("admin_offers"))

    # Vendor Logos
    @app.route("/admin/content/vendors")
    @login_required
    def admin_vendors():
        vendors = VendorLogo.query.order_by(VendorLogo.order).all()
        return render_template("admin_vendors.html", vendors=vendors)

    @app.route("/admin/content/vendors/new", methods=["GET", "POST"])
    @login_required
    def admin_vendor_new():
        if request.method == "POST":
            vendor = VendorLogo(
                name=request.form.get("name"),
                image_url=request.form.get("image_url"),
                is_active=bool(request.form.get("is_active")),
                order=request.form.get("order", type=int) or 0,
            )
            db.session.add(vendor)
            db.session.commit()
            flash("Logo de marca agregado.", "success")
            return redirect(url_for("admin_vendors"))
        return render_template("admin_vendor_form.html", vendor=None)

    @app.route("/admin/content/vendors/<int:vendor_id>/edit", methods=["GET", "POST"])
    @login_required
    def admin_vendor_edit(vendor_id: int):
        vendor = VendorLogo.query.get_or_404(vendor_id)
        if request.method == "POST":
            vendor.name = request.form.get("name")
            vendor.image_url = request.form.get("image_url")
            vendor.is_active = bool(request.form.get("is_active"))
            vendor.order = request.form.get("order", type=int) or 0
            db.session.commit()
            flash("Logo de marca actualizado.", "success")
            return redirect(url_for("admin_vendors"))
        return render_template("admin_vendor_form.html", vendor=vendor)

    @app.route("/admin/content/vendors/<int:vendor_id>/delete", methods=["POST"])
    @login_required
    def admin_vendor_delete(vendor_id: int):
        vendor = VendorLogo.query.get_or_404(vendor_id)
        db.session.delete(vendor)
        db.session.commit()
        flash("Logo de marca eliminado.", "info")
        return redirect(url_for("admin_vendors"))

    # Footer
    @app.route("/admin/content/footer")
    @login_required
    def admin_footer():
        sections = FooterSection.query.order_by(FooterSection.order).all()
        return render_template("admin_footer.html", sections=sections)

    @app.route("/admin/content/footer/new", methods=["GET", "POST"])
    @login_required
    def admin_footer_section_new():
        if request.method == "POST":
            section = FooterSection(
                section_type=request.form.get("section_type"),
                title=request.form.get("title"),
                content=request.form.get("content"),
                is_active=bool(request.form.get("is_active")),
                order=request.form.get("order", type=int) or 0,
            )
            db.session.add(section)
            db.session.commit()
            flash("Sección de footer agregada.", "success")
            return redirect(url_for("admin_footer"))
        return render_template("admin_footer_section_form.html", section=None)

    @app.route("/admin/content/footer/<int:section_id>/edit", methods=["GET", "POST"])
    @login_required
    def admin_footer_section_edit(section_id: int):
        section = FooterSection.query.get_or_404(section_id)
        if request.method == "POST":
            section.section_type = request.form.get("section_type")
            section.title = request.form.get("title")
            section.content = request.form.get("content")
            section.is_active = bool(request.form.get("is_active"))
            section.order = request.form.get("order", type=int) or 0
            db.session.commit()
            flash("Sección de footer actualizada.", "success")
            return redirect(url_for("admin_footer"))
        return render_template("admin_footer_section_form.html", section=section)

    @app.route("/admin/content/footer/<int:section_id>/delete", methods=["POST"])
    @login_required
    def admin_footer_section_delete(section_id: int):
        section = FooterSection.query.get_or_404(section_id)
        db.session.delete(section)
        db.session.commit()
        flash("Sección de footer eliminada.", "info")
        return redirect(url_for("admin_footer"))

    # Novedades
    @app.route("/admin/content/news")
    @login_required
    def admin_news():
        news = NewsItem.query.order_by(NewsItem.order).all()
        return render_template("admin_news.html", news=news)

    @app.route("/admin/content/news/new", methods=["GET", "POST"])
    @login_required
    def admin_news_new():
        if request.method == "POST":
            news = NewsItem(
                title=request.form.get("title"),
                description=request.form.get("description"),
                image_url=request.form.get("image_url"),
                link_url=request.form.get("link_url"),
                link_text=request.form.get("link_text"),
                is_active=bool(request.form.get("is_active")),
                order=request.form.get("order", type=int) or 0,
            )
            db.session.add(news)
            db.session.commit()
            flash("Novedad agregada.", "success")
            return redirect(url_for("admin_news"))
        return render_template("admin_news_form.html", news=None)

    @app.route("/admin/content/news/<int:news_id>/edit", methods=["GET", "POST"])
    @login_required
    def admin_news_edit(news_id: int):
        news = NewsItem.query.get_or_404(news_id)
        if request.method == "POST":
            news.title = request.form.get("title")
            news.description = request.form.get("description")
            news.image_url = request.form.get("image_url")
            news.link_url = request.form.get("link_url")
            news.link_text = request.form.get("link_text")
            news.is_active = bool(request.form.get("is_active"))
            news.order = request.form.get("order", type=int) or 0
            db.session.commit()
            flash("Novedad actualizada.", "success")
            return redirect(url_for("admin_news"))
        return render_template("admin_news_form.html", news=news)

    @app.route("/admin/content/news/<int:news_id>/delete", methods=["POST"])
    @login_required
    def admin_news_delete(news_id: int):
        news = NewsItem.query.get_or_404(news_id)
        db.session.delete(news)
        db.session.commit()
        flash("Novedad eliminada.", "info")
        return redirect(url_for("admin_news"))

    # Clientes
    @app.route("/admin/customers")
    @login_required
    def admin_customers():
        customers = Customer.query.order_by(Customer.last_order_date.desc()).all()
        return render_template("admin_customers.html", customers=customers)

    @app.route("/admin/customers/<int:customer_id>")
    @login_required
    def admin_customer_detail(customer_id: int):
        customer = Customer.query.get_or_404(customer_id)
        orders = Order.query.filter(
            (Order.customer_email == customer.email) | (Order.customer_phone == customer.phone)
        ).order_by(Order.created_at.desc()).all()
        return render_template("admin_customer_detail.html", customer=customer, orders=orders)


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)



