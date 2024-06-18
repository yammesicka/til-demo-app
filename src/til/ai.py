import json
import textwrap

from til.start import ai_client
from til.errors import TilAiCantExpandIdeaError


CREATE_IDEA_SYSTEM_PROMPT = textwrap.dedent("""
    You are a helpful assistant designed to output JSON.
    I'm going to give you an item called "Thing I learned today".
    You can greatly help me by providing a JSON (only json)
    with the following fields, which must describe the idea
    the user sent you in the best way possible. Be expressive
    and smart in your choices:

    - title
    - unicode_emoji
    - background_color
    - tags

    Remember! You can only provide JSON.
    Don't provide any other type of data.
    Don't say anything other than the JSON.
    Your response should be a valid JSON.
""").strip()


def expand_idea(idea):
    completion = ai_client.chat.completions.create(
        model="gpt-4o",
        max_tokens=100,
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": CREATE_IDEA_SYSTEM_PROMPT},
            {"role": "user", "content": idea}
        ]
    )

    if expanded_idea := completion.choices[0].message.content:
        return json.loads(expanded_idea)

    raise TilAiCantExpandIdeaError(f"I can't expand the {idea=}.")
