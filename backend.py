from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/login', methods=['POST'])
def authenticate():
    data = request.json
    username = data.get('email')
    password = data.get('password')
    # Hardcoded username and password for demonstration purposes
    if username == "admin" and password == "password":
        response = {"success": True, "message": "Authentication successful."}
    else:
        response = {"success": False, "message": "Invalid username or password."}

    return jsonify(response)

if __name__ == "__main__":
    app.run(debug=True)
