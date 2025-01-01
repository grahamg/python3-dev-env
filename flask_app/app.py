import os
import mysql.connector
from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

# Database configuration
DB_HOST = os.environ.get("MYSQL_HOST", "mysql_db")
DB_USER = os.environ.get("MYSQL_USER", "root")
DB_PASSWORD = os.environ.get("MYSQL_PASSWORD", "root")
DB_NAME = os.environ.get("MYSQL_DATABASE", "todo_db")

# Minimal HTML template
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Todo List</title>
</head>
<body>
    <h1>Todo List</h1>
    <ul>
        {% for todo in todos %}
        <li>
            {{ todo[1] }} 
            {% if todo[2] %}
                [Completed]
            {% else %}
                <form action="/complete/{{todo[0]}}" method="post" style="display:inline;">
                    <button type="submit">Mark as Completed</button>
                </form>
            {% endif %}
        </li>
        {% endfor %}
    </ul>
    <h2>Add Todo</h2>
    <form action="/add" method="post">
        <input type="text" name="task" placeholder="New task..." required>
        <button type="submit">Add</button>
    </form>
</body>
</html>
"""

@app.before_first_request
def create_table():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS todos (
            id INT AUTO_INCREMENT PRIMARY KEY,
            task VARCHAR(255) NOT NULL,
            completed BOOLEAN NOT NULL DEFAULT FALSE
        )
    """)
    conn.commit()
    cursor.close()
    conn.close()

def get_db_connection():
    return mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )

@app.route("/", methods=["GET"])
def index():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, task, completed FROM todos")
    todos = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template_string(HTML_TEMPLATE, todos=todos)

@app.route("/add", methods=["POST"])
def add_task():
    task = request.form["task"]
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO todos (task, completed) VALUES (%s, %s)", (task, False))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": "Task added."}), 201

@app.route("/complete/<int:task_id>", methods=["POST"])
def complete_task(task_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE todos SET completed = True WHERE id = %s", (task_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": "Task marked as completed."}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8003)
