from collections.abc import Iterable

from sqlalchemy.sql import insert
from til.start import app, db
from til.utils import datetime_now


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    # ideas = db.relationship("Idea", backref="author", lazy=True)


class Idea(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # Currently we don't use users
    # user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    date = db.Column(db.DateTime, default=datetime_now)
    last_modified = db.Column(
        db.DateTime,
        default=datetime_now,
        onupdate=datetime_now,
    )
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    icon = db.Column(db.String(50), nullable=True)
    background_color = db.Column(db.String(9), default="#FFFFFF")
    tags = db.relationship(
        "Tag",
        secondary="idea_tag",
        backref=db.backref("ideas", lazy=True),
    )

    def __str__(self):
        return f"<Idea {self.title}>"


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)

    @classmethod
    def get_or_create_many(cls, tag_names: Iterable[str]):
        existing_tags = Tag.query.filter(Tag.name.in_(tag_names)).all()
        existing_tag_names = {tag.name for tag in existing_tags}

        new_tags = [
            Tag(name=name)
            for name in tag_names
            if name not in existing_tag_names
        ]

        db.session.add_all(new_tags)
        db.session.commit()

        return existing_tags + new_tags


class IdeaTag(db.Model):
    __tablename__ = "idea_tag"
    idea_id = db.Column(db.Integer, db.ForeignKey("idea.id"), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey("tag.id"), primary_key=True)


with app.app_context():
    db.create_all()
