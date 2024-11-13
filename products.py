from flask import Blueprint, request, jsonify, current_app
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Product, Review, ProductImage
from auth import token_required, role_required
from werkzeug.utils import secure_filename
import os

products_bp = Blueprint('products', __name__)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

def save_image(file):
    filename = secure_filename(file.filename)
    file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)
    return file_path

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
              category_id:
                type: integer
              image_url:
                type: string
                description: URL изображения продукта
    """
    db = SessionLocal()
    products = db.query(Product).all()
    product_list = [{
        'id': product.id,
        'name': product.name,
        'description': product.description,
        'price': product.price,
        'category_id': product.category_id,
        'image_url': product.images[0].image_url if product.images else None
    } for product in products]
    db.close()
    return jsonify(product_list)

@products_bp.route('/products', methods=['POST'])
@token_required
@role_required('admin', 'seller')
def add_product(current_user):
    """Добавить новый продукт (только для администраторов и продавцов)
    ---
    tags:
      - Products
    consumes:
      - multipart/form-data
    parameters:
      - name: name
        in: formData
        type: string
        required: true
        description: Название продукта
      - name: description
        in: formData
        type: string
        required: true
        description: Описание продукта
      - name: price
        in: formData
        type: number
        required: true
        description: Цена продукта
      - name: category_id
        in: formData
        type: integer
        required: true
        description: ID категории
      - name: image
        in: formData
        type: file
        required: false
        description: Изображение продукта
    responses:
      201:
        description: Продукт успешно добавлен
      403:
        description: Недостаточно прав
    """
    data = request.form
    new_product = Product(
        name=data['name'],
        description=data['description'],
        price=float(data['price']),
        category_id=int(data['category_id'])
    )

    db = SessionLocal()
    db.add(new_product)
    db.commit()

    if 'image' in request.files and allowed_file(request.files['image'].filename):
        file = request.files['image']
        file_path = save_image(file)
        product_image = ProductImage(product_id=new_product.id, image_url=file_path)
        db.add(product_image)
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
    consumes:
      - multipart/form-data
    parameters:
      - name: product_id
        in: path
        required: true
        type: integer
      - name: name
        in: formData
        type: string
        description: Новое название продукта
      - name: description
        in: formData
        type: string
        description: Новое описание продукта
      - name: price
        in: formData
        type: number
        description: Новая цена продукта
      - name: category_id
        in: formData
        type: integer
        description: Новый ID категории
      - name: image
        in: formData
        type: file
        description: Новое изображение продукта
    responses:
      200:
        description: Продукт успешно обновлен
      404:
        description: Продукт не найден
      403:
        description: Недостаточно прав
    """
    db = SessionLocal()
    product = db.query(Product).filter_by(id=product_id).first()
    if not product:
        db.close()
        return jsonify({'message': 'Product not found'}), 404

    data = request.form
    product.name = data.get('name', product.name)
    product.description = data.get('description', product.description)
    product.price = float(data.get('price', product.price))
    product.category_id = int(data.get('category_id', product.category_id))

    if 'image' in request.files and allowed_file(request.files['image'].filename):
        file = request.files['image']
        file_path = save_image(file)
        product_image = db.query(ProductImage).filter_by(product_id=product_id).first()
        if product_image:
            product_image.image_url = file_path
        else:
            new_image = ProductImage(product_id=product_id, image_url=file_path)
            db.add(new_image)

    db.commit()
    db.close()
    return jsonify({'message': 'Product updated successfully'})

@products_bp.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    """Получить информацию о продукте
    ---
    tags:
      - Products
    parameters:
      - name: product_id
        in: path
        required: true
        type: integer
        description: ID продукта
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
            category_id:
              type: integer
            image_url:
              type: string
              description: URL изображения продукта
      404:
        description: Продукт не найден
    """
    db = SessionLocal()
    product = db.query(Product).filter_by(id=product_id).first()
    if not product:
        db.close()
        return jsonify({'message': 'Product not found'}), 404

    image_url = product.images[0].image_url if product.images else None
    product_data = {
        'id': product.id,
        'name': product.name,
        'description': product.description,
        'price': product.price,
        'category_id': product.category_id,
        'image_url': image_url
    }
    db.close()
    return jsonify(product_data)

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
    db = SessionLocal()
    product = db.query(Product).filter_by(id=product_id).first()
    if not product:
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
    """
    data = request.get_json()
    new_review = Review(
        product_id=product_id,
        user_id=current_user.id,
        content=data['content'],
        rating=data['rating']
    )
    db = SessionLocal()
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
    db = SessionLocal()
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
    db = SessionLocal()
    review = db.query(Review).filter_by(id=review_id, product_id=product_id).first()
    if not review:
        db.close()
        return jsonify({'message': 'Review not found'}), 404

    if current_user.role != 'admin' and current_user.id != review.user_id:
        db.close()
        return jsonify({'message': 'Permission denied'}), 403

    db.delete(review)
    db.commit()
    db.close()
    return jsonify({'message': 'Review deleted successfully'})
