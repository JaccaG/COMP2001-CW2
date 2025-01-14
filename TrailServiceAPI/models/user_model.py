from config import db, ma

# Defines a User model corresponding to the USERS table in the CW2 schema
class User(db.Model):
    __tablename__ = "USERS"
    __table_args__ = {"schema": "CW2"}

    UserID = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(100), nullable=True)
    Email_address = db.Column(db.String(255), unique=True, nullable=False)
    Password = db.Column(db.String(255), nullable=False)
    Role = db.Column(db.String(50), nullable=True)

# Sets up a schema to serialize and deserialize User objects
class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        include_relationships = True
        load_instance = True

# Creates instances of the schema for single and multiple users
user_schema = UserSchema()
users_schema = UserSchema(many=True)
