from flask_sqlalchemy import SQLAlchemy

# Initialize the database instance
db = SQLAlchemy()

# Define the BakeryItem model for SQLAlchemy
class BakeryItem(db.Model):
    __tablename__ = 'bakery_items'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    category = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f"<BakeryItem {self.name}>"
    
    def to_dict(self):
        """Helper function to convert BakeryItem instance to dictionary for GraphQL."""
        return {
            'id': self.id,
            'name': self.name,
            'price': self.price,
            'quantity': self.quantity,
            'category': self.category
        }
