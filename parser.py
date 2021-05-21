import math
from lark import Lark, InlineTransformer

# Implemente a gramática aqui! Você pode testar manualmente seu código executando
# o arquivo calc.py e testá-lo utilizando o pytest.
grammar = Lark(
    r"""
?start : assign* comp?
?assign : NAME "=" comp
?comp  : expr "<" expr  -> smaller
       | expr "<=" expr -> smaller_equal
       | expr ">" expr  -> greather
       | expr ">=" expr -> greather_equal
       | expr "==" expr -> equal
       | expr "!=" expr -> different
       | expr
?expr  : expr "+" term  -> add
       | expr "-" term  -> sub
       | term
?term  : term "*" exp   -> mul
       | term "/" exp   -> div
       | exp
?exp   : atom "^" exp   -> pow
       | atom
?atom  : NUMBER                         -> number
       | MATH_CONST                     -> math_const
       | NAME "(" expr ("," expr)* ")"  -> fcall
       | NAME                           -> var
       | "(" expr ")"
NUMBER : /-?(?:0|[1-9]\d*)(?:\.\d+)?(?:[eE][+-]?\d+)?/
MATH_CONST : /[+-]?(pi|e|tau|inf|nan)/
NAME   : /[-+]?\w+/
%ignore /\s+/
%ignore /\#.*/
""")

class CalcTransformer(InlineTransformer):
    from operator import add, sub, mul, truediv as div, pow  # ... e mais!

    def __init__(self):
        super().__init__()
        self.variables = {k: v for k, v in vars(
            math).items() if not k.startswith("_")}
        self.variables.update(max=max, min=min, abs=abs)
        self.env = {}
    
    def fcall(self, name, *args):
        name = str(name)
        fn = self.variables[name.split('-')[-1]]
        if name[0] == '-':
            return -fn(*args)
        return fn(*args)

    def var(self, name):
        try:
            return self.variables[name]
        except:
            return self.env[name]

    def assign(self, name, value):
        self.env[name] = value
        return self.env[name]
    
    def start(self, *args):
        return args[-1]
   
    def number(self, token):
        try:
            return int(token)
        except ValueError:
            return float(token)

    def greather(self, x, y):
        return x > y

    def greather_equal(self, x, y):
        return x >= y

    def smaller(self, x, y):
        return x < y
    
    def smaller_equal(self, x, y):
        return x <= y
    
    def equal(self, x, y):
        return x == y
    
    def different(self, x, y):
        return x != y

    def math_const (self, token):
        constValue = self.variables[token.split('-')[-1]]
        if token[0] == '-':
            constValue *= -1
        return constValue