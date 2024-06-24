from flask import Blueprint, request, jsonify, send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash
from models import User, Recipe
from extensions import db
import os

main = Blueprint('main', __name__)

@main.route('/api/signup', methods=['POST'])
def signup():
    data = request.get_json()
    username = data['username']
    password = generate_password_hash(data['password'], method='sha256')

    new_user = User(username=username, password=password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'user': {'username': new_user.username}})

@main.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()

    if not user or not check_password_hash(user.password, data['password']):
        return jsonify({'error': 'Invalid credentials'}), 401

    return jsonify({'user': {'username': user.username}})

@main.route('/api/recipes', methods=['GET'])
def get_recipes():
    recipes = Recipe.query.all()
    recipe_list = [{'id': recipe.id, 'title': recipe.title, 'ingredients': recipe.ingredients, 'instructions': recipe.instructions, 'category': recipe.category, 'image': recipe.image} for recipe in recipes]
    return jsonify(recipe_list)

@main.route('/api/recipes', methods=['POST'])
def add_recipe():
    data = request.form
    file = request.files.get('image')

    if file:
        file_path = os.path.join('static/uploads', file.filename)
        file.save(file_path)

    new_recipe = Recipe(
        title=data['title'],
        ingredients=data['ingredients'],
        instructions=data['instructions'],
        category=data['category'],
        image=file.filename if file else None,
        user_id=1  # Assuming user_id 1 for simplicity
    )

    db.session.add(new_recipe)
    db.session.commit()

    return jsonify({'message': 'Recipe added successfully'})

@main.route('/uploads/<filename>')
def upload(filename):
    return send_from_directory('static/uploads', filename)
