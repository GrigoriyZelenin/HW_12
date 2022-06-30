from json import JSONDecodeError

from flask import Blueprint, render_template, request, logging

from functions import add_post
from loader.utils import save_picture

loader_blueprint = Blueprint('loader_blueprint', __name__, template_folder='templates')


@loader_blueprint.route('/post')
def post_page():
    return render_template('post_form.html')

@loader_blueprint.route('/post', methods=['POST'])
def add_post_page():
    picture = request.files.get('picture')
    content = request.form.get('content')

    if not picture or not content:
        return "Отсутствует картинка или текст"
    if picture.filename.split(".")[-1] not in ["jpeg", "png"]:
        logging.info("Загруженный файл не картинка")
        return "Неверное расширение файла"
    picture_path: str = '/' + save_picture(picture)
    try:
        post: dict = add_post({'pic': picture_path, 'content': content})
    except FileNotFoundError:
        logging.error("Файл не найден")
        return "Файл не найден"
    except JSONDecodeError:
        return "невалидный файл"
    return render_template('post_uploaded.html', post=post)
