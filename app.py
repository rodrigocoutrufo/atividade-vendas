from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'  # Certifique-se de que esse caminho está correto
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Modelos
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), nullable=False)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)

class Sale(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)

@app.route('/product', methods=['GET', 'POST'])
def product():
    if request.method == 'POST':
        # Implementação para criar um produto
        data = request.json
        name = data.get('name')
        stock = data.get('stock')
        price = data.get('price')

        if not name or stock is None or price is None:
            return jsonify({"message": "Nome, estoque e preço são obrigatórios."}), 400

        product = Product(name=name, stock=stock, price=price)
        db.session.add(product)
        db.session.commit()

        return jsonify({"message": "Produto criado com sucesso!", "product_id": product.id}), 201
    else:
        # Implementação para retornar todos os produtos
        products = Product.query.all()
        return jsonify([{"id": p.id, "name": p.name, "stock": p.stock, "price": str(p.price)} for p in products]), 200


@app.route('/sale', methods=['GET', 'POST'])
def sale():
    if request.method == 'POST':
        data = request.json
        user_id = data.get('user_id')
        product_id = data.get('product_id')
        quantity = data.get('quantity')

        # Verifica se o produto existe
        product = Product.query.get(product_id)
        if not product:
            return jsonify({"message": "Produto não encontrado."}), 404

        # Verifica se há estoque suficiente
        if product.stock < quantity:
            return jsonify({"message": "Estoque insuficiente."}), 400

        # Realiza a venda
        sale_price = product.price * quantity
        sale = Sale(user_id=user_id, product_id=product_id, quantity=quantity, price=sale_price)
        db.session.add(sale)

        # Atualiza o estoque do produto
        product.stock -= quantity
        db.session.commit()

        return jsonify({"message": "Venda realizada com sucesso!", "sale_id": sale.id}), 201
    else:
        # Implementação para retornar todas as vendas
        sales = Sale.query.all()
        return jsonify([{"id": s.id, "user_id": s.user_id, "product_id": s.product_id, "quantity": s.quantity, "price": s.price} for s in sales]), 200

@app.route('/product/<int:id>', methods=['DELETE'])
def delete_product(id):
    product = Product.query.get(id)
    
    if not product:
        return jsonify({"message": "Produto não encontrado."}), 404
    
    db.session.delete(product)
    db.session.commit()

    return jsonify({"message": "Produto deletado com sucesso!"}), 200

@app.route('/test', methods=['GET', 'POST'])
def test():
    return jsonify({"message": "Teste OK!"}), 200
    

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Cria as tabelas
    app.run(debug=True, port=5001)
