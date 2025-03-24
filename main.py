import database as database
import menus
from users import user_operations
from admins import admin_operations
from inventory import inventory_operations
from orders import order_operations


def main():
    connection = database.create_connection()
    if not connection:
        return
    
    while True:
        menus.main_menu()
        choice = input("Enter your choice: ")

        if choice == '1':
            user_operations(connection)
        elif choice == '2':
            admin_operations(connection)
        elif choice == '3':
            inventory_operations(connection)
        elif choice == '4':
            order_operations(connection)
        elif choice == '0':
            print("Exiting program.")
            connection.close()
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
