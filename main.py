import getpass
import os
import colorama
from colorama import Fore, Style
from auth.user_auth import authenticate_user
from database.product_db import create, read, update, delete, view_product

colorama.init(autoreset=True)  # Initialize colors

def clear_screen():
    """Clears the terminal screen for a clean UI."""
    os.system('cls' if os.name == 'nt' else 'clear')


def show_workflows_management_menu(permissions):
    """Display the Workflows Menu after login."""
    while True:
        clear_screen()
        print(f"\n{Fore.CYAN}===== Workflows Management System ====={Style.RESET_ALL}")

        menu_options = {
            "1": ("🔄 Workflows", "workflows"),
            "2": ("📦 Products", "products"),
            "3": ("⚙️ Settings", "settings"),
            "4": ("🚪 Exit", None)
        }

        for key, (label, perm) in menu_options.items():
            if perm is None or perm in permissions:
                print(f"{Fore.GREEN}{key}. {label}{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}{key}. {label} (Restricted){Style.RESET_ALL}")

        choice = input("Enter your choice: ")

        if choice == "1" and "workflows" in permissions:
            print(f"{Fore.YELLOW}Workflows (Coming soon!){Style.RESET_ALL}")
        elif choice == "2" and "products" in permissions:
            show_products_menu(permissions)
        elif choice == "3" and "settings" in permissions:
            print(f"{Fore.YELLOW}Settings (Coming soon!){Style.RESET_ALL}")
        elif choice == "4":
            print(f"{Fore.YELLOW}Goodbye!{Style.RESET_ALL}")
            break
        else:
            print(f"{Fore.RED}❌ Invalid choice! Please select from the menu.{Style.RESET_ALL}")


def create_product_page():
    """Dedicated page for creating a new product."""
    clear_screen()
    print(f"\n{Fore.CYAN}===== Create Product ====={Style.RESET_ALL}")

    data = {
        "product_name": input("Enter Product Name: "),
        
        "fg_part": input("Enter FG Part (SMxxxxxxx): "),
        "fg_part_rev": input("Enter FG Part Revision (xxx.xx): "),

        "pcb_part": input("Enter PCB Part (SMxxxxxxx): "),
        "pcb_part_rev": input("Enter PCB Part Revision (xxx.xx): "),

        "smd_top": input("Enter SMD Top (SMxxxxxxx): "),
        "smd_top_rev": input("Enter SMD Top Revision (xxx.xx): "),

        "smd_bottom": input("Enter SMD Bottom (SMxxxxxxx): "),
        "smd_bottom_rev": input("Enter SMD Bottom Revision (xxx.xx): "),

        "sw_wrapper": input("Enter SW Wrapper (SMxxxxxxx): "),
        "sw_wrapper_rev": input("Enter SW Wrapper Revision (xxx.xx): "),

        "ecu_version": input("Enter ECU Version (xx.xx.xx): "),
        "checksum": input("Enter Checksum (xxxxxxxx): "),
        "proto_number": input("Enter Proto Number (4-digit number): "),
        "status": input("Enter Status (Proto/Released): "),
        "remark": input("Enter Remark: ")
    }

    if create(data):
        print(f"{Fore.GREEN}✅ Product created successfully!{Style.RESET_ALL}")
    else:
        print(f"{Fore.RED}❌ Product creation failed! Please try again.{Style.RESET_ALL}")

def show_products_menu(permissions):
    while True:
        clear_screen()
        print(f"\n{Fore.CYAN}===== Products Menu ====={Style.RESET_ALL}")
        
        menu_options = {
            "1": ("🆕 Create", "create_product"),
            "2": ("📜 View", "view_product"),
            "3": ("✏️ Update", "update_product"),
            "4": ("🗑️ Delete", "delete_product"),
            "5": ("🔙 Back", None)
        }

        for key, (label, perm) in menu_options.items():
            if perm is None or perm in permissions:
                print(f"{Fore.GREEN}{key}. {label}{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}{key}. {label} (Restricted){Style.RESET_ALL}")

        choice = input("Enter your choice: ")

        if choice == "5":
            return

        if choice == "1" and "create_product" in permissions:
            create_product_page()
        elif choice == "2" and "view_product" in permissions:
            show_view_options()
        elif choice == "3" and "update_product" in permissions:
            update_product()
        elif choice == "4" and "delete_product" in permissions:
            product_id = input("Enter Product ID to Delete: ")
            delete(product_id)
        else:
            print(f"{Fore.RED}❌ Invalid choice!{Style.RESET_ALL}")

def show_view_options():
    """Displays the view options: View all products or view a single product by ID."""
    while True:
        clear_screen()
        print(f"\n{Fore.CYAN}===== View Products ====={Style.RESET_ALL}")
        
        print(f"{Fore.GREEN}1. View All Products{Style.RESET_ALL}")
        print(f"{Fore.GREEN}2. View Product by ID{Style.RESET_ALL}")
        print(f"{Fore.RED}3. Back to Products Menu{Style.RESET_ALL}")

        choice = input("Enter your choice: ")

        if choice == "1":
            read()
        elif choice == "2":
            product_id = input("Enter Product ID to View: ")
            show_product_details(product_id)
        elif choice == "3":
            return
        else:
            print(f"{Fore.RED}❌ Invalid choice! Please enter a valid option.{Style.RESET_ALL}")

def show_product_details(product_id):
    """Display product details with a Back option."""
    clear_screen()
    product = view_product(product_id)
    
    if not product:
        print(f"{Fore.RED}❌ Product not found!{Style.RESET_ALL}")
        return

    print(f"\n{Fore.CYAN}====={product['product_name']}====={Style.RESET_ALL}")

    fields = [
        "ID", "FG Part", "FG Part Revision", "PCB Part", "PCB Part Revision", 
        "SMD Top", "SMD Top Revision", "SMD Bottom", "SMD Bottom Revision",
        "SW Wrapper", "SW Wrapper Revision", "ECU Version", "Checksum", 
        "Proto Number", "Status", "Remark", "Created At"
    ]

    values = [
        product['id'], product['fg_part'], product['fg_part_rev'], product['pcb_part'], product['pcb_part_rev'],
        product['smd_top'], product['smd_top_rev'], product['smd_bottom'], product['smd_bottom_rev'],
        product['sw_wrapper'], product['sw_wrapper_rev'], product['ecu_version'], product['checksum'],
        product['proto_number'], product['status'], product['remark'], product['created_at']
    ]

    for field, value in zip(fields, values):
        print(f"{Fore.YELLOW}{field.ljust(20)}: {Style.RESET_ALL}{value}")

    print(f"\n{Fore.GREEN}Press any key to go Back to Product Menu...{Style.RESET_ALL}")
    input()

def update_product():
    """Handles updating a product."""
    product_id = input("Enter Product ID to Update: ")
    print("\nFields that can be updated:")
    update_fields = [
        "product_name", "fg_part", "fg_part_rev", "pcb_part", "pcb_part_rev",
        "smd_top", "smd_top_rev", "smd_bottom", "smd_bottom_rev",
        "sw_wrapper", "sw_wrapper_rev", "ecu_version", "checksum",
        "proto_number", "status", "remark"
    ]
    for field in update_fields:
        print(f"- {field}")

    field = input("Enter Field to Update: ").strip()
    if field not in update_fields:
        print(f"{Fore.RED}❌ Invalid field selected!{Style.RESET_ALL}")
        return

    new_value = input(f"Enter new value for {field}: ")
    update(product_id, field, new_value)

def main():
    clear_screen()
    print(f"{Fore.CYAN}Welcome to Workflows CLI{Style.RESET_ALL}")
    username = input("Username: ")
    password = getpass.getpass("Password: ")

    role, permissions = authenticate_user(username, password)

    if role:
        clear_screen()
        print(f"{Fore.GREEN}Login successful! Role: {role}{Style.RESET_ALL}")
        show_workflows_management_menu(permissions)
    else:
        print(f"{Fore.RED}Invalid credentials. Try again.{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
