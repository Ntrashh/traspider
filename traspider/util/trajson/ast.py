



def subexpression(children):
    return {"type": "subexpression", 'children': children}


def field(name):
    return {"type": "field", "children": [], "value": name}