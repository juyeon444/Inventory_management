import menus
from utils import get_valid_int
from users import read_addresses_by_user_id
from inventory import read_all_products
from mysql.connector import Error


from decimal import Decimal

def create_order_with_items(connection):
    """Insert an order and its associated items into the database."""
    try:
        cursor = connection.cursor(dictionary=True)

        # Step 1: Collect order details
        user_id = get_valid_int("Enter user ID: ")
        shipping_address_id = get_valid_int("Enter shipping address ID: ")

        # Step 2: Initialize total_amount
        total_amount = 0.0
        order_items = []  # List to hold order items data

        # Step 3: Collect multiple items for the order
        print("Enter order items (press Enter without input to finish):")
        while True:
            product_input = input("Enter product ID (press Enter to finish): ").strip()

            # Stop if user presses Enter
            if product_input == "":
                break  

            # Ensure product_input is a valid integer
            if not product_input.isdigit():
                print("Invalid product ID. Please enter a valid number.")
                continue

            product_id = int(product_input)
            quantity = get_valid_int("Enter quantity: ")

            # Fetch unit price from products table
            unit_price_query = "SELECT price FROM products WHERE product_id = %s"
            cursor.execute(unit_price_query, (product_id,))
            result = cursor.fetchone()

            if result:
                unit_price = float(result["price"])  # Convert DECIMAL to float
                total_price = quantity * unit_price
                total_amount += total_price

                # Append the item to the list
                order_items.append((product_id, quantity, unit_price, total_price))
                print(f"Added {quantity} of Product {product_id} (Unit Price: ${unit_price:.2f}) to cart.")
            else:
                print(f"Product with ID {product_id} not found. Skipping...")

        # If no items were added, cancel the order creation
        if not order_items:
            print("No items added. Order creation cancelled.")
            return

        # Step 4: Insert into orders table
        orders_query = """
        INSERT INTO orders (user_id, total_amount, shipping_address_id, delivery_status)
        VALUES (%s, %s, %s, 'Pending')
        """
        cursor.execute(orders_query, (user_id, total_amount, shipping_address_id))

        # Retrieve the generated order_id
        order_id = cursor.lastrowid
        print(f"Order created with ID: {order_id}")

        # Step 5: Insert into order_items table (batch insert)
        order_items_query = """
        INSERT INTO order_items (order_id, product_id, quantity, unit_price, total_price)
        VALUES (%s, %s, %s, %s, %s)
        """
        cursor.executemany(order_items_query, [(order_id, *item) for item in order_items])

        # Step 6: Commit the transaction
        connection.commit()
        print("Order and items successfully created.")

    except Error as e:
        # Rollback the transaction in case of any error
        connection.rollback()
        print(f"Error: {e}")


def view_orders_by_delivery_status(connection):
    """Fetch and display all orders filtered by delivery status. If 0 is selected, show all orders."""
    
    print("\n Delivery Status Options:")
    print("1. Pending")
    print("2. Shipped")
    print("3. Delivered")
    print("4. Cancelled")
    print("0. View All Orders")
    
    status_choice = get_valid_int("Select a delivery status (0-4): ")
    
    status_mapping = {
        1: 'Pending',
        2: 'Shipped',
        3: 'Delivered',
        4: 'Cancelled'
    }
    
    try:
        cursor = connection.cursor(dictionary=True)
        
        if status_choice == 0:
            query = """
            SELECT o.order_id, u.user_id, u.username, o.total_amount, o.order_date, o.delivery_status,
                   a.street, a.city, a.state, a.country
            FROM orders o
            JOIN users u ON o.user_id = u.user_id
            JOIN addresses a ON o.shipping_address_id = a.address_id
            ORDER BY o.order_date DESC
            """
            cursor.execute(query)
            status_text = "All Orders"
        else:
            delivery_status = status_mapping.get(status_choice, None)
            if not delivery_status:
                print("Invalid selection. Returning to menu...")
                return

            query = """
            SELECT o.order_id, u.user_id, u.username, o.total_amount, o.order_date, o.delivery_status,
                   a.street, a.city, a.state, a.country
            FROM orders o
            JOIN users u ON o.user_id = u.user_id
            JOIN addresses a ON o.shipping_address_id = a.address_id
            WHERE o.delivery_status = %s
            ORDER BY o.order_date DESC
            """
            cursor.execute(query, (delivery_status,))
            status_text = f"Orders with Status: {delivery_status}"

        orders = cursor.fetchall()
        
        if orders:
            print(f"\n===== {status_text} =====")
            print("-" * 180)
            print(f"{'Order ID':<10} {'User ID':<10} {'Username':<20} {'Total ($)':<12} {'Order Date':<25} {'Status':<12} {'Shipping Address'}")
            print("-" * 180)
            for order in orders:
                order_date = order["order_date"].strftime('%Y-%m-%d %H:%M:%S') if order["order_date"] else "N/A"
                address = f"{order['street']}, {order['city']}, {order['state']}, {order['country']}"
                print(f"{order['order_id']:<10} {order['user_id']:<10} {order['username']:<20} ${order['total_amount']:<10.2f} {order_date:<25} {order['delivery_status']:<12} {address}")
            print("-" * 180)
        else:
            print(f"No orders found for {status_text}.")

    except Error as e:
        print(f"Error: {e}")


def read_orders_by_user_id(connection):
    """Fetch and display all orders placed by a specific user ID."""
    user_id = get_valid_int("Enter User ID: ")

    try:
        cursor = connection.cursor(dictionary=True)  
        query = """
        SELECT o.order_id, o.total_amount, o.order_date, o.delivery_status, 
               a.street, a.city, a.state, a.country
        FROM orders o
        JOIN addresses a ON o.shipping_address_id = a.address_id
        WHERE o.user_id = %s
        ORDER BY o.order_date DESC
        """
        cursor.execute(query, (user_id,))
        rows = cursor.fetchall()

        if rows:
            print(f"\n===== Orders for User ID: {user_id} =====")
            print("-" * 150)
            print(f"{'Order ID':<10} {'Total ($)':<12} {'Order Date':<25} {'Status':<12} {'Shipping Address'}")
            print("-" * 150)
            for row in rows:
                order_date = row["order_date"].strftime('%Y-%m-%d %H:%M:%S') if row["order_date"] else "N/A"
                address = f"{row['street']}, {row['city']}, {row['state']}, {row['country']}"
                print(f"{row['order_id']:<10} ${row['total_amount']:<10.2f} {order_date:<25} {row['delivery_status']:<12} {address}")
            print("-" * 150)
        else:
            print(f"No orders found for User ID: {user_id}")

    except Error as e:
        print(f"Error: {e}")


def read_order_by_order_id(connection):
    """Fetch and display all orders placed by a specific Order ID."""
    order_id = get_valid_int("Enter Order ID: ")

    try:
        cursor = connection.cursor(dictionary=True)  
        query = """
        SELECT o.order_id, o.total_amount, o.order_date, o.delivery_status, 
               a.street, a.city, a.state, a.country
        FROM orders o
        JOIN addresses a ON o.shipping_address_id = a.address_id
        WHERE o.order_id = %s
        ORDER BY o.order_date DESC
        """
        cursor.execute(query, (order_id,))
        rows = cursor.fetchall()

        if rows:
            print(f"\n===== Orders for User ID: {order_id} =====")
            print("-" * 150)
            print(f"{'Order ID':<10} {'Total ($)':<12} {'Order Date':<25} {'Status':<12} {'Shipping Address'}")
            print("-" * 150)
            for row in rows:
                order_date = row["order_date"].strftime('%Y-%m-%d %H:%M:%S') if row["order_date"] else "N/A"
                address = f"{row['street']}, {row['city']}, {row['state']}, {row['country']}"
                print(f"{row['order_id']:<10} ${row['total_amount']:<10.2f} {order_date:<25} {row['delivery_status']:<12} {address}")
            print("-" * 150)
        else:
            print(f"No orders found for User ID: {order_id}")

    except Error as e:
        print(f"Error: {e}")


def read_order_items_by_order_id(connection):
    """Fetch and display all order items for a specific order ID."""
    order_id = get_valid_int("Enter Order ID: ")

    try:
        cursor = connection.cursor(prepared=True)
        query = """
        SELECT oi.order_item_id, oi.order_id, p.product_name, oi.quantity, oi.unit_price, oi.total_price
        FROM order_items oi
        JOIN products p ON oi.product_id = p.product_id
        WHERE oi.order_id = %s
        """
        cursor.execute(query, (order_id,))
        rows = cursor.fetchall()

        if rows:
            print("\n===== Order Items =====")
            print("-" * 90)
            print(f"{'Item ID':<10} {'Order ID':<10} {'Product Name':<25} {'Qty':<5} {'Unit Price ($)':<15} {'Total ($)':<15}")
            print("-" * 90)
            for row in rows:
                print(f"{row[0]:<10} {row[1]:<10} {row[2]:<25} {row[3]:<5} ${row[4]:<13.2f} ${row[5]:<13.2f}")
            print("-" * 90)
        else:
            print(f"No order items found for Order ID: {order_id}")

    except Error as e:
        print(f"Error: {e}")


def update_order_status(connection):
    """Update the delivery status of an existing order using a numeric selection."""
    
    order_id = get_valid_int("Enter order ID to update: ")

    print("\n Delivery Status Options:")
    print("1. Pending")
    print("2. Shipped")
    print("3. Delivered")
    print("4. Cancelled")
    
    status_choice = get_valid_int("Select the new delivery status (1-4): ")

    status_mapping = {
        1: 'Pending',
        2: 'Shipped',
        3: 'Delivered',
        4: 'Cancelled'
    }

    new_status = status_mapping.get(status_choice)

    if not new_status:
        print("Invalid selection. Status update cancelled.")
        return

    try:
        cursor = connection.cursor(prepared=True)
        query = """
        UPDATE orders
        SET delivery_status = %s, status_updated_date = NOW()
        WHERE order_id = %s
        """
        cursor.execute(query, (new_status, order_id))
        connection.commit()

        if cursor.rowcount:
            print(f"Order ID {order_id} status updated to '{new_status}' successfully.")
        else:
            print(f"Order ID {order_id} not found or no change made.")

    except Error as e:
        print(f"Error: {e}")


def delete_order(connection):
    order_id = get_valid_int("Enter order ID to delete: ")
    """
    Delete an order and its associated items from the orders and order_items tables.
    """
    try:
        cursor = connection.cursor(prepared=True)

        # Delete order items explicitly (optional, as it cascades automatically)
        query_items = "DELETE FROM order_items WHERE order_id = %s"
        cursor.execute(query_items, (order_id,))
        print(f"{cursor.rowcount} item(s) deleted from order_items.")

        # Delete the order from the orders table
        query_order = "DELETE FROM orders WHERE order_id = %s"
        cursor.execute(query_order, (order_id,))
        connection.commit()

        if cursor.rowcount:
            print(f"Order {order_id} deleted successfully.")
        else:
            print(f"Order {order_id} not found.")
    except Error as e:
        print(f"Error: {e}")


def order_operations(connection):
    while True:
        menus.order_menu()
        choice = input("Enter your choice: ")

        if choice == '1':
            read_all_products(connection)
        elif choice == '2':
            read_addresses_by_user_id(connection)
        elif choice == '3':
            create_order_with_items(connection)
        elif choice == '4':
            read_orders_by_user_id(connection)
        elif choice == '5':
            read_order_by_order_id(connection)
        elif choice == '6':
            read_order_items_by_order_id(connection)
        elif choice == '7':
            view_orders_by_delivery_status(connection)
        elif choice == '8':
            update_order_status(connection)
        elif choice == '9':
            delete_order(connection)
        elif choice == '0':
            break
        else:
            print("Invalid choice. Please try again.")
