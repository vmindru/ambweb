from jinja2 import Environment


def environment(**options):
    env = Environment(**options)
    env.globals.update({
        'range': range
    })
    return env
