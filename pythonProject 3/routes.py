from buy import *
from sell import *
from user import *
from flask_cors import CORS  # Import CORS


app = Flask(__name__)
CORS(app)  # Enable CORS for the whole app


@app.route('/create_user', methods=['POST'])
def create_user():
    data = request.get_json()
    db = UserInfo()
    response, status_code = db.users(data)
    return jsonify(response), status_code


@app.route('/login_user', methods=['POST'])
def login_user():
    data = request.get_json()
    db = UserInfo()
    response, status_code = db.login(data)
    return jsonify(response), status_code


@app.route('/enter_purchase', methods=['POST', 'GET'])
def enter_purchase():
    data = request.get_json()
    db = PersonalInfo()
    response, status_code = db.purchase(data)
    return jsonify(response), status_code


@app.route('/view_purchase', methods=['POST', 'GET'])
def view_purchase():
    data = request.get_json()
    db = PersonalInfo()
    response, status_code = db.view_total_purchase(data)
    return jsonify(response), status_code


@app.route('/tot_sell_purchase', methods=['GET', 'POST'])
def tot_sell_purchase():
    data = request.get_json()
    db = PersonalInfo()
    response, status_code = db.total_sell_purchase(data)
    return jsonify(response), status_code


@app.route('/enter_sell', methods=['POST'])
def enter_sells():
    data = request.get_json()
    db = SellInfo()
    response, status_code = db.sell(data)
    return jsonify(response), status_code


@app.route('/view_sell', methods=['POST', 'GET'])
def view_sell():
    data = request.get_json()
    db = SellInfo()
    response, status_code = db.view_total_sell(data)
    return jsonify(response), status_code


if __name__ == "__main__":
    app.run(debug=True)