import pandas as pd
from database.connection import get_session, initialize_database
from models.user import User
from models.product import Product
from models.order import Order

def export_to_pandas():
    """Export data to Pandas DataFrame and display it."""
    # Initialize the database
    initialize_database()
    session = get_session()

    try:
        # Query all users and their orders
        data = (
            session.query(User.name, Product.name, Product.price)
            .join(Order, User.id == Order.user_id)
            .join(Product, Product.id == Order.product_id)
            .all()
        )

        # Convert to Pandas DataFrame
        df = pd.DataFrame(data, columns=["User", "Product", "Price"])
        print("\nExported Data:")
        print(df)

        # Save to CSV (optional)
        df.to_csv("user_orders.csv", index=False)
        print("\nData exported to 'user_orders.csv' successfully.")

    except Exception as e:
        print(f"An error occurred while exporting data: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    export_to_pandas()
