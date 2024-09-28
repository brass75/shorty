import json

from spiderweb import SpiderwebRouter, Request
from spiderweb.response import HttpResponse, TemplateResponse, RedirectResponse

from database.db import ShortyDB
from lib.encoder import encode_string
from lib.utils import get_url_prefix, validate_url

app = SpiderwebRouter(templates_dirs='src/templates')
db = ShortyDB()

try:
    with open('config.json') as f:
        config = json.load(f)
except Exception:
    config = {
        'host': 'localhost',
        'port': 8000
    }

PREFIX = f'{config.get('schema', 'http')}://{config['host']}:{config['port']}/'


def get_prefix(url: str) -> str:
    """
    Get the URL prefix

    :param url: URL to get the prefix for
    :return: The prefix for the URL or the appropriately configured one
    """
    prefix = get_url_prefix(url)
    return (prefix + '/' if prefix and not prefix.endswith('/') else '') or PREFIX


@app.route("/")
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
                'data': f"{repr(url_to_add)} is not a valid URL. <br>"
                        f"Please make sure to present a valid URL for shortening.",
            }
        )
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
                },
                status_code=409
            )
    return TemplateResponse(
        request, 'add_route.html.jinja2',
        context={
            'added_url': url_to_add,
            'short_link': f'{prefix}{encoded}',
            'success': True,
        }
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
            'data': f"We didn't recognize anything for {get_prefix(request.path)}{request.path}<br>"
                    f"Remember that shortened URLs are case sensitive.",
        }
    )


if __name__ == "__main__":
    app.start()
