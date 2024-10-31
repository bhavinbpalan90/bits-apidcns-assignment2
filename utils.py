import pandas as pd
import openai
from openai import OpenAI
import os
from dotenv import dotenv_values
import sqlite3
config = dotenv_values(".env")

# Access the API key
openApiKey = config['OPENAI_API_KEY']  # Use the key name you defined in the .env file

def qry_sqlLite(qry):
    conn = sqlite3.connect('bits.db')  # Change the name as needed
    df = pd.read_sql_query(qry, conn)
    conn.close()
    return df


def getTextToSQL(question):

    client = OpenAI(api_key=openApiKey)
    
    # Provide the Schema of Tables for Orders and Product
    tableSchema = "tables:\n" + "CREATE TABLE order_data (customer_id INTEGER,customer_name TEXT, customer_email TEXT,customer_phone_number TEXT,order_number INTEGER,order_date DATE,product_name TEXT,product_category TEXT,product_description TEXT,order_quantity INTEGER,total_order_value INTEGER,order_delivery_status TEXT) \n CREATE TABLE PRODUCT_DATA (  product_name TEXT, product_category TEXT, product_description TEXT, product_price REAL, product_in_stock INTEGER, product_rating REAL)" + "\n" + "query for:"
    
    
    # Formulate the prompt
    prompt = f"Based on the following Table Schema :\n{tableSchema}\n\nCan you generate a single SQL for SQLlite for this question: {question}?. If Question is related to Product, Respond from Product Table and include Product Name. if Question is related to Orders data, always include columns Order Date, Order Number and Product Name"
    
    # Call the LLM using the new API
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )

    sqlText = str(response.choices[0].message.content)

    #print(sqlText)

    df_output = qry_sqlLite(sqlText)

    #print(df_output.head())
    
    return df_output





# Function to query the LLM
def query_llm(question):

    client = OpenAI(api_key=openApiKey)

    df_filtered_rows = getTextToSQL(question)
    #print(df_filtered_rows.head())

    # Extract relevant data as a string
    relevant_data = df_filtered_rows.to_string(index=False)

    # Formulate the prompt
    prompt = f"Based on the following data:\n{relevant_data}\n\nCan you answer this question: {question}?. Generate Response in a Human Friendly way. Include Order Number and Product Name if it is available"
    
    # Call the LLM using the new API
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    
    return response.choices[0].message.content


