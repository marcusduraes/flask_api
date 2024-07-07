from flask import Flask, jsonify, make_response, request
from db.database import create_db_and_tables, session
from db.models import User

app = Flask(__name__)


@app.route("/", methods=["GET"])
def index():
    with session as ss:
        user_list = ss.query(User).all()
        user_dicts = [{'id': user.id, 'name': user.name, 'role': user.role} for user in user_list]
        return make_response(jsonify(user_dicts), 200)


@app.route("/<int:user_id>", methods=["GET"])
def get_by_id(user_id):
    with session as ss:
        users = ss.query(User).all()
        users_dict = [{'id': user.id, 'name': user.name, 'role': user.role} for user in users]
        user = next((i for i in users_dict if i["id"] == user_id), None)
        if user:
            return make_response(jsonify(user), 200)
        else:
            return make_response(jsonify({"error": "User not found"}), 404)


@app.route("/", methods=["POST"])
def create():
    body = request.get_json()

    required_fields = ["role", "name"]
    for i in required_fields:
        if i not in body:
            return make_response(jsonify({"error": f"Missing required field: {i}"}), 400)

    with session as ss:
        role, name = body['role'], body['name']
        user = User(role=role, name=name)
        ss.add(user)
        ss.commit()
        return make_response(jsonify({"id": user.id, "name": user.name, "role": user.role}), 201)


if __name__ == '__main__':
    create_db_and_tables()
    app.run(debug=True, host='0.0.0.0', port=8080)
