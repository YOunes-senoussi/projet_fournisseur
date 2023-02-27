from ninja import NinjaAPI

api = NinjaAPI()

@api.get("/hello")
def hello(request, name: str = "world"):
    return f"Hello {name}"

@api.get("/math")
def math(request, a: int, b: int):
    return {"add": a + b, "multiply": a * b}

@api.get("/math/{a}and{b}")
def math(request, a: int, b: int, c: int, d: int):
    return {"add": a + b, "multiply": a * b, "c": c, "d": d}
