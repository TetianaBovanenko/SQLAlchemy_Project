from database.connection import get_session, initialize_database
from models.user import User
from models.product import Product
from models.order import Order
from config import logger


def display_all_users(session):
    """Display all users."""
    users = session.query(User).all()
    if users:
        logger.info("All Users:")
        for user in users:
            print(f"- ID: {user.id}, Name: {user.name}, Email: {user.email}")
    else:
        print("No users found.")


def display_all_products(session):
    """Display all products."""
    products = session.query(Product).all()
    if products:
        logger.info("All Products:")
        for product in products:
            print(f"- ID: {product.id}, Name: {product.name}, Price: ${product.price:.2f}")
    else:
        print("No products found.")


def display_user_orders(session, user_id):
    """Display orders for a specific user."""
    user = session.query(User).filter_by(id=user_id).first()
    if user:
        print(f"{user.name}'s Orders:")
        if user.orders:
            for order in user.orders:
                product = order.product
                print(f"- Product: {product.name}, Price: ${product.price:.2f}")
        else:
            print("No orders found for this user.")
    else:
        print("User not found.")


def display_total_spend_per_user(session):
    """Display total spend per user."""
    from sqlalchemy import func

    results = (
        session.query(User.name, func.sum(Product.price).label("total_spend"))
        .join(Order, User.id == Order.user_id)
        .join(Product, Product.id == Order.product_id)
        .group_by(User.name)
        .all()
    )

    logger.info("Total Spend Per User:")
    for user_name, total_spend in results:
        print(f"- {user_name}: ${total_spend:.2f}")


def display_popular_products(session):
    """Display most popular products by order count."""
    from sqlalchemy import func

    results = (
        session.query(Product.name, func.count(Order.id).label("order_count"))
        .join(Order, Product.id == Order.product_id)
        .group_by(Product.name)
        .order_by(func.count(Order.id).desc())
        .all()
    )

    logger.info("Most Popular Products:")
    for product_name, order_count in results:
        print(f"- {product_name}: {order_count} orders")


def interactive_menu():
    """Interactive menu for user interaction."""
    initialize_database()
    session = get_session()

    try:
        while True:
            print("\n--- Main Menu ---")
            print("1. View all users")
            print("2. View all products")
            print("3. View user orders")
            print("4. View total spend per user")
            print("5. View most popular products")
            print("6. Exit")
            choice = input("Enter your choice: ")

            if choice == "1":
                display_all_users(session)
            elif choice == "2":
                display_all_products(session)
            elif choice == "3":
                try:
                    user_id = int(input("Enter user ID: "))
                    display_user_orders(session, user_id)
                except ValueError:
                    print("Invalid user ID. Please enter a number.")
            elif choice == "4":
                display_total_spend_per_user(session)
            elif choice == "5":
                display_popular_products(session)
            elif choice == "6":
                print("Goodbye!")
                break
            else:
                print("Invalid choice, please try again.")
    except Exception as e:
        logger.error(f"An error occurred in the menu: {e}")
    finally:
        session.close()


if __name__ == "__main__":
    interactive_menu()
