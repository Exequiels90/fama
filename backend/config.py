import os


BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    """Configuración base para la tienda online."""

    # Base de datos - usa DATABASE_URL si está disponible, sino SQLite local
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        "sqlite:///" + os.path.join(BASE_DIR, "shop.db")
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Clave secreta - DEBE cambiarse en producción
    SECRET_KEY = os.environ.get("SECRET_KEY", "cambia-esta-clave-en-produccion")

    # Para futuras integraciones (Mercado Pago, etc.)
    MERCADOPAGO_ACCESS_TOKEN = os.environ.get("MERCADOPAGO_ACCESS_TOKEN")
    MERCADOPAGO_PUBLIC_KEY = os.environ.get("MERCADOPAGO_PUBLIC_KEY")


class DevConfig(Config):
    DEBUG = True


class ProdConfig(Config):
    DEBUG = False



