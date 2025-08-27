from flask import Flask, request, jsonify
import mysql.connector

app = Flask(__name__)

# Configure MariaDB connection
db_config = {
    "host": "maria-db",
    "user": "root",
    "password": "wHu8QBfsjxcx6186Ko4FhkbS",
    "database": "gifted_greider"
}

# Helper function
def get_db_connection():
    return mysql.connector.connect(**db_config)


# CREATE
@app.route("/personal", methods=["POST"])
def create_person():
    data = request.json
    name = data.get("name")
    age = data.get("age")
    email = data.get("email")

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO personal (name, age, email) VALUES (%s, %s, %s)",
                   (name, age, email))
    conn.commit()
    new_id = cursor.lastrowid
    cursor.close()
    conn.close()
    return jsonify({"id": new_id, "message": "Person created"}), 201


# READ all
@app.route("/personal", methods=["GET"])
def get_all_persons():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM personal")
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(result)


# READ one
@app.route("/personal/<int:person_id>", methods=["GET"])
def get_person(person_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM personal WHERE id = %s", (person_id,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    if result:
        return jsonify(result)
    return jsonify({"error": "Person not found"}), 404


# UPDATE
@app.route("/personal/<int:person_id>", methods=["PUT"])
def update_person(person_id):
    data = request.json
    name = data.get("name")
    age = data.get("age")
    email = data.get("email")

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE personal SET name=%s, age=%s, email=%s WHERE id=%s
    """, (name, age, email, person_id))
    conn.commit()
    cursor.close()
    conn.close()

    if cursor.rowcount == 0:
        return jsonify({"error": "Person not found"}), 404

    return jsonify({"message": "Person updated"})


# DELETE
@app.route("/personal/<int:person_id>", methods=["DELETE"])
def delete_person(person_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM personal WHERE id = %s", (person_id,))
    conn.commit()
    cursor.close()
    conn.close()

    if cursor.rowcount == 0:
        return jsonify({"error": "Person not found"}), 404

    return jsonify({"message": "Person deleted"})


if __name__ == "__main__":
    app.run(debug=True)
