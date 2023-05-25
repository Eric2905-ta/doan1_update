import psycopg2
from flask import Flask, render_template, request
from flask_socketio import SocketIO
from threading import Lock

app = Flask(__name__)

"""
Background Thread
"""
thread = None
thread_lock = Lock()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'donsky!'
socketio = SocketIO(app, cors_allowed_origins='*')


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
    cur.execute("SELECT * FROM object WHERE state > 0.9")
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


"""
Generate random sequence of dummy sensor values and send it to our clients
"""

def background_thread():
    print("Generating random sensor values")
    while True:
        data, dataA, dataB, dataC, dataD = get_data()
        socketio.emit('updateROI', {
                      "dataA": dataA,
                      "dataB": dataB,
                      "dataC": dataC,
                      "dataD": dataD, })
        socketio.sleep(1)


def generate_messages(data):
    messages = []
    for element in data:
        message = f"ID {element[0]} in area {element[3]} needs support"
        messages.append(message)
    return messages


@app.route('/')
def index():
    # Get data from the database and the number of persons in each roid
    while True:
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

"""
Decorator for connect
"""
@socketio.on('connect')
def connect():
    global thread
    print('Client connected')

    global thread
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(background_thread)

"""
Decorator for disconnect
"""
@socketio.on('disconnect')
def disconnect():
    print('Client disconnected',  request.sid)

if __name__ == '__main__':
    # app.run()
    socketio.run(app)
