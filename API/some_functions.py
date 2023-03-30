import base64, io, pathlib, os, shutil, time
from PIL import Image
from functools import reduce

from django.db.models import F, Case, Value, When, Q, Avg, Max, Min, Count, Sum
from django.db.models.functions.math import Abs, Power, Round, Sqrt, Mod
from django.db.models.functions.text import Reverse, Concat, Lower, Upper, Length
from django.db import models

calcul_classes = {
    "value": Value,
    "append": F,
    "field": F,

    # work on a sequence of numbers
    "avg": Avg, # field, conditions
    "max": Max,
    "min": Min,
    "count": Count,
    "sum": Sum,

    # work on 1 or 2 numbers
    "abs": Abs,
    "round": Round,
    "sqrt": Sqrt,
    "mod": Mod,
    "power": Power,

    "reverse": Reverse,
    "concat": Concat,
    "lower": Lower,
    "upper": Upper,
    "length": Length,
}

# ################ 
models.CharField.register_lookup(Reverse)
# models.CharField.register_lookup(Concat)
models.CharField.register_lookup(Lower)
models.CharField.register_lookup(Upper)
models.CharField.register_lookup(Length)
# ################ 
models.FloatField.register_lookup(Abs)
models.FloatField.register_lookup(Round)
models.FloatField.register_lookup(Sqrt)
# ################ 
models.IntegerField.register_lookup(Abs)
models.IntegerField.register_lookup(Round)
models.IntegerField.register_lookup(Sqrt)
# ################## 
def get_now_stamp():
    return int(time.time())

# #####################
def simple_Q(conditions: dict):

    q = Q()
    for key, value in conditions.items():
        if key.startswith("-"):
            q &= ~Q(**{key[1:]: value})
        else:
            q &= Q(**{key: value})
    
    return q

# #####################
def Q_object(conditions):

    if isinstance(conditions, list):
        return reduce(lambda init_q, clause: init_q | Q_object(clause), conditions, Q())

    elif isinstance(conditions, dict):
        q = Q()
        for key, value in conditions.items():

            if key.startswith("-"):
                key = key[1:]
                q &= ~Q(**{key: get_expression(value, False)})
            else:
                q &= Q(**{key: get_expression(value, False)})

        # return Q(**{key: get_expression(value, False) for key, value in conditions.items()})

    return q

def get_expression(kwargs, str_is_field: bool = True):
    # sourcery skip: low-code-quality

    if isinstance(kwargs, dict):

        func_name = kwargs["function"]
        args = kwargs["args"]

        if func_name=="max": 
            return Max(F(args["col"]), filter=Q_object(args.get("conditions", [])))
        
        elif func_name=="min": 
            return Min(F(args["col"]), filter=Q_object(args.get("conditions", [])))
        
        elif func_name=="avg": 
            return Avg(F(args["col"]), filter=Q_object(args.get("conditions", [])))
        
        elif func_name=="sum": 
            return Sum(F(args["col"]), filter=Q_object(args.get("conditions", [])))
        
        elif func_name=="count": 
            return Count(F(args["col"]), filter=Q_object(args.get("conditions", [])), 
                        distinct=args.get("distinct", False))
        

        elif func_name=="abs": 
            return Abs(get_expression(args["n"], True))
        
        elif func_name=="power": 
            return Power(get_expression(args["x"], True), get_expression(args["y"], True))
        
        elif func_name=="round": 
            return Round(get_expression(args["n"], True), get_expression(args.get("r", 0), True))
        
        elif func_name=="sqrt": 
            return Sqrt(get_expression(args["n"], True))
        
        elif func_name=="mod": 
            return Mod(get_expression(args["x"], True), get_expression(args["y"], True))
        

        elif func_name=="reverse": 
            return Reverse(get_expression(args["s"], True))
        
        elif func_name=="concat": 

            strings = args["s"]
            if not isinstance(strings, list):
                strings = [strings]

            strings = list(map(lambda el: get_expression(el, True), strings))
            return Concat(*strings)
        
        elif func_name=="lower": 
            return Lower(get_expression(args["s"], True))
        
        elif func_name=="upper": 
            return Upper(get_expression(args["s"], True))
        
        elif func_name=="length": 
            return Length(get_expression(args["s"], True))
    
        
        elif func_name=="field": 
            return F(args)

    elif isinstance(kwargs, list):
        return list(map(lambda el: get_expression(el, str_is_field), kwargs))
    
    elif isinstance(kwargs, str):
        return F(kwargs) if str_is_field else Value(kwargs)

    return Value(kwargs)

# #####################
def decode_image(encoded_image: str):

    decoded_image = base64.b64decode(bytes(encoded_image, encoding="utf-8"))
    return Image.open(io.BytesIO(decoded_image))

def copy_image(source_path: str, destination_path: str):

    if not pathlib.Path(destination_path).suffix:
        destination_path += pathlib.Path(source_path).suffix

    pathlib.Path(destination_path).parent.mkdir(exist_ok=True)

    with open(source_path, mode="rb") as file_1:
        with open(destination_path, mode="wb") as file_2:
            file_2.write(file_1.read())

    return destination_path

def delete_img(img_path):
    
    if os.path.isfile(img_path):
        os.remove(img_path)

def delete_dir(dir_path):

    if os.path.isdir(dir_path):
        shutil.rmtree(dir_path)


"""

"""

# ################ Create, Update Store (unused)

"""

def create_store(kwargs: dict):

    encoded_img = kwargs.pop("encoded_img", None)
    try:
        if encoded_img is not None:
            encoded_img = encoded_img.split(",")[-1]
            image = decode_image(encoded_img)

            new_store = Store(**kwargs)
            new_store.save()

            img_path = f"static/stores/store_{new_store.id}/store_{new_store.id}.{image.format}"
            
            pathlib.Path(img_path).parent.mkdir(exist_ok=True)
            image.save(img_path)

        else:
            new_store = Store(**kwargs)
            new_store.save()

            img_path = f"static/stores/store_{new_store.id}/store_{new_store.id}"
            img_path = copy_image(source_path=DEFAULT_STORE_IMG_PATH, destination_path=img_path)

        new_store.image_url = img_path
        new_store.save()

        return Response({"store": new_store.to_dict()})
    
    except Exception as e:
        return Response(data={"error": e.__class__.__name__, "args": e.args}, status=400)

def update_store(store_id: int, kwargs: dict = None):

#     encoded_img = kwargs.pop("encoded_img", None)
#     set_default_img = kwargs.pop("set_default_img", False)

#     store = Store.objects.get(pk=store_id)
#     if store is not None:

#         if encoded_img is not None:
#             encoded_img = encoded_img.split(",")[-1]
#             image = decode_image(encoded_img)

#             store.update(**kwargs)
#             image.save(store.image_url)

#         else:
#             store.update(**kwargs)
#             if set_default_img:
#                 copy_image(source_path=DEFAULT_STORE_IMG_PATH, destination_path=store.image_url)

#     return store

"""

