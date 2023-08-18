#!/usr/bin/env python
# coding: utf-8

# In[10]:


import streamlit as st
import pandas as pd
import openai
import os

import streamlit as st
import pandas as pd
import sqlite3

# Load data
Orders = pd.read_excel(r'C:\Users\Abhirami.Gs\Desktop\GenAI\Site solutions\superstore.xlsx',sheet_name='Orders')
Returns = pd.read_excel(r'C:\Users\Abhirami.Gs\Desktop\GenAI\Site solutions\superstore.xlsx',sheet_name='Returns')
People = pd.read_excel(r'C:\Users\Abhirami.Gs\Desktop\GenAI\Site solutions\superstore.xlsx',sheet_name='People')

# Create an SQLite in-memory database
conn = sqlite3.connect(":memory:") #new database is created purely in memory

# Load data into SQLite database
Orders.to_sql("Orders", conn, index=False)
Returns.to_sql("Returns",conn,index=False)
People.to_sql("People",conn,index=False)

# Get table schema
Orders_schema = pd.read_sql("PRAGMA table_info(Orders)", conn)
Orders_schema_string = "\n".join("\t".join(map(str, row)) for row in Orders_schema.values)

Returns_schema = pd.read_sql("PRAGMA table_info(Returns)", conn)
Returns_schema_string = "\n".join("\t".join(map(str, row)) for row in Returns_schema.values)

People_schema = pd.read_sql("PRAGMA table_info(People)", conn)
People_schema_string = "\n".join("\t".join(map(str, row)) for row in People_schema.values)

# Sample rows
Orders_sample = Orders.sample(n=3)
Orders_sample_string = "\n".join("\t".join(map(str, row)) for row in Orders_sample.values)

Returns_sample = Returns.sample(n=3)
Returns_sample_string = "\n".join("\t".join(map(str, row)) for row in Returns_sample.values)


People_sample = People.sample(n=3)

People_sample_string = "\n".join("\t".join(map(str, row)) for row in People_sample.values)



# Print results
print("Orders Schema:\n", Orders_schema_string)

print("\nOrders Sample:\n", Orders_sample_string)

print("\nReturns Schema:\n", Returns_schema_string)

print("\nReturns Sample:\n", Returns_sample_string)

print("\nPeople Schema:\n", People_schema_string)

print("\nPeople Sample:\n", People_sample_string)


# close the connection
conn.close()

def create_prompt(schema1,schema2,schema3, rows_sample1, rows_sample2, rows_sample3, query, table_name1,table_name2, table_name3):
        prompt = (f"""
        Pretend to be a data scientist. You have a 3 SQLite tables named
        {table_name1} , {table_name2} and {table_name3}
        with the following schemas respectively:

        ```
        {schema1}

        {schema2}

        {schema3}
        ```

        The first few rows of each are like the ones given below respectively:

        ```{rows_sample1}```


        ```{rows_sample2}```

  
        ```{rows_sample3}```

        Based on this data, write a SQL query to answer the following question:
        {query}.
        Return the SQL query ONLY. we do not require any further explanation for it.
    
        """)

        return prompt


# Create a function to generate SQL query
def generate_sql_query(qn):

    openai.api_type="azure"
    openai.api_version="2023-03-15-preview"
    openai.api_base="https://openai-for-doa-coe-team-north-central.openai.azure.com/"
    openai.api_key="0cd5c99609e04171982f851b87bd45fd"
    
    

    schema1 = Orders_schema_string
    schema2 = Returns_schema_string
    schema3 = People_schema_string
    rows_sample1 = Orders_sample_string
    rows_sample2 = Returns_sample_string
    rows_sample3 = People_sample_string
    query = qn
    table_name1 = "Orders"
    table_name2 = "Returns"
    table_name3 = "People"


     
    prompt = create_prompt(schema1, schema2, schema3, rows_sample1, rows_sample2, rows_sample3, qn, table_name1, table_name2, table_name3)

    # Generate the SQL query
    response = openai.ChatCompletion.create(
        engine="gpt-35-turbo",
        temperature = 0,
        messages=[
            {"role": "system", "content": "Assistant is a large language model trained by OpenAI."},
            {"role": "user", "content": (prompt)}
         ]
    )

    sql_query = response['choices'][0]['message']['content']

    return sql_query

# Get the input question from the user
qn = st.text_input("Enter your question:")

# Generate the SQL query
sql_query = generate_sql_query(qn)

# Print the SQL query
st.write(sql_query)

# Connect to the SQLite database
conn = sqlite3.connect(":memory:") #Every :memory: database is distinct from every other
Orders.to_sql("Orders", conn, index=False)
Returns.to_sql("Returns",conn,index=False)
People.to_sql("People",conn,index=False)


# Execute the SQL query and store the results in a pandas DataFrame
df = pd.read_sql_query(sql_query, conn)

# Close the database connection
conn.close()

# Display the DataFrame
st.write(df)


# In[ ]:




