from flask import Flask, jsonify, make_response, request

app = Flask(__name__)
data = []


@app.route("/", methods=["GET"])
def index():
    response = make_response(jsonify(data), 200)
    return response


@app.route("/<int:user_id>", methods=["GET"])
def get_by_id(user_id):
    user = next((i for i in data if i["id"] == user_id), None)
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

    row = {"id": len(data) + 1, **body}
    data.append(row)
    return make_response(jsonify(data), 201)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)

