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


def eval_line(line):
    """Evaluates all expressions in a line and returns the resulting value."""
    # does this need to be passed an environment? look at "logo apply for clue"
    pass

def exp_eval(exp, env):
    """Evaluates the first expression in a line."""
    pass


#<-------------------------------<%>------------------------------->#


def apply_procedure(proc, args, env):
    """Orchestrates the applying of operands to a procedure."""
    pass

def collect_args(args):
    """Evaluate arguments."""
    # might need to call apply_procedure if a value isnt primitive, variable, or quoted.
    pass

def logo_apply(proc, args):
    """"""
    # check if primitive or user-defined
    # if primitive, apply args to Python function from dictionary
    # if user-defined, create a new environment, create local vars and link args to them
    # then call eval line again but passing in the new env this time (?)
    pass


#<-------------------------------<%>------------------------------->#

if __name__ == "__main__":
    print("[" in 'print sentence "this')
    print('print sentence "this [is a [deep] list]'.index("["))
