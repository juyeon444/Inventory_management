from password_security import hash_password
import menus
from utils import get_valid_int
from mysql.connector import Error


def create_user(connection):
    username = input("Enter username: ").strip()
    password = input("Enter password: ").strip()
    if not password:
        print("Password is required.")
        return
    email = input("Enter email: ").strip()
    first_name = input("Enter first name: ").strip()
    last_name = input("Enter last name: ").strip()
    phone_number = input("Enter phone number: ").strip()
            
    try:
        cursor = connection.cursor(prepared=True)
        
        query = """
        INSERT INTO users (username, password, email, first_name, last_name, phone_number, role)
        VALUES (%s, %s, %s, %s, %s, %s, 'customer')
        """
        cursor.execute(query, (username, hash_password(password), email, first_name, last_name, phone_number))
        connection.commit()
        print("User created successfully.")
    except Error as e:
        print("Database operation failed.")


def read_all_users(connection):
    """Read all users from the users table and display their information."""    
    try:
        cursor = connection.cursor(dictionary=True)  
        query = """
        SELECT user_id, username, email, first_name, last_name, phone_number, role, created_at
        FROM users
        ORDER BY user_id
        """
        cursor.execute(query)
        users = cursor.fetchall()

        if users:
            print("\n User List:")
            print("-" * 180)
            print(f"{'ID':<5} {'Username':<20} {'Email':<30} {'First Name':<15} {'Last Name':<15} {'Phone':<15} {'Role':<10} {'Created At':<20}")
            print("-" * 180)

            for user in users:
                created_at = user["created_at"]

                if isinstance(created_at, str):
                    from datetime import datetime
                    created_at = datetime.strptime(created_at, '%Y-%m-%d %H:%M:%S')

                created_at_str = created_at.strftime('%Y-%m-%d %H:%M:%S') if created_at else 'N/A'

                print(f"{user['user_id']:<5} {user['username']:<20} {user['email']:<30} {user['first_name']:<15} {user['last_name']:<15} {user['phone_number']:<15} {user['role']:<10} {created_at_str:<20}")

            print("-" * 180)
        else:
            print("No user found.")
    except Error as e:
        print("Database operation failed.")


def read_user_by_user_id(connection):
    """Fetch a specific user by user_id and display their information."""
    user_id = get_valid_int("Enter user ID: ")

    try:
        cursor = connection.cursor(dictionary=True)  # ✅ Use dictionary cursor
        query = """
        SELECT user_id, username, email, first_name, last_name, phone_number, role, created_at
        FROM users
        WHERE user_id = %s
        """
        cursor.execute(query, (user_id,))
        user = cursor.fetchone()

        if user:
            print("\n User Details:")
            print("-" * 180)
            print(f"{'ID':<5} {'Username':<20} {'Email':<30} {'First Name':<15} {'Last Name':<15} {'Phone':<15} {'Role':<10} {'Created At':<20}")
            print("-" * 180)

            created_at = user["created_at"]

            # Ensure created_at is a datetime object before formatting
            if isinstance(created_at, str):
                from datetime import datetime
                created_at = datetime.strptime(created_at, '%Y-%m-%d %H:%M:%S')

            created_at_str = created_at.strftime('%Y-%m-%d %H:%M:%S') if created_at else 'N/A'

            print(f"{user['user_id']:<5} {user['username']:<20} {user['email']:<30} {user['first_name']:<15} {user['last_name']:<15} {user['phone_number']:<15} {user['role']:<10} {created_at_str:<20}")
            print("-" * 180)
        else:
            print(f"No user found with user_id: {user_id}")

    except Error as e:
        print("Database operation failed.")



def update_user_password(connection):
    user_id = get_valid_int("Enter user ID: ")
    new_password = input("Enter new password: ").strip()
    if not new_password:
        print("Password is required.")
        return
            
    """Update a user's password using a Prepared Statement."""
    try:
        cursor = connection.cursor(prepared=True)
        query = """
        UPDATE users
        SET password = %s
        WHERE user_id = %s
        """
        cursor.execute(query, (hash_password(new_password), user_id))
        connection.commit()
        print("Password updated successfully.")
    except Error as e:
        print("Database operation failed.")


def update_user_contact(connection):
    """Update a user's email and phone number."""
    user_id = get_valid_int("Enter user ID: ")
    new_email = input("Enter new email: ").strip()
    new_phone_number = input("Enter new phone number: ").strip()

    try:
        cursor = connection.cursor()  
        query = """
        UPDATE users  
        SET email = %s, phone_number = %s
        WHERE user_id = %s
        """
        cursor.execute(query, (new_email, new_phone_number, user_id))
        connection.commit()

        if cursor.rowcount > 0:
            print("Email and phone number updated successfully.")
        else:
            print("No user found with the given ID. No changes made.")

    except Error as e:
        print("Database operation failed.")


def delete_user(connection):
    user_id = get_valid_int("Enter user ID to delete: ")
        
    try:        
        cursor = connection.cursor(prepared=True)
        query = "DELETE FROM users WHERE user_id = %s"
        cursor.execute(query, (user_id,))
        connection.commit()

        print("User deleted successfully.")
    except Error as e:
        print("Database operation failed.")


def create_address(connection):
    user_id = get_valid_int("Enter user ID: ")
    street = input("Enter street: ").strip()
    city = input("Enter city: ").strip()
    state = input("Enter state: ").strip()
    postal_code = input("Enter postal code: ").strip()
    country = input("Enter country: ").strip()

    """Insert a new address into the addresses table."""
    try:
        cursor = connection.cursor(prepared=True)
        query = """
        INSERT INTO addresses (user_id, street, city, state, postal_code, country)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (user_id, street, city, state, postal_code, country))
        connection.commit()
        print("Address created successfully.")
    except Error as e:
        print("Database operation failed.")


def view_all_addresses(connection):
    """Retrieve and display all addresses from the addresses table."""
    try:
        cursor = connection.cursor(prepared=True)
        query = """
        SELECT a.address_id, u.user_id, u.username, a.street, a.city, a.state, a.postal_code, a.country
        FROM addresses a
        JOIN users u ON a.user_id = u.user_id
        ORDER BY a.address_id;
        """
        cursor.execute(query)
        addresses = cursor.fetchall()

        if addresses:
            print("\n All Addresses:")
            print("-" * 130)
            print(f"{'Address ID':<12} {'User ID':<8} {'Username':<20} {'Street':<25} {'City':<15} {'State':<15} {'Postal Code':<12} {'Country':<15}")
            print("-" * 130)

            for address in addresses:
                print(f"{address[0]:<12} {address[1]:<8} {address[2]:<20} {address[3]:<25} {address[4]:<15} {address[5]:<15} {address[6]:<12} {address[7]:<15}")

            print("-" * 130)
        else:
            print("No addresses found.")
    except Error as e:
        print("Database operation failed.")


def read_addresses_by_user_id(connection):
    """Fetch all addresses from the addresses table for a given user ID."""
    user_id = get_valid_int("Enter user ID: ")

    try:
        cursor = connection.cursor(dictionary=True) 
        query = """
        SELECT a.address_id, u.user_id, u.username, a.street, a.city, a.state, a.postal_code, a.country
        FROM addresses a
        JOIN users u ON a.user_id = u.user_id
        WHERE u.user_id = %s
        ORDER BY a.address_id;
        """
        cursor.execute(query, (user_id,))
        rows = cursor.fetchall()

        if rows:
            print(f"\n Addresses for User: {rows[0]['username']} (User ID: {user_id})")
            print("-" * 130)
            print(f"{'Address ID':<12} {'User ID':<8} {'Username':<20} {'Street':<25} {'City':<15} {'State':<15} {'Postal Code':<12} {'Country':<15}")
            print("-" * 130)

            for row in rows:
                print(f"{row['address_id']:<12} {row['user_id']:<8} {row['username']:<20} {row['street']:<25} {row['city']:<15} {row['state']:<15} {row['postal_code']:<12} {row['country']:<15}")

            print("-" * 130)
        else:
            print(f"No addresses found for User ID: {user_id}")

    except Error as e:
        print("Database operation failed.")


def read_addresses_by_address_id(connection):
    """Fetch a specific address using address_id and display correctly formatted output."""
    address_id = get_valid_int("Enter Address ID: ")

    try:
        cursor = connection.cursor(dictionary=True)  
        query = """
        SELECT a.address_id, u.user_id, u.username, a.street, a.city, a.state, a.postal_code, a.country
        FROM addresses a
        JOIN users u ON a.user_id = u.user_id
        WHERE a.address_id = %s
        """
        cursor.execute(query, (address_id,))
        address = cursor.fetchone()

        if address:
            print("\n=====  Address Details =====")
            print("-" * 140)
            print(f"{'Address ID':<12} {'User ID':<8} {'Username':<20} {'Street':<25} {'City':<15} {'State':<15} {'Postal Code':<12} {'Country':<15}")
            print("-" * 140)

            print(f"{address['address_id']:<12} {address['user_id']:<8} {address['username']:<20} {address['street']:<25} {address['city']:<15} {address['state']:<15} {address['postal_code']:<12} {address['country']:<15}")
            
            print("-" * 140)
        else:
            print(f"No address found with Address ID: {address_id}")

    except Error as e:
        print("Database operation failed.")


def update_address(connection):
    address_id = get_valid_int("Enter address ID to update: ")
    new_street = input("Enter new street: ").strip()
    new_city = input("Enter new city: ").strip()
    new_state = input("Enter new state: ").strip()
    new_postal_code = input("Enter new postal code: ").strip()
    new_country = input("Enter new country: ").strip()
            
    """Update an existing address in the addresses table."""
    try:
        cursor = connection.cursor(prepared=True)

        # Update query
        query = """
        UPDATE addresses
        SET street = %s, city = %s, state = %s, postal_code = %s, country = %s
        WHERE address_id = %s
        """
        # Execute the query with provided parameters
        cursor.execute(query, (new_street, new_city, new_state, new_postal_code, new_country, address_id))
        connection.commit()

        print("Address updated successfully.")
    except Error as e:
        print("Database operation failed.")


def delete_address(connection):
    address_id = get_valid_int("Enter address ID to delete: ")   
    """Delete an address from the addresses table."""
    try:
        cursor = connection.cursor(prepared=True)
        query = "DELETE FROM addresses WHERE address_id = %s"
        cursor.execute(query, (address_id,))
        connection.commit()
        print("Address deleted successfully.")
    except Error as e:
        print("Database operation failed.")


def user_operations(connection):
    while True:
        menus.user_menu()
        choice = input("Enter your choice: ")
        
        if choice == '1':
            create_user(connection)
        elif choice == '2':
            read_all_users(connection)
        elif choice == '3':
            read_user_by_user_id(connection)
        elif choice == '4':
            update_user_password(connection)
        elif choice == '5':
            update_user_contact(connection)
        elif choice == '6':
            delete_user(connection)
        elif choice == '7':
            create_address(connection)
        elif choice == '8':
            view_all_addresses(connection)
        elif choice == '9':
            read_addresses_by_user_id(connection)
        elif choice == '10':
            read_addresses_by_address_id(connection)
        elif choice == '11':
            update_address(connection)
        elif choice == '12':
            delete_address(connection)
        elif choice == '0':
            break
        else:
            print("Invalid choice. Please try again.")
            
