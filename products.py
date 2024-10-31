from flask import Blueprint, request, jsonify
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Product, Review
from auth import token_required, role_required

products_bp = Blueprint('products', __name__)

# Получить список всех продуктов
# Этот маршрут позволяет любому пользователю получить список всех доступных продуктов.
@products_bp.route('/products', methods=['GET'])
def list_products():
    db: Session = SessionLocal()
    products = db.query(Product).all()
    db.close()
    # Возвращаем список продуктов в формате JSON.
    return jsonify([{
        'id': product.id,
        'name': product.name,
        'description': product.description,
        'price': product.price
    } for product in products])

# Получить информацию о конкретном продукте
# Этот маршрут позволяет получить информацию о конкретном продукте по его идентификатору.
@products_bp.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    db: Session = SessionLocal()
    product = db.query(Product).filter_by(id=product_id).first()
    db.close()
    if product is None:
        return jsonify({'message': 'Product not found'}), 404
    # Возвращаем информацию о продукте в формате JSON.
    return jsonify({
        'id': product.id,
        'name': product.name,
        'description': product.description,
        'price': product.price
    })

# Добавить новый продукт (только для администраторов и продавцов)
# Этот маршрут позволяет администраторам и продавцам добавлять новые продукты.
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
    # Возвращаем сообщение о успешном добавлении продукта.
    return jsonify({'message': 'Product added successfully'}), 201

# Обновить продукт (только для администраторов и продавцов)
# Этот маршрут позволяет администраторам и продавцам обновлять существующие продукты по их идентификатору.
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
    # Обновляем данные продукта, если они указаны в запросе.
    product.name = data.get('name', product.name)
    product.description = data.get('description', product.description)
    product.price = data.get('price', product.price)

    db.commit()
    db.close()
    # Возвращаем сообщение о успешном обновлении продукта.
    return jsonify({'message': 'Product updated successfully'})

# Удалить продукт (только для администраторов и продавцов)
# Этот маршрут позволяет администраторам и продавцам удалять существующие продукты по их идентификатору.
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
    # Возвращаем сообщение о успешном удалении продукта.
    return jsonify({'message': 'Product deleted successfully'})

# Добавить отзыв к продукту
# Этот маршрут позволяет любому авторизованному пользователю добавлять отзыв к продукту.
@products_bp.route('/products/<int:product_id>/review', methods=['POST'])
@token_required
def add_review(current_user, product_id):
    data = request.get_json()
    new_review = Review(
        product_id=product_id,
        user_id=current_user.id,
        content=data['content'],
        rating=data['rating']
    )
    db: Session = SessionLocal()
    db.add(new_review)
    db.commit()
    db.close()
    # Возвращаем сообщение о успешном добавлении отзыва.
    return jsonify({'message': 'Review added successfully'}), 201

# Получить все отзывы для продукта
# Этот маршрут позволяет любому пользователю получить все отзывы, связанные с определенным продуктом.
@products_bp.route('/products/<int:product_id>/reviews', methods=['GET'])
def get_reviews(product_id):
    db: Session = SessionLocal()
    reviews = db.query(Review).filter_by(product_id=product_id).all()
    db.close()
    # Возвращаем список отзывов в формате JSON.
    return jsonify([{
        'id': review.id,
        'user_id': review.user_id,
        'content': review.content,
        'rating': review.rating
    } for review in reviews])

# Удалить отзыв (только администратор или автор отзыва)
# Этот маршрут позволяет удалять отзыв. Только администратор или автор отзыва могут это сделать.
@products_bp.route('/products/<int:product_id>/review/<int:review_id>', methods=['DELETE'])
@token_required
def delete_review(current_user, product_id, review_id):
    db: Session = SessionLocal()
    review = db.query(Review).filter_by(id=review_id, product_id=product_id).first()
    if review is None:
        db.close()
        return jsonify({'message': 'Review not found'}), 404

    # Проверка прав пользователя (администратор или автор отзыва)
    if current_user.role != 'admin' and current_user.id != review.user_id:
        db.close()
        return jsonify({'message': 'Permission denied'}), 403

    db.delete(review)
    db.commit()
    db.close()
    # Возвращаем сообщение о успешном удалении отзыва.
    return jsonify({'message': 'Review deleted successfully'})
