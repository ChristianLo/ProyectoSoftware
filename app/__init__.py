from functools import wraps

from flask import Flask, render_template, request

app = Flask(__name__, template_folder='templates', static_folder='static')
app.secret_key = 'development key'


def templates(template=None):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            template_name = template
            if template_name is None:
                template_name = request.endpoint.replace('.', '/') + '.html'
            ctx = f(*args, **kwargs)
            if ctx is None:
                ctx = {}
            elif not isinstance(ctx, dict):
                return ctx
            return render_template("pages/"+template_name, **ctx)

        return decorated_function

    return decorator


from app import views
