
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///budget.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# SQLAlchemy model for items
class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    date = db.Column(db.String(20), nullable=False)
    notes = db.Column(db.String(200))
    paid = db.Column(db.Boolean, default=False)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'category': self.category,
            'amount': self.amount,
            'date': self.date,
            'notes': self.notes,
            'paid': self.paid
        }


@app.route('/api/items', methods=['GET'])
def get_items():
    items = Item.query.all()
    return jsonify([item.to_dict() for item in items])


@app.route('/api/items', methods=['POST'])
def add_item():
    data = request.get_json()
    item = Item(
        name=data.get('name'),
        category=data.get('category'),
        amount=float(data.get('amount', 0)),
        date=data.get('date'),
        notes=data.get('notes', ''),
        paid=bool(data.get('paid', False))
    )
    db.session.add(item)
    db.session.commit()
    return jsonify({'success': True, 'item': item.to_dict()}), 201


@app.route('/api/items/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    data = request.get_json()
    item = Item.query.get(item_id)
    if item:
        item.name = data.get('name', item.name)
        item.category = data.get('category', item.category)
        item.amount = float(data.get('amount', item.amount))
        item.date = data.get('date', item.date)
        item.notes = data.get('notes', item.notes)
        item.paid = bool(data.get('paid', item.paid))
        db.session.commit()
        return jsonify({'success': True, 'item': item.to_dict()})
    return jsonify({'success': False, 'error': 'Item not found'}), 404


@app.route('/api/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    item = Item.query.get(item_id)
    if item:
        db.session.delete(item)
        db.session.commit()
        return jsonify({'success': True, 'item': item.to_dict()})
    return jsonify({'success': False, 'error': 'Item not found'}), 404


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5001)
