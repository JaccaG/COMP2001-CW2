from config import db, ma

class Trail(db.Model):
    __tablename__ = "TRAIL"
    __table_args__ = {"schema": "CW2"}  # Specify schema

    TrailID = db.Column(db.Integer, primary_key=True)
    TrailName = db.Column(db.String(100), nullable=True)
    TrailSummary = db.Column(db.String(255), nullable=True)
    TrailDescription = db.Column(db.Text, nullable=True)
    Difficulty = db.Column(db.String(50), nullable=True)
    Location = db.Column(db.String(100), nullable=True)
    Length = db.Column(db.Float, nullable=True)
    ElevationGain = db.Column(db.Integer, nullable=True)
    RouteType = db.Column(db.String(50), nullable=True)
    OwnerID = db.Column(db.Integer, db.ForeignKey('CW2.USERS.UserID'), nullable=True)
    Pt1_Lat = db.Column(db.Float, nullable=True)
    Pt1_Long = db.Column(db.Float, nullable=True)
    Pt1_Desc = db.Column(db.String(255), nullable=True)
    Pt2_Lat = db.Column(db.Float, nullable=True)
    Pt2_Long = db.Column(db.Float, nullable=True)
    Pt2_Desc = db.Column(db.String(255), nullable=True)

    def to_dict(self):
        """Convert the model to a dictionary representation."""
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}

# Schema for serialization/deserialization
class TrailSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Trail
        include_relationships = True
        load_instance = True

trail_schema = TrailSchema()
trails_schema = TrailSchema(many=True)
