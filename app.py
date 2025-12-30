from flask import Flask, request, jsonify
from db import get_connection, create_table

app = Flask(__name__)

# Create table on app start
create_table()

# ---------------- HOME ----------------
@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Backend API with MySQL is running"})


# ---------------- CREATE USER ----------------
@app.route("/users", methods=["POST"])
def add_user():
    data = request.get_json()

    name = data.get("name")
    email = data.get("email")
    age = data.get("age")

    if not name or not email:
        return jsonify({"error": "Name and email are required"}), 400

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO users (name, email, age) VALUES (%s, %s, %s)",
            (name, email, age)
        )

        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({"message": "User created successfully"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ---------------- GET ALL USERS ----------------
@app.route("/users", methods=["GET"])
def get_users():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()

    cursor.close()
    conn.close()

    return jsonify(users), 200


# ---------------- UPDATE USER ----------------
@app.route("/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    data = request.get_json()

    name = data.get("name")
    age = data.get("age")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE users SET name=%s, age=%s WHERE id=%s",
        (name, age, user_id)
    )

    conn.commit()

    if cursor.rowcount == 0:
        cursor.close()
        conn.close()
        return jsonify({"error": "User not found"}), 404

    cursor.close()
    conn.close()
    return jsonify({"message": "User updated successfully"}), 200


# ---------------- DELETE USER ----------------
@app.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM users WHERE id=%s", (user_id,))
    conn.commit()

    if cursor.rowcount == 0:
        cursor.close()
        conn.close()
        return jsonify({"error": "User not found"}), 404

    cursor.close()
    conn.close()
    return jsonify({"message": "User deleted successfully"}), 200


# ---------------- RUN APP ----------------
if __name__ == "__main__":
    app.run(debug=True)
