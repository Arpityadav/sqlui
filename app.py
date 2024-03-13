from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
import sqlite3
import google.generativeai as genai
import pandas as pd 
from sqlalchemy import create_engine

# Function to fetch data from SQLite database
def fetch_data():
    # SQLAlchemy connectable
    cnx = create_engine('sqlite:///student.db').connect()
    
    # Table named 'STUDENT' will be returned as a dataframe.
    df = pd.read_sql_table('STUDENT', cnx)
    return df


genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(question, prompt):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content([prompt[0], question])

    return response.text

def read_sql_query(sql, db):
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute(sql)
    rows = cur.fetchall()

    conn.commit()
    conn.close()

    for row in rows:
        print(row)
    return rows


# Define the prompt

prompt = [
    """
    You are an expert in converting English questions to SQL query!
    The SQL database has the name STUDENT and has the following columns NAME, CLASS, SECTION \n\nFor example, \nExample 1 How many entries of records are present?, the SQL command will be something like this SELECT COUNT(*) FROM STUDENT;
    nExample 2- Tell me all the students studying in Data Science class?, the SQL command will be something like this SELECT FROM STUDENT where CLASS="Data Science";
    also the sql code should not have in beginning or end and sql word in output
    """
]

# Streamlit app

st.set_page_config(page_title="I can retrieve any SQL query")
st.header("Gemini App to retrieve SQL query and SQL Data")

st.title('Student Table')

# Fetching data from SQLite database
df = fetch_data()

# Displaying the table
st.write(df)

question = st.text_input("Input: ", key="input", placeholder="I want all the students of section A")

submit = st.button("Ask the question")


# If the submit button is clicked

if submit:

    response = get_gemini_response(question, prompt)
    st.subheader("The Response is ")
    st.write("SQL Query is " + response)

    st.write("Result of this query: ")
    response = read_sql_query(response, "student.db")
    for row in response:
        print(row)
        st.header(row)