



def subexpression(children):
    return {"type": "subexpression", 'children': children}

def arrexpression(left, right):
    return {"type": "arrexpression", 'children': [left, right]}


def field(name):
    return {"type": "field", "children": [], "value": name}