from config import db, ma

# Defines the TRAIL_FEATURE link table, which associates a trail with a feature
class TrailFeature(db.Model):
    __tablename__ = "TRAIL_FEATURE"
    __table_args__ = {"schema": "CW2"}

    TrailID = db.Column(db.Integer, db.ForeignKey("CW2.TRAIL.TrailID"), primary_key=True)
    TrailFeatureID = db.Column(db.Integer, db.ForeignKey("CW2.FEATURE.TrailFeatureID"), primary_key=True)

    # Optional realtionships for better cross-access if desired
    # trail = db.relationship("Trail", backref="trail_features", lazy='joined')
    # feature = db.relationship("Feature", backref="feature_trails", lazy='joined')

class TrailFeatureSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = TrailFeature
        include_fk = True
        include_relationships = True
        load_instance = True

trail_feature_schema = TrailFeatureSchema()
trail_features_schema = TrailFeatureSchema(many=True)
