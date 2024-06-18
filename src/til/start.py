from pathlib import Path
import logging

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import openai

from til import utils


ROOT = Path(__file__).resolve().parent.parent
logger = logging.getLogger(__name__)


app = Flask(
    __name__,
    template_folder=ROOT / 'templates',
    static_folder=ROOT / 'static',
)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///til.db'

env = utils.load_env(ROOT.parent / '.env')
if not env.get('OPENAI_API_KEY'):
    logger.critical('OPENAI_API_KEY is required')
    raise RuntimeError('OPENAI_API_KEY is required')

ai_client = openai.OpenAI(api_key=env['OPENAI_API_KEY'])
db = SQLAlchemy(app)
