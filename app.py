from flask import Flask, jsonify, request, g
from flask_cors import CORS
import sqlite3
import os

app = Flask(__name__)
CORS(app)
DATABASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'test_database.db')
def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row  # This ensures rows can be accessed like dictionaries
    return g.db

@app.teardown_appcontext
def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

# Initialize the database (optional)
def init_db():
    with app.app_context():
        db = get_db()
        db.execute('''CREATE TABLE IF NOT EXISTS products (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        product TEXT NOT NULL,
                        price REAL NOT NULL
                      )''')
        db.commit()

# Initialize the database (call only once or when needed)
init_db()

### Routes ###

# a simplee html script
@app.route('/webapp')
def get_webapp():
    #return jsonify({'message': 'Hello, World!'})
    return ('''
        <!DOCTYPE html>
        <html lang='en'>
            <head></head>
            <body>
               <h1>Hello world</h1>
            </body>
        </html>
    '''
    )

# GET: Retrieve all products
@app.route('/products', methods=['GET'])
def get_products():
    db = get_db()
    cursor = db.execute('SELECT * FROM products;')
    products = cursor.fetchall()

    # Convert each row into a dictionary
    return jsonify([dict(row) for row in products])

# POST: Add a new product
@app.route('/products', methods=['POST'])
def add_product():
    data = request.json
    product_name = data.get('product')
    price = data.get('price')

    if not product_name or not price:
        return jsonify({'error': 'Product name and price are required'}), 400

    db = get_db()
    db.execute('INSERT INTO products (product, price) VALUES (?, ?)', (product_name, price))
    db.commit()

    return jsonify({'message': 'Product added successfully'}), 201

# PATCH: Update a product
@app.route('/products/<int:product_id>', methods=['PATCH'])
def update_product(product_id):
    data = request.json
    product_name = data.get('product')
    price = data.get('price')

    if not product_name and not price:
        return jsonify({'error': 'Nothing to update'}), 400

    db = get_db()
    # Build dynamic SQL query based on provided data
    if product_name:
        db.execute('UPDATE products SET product = ? WHERE id = ?', (product_name, product_id))
    if price:
        db.execute('UPDATE products SET price = ? WHERE id = ?', (price, product_id))
    db.commit()

    return jsonify({'message': 'Product updated successfully'}), 200

# DELETE: Delete a product
@app.route('/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    db = get_db()
    db.execute('DELETE FROM products WHERE id = ?', (product_id,))
    db.commit()
    return jsonify({'message': 'Product with id {} deleted successfully'.format(product_id)}), 200

# GET: a single product info
@app.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    db = get_db()
    
    # Fetch a single product based on its ID
    cursor = db.execute('SELECT * FROM products WHERE id = ?', (product_id,))
    product = cursor.fetchone()  # Use fetchone() instead of fetchall()

    # Check if product exists
    if product is None:
        return jsonify({'error': 'Product not found'}), 404

    # Convert the row to a dictionary
    return jsonify(dict(product))


if __name__ == '__main__':
    app.run(debug=True)