from flask import Flask, request, render_template, jsonify, Response
from flask_cors import CORS, cross_origin

import json

app = Flask(__name__)
CORS(app)
# name=y
customers = [{'id': 1, 'name': 'danny', 'address': 'tel-aviv', 'email': 'danny@tel-aviv.com'},
             {'id': 2, 'name': 'marina', 'address': 'beer sheav', 'email': 'marina@beer7.com'},
             {'id': 3, 'name': 'david', 'address': 'herzeliya', 'email': 'david@hertzelyia.com'}]

# localhost:5000/
# static page
# dynamic page
@app.route("/")
def home():
    return render_template('index.html')


# url/<resource> <--- GET POST
@app.route('/customers', methods=['GET', 'POST'])
def get_or_post_customer():
    print('***************************************************')
    if request.method == 'GET':
        # pseudo - select * from Customers
        # parsing
        # turn to json
        print(request.args.to_dict())
        search_args = request.args.to_dict()
        if len(search_args) == 0:
            return jsonify(customers)
        results = []
        for c in customers:
            if "name" in search_args.keys():
                if c["name"].find(search_args["name"]) < 0:
                    continue
            if "address" in search_args.keys() and \
                    c["address"].find(search_args["address"]) < 0:
                continue
            results.append(c)

        return jsonify(results)

    if request.method == 'POST':
        #  {'id': 4 [not be sent with DB], 'name': 'david', 'address': 'herzeliya'}
        new_customer = request.get_json()
        print('new_customer', new_customer)
        customers.append(new_customer)
        return '{"status": "success"}'

@app.route('/customers/<int:id>', methods=['GET', 'PUT', 'DELETE', 'PATCH'])
@cross_origin()
def get_customer_by_id(id):
    global customers
    if request.method == 'GET':
        # pseudo - select * from Customers where Customer.id == id
        # parsing
        # turn to json
        for c in customers:
            if c["id"] == id:
                return jsonify(c)
        return '{}'
    if request.method == 'PUT':
        #  {'id': 4 [not be sent with DB], 'name': 'david', 'address': 'herzeliya'}
        # 1. if not exist --> add
        # 2. if exist, update fields with given data
        # 3.           missing fields will have None value
        updated_new_customer = request.get_json()
        for c in customers:
            if c["id"] == id:
                c["id"] = updated_new_customer["id"] if "id" in updated_new_customer.keys() else None
                c["name"] = updated_new_customer["name"] if "name" in updated_new_customer.keys() else None
                c["address"] = updated_new_customer["address"] if "address" in updated_new_customer.keys() else None
                return jsonify(updated_new_customer)
        customers.append(updated_new_customer)
        return jsonify(updated_new_customer)
    if request.method == 'PATCH':
        #  {'id': 4 [not be sent with DB], 'name': 'david', 'address': 'herzeliya'}
        # 1. if not exist --> return
        # 2. if exist, update fields with given data
        # 3.           missing fields will remain the same
        updated_customer = request.get_json()
        for c in customers:
            if c["id"] == id:
                c["id"] = updated_customer["id"] if "id" in updated_customer.keys() else c["id"]
                c["name"] = updated_customer["name"] if "name" in updated_customer.keys() else c["name"]
                c["address"] = updated_customer["address"] if "address" in updated_customer.keys() else c["address"]
                return jsonify(updated_customer)
        return '{"status": "not found"}'
    if request.method == 'DELETE':
        customers = [c for c in customers if c["id"] != id]
        return jsonify(customers)

app.run(debug=True, port=5000)

