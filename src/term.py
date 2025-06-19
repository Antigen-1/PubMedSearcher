import typing

class Or:
    def __init__(self, *args):
        self.subforms = args
class And:
    def __init__(self, *args):
        self.subforms = args
class Plain:
    def __init__(self, *args):
        sep = " "
        self.text = repr(sep.join(args))
class Annotation:
    def __init__(self, arg, *args):
        sep = " "
        self.text = f"{repr(sep.join(args))}[{arg}]"

ParsedTerm = typing.Union[Or, And, Plain, Annotation]

def render_term(parsed_term: ParsedTerm) -> str:
    sep = ""
    if isinstance(parsed_term, Or):
        sep = " OR "
    if isinstance(parsed_term, And):
        sep = " AND "
    if isinstance(parsed_term, Or) or isinstance(parsed_term, And):
        l = []
        for subform in parsed_term.subforms:
            l.append(render_term(subform))
        return sep.join(l)
    if isinstance(parsed_term, Plain) or isinstance(parsed_term, Annotation):
        return parsed_term.text
        
def cons_term(t, *args) -> ParsedTerm:
    if t == "Plain":
        return Plain(*args)
    if t == "Or":
        return Or(*args)
    if t == "And":
        return And(*args)
    return Annotation(t, *args)