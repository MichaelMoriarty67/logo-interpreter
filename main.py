import primitives

class Environment:
    def __init__(self, procedures, vars, base_env = None, name = None ):
        self.procedures = procedures
        self.variables = vars
        self.base_env = base_env
        self.name = name
    
    def add_proc(self, name, value, args = (), args_count = 0, user_defined = True):
        """Adds or updates a name in the procedures dictionairy."""
        proc = Procedure(
            name,
            args,
            value,
            user_defined,
            args_count
        )
        self.procedures[name] = proc

    def add_var(self, name, value):
        """Adds or updates a name in the variables dictionairy."""
        e, _ = self.get_var(name)
        if e is not None:
            e.variables[name] = value
        else:
            GLOBAL_ENV.variables[name] = value
        
        self.variables[name] = value

    def rem_name(self, name):
        """Removes a name in the values dictionairy."""
        pass
    
    def get_proc(self, name):
        """Returns the value bound to a specified name or None."""
        return self.procedures[name]
    
    def get_var(self, name):
        """Returns the value bound to a specified name and the env it's found in."""
        env = self
        value = None
        while env:
            try:
                value = self.variables[name]
                return env, value
            except UnboundLocalError and KeyError:
                env = env.base_env
        return env, value


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
    """Tokenizes, analyzes, and creates a nested list structure from a line of Logo code."""
    tokens = tokenizer(text)
    return tokens

def tokenizer(text):
    """Takes in a line of Logo code and returns it as a list of tokens."""

    # doesn't work for values that come after a []
    # ie: print sentence "this [is a [deep] list]
    #                                        ^^^

    data = []
    if "[" in text:
        b1 = text.index("[")
        print("Index of [ found at: {}".format(b1))
        data.extend(text[:b1].split())

        print("Text post [: {}".format(text[b1:]))
        b2 = find_last_closed_bracket(text[b1:])
        print("Index of ]: {}".format(b2))
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


def isprimitive(exp):
    """Determines if syntax of "exp" matches a Logo primitive value."""
    if type(exp).__name__ == "list" or exp.isdigit() or exp.lower() == "true" or exp.lower() == "false":
        return True
    return False

def isvariable(exp):
    """Determines if syntax of "exp" matches a Logo varibale value."""
    if exp[0] == ":":
        return True
    return False

def isquoted(exp):
    """Determines if syntax of "exp" matches a Logo quoted value."""
    if exp[0] =='"':
        return True
    return False

def isdefinition(exp):
    """Determines if syntax of "exp" matches a Logo definition value."""
    # why do I need this if I could use just apply `to`
    # a: because you are accessing an undefined amount of operands which can't be done with
    #    the current implementation where operand count must be known.
    return False


#<-------------------------------<%>------------------------------->#

def eval_line(line, env):
    """Evaluates all expressions in a line and returns the resulting value."""
    evals = [] 
    
    def exp_eval(exp):
        nonlocal evals

        if isprimitive(exp):
            return exp
        elif isvariable(exp):
            return env.get_var(exp[1:])
        elif isquoted(exp):
            return eval_quoted(exp)
        elif isdefinition(exp):
            return eval_definition(exp, env)
        else:
            proc = env.get_proc(exp)
            if proc.args_count != len(evals):
                raise TypeError("Invalid args provided for procedure: {}".format(proc.name))
            print("'Evals' before apply_procedure: {}".format(evals))
            val = apply_procedure(proc, evals, env)
            evals = []
            print("Val to be added to 'evals' post apply_procedure: {}".format(val))
            return val

    while line:
        val = exp_eval(line.pop())
        evals.insert(0, val)
    
    return evals[0] # return value of last expression 


def eval_quoted(exp):
    return exp[1:]


#<-------------------------------<%>------------------------------->#


def apply_procedure(proc, args, env):
    """Orchestrates the applying of operands to a procedure."""
    
    if proc.user_defined:
        sub_env = Environment({}, {}, env, proc.name) # new env that's dynamically scoped
        for i in len(args):
            sub_env.add_var(proc.args[i], args[i]) # bind operands in new env
        
        lines = proc.body
        while lines:
            if lines[0][0] == "output":
                return eval_line(lines[0][1:], sub_env)
            
            if lines[0][0] == "stop":
                break
            
            eval_line(lines.pop(0), sub_env) # call eval_line on each line of the body

        # hardcoded search for output & stop probs works but feels janky...
        # would be better done if I could achieve the same using "output" as a logo call expression

        return None

    else:
        if proc.name == "make": # sort of a workaround, more robust system for working with env would be better
            return proc.body(env, *args)
        return proc.body(*args) # unpacks the list of args and applies them to the procedure.
    
        # do I need to create a new env for primitive procedures?


#<-------------------------------<%>------------------------------->#

def logo_cold_start():
    """Starts a logo global environment."""
    g = Environment({}, {}, None, "GLOBAL")
    g.add_proc("print", primitives.logo_print_procedure, ("text"), 1, False)
    g.add_proc("sentence", primitives.logo_sentence_procedure, ("item1", "item2"), 2, False)
    g.add_proc("list", primitives.logo_list_procedure, ("item1", "item2"), 2, False)
    g.add_proc("fput", primitives.logo_fput_procedure, ("item1", "item2"), 2, False)
    g.add_proc("first", primitives.logo_first_procedure, ("setence"), 1, False)
    g.add_proc("last", primitives.logo_last_procedure, ("setence"), 1, False)
    g.add_proc("butfirst", primitives.logo_butfirst_procedure, ("setence"), 1, False)
    g.add_proc("make", primitives.logo_make_procedure, ("name", "value"), 2, False)
    return g


def logo_repl_loop():
    try:
        GLOBAL_ENV = logo_cold_start()

        while True:
            tokens = parse_text(input("? "))
            print("Tokens from parser: {}".format(tokens))
            eval_line(tokens, GLOBAL_ENV)
    except Exception as e:
        print("Found an Error of type {}: {}".format(type(e), e))

def logo_repl_debug_loop():
    GLOBAL_ENV = logo_cold_start()

    while True:
        tokens = parse_text(input("? "))
        print("Tokens from parser: {}".format(tokens))
        eval_line(tokens, GLOBAL_ENV)


#<-------------------------------<%>------------------------------->#

if __name__ == "__main__":
    global GLOBAL_ENV
    logo_repl_debug_loop()
