class ExpTree:
    def __init__(self, operator, operands):
        self.operator = operator
        self.operands = operands

    def __repr__(self) -> str:
        return "{}({})".format(
            self.operator, list(map(repr, self.operands))
        )


class Environment:
    def __init__(self, procedures, vars, name = None):
        self.procedures = procedures
        self.variables = vars
        self.name = name
    
    def add_name(self, name, value):
        """Adds or updates a name in the values dictionairy."""
        pass

    def rem_name(self, name):
        """Removes a name in the values dictionairy."""
        pass
    
    def get_val(self, name):
        """Returns the value bound to a specified name or None."""
        pass

    def __repr__(self) -> str: # this could be formatted cooler to show more like a receipt
        return """{}
        _________
        {}
        
        """.format(self.name, self.values)
    

class Procedure:
    def __init__(self, name, args, body, user_defined, args_count) -> None:
        self.name = name
        self.body = body
        self.args = args
        self.user_defined = user_defined
        self.args_count = args_count


#<-------------------------------<%>------------------------------->#


def parse_text(text):
    """Tokenizes, analyzes, and creates an ExpTree from passed text."""
    tokens = tokenizer(text)
    return tokens

def tokenizer(text):
    """Takes in a line of Logo code and returns it as a list of tokens."""
    # find a way to nest lists when a [ is found and end when a ] is found.
    # I feel like recursion is going to be the best way
    data = []
    if "[" in text:
        b1 = text.index("[")
        print(b1)
        data.extend(text[:b1].split())

        print(text[b1:])
        b2 = find_last_closed_bracket(text[b1:])
        print("b2: {}".format(b2))
        nested_text = tokenizer(text[b1+1:b1+b2])
        data.append(nested_text)
    
    else:
        data.extend(text.split())
    
    return data

def find_last_closed_bracket(text):
    """Find the last closed square bracket from a string of text."""
    for i in range(len(text)):
        if text[-i] == "]":
            return len(text)-i
    return None


#<-------------------------------<%>------------------------------->#

def eval_line(line, env):
    """Evaluates all expressions in a line and returns the resulting value."""
    evals = [] 
    
    def exp_eval(exp):
        if isprimitive(exp):
            return exp
        elif isvariable(exp):
            return env.get_var(exp)
        elif isquoted(exp):
            return eval_quoted(exp)
        elif isdefintiton(exp):
            return eval_definition(exp, env)
        else:
            proc = env.get_proc(exp)
            if proc.args_count != len(list):
                raise TypeError("Invalid args provided for procedure: {}".format(proc.name))
            val = apply_procedure(proc, tuple(evals), env)
            evals = []
            return val

    while line:
        val = exp_eval(line.pop())
        evals.append(val)
    
    return evals[0] # return value of last expression (why tho?)

#<-------------------------------<%>------------------------------->#


def apply_procedure(proc, args, env):
    """Orchestrates the applying of operands to a procedure."""
    if proc.user_defined:
        # new env that's dynamically scoped
        # create vars in new env
        # call eval_line on each line of the body
        pass

    else:
        return proc.body(args)
        


def collect_args(args):
    """Evaluate arguments."""
    # don't need this function because all args have already been evaluated.
    pass

def logo_apply(proc, args):
    """"""
    # don't need this anymore
    pass


#<-------------------------------<%>------------------------------->#

if __name__ == "__main__":
    print("[" in 'print sentence "this')
    print('print sentence "this [is a [deep] list]'.index("["))
