CREATE DATABASE IF NOT EXISTS workflows;

USE workflows;

-- Create Users Table
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role ENUM('admin', 'user') NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create Products Table with new fields
CREATE TABLE IF NOT EXISTS products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    product_name VARCHAR(255) NOT NULL,

    fg_part VARCHAR(10) NOT NULL CHECK (fg_part REGEXP '^SM[0-9]{7}$'),
    fg_part_rev VARCHAR(6) NOT NULL CHECK (fg_part_rev REGEXP '^[0-9]{3}\\.[0-9]{2}$'),

    pcb_part VARCHAR(10) NOT NULL CHECK (pcb_part REGEXP '^SM[0-9]{7}$'),
    pcb_part_rev VARCHAR(6) NOT NULL CHECK (pcb_part_rev REGEXP '^[0-9]{3}\\.[0-9]{2}$'),

    smd_top VARCHAR(10) NOT NULL CHECK (smd_top REGEXP '^SM[0-9]{7}$'),
    smd_top_rev VARCHAR(6) NOT NULL CHECK (smd_top_rev REGEXP '^[0-9]{3}\\.[0-9]{2}$'),

    smd_bottom VARCHAR(10) NOT NULL CHECK (smd_bottom REGEXP '^SM[0-9]{7}$'),
    smd_bottom_rev VARCHAR(6) NOT NULL CHECK (smd_bottom_rev REGEXP '^[0-9]{3}\\.[0-9]{2}$'),

    sw_wrapper VARCHAR(10) NOT NULL CHECK (sw_wrapper REGEXP '^SM[0-9]{7}$'),
    sw_wrapper_rev VARCHAR(6) NOT NULL CHECK (sw_wrapper_rev REGEXP '^[0-9]{3}\\.[0-9]{2}$'),

    ecu_version VARCHAR(10) NOT NULL CHECK (ecu_version REGEXP '^[0-9]{2}\\.[0-9]{2}\\.[0-9]{2}$'),
    checksum VARCHAR(8) NOT NULL CHECK (checksum REGEXP '^[0-9A-Fa-f]{8}$'),

    proto_number VARCHAR(4) NOT NULL CHECK (proto_number REGEXP '^[0-9]{4}$'),
    
    status ENUM('Proto', 'Released') NOT NULL,
    remark TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
