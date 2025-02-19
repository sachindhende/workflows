import getpass
import os
import colorama
import csv
from colorama import Fore, Style
from auth.user_auth import authenticate_user
from database.product_db import create_product, read_products, update_product, delete_product, view_product, export_products_to_csv, search_product
from database.product_db import validate_part_id, validate_revision, validate_ecu_version, validate_checksum

colorama.init(autoreset=True)  # Initialize colors

def clear_screen():
    """Clears the terminal screen for a clean UI."""
    os.system('cls' if os.name == 'nt' else 'clear')


def show_workflows_management_menu(permissions):
    """Display the Workflows Menu after login."""
    while True:
        clear_screen()
        print(f"\n{Fore.CYAN}************************** Workflow Management System **************************{Style.RESET_ALL}")

        menu_options = {
            "1": ("🔄 Workflows", "workflows"),
            "2": ("📦 Products", "products"),
            "3": ("🛠️ Utilities", None),
            "7": ("⚙️ Settings", "settings"),
            "9": ("🚪 Logout", None)
        }

        for key, (label, perm) in menu_options.items():
            if perm is None or perm in permissions:
                print(f"{Fore.WHITE}{key}. {label}{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}{key}. {label} (Restricted){Style.RESET_ALL}")

        choice = input("Enter your choice: ")

        if choice == "1" and "workflows" in permissions:
            print(f"{Fore.YELLOW}Workflows (Coming soon!){Style.RESET_ALL}")         
        elif choice == "2" and "products" in permissions:
            show_products_menu(permissions)
        elif choice == "3" and "utilities" in permissions:
            print(f"{Fore.YELLOW}Utilities (Coming soon!){Style.RESET_ALL}")
        elif choice == "7" and "settings" in permissions:
            print(f"{Fore.YELLOW}Settings (Coming soon!){Style.RESET_ALL}")    
        elif choice == "9":           
            print(f"{Fore.YELLOW}Goodbye!{Style.RESET_ALL}")
            clear_screen()
            main()
        else:
            print(f"{Fore.RED}❌ Invalid choice! Please select from the menu.{Style.RESET_ALL}")


def get_valid_input(prompt, validation_func, error_message):
    """Continuously prompts the user until a valid input is given."""
    while True:
        value = input(prompt).strip()
        if validation_func(value):
            return value
        print(f"{Fore.RED}{error_message}{Style.RESET_ALL}")

def create_product_page():
    """Dedicated page for creating a new product with validation loops."""
    clear_screen()
    print(f"\n{Fore.CYAN}******************************** Create Product ********************************{Style.RESET_ALL}")
    
    data = {
        "product_name": input("Enter Product Name: ").strip(),
        "fg_part": get_valid_input("Enter FG Part (SMxxxxxxx): ", validate_part_id, "Invalid FG Part! Must follow format 'SMxxxxxxx'."),
        "fg_part_rev": get_valid_input("Enter FG Part Revision (xxx.xx): ", validate_revision, "Invalid revision format! Must follow 'xxx.xx'."),
        "pcb_part": get_valid_input("Enter PCB Part (SMxxxxxxx): ", validate_part_id, "Invalid PCB Part! Must follow format 'SMxxxxxxx'."),
        "pcb_part_rev": get_valid_input("Enter PCB Part Revision (xxx.xx): ", validate_revision, "Invalid revision format! Must follow 'xxx.xx'."),
        "smd_top": get_valid_input("Enter SMD Top (SMxxxxxxx): ", validate_part_id, "Invalid SMD Top! Must follow format 'SMxxxxxxx'."),
        "smd_top_rev": get_valid_input("Enter SMD Top Revision (xxx.xx): ", validate_revision, "Invalid revision format! Must follow 'xxx.xx'."),
        "smd_bottom": get_valid_input("Enter SMD Bottom (SMxxxxxxx): ", validate_part_id, "Invalid SMD Bottom! Must follow format 'SMxxxxxxx'."),
        "smd_bottom_rev": get_valid_input("Enter SMD Bottom Revision (xxx.xx): ", validate_revision, "Invalid revision format! Must follow 'xxx.xx'."),
        "sw_wrapper": get_valid_input("Enter SW Wrapper (SMxxxxxxx): ", validate_part_id, "Invalid SW Wrapper! Must follow format 'SMxxxxxxx'."),
        "sw_wrapper_rev": get_valid_input("Enter SW Wrapper Revision (xxx.xx): ", validate_revision, "Invalid revision format! Must follow 'xxx.xx'."),
        "ecu_version": get_valid_input("Enter ECU Version (xx.xx.xx): ", validate_ecu_version, "Invalid ECU Version! Must follow format 'xx.xx.xx'."),
        "checksum": get_valid_input("Enter Checksum (xxxxxxxx): ", validate_checksum, "Invalid Checksum! Must be 8-character hexadecimal."),
        "status": input("Enter Status (Proto/Released): ").strip(),
        "remark": input("Enter Remark: ").strip()
    }
    create_product(data)


def show_product_details(product_id):
    """Display product details with a Back option."""
    clear_screen()
    product = view_product(product_id)
    
    if not product:
        print(f"{Fore.RED}❌ Product not found!{Style.RESET_ALL}")
        return

    print(f"\n{Fore.CYAN}******************************* {product['product_name']} *******************************{Style.RESET_ALL}")

    fields = [
        "ID", "FG Part", "FG Part Revision", "PCB Part", "PCB Part Revision", 
        "SMD Top", "SMD Top Revision", "SMD Bottom", "SMD Bottom Revision",
        "SW Wrapper", "SW Wrapper Revision", "ECU Version", "Checksum", "Status", "Remark", "Created At"
    ]

    values = [
        product['id'], product['fg_part'], product['fg_part_rev'], product['pcb_part'], product['pcb_part_rev'],
        product['smd_top'], product['smd_top_rev'], product['smd_bottom'], product['smd_bottom_rev'],
        product['sw_wrapper'], product['sw_wrapper_rev'], product['ecu_version'], product['checksum'],
        product['status'], product['remark'], product['created_at']
    ]

    for field, value in zip(fields, values):
        print(f"{Fore.YELLOW}{field.ljust(20)}: {Style.RESET_ALL}{value}")

    print(f"\n{Fore.GREEN}                   Press any key to go Back to Product Menu...{Style.RESET_ALL}")
    input()


def show_products_menu(permissions):
    while True:
        clear_screen()
        print(f"\n{Fore.CYAN}****************************** Product Management ******************************{Style.RESET_ALL}")
        
        menu_options = {
            "1": ("🆕 Create", "create_product"),
            "2": ("📜 Read", "view_product"),
            "3": ("✏️ Update", "update_product"),
            "4": ("🗑️ Delete", "delete_product"),
            "5": ("📤 Export", None),
            "6": ("🔍 Search", None),
            "8": ("🔙 Back", None)                 
        }

        for key, (label, perm) in menu_options.items():
            if perm is None or perm in permissions:
                print(f"{Fore.WHITE}{key}. {label}{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}{key}. {label}{Style.RESET_ALL}")

        choice = input("Enter your choice: ")

        if choice == "8":
            clear_screen()
            return
        elif choice == "1" and "create_product" in permissions:
            create_product_page()
        elif choice == "2":
            clear_screen()
            read_products()
        elif choice == "3" and "update_product" in permissions:
            product_id = input("Enter Product ID to Update: ")
            field = input("Enter Field to Update: ")
            new_value = input("Enter New Value: ")
            update_product(product_id, field, new_value)
        elif choice == "4" and "delete_product" in permissions:
            product_id = input("Enter Product ID to Delete: ")
            delete_product(product_id)
        elif choice == "5":
            export_products_to_csv()
        elif choice == "6":
            product_id = input("Enter Product ID to View: ")
            show_product_details(product_id)
        else:
            print(f"{Fore.RED}❌ Invalid choice!{Style.RESET_ALL}")

def main():
    clear_screen()
    print(f"{Fore.CYAN}Welcome to Workflows{Style.RESET_ALL}")
    username = input("Username: ")
    password = getpass.getpass("Password: ")

    role, permissions = authenticate_user(username, password)

    if role:
        clear_screen()
        print(f"{Fore.GREEN}Login successful! Role: {role}{Style.RESET_ALL}")
        show_workflows_management_menu(permissions)
    else:
        print(f"{Fore.RED}Invalid credentials. Try again.{Style.RESET_ALL}")
        main()

if __name__ == "__main__":
    main()