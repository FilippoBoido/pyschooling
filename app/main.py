from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import random
from operator import add, sub, floordiv, mul

app = FastAPI()
app.mount("/static", StaticFiles(directory="_static"), name="static")
templates = Jinja2Templates(directory="templates")


def https_url_for(request: Request, name: str, **path_params) -> str:
    """ Workaround function, since jinja2 url_for does not construct the path with https

    :param request:
    :param name:
    :param path_params:
    :return:
    """
    http_url = request.url_for(name, **path_params)
    if 'localhost' in http_url:
        return http_url
    else:
        return http_url.replace("http", "https", 1)


templates.env.globals["https_url_for"] = https_url_for


def find_divisible_numbers():
    dividend = random.randint(1, 1000)
    divisor = random.randint(1, 20)
    while (dividend % divisor) != 0:
        dividend = random.randint(1, 1000)
        divisor = random.randint(1, 20)
    return dividend, divisor


def table_filler(exercises: list, results: list):
    ops = {"+": add, "-": sub, ':': floordiv, '*': mul}

    operators = ['+', '-', ':', '*']
    str_operator = operators[random.randint(0, 3)]
    x_pos = random.randint(1, 3)

    if str_operator == ':':
        var_1, var_2 = find_divisible_numbers()
        str_operator = ':'
    elif str_operator == '*':
        var_1 = random.randint(0, 1000)
        var_2 = random.randint(0, 10)
    else:
        var_1 = random.randint(0, 1000)
        var_2 = random.randint(0, 1000)
    fun_operator = ops[str_operator]
    var_3 = fun_operator(var_1, var_2)
    results.append(
        {
            "var_1": var_1,
            "operator": str_operator,
            "var_2": var_2,
            "var_3": var_3
        }
    )

    if x_pos == 1:
        var_1 = ''
    elif x_pos == 2:
        var_2 = ''
    elif x_pos == 3:
        var_3 = ''

    exercises.append(
        {
            "var_1": var_1,
            "operator": str_operator,
            "var_2": var_2,
            "var_3": var_3
        }
    )


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    exercises = []
    results = []

    for i in range(0, 25):
        table_filler(exercises, results)

    return templates.TemplateResponse(
        "page.html",
        {
            "request": request,
            "exercises": exercises,
            "results": results
        }
    )
