from flask import Blueprint, jsonify, request
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Category, Product, ProductImage
from auth import token_required, role_required
from sqlalchemy.orm import joinedload
from flask import current_app
import os

categories_bp = Blueprint('categories', __name__)

def get_image_url(filename):
    return f"{current_app.config['BASE_URL']}/static/uploads/{filename}"

@categories_bp.route('/categories', methods=['GET'])
def list_categories():
    """List all product categories
    ---
    tags:
      - Categories
    responses:
      200:
        description: List of categories
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
    """
    db = SessionLocal()
    categories = db.query(Category).all()
    db.close()
    return jsonify([{
        'id': category.id,
        'name': category.name,
        'description': category.description
    } for category in categories])

@categories_bp.route('/categories', methods=['POST'])
@token_required
@role_required('admin', 'seller')
def add_category(current_user):
    """Add a new product category
    ---
    tags:
      - Categories
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
              description: Category name
            description:
              type: string
              description: Category description
    responses:
      201:
        description: Category created
      403:
        description: Permission denied
    """
    data = request.get_json()
    new_category = Category(name=data['name'], description=data['description'])
    db = SessionLocal()
    db.add(new_category)
    db.commit()
    db.close()
    return jsonify({'message': 'Category added successfully'}), 201

@categories_bp.route('/categories/<int:category_id>', methods=['PUT'])
@token_required
@role_required('admin')
def update_category(current_user, category_id):
    """Update a product category
    ---
    tags:
      - Categories
    security:
      - Bearer: []
    parameters:
      - name: category_id
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
              description: New category name
            description:
              type: string
              description: New category description
    responses:
      200:
        description: Category updated
      404:
        description: Category not found
      403:
        description: Permission denied
    """
    db = SessionLocal()
    category = db.query(Category).filter_by(id=category_id).first()
    if not category:
        db.close()
        return jsonify({'message': 'Category not found'}), 404

    data = request.get_json()
    category.name = data.get('name', category.name)
    category.description = data.get('description', category.description)
    db.commit()
    db.close()
    return jsonify({'message': 'Category updated successfully'})

@categories_bp.route('/categories/<int:category_id>', methods=['DELETE'])
@token_required
@role_required('admin')
def delete_category(current_user, category_id):
    """Delete a product category
    ---
    tags:
      - Categories
    security:
      - Bearer: []
    parameters:
      - name: category_id
        in: path
        required: true
        type: integer
    responses:
      200:
        description: Category deleted
      404:
        description: Category not found
      403:
        description: Permission denied
    """
    db = SessionLocal()
    category = db.query(Category).filter_by(id=category_id).first()
    if not category:
        db.close()
        return jsonify({'message': 'Category not found'}), 404

    db.delete(category)
    db.commit()
    db.close()
    return jsonify({'message': 'Category deleted successfully'})


@categories_bp.route('/categories/<int:category_id>/products', methods=['GET'])
def list_products_in_category(category_id):
    """Получить список продуктов в категории
    ---
    tags:
      - Categories
    parameters:
      - name: category_id
        in: path
        required: true
        type: integer
        description: ID категории
    responses:
      200:
        description: Список продуктов в категории
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
      404:
        description: Категория не найдена
    """
    db = SessionLocal()
    category = db.query(Category).filter_by(id=category_id).first()
    if not category:
        db.close()
        return jsonify({'message': 'Category not found'}), 404

    # Подгружаем связанные изображения с продуктами
    products = db.query(Product).options(joinedload(Product.images)).filter_by(category_id=category_id).all()

    product_list = [{
        'id': product.id,
        'name': product.name,
        'description': product.description,
        'price': product.price,
        'category_id': product.category_id,
        'image_url': get_image_url(product.images[0].image_url) if product.images else None
    } for product in products]

    db.close()
    return jsonify(product_list)
