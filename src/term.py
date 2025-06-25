import typing
import core
import path
import os.path

def isTerm(v) -> bool:
    return isinstance(v, Or) or isinstance(v, And) or isinstance(v, Plain) or isinstance(v, Annotation)

class Or:
    def __init__(self, *args):
        assert len(args) > 0
        for arg in args:
            assert isTerm(arg)
        self.subforms = args
class And:
    def __init__(self, *args):
        assert len(args) > 0
        for arg in args:
            assert isTerm(arg)
        self.subforms = args
class Plain:
    def __init__(self, *args):
        assert len(args) > 0
        for arg in args:
            assert isinstance(arg, str)
        sep = " "
        self.text = repr(sep.join(args))
class Annotation:
    def __init__(self, arg, *args):
        assert len(args) > 0
        assert isinstance(arg, str)
        for a in args:
            assert isinstance(a, str)
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
        if len(l) == 1:
            return l[0]
        return "(" + sep.join(l) + ")"
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

code = ""
with open(os.path.join(path.SRC_PATH, "json", "parser.json"), "rt") as f:
    code = f.read().rstrip()
parse_term = core.run(code)

def compile_term(s: str) -> str:
    parsed_term = parse_term(s, cons_term, lambda s: s=="(", lambda s: s==")", lambda s: s.isspace(), lambda s: s=="\\", Exception)
    if isinstance(parsed_term, Exception):
        raise parsed_term
    return render_term(parsed_term)