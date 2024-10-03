import json
import logging

from spiderweb import SpiderwebRouter, Request
from spiderweb.response import TemplateResponse, RedirectResponse

from database.db import ShortyDB
from lib.encoder import encode_string
from lib.utils import get_url_prefix, validate_url, get_data_dir
import os

logger = logging.getLogger('app')


DATA_DIR = get_data_dir()
logger.warning(f'Using {DATA_DIR=}')
if not os.path.exists(DATA_DIR):
    os.mkdir(DATA_DIR)
CONFIG_PATH = f'{DATA_DIR}/config.json'
logger.warning(f'Using config from {CONFIG_PATH=}')

try:
    with open(CONFIG_PATH) as f:
        config = json.load(f)
except Exception:
    logger.warning('Failed to load config. Using default.')
    config = {'server': {'host': 'localhost', 'port': 8000}}

if template_dir := config.get('templates', ''):
    if template_dir.startswith('data/'):
        TEMPLATE_DIR = f'{DATA_DIR}/{template_dir.removeprefix('data/')}'
    else:
        TEMPLATE_DIR = template_dir
else:
    TEMPLATE_DIR = 'templates' if os.getcwd().endswith('/src') else 'src/templates'
logger.warning(f'Templates at: {TEMPLATE_DIR=}')

# Initialize the app
app = SpiderwebRouter(templates_dirs=TEMPLATE_DIR)

# Initialize the data store
db = ShortyDB(path=DATA_DIR)


def set_prefix(_config: dict) -> str:
    """
    Generate the prefix from the config

    :param _config: The config
    :return: URL prefix
    """
    if not (server := _config.get('server')):
        return 'http://localhost:8000/'
    if (schema := server.get('schema', 'http')) not in ['http', 'https']:
        schema = 'http'
    host = server.get('host', 'localhost')
    port = server.get('port')
    return f'{schema}://{host}{f':{port}' if port else ''}/'


def get_prefix(url: str) -> str:
    """
    Get the URL prefix

    :param url: URL to get the prefix for
    :return: The prefix for the URL or the appropriately configured one
    """
    prefix = get_url_prefix(url)
    return (prefix + '/' if prefix and not prefix.endswith('/') else '') or set_prefix(config)


@app.route('/')
def index(request):
    return TemplateResponse(request, 'add_route.html.jinja2')


@app.route('/routes/v1/add', allowed_methods=['POST', 'GET'])
def add(request: Request) -> TemplateResponse:
    if request.method != 'POST':
        return TemplateResponse(request, 'add_route.html.jinja2')
    url_to_add = request.POST['url_to_add']
    if not validate_url(url_to_add):
        return TemplateResponse(
            request,
            'add_route.html.jinja2',
            status_code=400,
            context={
                'error': 'Invalid URL',
                'data': f'{repr(url_to_add)} is not a valid URL. <br>'
                f'Please make sure to present a valid URL for shortening.',
            },
        )
    if not (encoded := request.POST.get('custom_code', '').strip()):
        encoded = encode_string(url_to_add)
    prefix = get_prefix(request.path)
    try:
        db[encoded] = url_to_add
    except ShortyDB.ShortyDBError:
        if (existing := db[encoded]) != url_to_add:
            return TemplateResponse(
                request,
                'add_route.html.jinja2',
                context={
                    'added_url': url_to_add,
                    'existing_url': existing,
                    'short_link': f'{prefix}{encoded}',
                    'failed': True,
                    'encoded': encoded,
                },
                status_code=409,
            )
    return TemplateResponse(
        request,
        'add_route.html.jinja2',
        context={
            'added_url': url_to_add,
            'short_link': f'{prefix}{encoded}',
            'success': True,
            'encoded': encoded,
        },
    )


@app.route('/<str:encoded_url>')
def redirector(request: Request, encoded_url: str) -> RedirectResponse | TemplateResponse:
    if redirect_url := db.get(encoded_url):
        return RedirectResponse(redirect_url)
    return http404(request)


@app.error(404)
def http404(request: Request) -> TemplateResponse:
    return TemplateResponse(
        request,
        'add_route.html.jinja2',
        status_code=404,
        context={
            'error': "Sorry! We couldn't find what you were looking for!",
            'data': f"We didn't recognize anything for {get_prefix(request.path).lstrip('/')}{request.path}<br>"
            f'Remember that shortened URLs are case sensitive.',
        },
    )


@app.route('/get/urls', allowed_methods=['GET'])
def get_urls(request: Request) -> TemplateResponse:
    """
    Return a table with all the shortened URLs

    :param request: Request object
    :return: TemplateResponse with the data needed
    """
    return TemplateResponse(
        request,
        'url_table.html.jinja2',
        context={
            'db': db.items(),
            'prefix': get_prefix(request.path),
        },
    )


if __name__ == '__main__':
    app.start()
