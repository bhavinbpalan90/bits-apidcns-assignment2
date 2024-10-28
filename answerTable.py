import pandas as pd
import openai
from openai import OpenAI
import os
from dotenv import dotenv_values
import sqlite3
config = dotenv_values(".env")

# Access the API key
openApiKey = config['OPENAI_API_KEY']  # Use the key name you defined in the .env file

#print(openApiKey)  # This will print your API key

def qry_sqlLite(qry):
    conn = sqlite3.connect('bits.db')  # Change the name as needed
    df = pd.read_sql_query(qry, conn)
    conn.close()
    return df


# Generate the dataset
#synthetic_dataset = generate_order_data(num_records)
#write_to_sqlLite(synthetic_dataset)

df_output = qry_sqlLite('SELECT * FROM orders_data')


# Function to query the LLM
def query_llm(question, dataframe):

    client = OpenAI(api_key=openApiKey)

    # Extract relevant data as a string
    relevant_data = dataframe.to_string(index=False)
    
    # Formulate the prompt
    prompt = f"Based on the following data:\n{relevant_data}\n\nCan you answer this question: {question}?"
    
    # Call the LLM using the new API
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    
    return response.choices[0].message.content

# Example question
#question = "Could you please provide the delivery status for order number 12592"
question = "Could you please provide the Full order information for order number 12592"
answer = query_llm(question, df_output)

print(answer)
