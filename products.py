from flask import Blueprint, request, jsonify
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Product
from auth import token_required, role_required

products_bp = Blueprint('products', __name__)

# Получить список всех продуктов
@products_bp.route('/products', methods=['GET'])
def list_products():
    db: Session = SessionLocal()
    products = db.query(Product).all()
    db.close()
    return jsonify([{
        'id': product.id,
        'name': product.name,
        'description': product.description,
        'price': product.price
    } for product in products])

# Получить информацию о конкретном продукте
@products_bp.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    db: Session = SessionLocal()
    product = db.query(Product).filter_by(id=product_id).first()
    db.close()
    if product is None:
        return jsonify({'message': 'Product not found'}), 404
    return jsonify({
        'id': product.id,
        'name': product.name,
        'description': product.description,
        'price': product.price
    })

# Добавить новый продукт (только для администраторов и продавцов)
@products_bp.route('/products', methods=['POST'])
@token_required
@role_required('admin', 'seller')
def add_product(current_user):
    data = request.get_json()
    new_product = Product(
        name=data['name'],
        description=data['description'],
        price=data['price']
    )
    db: Session = SessionLocal()
    db.add(new_product)
    db.commit()
    db.close()
    return jsonify({'message': 'Product added successfully'}), 201

# Обновить продукт (только для администраторов и продавцов)
@products_bp.route('/products/<int:product_id>', methods=['PUT'])
@token_required
@role_required('admin', 'seller')
def update_product(current_user, product_id):
    db: Session = SessionLocal()
    product = db.query(Product).filter_by(id=product_id).first()
    if product is None:
        db.close()
        return jsonify({'message': 'Product not found'}), 404

    data = request.get_json()
    product.name = data.get('name', product.name)
    product.description = data.get('description', product.description)
    product.price = data.get('price', product.price)

    db.commit()
    db.close()
    return jsonify({'message': 'Product updated successfully'})

# Удалить продукт (только для администраторов и продавцов)
@products_bp.route('/products/<int:product_id>', methods=['DELETE'])
@token_required
@role_required('admin', 'seller')
def delete_product(current_user, product_id):
    db: Session = SessionLocal()
    product = db.query(Product).filter_by(id=product_id).first()
    if product is None:
        db.close()
        return jsonify({'message': 'Product not found'}), 404

    db.delete(product)
    db.commit()
    db.close()
    return jsonify({'message': 'Product deleted successfully'})
