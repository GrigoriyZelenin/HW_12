import logging
from json import JSONDecodeError

from flask import Blueprint, render_template, request

from functions import get_posts_by_str

main_blueprint = Blueprint('main_blueprint', __name__, template_folder='templates')


@main_blueprint.route('/')
def main_page():
    return render_template('index.html')

@main_blueprint.route('/search/')
def search_page():
    logging.info("Выполняю поиск")
    search_query = request.args.get('s', '')
    try:
        posts = get_posts_by_str(search_query)
    except FileNotFoundError:
        logging.error("Файл не найден")
        return "Файл не найден"
    except JSONDecodeError:
        return "невалидный файл"
    return render_template('post_list.html', posts=posts, query=search_query)