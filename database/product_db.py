import mysql.connector
import re
import colorama
from colorama import Fore, Style
from database.db_connector import get_db_connection

# Validation Functions
def validate_part_id(value):
    """Validates part ID format: 'SM' followed by 7 digits (SMxxxxxxx)."""
    return bool(re.match(r'^SM\d{7}$', value))

def validate_revision(value):
    """Validates revision format: xxx.xx (e.g., 003.03)."""
    return bool(re.match(r'^\d{3}\.\d{2}$', value))

def validate_ecu_version(value):
    """Validates ECU Version format: xx.xx.xx"""
    return bool(re.match(r'^\d{2}\.\d{2}\.\d{2}$', value))

def validate_checksum(value):
    """Validates Checksum format: 8-character hexadecimal string."""
    return bool(re.match(r'^[0-9A-Fa-f]{8}$', value))

def validate_proto_number(value):
    """Validates Proto Number: 4-digit number (e.g., 1278)."""
    return bool(re.match(r'^\d{4}$', value))

# Create Product
def create(data):
    """Validates and inserts a new product into the database with debugging output."""

    # Validate part IDs
    parts = ['fg_part', 'pcb_part', 'smd_top', 'smd_bottom', 'sw_wrapper']
    for part in parts:
        if not validate_part_id(data[part]):
            print(f"❌ Invalid {part.replace('_', ' ').title()}! Must follow format 'SMxxxxxxx'.")
            input("\nPress Enter to continue...")  # Pause for user
            return False

    # Validate revision fields
    revisions = ['fg_part_rev', 'pcb_part_rev', 'smd_top_rev', 'smd_bottom_rev', 'sw_wrapper_rev']
    for rev in revisions:
        if not validate_revision(data[rev]):
            print(f"❌ Invalid {rev.replace('_', ' ').title()}! Must follow format 'xxx.xx'.")
            input("\nPress Enter to continue...")  # Pause for user
            return False

    # Validate other fields
    if not validate_ecu_version(data['ecu_version']):
        print("❌ Invalid ECU Version! Must follow format 'xx.xx.xx'.")
        input("\nPress Enter to continue...")  # Pause for user
        return False

    if not validate_checksum(data['checksum']):
        print("❌ Invalid Checksum! Must be 8-character hexadecimal (e.g., 77CB3BB0).")
        input("\nPress Enter to continue...")  # Pause for user
        return False

    if not validate_proto_number(data['proto_number']):
        print("❌ Invalid Proto Number! Must be a 4-digit number (e.g., 1278).")
        input("\nPress Enter to continue...")  # Pause for user
        return False

    # Ensure proto_number is converted to an integer if the database column expects it
    proto_number_value = int(data['proto_number']) if data['proto_number'].isdigit() else None
    if proto_number_value is None:
        print("❌ Proto Number must be a valid integer!")
        input("\nPress Enter to continue...")  # Pause for user
        return False

    # Ensure database connection
    conn = get_db_connection()
    if not conn:
        print("❌ Database connection failed!")
        input("\nPress Enter to continue...")  # Pause for user
        return False

    cursor = conn.cursor()

    sql = """INSERT INTO products 
        (product_name, fg_part, fg_part_rev, pcb_part, pcb_part_rev, 
         smd_top, smd_top_rev, smd_bottom, smd_bottom_rev, 
         sw_wrapper, sw_wrapper_rev, ecu_version, checksum, 
         proto_number, status, remark) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
    
    values = (
        data['product_name'].strip(), data['fg_part'].strip(), data['fg_part_rev'].strip(), 
        data['pcb_part'].strip(), data['pcb_part_rev'].strip(), 
        data['smd_top'].strip(), data['smd_top_rev'].strip(), 
        data['smd_bottom'].strip(), data['smd_bottom_rev'].strip(), 
        data['sw_wrapper'].strip(), data['sw_wrapper_rev'].strip(), 
        data['ecu_version'].strip(), data['checksum'].strip(), 
        proto_number_value, data['status'].strip(), data['remark'].strip()
    )

    # Debug: Print SQL query and values before execution
    print("\n🛠️ DEBUG: Attempting to execute SQL command:")
    print(f"Query: {sql}")
    print(f"Values: {values}")

    try:
        cursor.execute(sql, values)
        conn.commit()
        print("✅ Product created successfully!")
        return True  
    except mysql.connector.Error as err:
        print("\n❌ SQL Execution Error: ", err)
        print("❌ SQL Query: ", sql)
        print("❌ Values Sent: ", values)
        input("\nPress Enter to continue...")  # Pause for user to read error
        return False  
    finally:
        cursor.close()
        conn.close()



# Read Products
def read():
    """Fetch and display all products from the database."""
    conn = get_db_connection()
    if not conn:
        print("❌ Database connection failed!")
        return

    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id, product_name, fg_part, fg_part_rev, proto_number, status FROM products")
    products = cursor.fetchall()

    print(f"\n{Fore.CYAN}===== All Products ====={Style.RESET_ALL}")
    
    if not products:
        print(f"{Fore.YELLOW}No products found.{Style.RESET_ALL}")
    else:
        print(f"{Fore.GREEN}{'ID'.ljust(5)} | {'Product Name'.ljust(25)} | {'FG Part'.ljust(15)} | {'Rev'.ljust(5)} | {'Proto #'.ljust(6)} | {'Status'}{Style.RESET_ALL}")
        print("-" * 80)
        for product in products:
            print(f"{str(product['id']).ljust(5)} | {product['product_name'].ljust(25)} | {product['fg_part'].ljust(15)} | {product['fg_part_rev'].ljust(5)} | {product['proto_number'].ljust(6)} | {product['status']}")

    cursor.close()
    conn.close()

    print(f"\n{Fore.GREEN}Press any key to go back...{Style.RESET_ALL}")
    input()


# Update Product
def update(product_id, field, new_value):
    """Updates a specific field of a product, including revision fields and proto_number."""
    conn = get_db_connection()
    if not conn:
        print("❌ Database connection failed!")
        return

    # Validate input
    if field in ['fg_part', 'pcb_part', 'smd_top', 'smd_bottom', 'sw_wrapper'] and not validate_part_id(new_value):
        print("❌ Invalid part ID format!")
        return

    if field.endswith('_rev') and not validate_revision(new_value):
        print("❌ Invalid revision format! Must be xxx.xx")
        return

    if field == 'proto_number' and not validate_proto_number(new_value):
        print("❌ Invalid Proto Number! Must be a 4-digit number.")
        return

    cursor = conn.cursor()
    sql = f"UPDATE products SET {field} = %s WHERE id = %s"
    
    try:
        cursor.execute(sql, (new_value, product_id))
        conn.commit()
        print("✅ Product updated successfully!")
    except mysql.connector.Error as err:
        print(f"❌ Error: {err}")
    finally:
        cursor.close()
        conn.close()


# Delete Product
def delete(product_id):
    """Deletes a product by ID."""
    conn = get_db_connection()
    if not conn:
        print("❌ Database connection failed!")
        return

    cursor = conn.cursor()
    sql = "DELETE FROM products WHERE id = %s"
    
    try:
        cursor.execute(sql, (product_id,))
        conn.commit()
        print("✅ Product deleted successfully!")
    except mysql.connector.Error as err:
        print(f"❌ Error: {err}")
    finally:
        cursor.close()
        conn.close()


# View Product
def view_product(product_id):
    """Fetch and return a single product from the database by ID."""
    conn = get_db_connection()
    if not conn:
        print("❌ Database connection failed!")
        return None

    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM products WHERE id = %s", (product_id,))
    product = cursor.fetchone()

    cursor.close()
    conn.close()

    return product  # Return product details as a dictionary or None if not found
