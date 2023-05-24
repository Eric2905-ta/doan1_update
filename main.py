import psycopg2
from flask import Flask, render_template

app = Flask(__name__)

def get_data():
    # Establish a connection to the PostgreSQL database
    conn = psycopg2.connect(
    host="localhost",
    database="retailer_db",
    user="root",
    password="password",
    port="5432")

    # Create a cursor object to interact with the database
    cur = conn.cursor()

    # Execute the SQL query to fetch data from the "object" table
    cur.execute("SELECT * FROM object WHERE state > 1")
    # Fetch all the rows returned by the query
    data = cur.fetchall()

    # Get number of persons in roid A
    cur.execute("SELECT COUNT(ID) AS NUMA FROM object WHERE roi = 'RA'")
    dataA = cur.fetchone()[0]

    # Get number of persons in roid B
    cur.execute("SELECT COUNT(ID) AS NUMB FROM object WHERE roi = 'RB'")
    dataB = cur.fetchone()[0]

    # Get number of persons in roi C
    cur.execute("SELECT COUNT(ID) AS NUMC FROM object WHERE roi = 'RC'")
    dataC = cur.fetchone()[0]

    # Get number of persons in roi D
    cur.execute("SELECT COUNT(ID) AS NUMD FROM object WHERE roi = 'RF'")
    dataD = cur.fetchone()[0]

    # Close the cursor and the database connection
    cur.close()
    conn.close()

    return data, dataA, dataB, dataC, dataD

def generate_messages(data):
    messages = []
    for element in data:
        message = f"ID {element[0]} in area {element[3]} needs support"
        messages.append(message)
    return messages

@app.route('/')
def index():
    # Get data from the database and the number of persons in each roid
    data, dataA, dataB, dataC, dataD = get_data()

    # Generate the messages
    messages = generate_messages(data)

    # Print the values of dataA, dataB, dataC, and dataD
    print("dataA:", dataA)
    print("dataB:", dataB)
    print("dataC:", dataC)
    print("dataD:", dataD)

    # Render the template with the messages and person counts
    return render_template('app.html', messages=messages, dataA=dataA, dataB=dataB, dataC=dataC, dataD=dataD)

if __name__ == '__main__':
    app.run()
