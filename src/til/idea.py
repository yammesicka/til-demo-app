from sqlalchemy.sql import delete, func, select, update

from til.utils import today
from til import ai
from til.schema import Idea, IdeaTag, Tag
from til.start import db


def normalize(db_idea: Idea) -> dict[str, str]:
    return {
        "id": db_idea.id,
        "title": db_idea.title,
        "description": db_idea.description,
        "icon": db_idea.icon,
        "background_color": db_idea.background_color,
    }


def get_all(date: str | None) -> list[dict[str, str]]:
    date = date or today()
    query = (
        select(Idea).
        where(func.date(Idea.date) == date).
        order_by(Idea.date.desc())
    )
    db_ideas = db.session.execute(query).scalars().all()
    ideas = [normalize(db_idea) for db_idea in db_ideas]
    return ideas


def _normalize_expanded(
    new_idea: str,
    expanded: dict[str, str | list[str]],
) -> dict[str, str | list[str]]:
    return {
        "title": expanded["title"],
        "description": new_idea,
        "icon": expanded["unicode_emoji"],
        "background_color": expanded["background_color"],
        "tags": Tag.get_or_create_many(expanded["tags"]),
    }


def add(new_idea: str):
    expanded = ai.expand_idea(new_idea)
    expanded_idea = _normalize_expanded(new_idea, expanded)

    added_idea = Idea(**expanded_idea)
    db.session.add(added_idea)
    db.session.commit()

    return {"id": added_idea.id, **expanded_idea}


def edit(idea_id: int, new_idea: str):
    query = delete(IdeaTag).where(IdeaTag.idea_id == idea_id)
    db.session.execute(query)

    expanded = ai.expand_idea(new_idea)
    expanded_idea = _normalize_expanded(new_idea, expanded)

    query = update(Idea).where(Idea.id == idea_id).values(**expanded_idea)
    db.session.execute(query)
    db.session.commit()

    return {"id": idea_id, **expanded_idea}


def remove(idea_id: int):
    query = delete(Idea).where(Idea.id == idea_id)
    db.session.execute(query)
    db.session.commit()
