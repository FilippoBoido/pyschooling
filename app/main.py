from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import random
from operator import add, sub, floordiv, mul

app = FastAPI()
app.mount("/static", StaticFiles(directory="_static"), name="static")
templates = Jinja2Templates(directory="templates")


def find_divisible_numbers():
    dividend = random.randint(1, 1000)
    divisor = random.randint(1, 20)
    while (dividend % divisor) != 0:
        dividend = random.randint(1, 1000)
        divisor = random.randint(1, 20)
    return dividend, divisor


def table_filler(exercises: list, results: list, operators=None, max_value=1000):
    ops = {"+": add, "-": sub, ':': floordiv, '*': mul}
    if operators is None:
        operators = ['+', '-', ':', '*']

    str_operator = operators[random.randint(0, len(operators)-1)]
    x_pos = random.randint(1, 3)

    if str_operator == ':':
        var_1, var_2 = find_divisible_numbers()
        str_operator = ':'
    elif str_operator == '*':
        var_1 = random.randint(0, max_value)
        var_2 = random.randint(0, 10)
    else:
        var_1 = random.randint(0, max_value)
        var_2 = random.randint(0, max_value)
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

    return templates.TemplateResponse(
        "index.html", { "request": request}
    )


@app.get("/mixed-excercises-medium", response_class=HTMLResponse)
async def mixed_excercises_medium(request: Request):
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



@app.get("/sum-and-sub-medium", response_class=HTMLResponse)
async def sum_and_sub_medium(request: Request):
    exercises = []
    results = []

    for i in range(0, 25):
        table_filler(exercises, results,['+', '-'])

    return templates.TemplateResponse(
        "page.html",
        {
            "request": request,
            "exercises": exercises,
            "results": results
        }
    )


@app.get("/add-simple", response_class=HTMLResponse)
async def add_simple(request: Request):
    exercises = []
    results = []

    for i in range(0, 25):
        table_filler(exercises, results,['+'], 10)

    return templates.TemplateResponse(
        "page.html",
        {
            "request": request,
            "exercises": exercises,
            "results": results
        }
    )