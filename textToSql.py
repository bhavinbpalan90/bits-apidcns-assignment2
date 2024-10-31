import torch
from transformers import T5Tokenizer, T5ForConditionalGeneration

# Initialize the tokenizer from Hugging Face Transformers library
tokenizer = T5Tokenizer.from_pretrained('t5-small')

# Load the model
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = T5ForConditionalGeneration.from_pretrained('cssupport/t5-small-awesome-text-to-sql')
model = model.to(device)
model.eval()

def generate_sql(input_prompt):
    # Tokenize the input prompt
    tableSchema = "tables:\n" + "CREATE TABLE orders_data (customer_id INTEGER,customer_name TEXT, customer_email TEXT,customer_phone_number TEXT,order_number INTEGER,order_date DATE,product_name TEXT,product_category TEXT,product_description TEXT,order_quantity INTEGER,total_order_value INTEGER,order_delivery_status TEXT) \n CREATE TABLE PRODUCT_DATA (  product_name TEXT, product_category TEXT, product_description TEXT, product_price REAL, product_in_stock INTEGER, product_rating REAL)" + "\n" + "query for:"
    finalInput = tableSchema + input_prompt + "if output is from Orders Tables, include Order Date, Order Number and Product Name"
    #" If question is related to order, include Order No, Order Date and Product Name. If Question is related to Product, get it from Product table"
    inputs = tokenizer(finalInput, padding=True, truncation=True, return_tensors="pt").to(device)
    
    # Forward pass
    with torch.no_grad():
        outputs = model.generate(**inputs, max_length=512)
    
    # Decode the output IDs to a string (SQL query in this case)
    generated_sql = tokenizer.decode(outputs[0], skip_special_tokens=True)
    
    return generated_sql

# Test the function
#input_prompt = "tables:\n" + "CREATE TABLE Catalogs (date_of_latest_revision VARCHAR)" + "\n" +"query for: Find the dates on which more than one revisions were made."
#input_prompt = "tables:\n" + "CREATE TABLE table_22767 ( \"Year\" real, \"World\" real, \"Asia\" text, \"Africa\" text, \"Europe\" text, \"Latin America/Caribbean\" text, \"Northern America\" text, \"Oceania\" text )" + "\n" +"query for:what will the population of Asia be when Latin America/Caribbean is 783 (7.5%)?."
#input_prompt = "tables:\n" + "CREATE TABLE procedures ( subject_id text, hadm_id text, icd9_code text, short_title text, long_title text ) CREATE TABLE diagnoses ( subject_id text, hadm_id text, icd9_code text, short_title text, long_title text ) CREATE TABLE lab ( subject_id text, hadm_id text, itemid text, charttime text, flag text, value_unit text, label text, fluid text ) CREATE TABLE demographic ( subject_id text, hadm_id text, name text, marital_status text, age text, dob text, gender text, language text, religion text, admission_type text, days_stay text, insurance text, ethnicity text, expire_flag text, admission_location text, discharge_location text, diagnosis text, dod text, dob_year text, dod_year text, admittime text, dischtime text, admityear text ) CREATE TABLE prescriptions ( subject_id text, hadm_id text, icustay_id text, drug_type text, drug text, formulary_drug_cd text, route text, drug_dose text )" + "\n" +"query for:" + "what is the total number of patients who were diagnosed with icd9 code 2254?"
#input_prompt = "tables:\n" + "CREATE TABLE orders_data (customer_id INTEGER,customer_name TEXT, customer_email TEXT,customer_phone_number TEXT,order_number INTEGER,order_date DATE,product_name TEXT,product_category TEXT,product_description TEXT,order_quantity INTEGER,total_order_value INTEGER,order_delivery_status TEXT) CREATE TABLE PRODUCT_DATA (  product_name TEXT, product_category TEXT, product_description TEXT, product_price REAL, product_in_stock INTEGER, product_rating REAL)" + "\n" + "query for:" + "Provide List of all Products"


#input_prompt = 'Provide me Order Delivery Status for the Order 1234. '
input_prompt = 'Provide me List of all Products and its Category. '
generated_sql = generate_sql(input_prompt)

print(f"The generated SQL query is: {generated_sql}")
