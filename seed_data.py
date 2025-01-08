from database.connection import get_session, initialize_database
from models.user import User
from models.product import Product
from models.order import Order
from config import logger

def seed_data():
    # Initialize the database
    initialize_database()

    # Start a session
    session = get_session()

    try:
        # Add sample users
        users = [
            User(name="Alice Johnson", email="alice@example.com"),
            User(name="Bob Smith", email="bob@example.com"),
            User(name="Charlie Brown", email="charlie@example.com"),
        ]
        session.add_all(users)

        # Add sample products
        products = [
            Product(name="Laptop", price=1200.00),
            Product(name="Smartphone", price=800.00),
            Product(name="Headphones", price=150.00),
        ]
        session.add_all(products)

        # Add sample orders
        orders = [
            Order(user_id=1, product_id=1),
            Order(user_id=1, product_id=3),
            Order(user_id=2, product_id=2),
        ]
        session.add_all(orders)

        session.commit()
        logger.info("Database seeded with sample data!")

    except Exception as e:
        logger.error(f"An error occurred while seeding the database: {e}")
        session.rollback()
    finally:
        session.close()

if __name__ == "__main__":
    seed_data()
