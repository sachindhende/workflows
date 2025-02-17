import mysql.connector
import re
import csv
from colorama import Fore, Style
from database.db_connector import get_db_connection

# Validation functions
def validate_part_id(value):
    return bool(re.match(r'^SM\d{7}$', value))

def validate_revision(value):
    return bool(re.match(r'^\d{3}\.\d{2}$', value))

def validate_ecu_version(value):
    return bool(re.match(r'^\d{2}\.\d{2}\.\d{2}$', value))

def validate_checksum(value):
    return bool(re.match(r'^[0-9A-Fa-f]{8}$', value))

def create_product(data):
    errors = []
    for part in ['fg_part', 'pcb_part', 'smd_top', 'smd_bottom', 'sw_wrapper']:
        if not validate_part_id(data[part]):
            errors.append(f"Invalid {part.replace('_', ' ').title()}! Must follow format 'SMxxxxxxx'.")
    for rev in ['fg_part_rev', 'pcb_part_rev', 'smd_top_rev', 'smd_bottom_rev', 'sw_wrapper_rev']:
        if not validate_revision(data[rev]):
            errors.append(f"Invalid {rev.replace('_', ' ').title()}! Must follow format 'xxx.xx'.")
    if not validate_ecu_version(data['ecu_version']):
        errors.append("Invalid ECU Version! Must follow format 'xx.xx.xx'.")
    if not validate_checksum(data['checksum']):
        errors.append("Invalid Checksum! Must be 8-character hexadecimal.")
    if errors:
        print("\n".join(errors))
        return False
    conn = get_db_connection()
    if not conn:
        print("Database connection failed!")
        return False
    cursor = conn.cursor()
    sql = """INSERT INTO products 
        (product_name, fg_part, fg_part_rev, pcb_part, pcb_part_rev, 
         smd_top, smd_top_rev, smd_bottom, smd_bottom_rev, 
         sw_wrapper, sw_wrapper_rev, ecu_version, checksum, 
         status, remark) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
    
    values = (
        data['product_name'].strip(), data['fg_part'].strip(), data['fg_part_rev'].strip(), 
        data['pcb_part'].strip(), data['pcb_part_rev'].strip(), 
        data['smd_top'].strip(), data['smd_top_rev'].strip(), 
        data['smd_bottom'].strip(), data['smd_bottom_rev'].strip(), 
        data['sw_wrapper'].strip(), data['sw_wrapper_rev'].strip(), 
        data['ecu_version'].strip(), data['checksum'].strip(), 
        data['status'].strip(), data['remark'].strip()
    )
    try:
        cursor.execute(sql, values)
        conn.commit()
        print("Product created successfully!")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()
        conn.close()

def export_products_to_csv():
    conn = get_db_connection()
    if not conn:
        print("Database connection failed!")
        return
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
    if not products:
        print("No products found.")
        return
    with open("products_export.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([desc[0] for desc in cursor.description])
        writer.writerows(products)
    print("Products exported successfully to 'products_export.csv'.")
    cursor.close()
    conn.close()

def search_product():
    conn = get_db_connection()
    if not conn:
        print("Database connection failed!")
        return
    search_term = input("Enter search term (Product Name or FG Part): ").strip()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM products WHERE product_name LIKE %s OR fg_part LIKE %s OR id LIKE %s", (f"%{search_term}%", f"%{search_term}%"))
    results = cursor.fetchall()
    if not results:
        print("No matching products found.")
    else:
        for product in results:
            print(f"ID: {product['id']}, Name: {product['product_name']}, FG Part: {product['fg_part']}, Status: {product['status']}")
    cursor.close()
    conn.close()

def read_products():
    """Fetch and display all products from the database."""
    conn = get_db_connection()
    if not conn:
        print("❌ Database connection failed!")
        return

    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id, product_name, fg_part, fg_part_rev, ecu_version, status FROM products")
    products = cursor.fetchall()

    print(f"\n{Fore.CYAN}********************************* All Products *********************************{Style.RESET_ALL}")
    
    if not products:
        print(f"{Fore.YELLOW}No products found.{Style.RESET_ALL}")
    else:
        print(f"{Fore.YELLOW}{'ID'.ljust(5)} | {'Product Name'.ljust(25)} | {'FG Part'.ljust(15)} | {'Rev   '.ljust(5)} | {'ECU Ver'.ljust(6)}  | {'Status'}{Style.RESET_ALL}")
        print("-" * 80)
        for product in products:
            print(f"{str(product['id']).ljust(5)} | {product['product_name'].ljust(25)} | {product['fg_part'].ljust(15)} | {product['fg_part_rev'].ljust(5)} | {product['ecu_version'].ljust(6)} | {product['status']}")

    cursor.close()
    conn.close()

    print(f"\n{Fore.GREEN}                             Press any key to go back...{Style.RESET_ALL}")
    input()


# Update Product
def update_product(product_id, field, new_value):
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
def delete_product(product_id):
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

    return product 
