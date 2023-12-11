from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///recipes.db'
db = SQLAlchemy(app)

class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    ingredients = db.Column(db.String(300), nullable=False)
    instructions = db.Column(db.String(500), nullable=False)

    def to_json(self):
        return {
            'id': self.id,
            'title': self.title,
            'ingredients': self.ingredients,
            'instructions': self.instructions
        }

@app.route('/recipes', methods=['GET', 'POST'])
def recipes():
    if request.method == 'GET':
        return jsonify([recipe.to_json() for recipe in Recipe.query.all()])
    elif request.method == 'POST':
        data = request.json
        new_recipe = Recipe(title=data['title'], ingredients=data['ingredients'], instructions=data['instructions'])
        db.session.add(new_recipe)
        db.session.commit()
        return jsonify(new_recipe.to_json()), 201

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
