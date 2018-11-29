from wsgi import db

class Product(db.Model):
    __tablename__ = "products"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    description = db.Column(db.Text())

    def __init__(self, product_name, product_desc):
        self.name = product_name
        self.description = product_desc

    def __repr__(self):
        return '<id {}>'.format(self.id)
