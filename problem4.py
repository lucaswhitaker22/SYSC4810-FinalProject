from problem2 import PasswordManager
from problem1 import AccessControl, Role, Permission
from flask import Flask, request, jsonify, session
from functools import wraps

app = Flask(__name__)
app.secret_key = 'your_secret_key_here' 

password_manager = PasswordManager()
access_control = AccessControl()

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            return jsonify({"error": "Unauthorized"}), 401
        return f(*args, **kwargs)
    return decorated_function

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    role = password_manager.verify_user(username, password)
    if role:
        session['username'] = username
        session['role'] = role
        return jsonify({"message": "Login successful", "role": role}), 200
    else:
        return jsonify({"error": "Invalid credentials"}), 401
    
@app.route('/logout', methods=['POST'])
@login_required
def logout():
    session.clear()
    return jsonify({"message": "Logout successful"}), 200

@app.route('/user_info', methods=['GET'])
@login_required
def user_info():
    username = session['username']
    role = Role[session['role']]
    permissions = access_control.get_user_permissions(role)
    return jsonify({
        "username": username,
        "role": role.name,
        "permissions": [perm.name for perm in permissions]
    }), 200

if __name__ == '__main__':
    app.run(debug=True)