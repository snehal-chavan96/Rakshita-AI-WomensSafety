from werkzeug.security import generate_password_hash, check_password_hash
from database import db
import json

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)  # From Signup page
    email = db.Column(db.String(100), unique=True, nullable=False)  # From Signup page
    phone_number = db.Column(db.String(20), nullable=False)  # From Signup page
    password_hash = db.Column(db.String(200), nullable=False)  # From Signup page

    address = db.Column(db.String(300))  # From Personal Details page
    trusted_contacts = db.Column(db.Text)  # From Personal Details page, stored as JSON string

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def set_trusted_contacts(self, contacts_list):
        self.trusted_contacts = json.dumps(contacts_list)  # Example: ["9876543210", "9876543211"]

    def get_trusted_contacts(self):
        if self.trusted_contacts:
            return json.loads(self.trusted_contacts)
        return []



# from werkzeug.security import generate_password_hash, check_password_hash
# from database import db

# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(100), nullable=False)
#     email = db.Column(db.String(100), unique=True, nullable=False)
#     password_hash = db.Column(db.String(200), nullable=False)  # Store hashed password

#     def set_password(self, password):
#         self.password_hash = generate_password_hash(password)

#     def check_password(self, password):
#         return check_password_hash(self.password_hash, password)
