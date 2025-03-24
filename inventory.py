import menus
from utils import get_valid_int, get_valid_float
from mysql.connector import Error


def create_brand(connection):
    brand_name = input("Enter brand name: ").strip()
            
    """Insert a new brand into the brands table."""
    try:
        cursor = connection.cursor(prepared=True)
        query = "INSERT INTO brands (brand_name) VALUES (%s)"
        cursor.execute(query, (brand_name,))
        connection.commit()
        print("Brand created successfully.")
    except Error as e:
        print(f"Error: {e}")


def read_all_brands(connection):
    """Fetch and display all brands from the brands table."""
    try:
        cursor = connection.cursor(prepared=True)
        query = "SELECT * FROM brands ORDER BY brand_id"
        cursor.execute(query)
        rows = cursor.fetchall()

        if rows:
            print("\n===== Brand List =====")
            print("-" * 40)
            print(f"{'Brand ID':<10} {'Brand Name':<25}")
            print("-" * 40)
            for row in rows:
                print(f"{row[0]:<10} {row[1]:<25}")
            print("-" * 40)
        else:
            print("No brands found.")
    except Error as e:
        print(f"Error: {e}")


def view_brand_by_id(connection):
    """Fetch and display a brand's details by brand_id."""
    brand_id = get_valid_int("Enter Brand ID: ")

    try:
        cursor = connection.cursor(dictionary=True)  
        query = "SELECT brand_id, brand_name FROM brands WHERE brand_id = %s"
        cursor.execute(query, (brand_id,))
        brand = cursor.fetchone()

        if brand:
            print("\n===== Brand Details =====")
            print("-" * 40)
            print(f"{'Brand ID':<10} {'Brand Name':<25}")
            print("-" * 40)
            print(f"{brand['brand_id']:<10} {brand['brand_name']:<25}")
            print("-" * 40)
        else:
            print(f"No brand found with ID: {brand_id}")

    except Error as e:
        print(f"Error: {e}")


def update_brand(connection):
    brand_id = get_valid_int("Enter brand ID to update: ")
    new_brand_name = input("Enter new brand name: ").strip()

    """Update the name of an existing brand."""
    try:
        if not new_brand_name.strip():
            print("Brand name cannot be empty.")
            return

        cursor = connection.cursor(prepared=True)
        query = "UPDATE brands SET brand_name = %s WHERE brand_id = %s"
        cursor.execute(query, (new_brand_name, brand_id))
        connection.commit()

        if cursor.rowcount:
            print("Brand updated successfully.")
        else:
            print("Brand not found or no change made.")
    except Error as e:
        print(f"Error: {e}")


def delete_brand(connection):
    brand_id = get_valid_int("Enter brand ID to delete: ")

    """Delete a brand from the brands table."""
    try:
        cursor = connection.cursor(prepared=True)
        query = "DELETE FROM brands WHERE brand_id = %s"
        cursor.execute(query, (brand_id,))
        connection.commit()

        if cursor.rowcount:
            print("Brand deleted successfully.")
        else:
            print("Brand not found.")
    except Error as e:
        print(f"Error: {e}")


def create_supplier(connection):
    supplier_name = input("Enter supplier name: ").strip()
    contact_email = input("Enter contact email: ").strip()
    contact_phone_number = input("Enter contact phone number: ").strip()
    street = input("Enter street: ").strip()
    city = input("Enter city: ").strip()
    state = input("Enter state: ").strip()
    postal_code = input("Enter postal code: ").strip()
    country = input("Enter country: ").strip()
            
    """Insert a new supplier into the suppliers table."""
    try:
        cursor = connection.cursor(prepared=True)
        query = """
        INSERT INTO suppliers (supplier_name, contact_email, contact_phone_number, street, city, state, postal_code, country)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (supplier_name, contact_email, contact_phone_number, street, city, state, postal_code, country))
        connection.commit()
        print("Supplier created successfully.")
    except Error as e:
        print(f"Error: {e}")


def read_all_suppliers(connection):
    """Fetch and display all suppliers from the suppliers table with properly formatted output."""
    try:
        cursor = connection.cursor(dictionary=True) 
        query = """
        SELECT supplier_id, supplier_name, contact_email, contact_phone_number, 
               street, city, state, postal_code, country
        FROM suppliers 
        ORDER BY supplier_id
        """
        cursor.execute(query)
        rows = cursor.fetchall()

        if rows:
            print("\n Supplier List")
            print("-" * 210)
            print(f"{'ID':<5} {'Name':<40} {'Email':<40} {'Phone':<20} {'Street':<30} {'City':<20} {'State':<20} {'ZIP':<10} {'Country':<20}")
            print("-" * 210)
            for row in rows:
                print(f"{row['supplier_id']:<5} "
                      f"{row['supplier_name']:<40} "
                      f"{row['contact_email']:<40} "
                      f"{row['contact_phone_number']:<20} "
                      f"{row['street']:<30} "
                      f"{row['city']:<20} "
                      f"{row['state']:<20} "
                      f"{row['postal_code']:<10} "
                      f"{row['country']:<20}")
            print("-" * 210)
        else:
            print("No suppliers found.")
    
    except Error as e:
        print(f"Error: {e}")


def view_supplier_by_id(connection):
    """Fetch and display a supplier's details by supplier_id."""
    supplier_id = get_valid_int("Enter Supplier ID: ")

    try:
        cursor = connection.cursor(dictionary=True)  
        query = """
        SELECT supplier_id, supplier_name, contact_email, contact_phone_number, 
               street, city, state, postal_code, country
        FROM suppliers WHERE supplier_id = %s
        """
        cursor.execute(query, (supplier_id,))
        supplier = cursor.fetchone()

        if supplier:
            print("\n===== Supplier Details =====")
            print("-" * 210)
            print(f"{'ID':<5} {'Name':<40} {'Email':<40} {'Phone':<20} {'Street':<30} {'City':<20} {'State':<20} {'ZIP':<10} {'Country':<20}")
            print("-" * 210)
            print(f"{supplier['supplier_id']:<5} "
                  f"{supplier['supplier_name']:<40} "
                  f"{supplier['contact_email']:<40} "
                  f"{supplier['contact_phone_number']:<20} "
                  f"{supplier['street']:<30} "
                  f"{supplier['city']:<20} "
                  f"{supplier['state']:<20} "
                  f"{supplier['postal_code']:<10} "
                  f"{supplier['country']:<20}")
            print("-" * 210)
        else:
            print(f"No supplier found with ID: {supplier_id}")

    except Error as e:
        print(f"Error: {e}")


def update_supplier(connection):
    supplier_id = get_valid_int("Enter supplier ID to update: ")
    new_supplier_name = input("Enter new supplier name: ").strip()
    new_contact_email = input("Enter new contact email: ").strip() 
    new_contact_phone_number = input("Enter new contact phone number: ").strip() 
    new_street = input("Enter new street: ").strip() 
    new_city = input("Enter new city: ").strip() 
    new_state = input("Enter new state: ").strip() 
    new_postal_code = input("Enter new postal code: ").strip() 
    new_country = input("Enter new country: ").strip() 
            
    """Update an existing supplier."""
    try:
        cursor = connection.cursor(prepared=True)
        updates = []
        params = []

        if new_supplier_name:
            updates.append("supplier_name = %s")
            params.append(new_supplier_name)
        if new_contact_email:
            updates.append("contact_email = %s")
            params.append(new_contact_email)
        if new_contact_phone_number:
            updates.append("contact_phone_number = %s")
            params.append(new_contact_phone_number)
        if new_street:
            updates.append("street = %s")
            params.append(new_street)
        if new_city:
            updates.append("city = %s")
            params.append(new_city)
        if new_state:
            updates.append("state = %s")
            params.append(new_state)
        if new_postal_code:
            updates.append("postal_code = %s")
            params.append(new_postal_code)
        if new_country:
            updates.append("country = %s")
            params.append(new_country)

        if updates:
            query = f"UPDATE suppliers SET {', '.join(updates)} WHERE supplier_id = %s"
            params.append(supplier_id)
            cursor.execute(query, tuple(params))
            connection.commit()
            print("Supplier updated successfully.")
        else:
            print("No fields to update.")
    except Error as e:
        print(f"Error: {e}")


def delete_supplier(connection):
    supplier_id = get_valid_int("Enter supplier ID to delete: ")
            
    """Delete a supplier from the suppliers table."""
    try:
        cursor = connection.cursor(prepared=True)
        query = "DELETE FROM suppliers WHERE supplier_id = %s"
        cursor.execute(query, (supplier_id,))
        connection.commit()

        if cursor.rowcount:
            print("Supplier deleted successfully.")
        else:
            print("Supplier not found.")
    except Error as e:
        print(f"Error: {e}")


def create_product(connection):
    """
    Inserts a new product into the products table.
    """
    try:
        cursor = connection.cursor(prepared=True)

        # Get product details from the user
        product_name = input("Enter product name: ").strip()
        product_description = input("Enter product description: ").strip()
        
        # Validate and get price (up to 2 decimal places)
        price = get_valid_float("Enter product price (up to 2 decimal places): ", 2)
        
        # Get and validate brand ID and supplier ID
        brand_id = get_valid_int("Enter brand ID: ")
        supplier_id = get_valid_int("Enter supplier ID: ")

        # Insert the product into the database
        query = """
        INSERT INTO products (product_name, product_description, price, brand_id, supplier_id)
        VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(query, (product_name, product_description, price, brand_id, supplier_id))
        connection.commit()

        print("Product created successfully.")
    
    except Error as e:
        print(f"Error: {e}")
    
    finally:
        cursor.close()


def read_all_products(connection):
    """
    Fetch and display all products from the products table,
    including brand name and supplier name instead of just IDs.
    """
    try:
        cursor = connection.cursor(prepared=True)
        query = """
        SELECT 
            p.product_id, 
            p.product_name, 
            p.product_description, 
            p.price, 
            b.brand_name, 
            s.supplier_name
        FROM products p
        LEFT JOIN brands b ON p.brand_id = b.brand_id
        LEFT JOIN suppliers s ON p.supplier_id = s.supplier_id
        ORDER BY p.product_id;
        """
        cursor.execute(query)
        rows = cursor.fetchall()

        if rows:
            print("\n Product List:")
            print("-" * 120)
            print(f"{'ID':<5} {'Name':<30} {'Price ($)':<12} {'Brand':<20} {'Supplier':<30}")
            print("-" * 120)
            for row in rows:
                print(f"{row[0]:<5} {row[1]:<30} ${row[3]:<10.2f} {row[4] if row[4] else 'No Brand':<20} {row[5] if row[5] else 'No Supplier':<30}")
            print("-" * 120)
        else:
            print("No products found.")
    except Error as e:
        print(f"Error: {e}")


def view_product_by_id(connection):
    """Fetch and display a product's details by product_id."""
    product_id = get_valid_int("Enter Product ID: ")

    try:
        cursor = connection.cursor(dictionary=True)  
        query = """
        SELECT p.product_id, p.product_name, p.product_description, p.price, 
               b.brand_name, s.supplier_name
        FROM products p
        LEFT JOIN brands b ON p.brand_id = b.brand_id
        LEFT JOIN suppliers s ON p.supplier_id = s.supplier_id
        WHERE p.product_id = %s
        """
        cursor.execute(query, (product_id,))
        product = cursor.fetchone()

        if product:
            product_description = product['product_description'] if product['product_description'] else "N/A"

            print("\n===== Product Details =====")
            print("-" * 150)
            print(f"{'ID':<5} {'Name':<25} {'Description':<60} {'Price ($)':<12} {'Brand':<20} {'Supplier':<25}")
            print("-" * 150)
            print(f"{product['product_id']:<5} {product['product_name']:<25} {product_description:<60} "
                  f"${product['price']:<10.2f} {product['brand_name'] if product['brand_name'] else 'No Brand':<20} {product['supplier_name'] if product['supplier_name'] else 'No Supplier':<25}")
            print("-" * 150)
        else:
            print(f"No product found with ID: {product_id}")

    except Error as e:
        print(f"Error: {e}")


def update_product(connection):
    """
    Update an existing product's details in the database.
    """
    product_id = get_valid_int("Enter Product ID to update: ")
    if product_id is None:
        return  # Return to menu if no input is provided

    new_product_name = input("Enter new product name (Press Enter to keep unchanged): ").strip()
    new_product_description = input("Enter new product description (Press Enter to keep unchanged): ").strip()
    
    # Validate price with fixed decimal places
    new_price = get_valid_float("Enter new price (Press Enter to keep unchanged): ", decimal_places=2)
    
    # Validate brand and supplier (allow keeping old values)
    new_brand_id = get_valid_int("Enter new brand ID (Press Enter to keep unchanged): ")
    new_supplier_id = get_valid_int("Enter new supplier ID (Press Enter to keep unchanged): ")

    try:
        cursor = connection.cursor(prepared=True)
        updates = []
        params = []

        if new_product_name:
            updates.append("product_name = %s")
            params.append(new_product_name)
        if new_product_description:
            updates.append("product_description = %s")
            params.append(new_product_description)
        if new_price is not None:
            updates.append("price = %s")
            params.append(new_price)
        if new_brand_id is not None:
            updates.append("brand_id = %s")
            params.append(new_brand_id)
        if new_supplier_id is not None:
            updates.append("supplier_id = %s")
            params.append(new_supplier_id)

        if updates:
            query = f"UPDATE products SET {', '.join(updates)} WHERE product_id = %s"
            params.append(product_id)
            cursor.execute(query, tuple(params))
            connection.commit()
            print("Product updated successfully.")
        else:
            print("⚠ No fields were updated.")
    except Error as e:
        print(f"Error: {e}")


def delete_product(connection):
    product_id = get_valid_int("Enter product ID to delete: ")
            
    """Delete a product from the products table."""
    try:
        cursor = connection.cursor(prepared=True)
        query = "DELETE FROM products WHERE product_id = %s"
        cursor.execute(query, (product_id,))
        connection.commit()

        if cursor.rowcount:
            print("Product deleted successfully.")
        else:
            print("Product not found.")
    except Error as e:
        print(f"Error: {e}")


def create_inventory(connection):
    """
    Add stock to the inventory for a specific product.
    """
    product_id = get_valid_int("Enter Product ID to add to inventory: ")
    if product_id is None:
        return  # Return to menu if no input is provided

    stock_quantity = get_valid_int("Enter stock quantity: ")
    
    try:
        cursor = connection.cursor(prepared=True)
        
        # Check if the product already exists in inventory
        query_check = "SELECT COUNT(*) FROM inventory WHERE product_id = %s"
        cursor.execute(query_check, (product_id,))
        exists = cursor.fetchone()[0]

        if exists:
            # Update existing stock
            query_update = "UPDATE inventory SET stock_quantity = stock_quantity + %s WHERE product_id = %s"
            cursor.execute(query_update, (stock_quantity, product_id))
            print("Inventory updated successfully.")
        else:
            # Insert new inventory record
            query_insert = "INSERT INTO inventory (product_id, stock_quantity) VALUES (%s, %s)"
            cursor.execute(query_insert, (product_id, stock_quantity))
            print("Inventory added successfully.")

        connection.commit()
    except Error as e:
        print(f"Error: {e}")


def read_all_inventory(connection):
    """
    Fetch and display all inventory records with product names in a well-formatted table.
    """
    try:
        cursor = connection.cursor(dictionary=True)  # ✅ Use dictionary cursor for better column referencing
        query = """
        SELECT i.inventory_id, p.product_name, i.stock_quantity 
        FROM inventory i
        JOIN products p ON i.product_id = p.product_id
        ORDER BY i.inventory_id;
        """
        cursor.execute(query)
        rows = cursor.fetchall()

        if rows:
            print("\n Inventory List")
            print("-" * 80)
            print(f"{'Inventory ID':<15} {'Product Name':<40} {'Stock Quantity':<15}")
            print("-" * 80)
            for row in rows:
                print(f"{row['inventory_id']:<15} {row['product_name']:<40} {row['stock_quantity']:<15}")
            print("-" * 80)
        else:
            print("No inventory records found.")

    except Error as e:
        print(f"Error: {e}")


def read_inventory_by_product(connection):
    """
    Fetch and display inventory details for a specific product in a well-formatted table.
    """
    product_id = get_valid_int("Enter Product ID to check inventory: ")
    if product_id is None:
        return  # Return to menu if no input

    try:
        cursor = connection.cursor(dictionary=True)  
        query = """
        SELECT i.inventory_id, p.product_name, i.stock_quantity 
        FROM inventory i
        JOIN products p ON i.product_id = p.product_id
        WHERE i.product_id = %s;
        """
        cursor.execute(query, (product_id,))
        rows = cursor.fetchall()

        if rows:
            print("\n===== Inventory Details =====")
            print("-" * 80)
            print(f"{'Inventory ID':<15} {'Product Name':<40} {'Stock Quantity':<15}")
            print("-" * 80)
            for row in rows:
                print(f"{row['inventory_id']:<15} {row['product_name']:<40} {row['stock_quantity']:<15}")
            print("-" * 80)
        else:
            print("No inventory record found for this product.")

    except Error as e:
        print(f"Error: {e}")


def update_inventory(connection):
    """
    Update the stock quantity of a product in inventory.
    """
    inventory_id = get_valid_int("Enter Inventory ID to update: ")
    if inventory_id is None:
        return  # Return to menu if no input

    new_stock_quantity = get_valid_int("Enter new stock quantity: ")
    if new_stock_quantity is None:
        return  # Return to menu if no input

    try:
        cursor = connection.cursor(prepared=True)
        query = "UPDATE inventory SET stock_quantity = %s WHERE inventory_id = %s"
        cursor.execute(query, (new_stock_quantity, inventory_id))
        connection.commit()

        if cursor.rowcount > 0:
            print(f"Inventory ID {inventory_id} updated successfully. New stock: {new_stock_quantity}")
        else:
            print(f"No inventory record found with ID {inventory_id}.")
    except Error as e:
        print(f"Error: {e}")


def delete_inventory(connection):
    """
    Delete an inventory record from the inventory table.
    """
    inventory_id = get_valid_int("Enter Inventory ID to delete: ")
    if inventory_id is None:
        return  # Return to menu if no input

    try:
        cursor = connection.cursor(prepared=True)
        query = "DELETE FROM inventory WHERE inventory_id = %s"
        cursor.execute(query, (inventory_id,))
        connection.commit()

        if cursor.rowcount > 0:
            print(f"Inventory ID {inventory_id} deleted successfully.")
        else:
            print(f"No inventory record found with ID {inventory_id}.")
    except Error as e:
        print(f"Error: {e}")


def inventory_operations(connection):
    while True:
        menus.inventory_menu()
        choice = input("Enter your choice: ")

        if choice == '1':
            create_brand(connection)
        elif choice == '2':
            read_all_brands(connection)
        elif choice == '3':
            view_brand_by_id(connection)
        elif choice == '4':
            update_brand(connection)
        elif choice == '5':
            delete_brand(connection)
        elif choice == '6':
            create_supplier(connection)
        elif choice == '7':
            read_all_suppliers(connection)
        elif choice == '8':
            view_supplier_by_id(connection)
        elif choice == '9':
            update_supplier(connection)
        elif choice == '10':
            delete_supplier(connection)
        elif choice == '11':
            create_product(connection)
        elif choice == '12':
            read_all_products(connection)
        elif choice == '13':
            view_product_by_id(connection)
        elif choice == '14':
            update_product(connection)
        elif choice == '15':
            delete_product(connection)
        elif choice == '16':
            create_inventory(connection)
        elif choice == '17':
            read_all_inventory(connection)
        elif choice == '18':
            read_inventory_by_product(connection)
        elif choice == '19':
            update_inventory(connection)
        elif choice == '20':
            delete_inventory(connection)
        elif choice == '0':
            break
        else:
            print("Invalid choice. Please try again.")
