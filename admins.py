import menus
from users import read_user_by_user_id
from utils import get_valid_int
from mysql.connector import Error


def get_admin_level_and_department():
    """Get admin level and department input from the user and validate."""
    # Admin level mapping
    admin_level_mapping = {
        '1': 'super admin',
        '2': 'warehouse manager',
        '3': 'sales manager',
        '4': 'support manager'
    }

    # Department mapping
    department_mapping = {
        '1': 'Customer Service',
        '2': 'Warehouse Operations',
        '3': 'Sales',
        '4': 'Executive Management',
        '5': 'Marketing',
        '6': 'IT Administration',
        '7': 'Product Management'
    }

    # Get admin level
    admin_level = input("Enter admin level (1: super admin, 2: warehouse manager, 3: sales manager, 4: support manager): ")
    admin_level_str = admin_level_mapping.get(admin_level)
    if not admin_level_str:
        print("Invalid admin level. Please choose a valid option.")
        return None, None

    # Get department
    department = input("Enter department (1: Customer Service, 2: Warehouse Operations, 3: Sales, 4: Executive Management, 5: Marketing, 6: IT Administration, 7: Product Management): ")
    department_str = department_mapping.get(department)
    if not department_str:
        print("Invalid department. Please choose a valid option.")
        return None, None

    return admin_level_str, department_str


def create_admin(connection):
    username = input("Enter username: ").strip()
    password = input("Enter password: ").strip()
    email = input("Enter email: ").strip()
    first_name = input("Enter first name: ").strip()
    last_name = input("Enter last name: ").strip()
    phone_number = input("Enter phone number: ").strip()
    
    admin_level_str, department_str = get_admin_level_and_department()
    
    if not admin_level_str or not department_str:
        print("Create canceled due to invalid input.")
        return
    
    try:
        cursor = connection.cursor()
        query = "CALL create_admin_account(%s, %s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(query, (username, password, email, first_name, last_name, phone_number, admin_level_str, department_str))            
        connection.commit()
        print("Admin account created successfully.")
    except Error as e:
        if e.errno == 1644:
            print("Error: An account with this username or email already exists.")
        else:
            print(f"Error: {e}")

def view_admins(connection):
    """Fetch all admins and display correctly formatted output."""
    try:
        cursor = connection.cursor(dictionary=True)  
        query = """
        SELECT 
            a.admin_id, 
            u.user_id, 
            u.username, 
            u.email, 
            CONCAT(u.first_name, ' ', u.last_name) AS full_name,  
            u.phone_number, 
            u.role,
            a.admin_level, 
            a.department 
        FROM admins a
        JOIN users u ON a.user_id = u.user_id
        ORDER BY a.admin_id
        """
        cursor.execute(query)
        rows = cursor.fetchall()

        if rows:
            print("\n Admins List")
            print("-" * 170)
            print(f"{'Admin ID':<10} {'User ID':<8} {'Username':<20} {'Email':<30} {'Name':<25} {'Phone':<15} {'Role':<10} {'Admin Level':<20} {'Department':<25}")
            print("-" * 170)

            for row in rows:
                print(f"{row['admin_id']:<10} {row['user_id']:<8} {row['username']:<20} {row['email']:<30} {row['full_name']:<25} {row['phone_number']:<15} {row['role']:<10} {row['admin_level']:<20} {row['department']:<25}")
            
            print("-" * 170)
        else:
            print("No admins found.")

    except Error as e:
        print(f"Error: {e}")


def view_admin_by_admin_id(connection):
    """Retrieve and display an admin's details by admin_id, including user information in a properly formatted way."""
    
    admin_id = get_valid_int("Enter Admin ID to view admin details: ")

    try:
        cursor = connection.cursor(dictionary=True)  
        query = """
        SELECT 
            a.admin_id, 
            u.user_id, 
            u.username, 
            u.email, 
            CONCAT(u.first_name, ' ', u.last_name) AS full_name,  
            u.phone_number, 
            a.admin_level, 
            a.department 
        FROM admins a
        JOIN users u ON a.user_id = u.user_id
        WHERE a.admin_id = %s
        """
        cursor.execute(query, (admin_id,))
        admin = cursor.fetchone()

        if admin:
            print("\n=====  Admin Details =====")
            print("-" * 170)
            print(f"{'Admin ID':<10} {'User ID':<8} {'Username':<20} {'Email':<30} {'Name':<25} {'Phone':<15} {'Admin Level':<20} {'Department':<25}")
            print("-" * 170)
            print(f"{admin['admin_id']:<10} {admin['user_id']:<8} {admin['username']:<20} {admin['email']:<30} {admin['full_name']:<25} {admin['phone_number']:<15} {admin['admin_level']:<20} {admin['department']:<25}")
            print("-" * 170)
        else:
            print(f"No admin found with Admin ID: {admin_id}")

    except Error as e:
        print(f"Error: {e}")


def view_admin_by_user_id(connection):
    """Retrieve and display an admin's details by user_id with properly formatted output."""
    
    user_id = get_valid_int("Enter User ID to view admin details: ")

    try:
        cursor = connection.cursor(dictionary=True)  
        query = """
        SELECT 
            a.admin_id, 
            u.user_id, 
            u.username, 
            u.email, 
            CONCAT(u.first_name, ' ', u.last_name) AS full_name,  
            u.phone_number, 
            a.admin_level, 
            a.department 
        FROM admins a
        JOIN users u ON a.user_id = u.user_id
        WHERE a.user_id = %s
        """
        cursor.execute(query, (user_id,))
        admin = cursor.fetchone()

        if admin:
            print("\n===== Admin Details =====")
            print("-" * 170)
            print(f"{'Admin ID':<10} {'User ID':<8} {'Username':<20} {'Email':<30} {'Name':<25} {'Phone':<15} {'Admin Level':<20} {'Department':<25}")
            print("-" * 170)
            print(f"{admin['admin_id']:<10} {admin['user_id']:<8} {admin['username']:<20} {admin['email']:<30} {admin['full_name']:<25} {admin['phone_number']:<15} {admin['admin_level']:<20} {admin['department']:<25}")
            print("-" * 170)
        else:
            print(f"No admin found with User ID: {user_id}")

    except Error as e:
        print(f"Error: {e}")


def update_admin(connection):
    """Update an existing admin in the admins table."""
    
    admin_id = get_valid_int("Enter admin ID to update: ")
     
    admin_level_str, department_str = get_admin_level_and_department()
    if not admin_level_str or not department_str:
        print("Update canceled due to invalid input.")
        return
    
    try:
        cursor = connection.cursor(prepared=True)
        query = """
        UPDATE admins
        SET admin_level = %s, department = %s
        WHERE admin_id = %s
        """
        cursor.execute(query, (admin_level_str, department_str, admin_id))
        connection.commit()

        if cursor.rowcount > 0:
            print("Admin updated successfully.")
        else:
            print("No admin found with the given ID.")
    except Error as e:
        print(f"Error: {e}")


def delete_admin(connection):
    """Delete an admin using the stored procedure and update the user's role to 'customer'."""
    admin_id = get_valid_int("Enter admin ID to delete: ")
    if admin_id is None:
        return  # Return to the menu if the user presses Enter

    try:
        cursor = connection.cursor(prepared=True)
        
        # Call the stored procedure
        query = "CALL delete_admin_account(%s)"
        cursor.execute(query, (admin_id,))
        connection.commit()

        if cursor.rowcount > 0:
            print("Admin deleted successfully and role updated to 'customer' in users table.")
        else:
            print("Admin ID not found.")

    except Error as e:
        print(f"Error: {e}")

    finally:
        cursor.close()


def promote_user_to_admin(connection):
    user_id = get_valid_int("Enter user ID to promote to admin: ")
    admin_level_str, department_str = get_admin_level_and_department()
    
    if not admin_level_str or not department_str:
        print("Promote canceled due to invalid input.")
        return
                
    """Call the promote_user_to_admin stored procedure to make an existing user an admin."""
    try:
        cursor = connection.cursor()
        query = "CALL promote_user_to_admin(%s, %s, %s)"
        cursor.execute(query, (user_id, admin_level_str, department_str))
        connection.commit()
        print("User promoted to admin successfully.")

    except Error as e:
        print(f"Error: {e}")
    finally:
        cursor.close()


def read_customers(connection):
    """Fetch all users who are not admins (role = 'customer')."""
    try:
        cursor = connection.cursor()
        query = """
        SELECT user_id, username, email, first_name, last_name, phone_number, created_at
        FROM users
        WHERE role = 'customer'
        ORDER BY user_id
        """
        cursor.execute(query)
        customers = cursor.fetchall()

        if customers:
            print("\n Customers List")
            print("-" * 120)
            print(f"{'ID':<5} {'Username':<20} {'Email':<30} {'Name':<20} {'Phone':<15} {'Created At':<20}")
            print("-" * 120)
            for customer in customers:
                created_at = customer[6].strftime('%Y-%m-%d %H:%M:%S') if customer[6] else 'N/A'
                print(f"{customer[0]:<5} {customer[1]:<20} {customer[2]:<30} {customer[3]+' '+customer[4]:<20} "
                      f"{customer[5] if customer[5] else 'N/A':<15} {created_at:<20}")
            print("-" * 120)        
        else:
            print("No customers found.")

    except Error as e:
        print(f"Error: {e}")


def admin_operations(connection):
    while True:
        menus.admin_menu()
        choice = input("Enter your choice: ")

        if choice == '1':
            create_admin(connection)
        elif choice == '2':
            view_admins(connection)
        elif choice == '3':
            view_admin_by_admin_id(connection)
        elif choice == '4':
            view_admin_by_user_id(connection)
        elif choice == '5':
            update_admin(connection)
        elif choice == '6':
            delete_admin(connection)
        elif choice == '7':
            promote_user_to_admin(connection)
        elif choice == '8':
            read_customers(connection)
        elif choice == '9':
            read_user_by_user_id(connection)
        elif choice == '0':
            break
        else:
            print("Invalid choice. Please try again.")
