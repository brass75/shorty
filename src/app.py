from spiderweb import SpiderwebRouter
from spiderweb.response import HttpResponse, TemplateResponse, RedirectResponse

from database.db import ShortyDB
from lib.encoder import encode_string

app = SpiderwebRouter(templates_dirs='src/templates')
db = ShortyDB()


@app.route("/")
def index(request):
    return TemplateResponse(request, 'add_route.html.jinja2')


@app.route('/routes/v1/add', allowed_methods=['POST', 'GET'])
def add(request):
    if request.method != 'POST':
        return TemplateResponse(request, 'add_route.html.jinja2')
    url_to_add = request.POST['url_to_add']
    encoded = encode_string(url_to_add)
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
                    'short_link': f'http://localhost:8000/{encoded}',
                    'failed': True,
                }
            )
    return TemplateResponse(
        request, 'add_route.html.jinja2',
        context={
            'added_url': url_to_add,
            'short_link': f'http://localhost:8000/{encoded}',
            'success': True,
        }
    )


@app.route('/<str:encoded_url>')
def redirector(request, encoded_url):
    if redirect_url := db.get(encoded_url):
        return RedirectResponse(redirect_url)
    return TemplateResponse(request, 'add_route.html.jinja2', status_code=404)


if __name__ == "__main__":
    app.start()
