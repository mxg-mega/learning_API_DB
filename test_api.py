from flask import Flask, jsonify, request

app = Flask(__name__)

# Dummy data
products = [
    {'id': 1, 'name': 'Product 1', 'price': 10, 'quantity': 100},
    {'id': 2, 'name': 'Product 2', 'price': 20, 'quantity': 50}
]

# API to get all products
@app.route('/products', methods=['GET'])
def get_products():
    return jsonify(products)

# API to add a new product
@app.route('/products', methods=['POST'])
def add_product():
    new_product = request.get_json()
    products.append(new_product)
    return jsonify({'message': 'Product added successfully!'}), 201

@app.route('/products', methods=['PATCH'])
def update_product():
    product_id = request.args.get('id')
    print(product_id)
    for i in range(len(products)):
        print(type(products[i]['id']))
        # print(i)
        if str(products[i]['id']) == product_id:
            print("finally")
            products[i].update(request.get_json())
            break

    return jsonify({"message": "Product updated succesfully!"}), 200
                


if __name__ == '__main__':
    app.run(debug=True)
