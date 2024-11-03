from flask import Blueprint, request, jsonify
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Product, Review
from auth import token_required, role_required

products_bp = Blueprint('products', __name__)

@products_bp.route('/products', methods=['GET'])
def list_products():
    """Получить список всех продуктов
    ---
    tags:
      - Products
    responses:
      200:
        description: Список продуктов
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
              name:
                type: string
              description:
                type: string
              price:
                type: number
    """
    db: Session = SessionLocal()
    products = db.query(Product).all()
    db.close()
    return jsonify([{
        'id': product.id,
        'name': product.name,
        'description': product.description,
        'price': product.price
    } for product in products])

@products_bp.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    """Получить информацию о конкретном продукте
    ---
    tags:
      - Products
    parameters:
      - name: product_id
        in: path
        required: true
        type: integer
    responses:
      200:
        description: Информация о продукте
        schema:
          type: object
          properties:
            id:
              type: integer
            name:
              type: string
            description:
              type: string
            price:
              type: number
      404:
        description: Продукт не найден
    """
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

@products_bp.route('/products', methods=['POST'])
@token_required
@role_required('admin', 'seller')
def add_product(current_user):
    """Добавить новый продукт (только для администраторов и продавцов)
    ---
    tags:
      - Products
    security:
      - Bearer: []
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            name:
              type: string
              description: Название продукта
            description:
              type: string
              description: Описание продукта
            price:
              type: number
              description: Цена продукта
    responses:
      201:
        description: Продукт успешно добавлен
      403:
        description: Недостаточно прав
    """
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

@products_bp.route('/products/<int:product_id>', methods=['PUT'])
@token_required
@role_required('admin', 'seller')
def update_product(current_user, product_id):
    """Обновить продукт (только для администраторов и продавцов)
    ---
    tags:
      - Products
    security:
      - Bearer: []
    parameters:
      - name: product_id
        in: path
        required: true
        type: integer
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            name:
              type: string
            description:
              type: string
            price:
              type: number
    responses:
      200:
        description: Продукт успешно обновлен
      404:
        description: Продукт не найден
      403:
        description: Недостаточно прав
    """
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

@products_bp.route('/products/<int:product_id>', methods=['DELETE'])
@token_required
@role_required('admin', 'seller')
def delete_product(current_user, product_id):
    """Удалить продукт (только для администраторов и продавцов)
    ---
    tags:
      - Products
    security:
      - Bearer: []
    parameters:
      - name: product_id
        in: path
        required: true
        type: integer
    responses:
      200:
        description: Продукт успешно удален
      404:
        description: Продукт не найден
      403:
        description: Недостаточно прав
    """
    db: Session = SessionLocal()
    product = db.query(Product).filter_by(id=product_id).first()
    if product is None:
        db.close()
        return jsonify({'message': 'Product not found'}), 404

    db.delete(product)
    db.commit()
    db.close()
    return jsonify({'message': 'Product deleted successfully'})

@products_bp.route('/products/<int:product_id>/review', methods=['POST'])
@token_required
def add_review(current_user, product_id):
    """Добавить отзыв к продукту
    ---
    tags:
      - Reviews
    security:
      - Bearer: []
    parameters:
      - name: product_id
        in: path
        required: true
        type: integer
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            content:
              type: string
            rating:
              type: integer
    responses:
      201:
        description: Отзыв успешно добавлен
      404:
        description: Продукт не найден
      403:
        description: Недостаточно прав
    """
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
    return jsonify({'message': 'Review added successfully'}), 201

@products_bp.route('/products/<int:product_id>/reviews', methods=['GET'])
def get_reviews(product_id):
    """Получить все отзывы для продукта
    ---
    tags:
      - Reviews
    parameters:
      - name: product_id
        in: path
        required: true
        type: integer
    responses:
      200:
        description: Список отзывов
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
              user_id:
                type: integer
              content:
                type: string
              rating:
                type: integer
    """
    db: Session = SessionLocal()
    reviews = db.query(Review).filter_by(product_id=product_id).all()
    db.close()
    return jsonify([{
        'id': review.id,
        'user_id': review.user_id,
        'content': review.content,
        'rating': review.rating
    } for review in reviews])

@products_bp.route('/products/<int:product_id>/review/<int:review_id>', methods=['DELETE'])
@token_required
def delete_review(current_user, product_id, review_id):
    """Удалить отзыв (только администратор или автор отзыва)
    ---
    tags:
      - Reviews
    security:
      - Bearer: []
    parameters:
      - name: product_id
        in: path
        required: true
        type: integer
      - name: review_id
        in: path
        required: true
        type: integer
    responses:
      200:
        description: Отзыв успешно удален
      404:
        description: Отзыв не найден
      403:
        description: Недостаточно прав
    """
    db: Session = SessionLocal()
    review = db.query(Review).filter_by(id=review_id, product_id=product_id).first()
    if review is None:
        db.close()
        return jsonify({'message': 'Review not found'}), 404

    if current_user.role != 'admin' and current_user.id != review.user_id:
        db.close()
        return jsonify({'message': 'Permission denied'}), 403

    db.delete(review)
    db.commit()
    db.close()
    return jsonify({'message': 'Review deleted successfully'})
