from http.client import BAD_REQUEST


from flask import render_template, request

from til.utils import today
from til import idea
from til.start import app


@app.route('/')
def main():
    ideas = idea.get_all(date=today())
    return render_template('index.html', ideas=ideas)


@app.route("/idea", methods=["POST"])
def add_idea():
    new_idea = request.form["idea"]
    expanded_idea = idea.add(new_idea)
    return render_template('idea.html', idea=expanded_idea)


@app.route("/idea", methods=["DELETE"])
def delete_idea():
    idea_id = int(request.args["id"])
    idea.remove(idea_id)
    return {"id": idea_id}


@app.route("/idea", methods=["PUT"])
def update_idea():
    idea_id = request.form["id"]
    new_idea = request.form["idea"]

    updated_idea = idea.edit(idea_id, new_idea)
    return render_template('idea.html', idea=updated_idea)


if __name__ == '__main__':
    app.run(debug=True)
