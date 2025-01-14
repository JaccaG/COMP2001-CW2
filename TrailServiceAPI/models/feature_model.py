from config import db, ma

# Represents the FEATURE table with a single colum describing the trail's features
class Feature(db.Model):
    __tablename__ = "FEATURE"
    __table_args__ = {"schema": "CW2"}

    TrailFeatureID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    TrailFeature = db.Column(db.String(100), nullable=True)

    # trail_features = db.relationship("TrailFeature", back_populates="feature")

class FeatureSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Feature
        include_relationships = True
        load_instance = True

feature_schema = FeatureSchema()
features_schema = FeatureSchema(many=True)
