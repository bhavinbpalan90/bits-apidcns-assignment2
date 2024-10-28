import pandas as pd
import numpy as np
from faker import Faker
import random
from datetime import datetime, timedelta
import sqlite3

# Initialize Faker
faker = Faker()

# Constants
num_records = 100

pd.set_option('display.max_columns', None)


# Define 20 different product names, categories, and descriptions
product_data = {
    "Wireless Headphones": {
        "category": "Electronics",
        "description": "High-quality wireless headphones with noise cancellation."
    },
    "Smartphone 128GB": {
        "category": "Electronics",
        "description": "Latest smartphone featuring 128GB storage and advanced camera."
    },
    "Smart Air Fryer": {
        "category": "Home Appliance",
        "description": "Smart air fryer with multiple cooking presets."
    },
    "Energy-Efficient Washing Machine": {
        "category": "Home Appliance",
        "description": "High-efficiency washing machine with energy-saving technology."
    },
    "Stylish Summer Dress": {
        "category": "Clothing",
        "description": "Elegant summer dress perfect for casual outings."
    },
    "Men's Running Shoes": {
        "category": "Clothing",
        "description": "Comfortable and durable men's running shoes."
    },
    "Bestselling Thriller Novel": {
        "category": "Books",
        "description": "A gripping thriller that keeps you on the edge of your seat."
    },
    "Inspirational Self-Help Book": {
        "category": "Books",
        "description": "An inspiring self-help book for personal development."
    },
    "Educational Building Blocks": {
        "category": "Toys",
        "description": "Creative building blocks for educational play."
    },
    "Remote Control Racing Car": {
        "category": "Toys",
        "description": "Fast and fun remote control racing car for kids."
    },
    "Durable Yoga Mat": {
        "category": "Sports",
        "description": "High-quality yoga mat for all your workout needs."
    },
    "High-Performance Bicycle": {
        "category": "Sports",
        "description": "Lightweight and durable bicycle for serious riders."
    },
    "Non-Stick Frying Pan": {
        "category": "Kitchenware",
        "description": "High-quality non-stick frying pan for easy cooking."
    },
    "Stainless Steel Knife Set": {
        "category": "Kitchenware",
        "description": "Professional stainless steel knife set for kitchen enthusiasts."
    },
    "Organic Skincare Cream": {
        "category": "Beauty",
        "description": "Nourishing organic skincare cream for all skin types."
    },
    "Luxury Perfume for Women": {
        "category": "Beauty",
        "description": "Elegant and captivating luxury perfume for women."
    },
    "Premium Car Wax": {
        "category": "Automotive",
        "description": "High-quality car wax for a glossy and protective finish."
    },
    "Car Vacuum Cleaner": {
        "category": "Automotive",
        "description": "Powerful car vacuum cleaner for thorough cleaning."
    },
    "Ergonomic Gardening Tools": {
        "category": "Gardening",
        "description": "Comfortable gardening tools designed for ease of use."
    },
    "Decorative Flower Pots": {
        "category": "Gardening",
        "description": "Beautiful decorative pots for your indoor and outdoor plants."
    }
}

# Function to generate order data
def generate_order_data(num_records):
    records = []
    product_names = list(product_data.keys())
    
    for _ in range(num_records):
        customer_id = random.randint(10000, 99999)  # 5-digit integer for customer ID
        customer_name = faker.name()
        customer_email = faker.email()
        customer_phone = faker.phone_number()
        
        order_number = random.randint(10000, 99999)  # 5-digit integer for order number
        order_date = faker.date_between(start_date='-1y', end_date='today')
        
        product_name = random.choice(product_names)
        product_category = product_data[product_name]["category"]
        product_description = product_data[product_name]["description"]
        
        order_quantity = random.randint(1, 5)
        total_order_value = random.randint(10, 500) * order_quantity  # Integer value
        
        order_delivery_status = random.choice(['Delivered', 'Pending', 'Cancelled'])
        
        records.append({
            "customer_id": customer_id,
            "customer_name": customer_name,
            "customer_email": customer_email,
            "customer_phone_number": customer_phone,
            "order_number": order_number,
            "order_date": order_date,
            "product_name": product_name,
            "product_category": product_category,
            "product_description": product_description,
            "order_quantity": order_quantity,
            "total_order_value": total_order_value,
            "order_delivery_status": order_delivery_status
        })
    
    return pd.DataFrame(records)

def write_to_sqlLite(dataset):
    conn = sqlite3.connect('bits.db')  # Change the name as needed
    dataset.to_sql('orders_data', conn, if_exists='replace', index=False)
    conn.close()
    return 'Completed'


def qry_sqlLite(qry):
    conn = sqlite3.connect('bits.db')  # Change the name as needed
    df = pd.read_sql_query(qry, conn)
    conn.close()
    return df


# Generate the dataset
synthetic_dataset = generate_order_data(num_records)
write_to_sqlLite(synthetic_dataset)

df_output = qry_sqlLite('SELECT * FROM orders_data limit 10')
print(df_output.head())