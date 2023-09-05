import primitives
import classes

GLOBAL_ENV = classes.Environment({}, {}, None, "GLOBAL")


def isprimitive(exp):
    """Determines if syntax of "exp" matches a Logo primitive value."""
    if (
        type(exp).__name__ == "list"
        or exp.isdigit()
        or exp.lower() == "true"
        or exp.lower() == "false"
    ):
        return True
    return False


def isvariable(exp):
    """Determines if syntax of "exp" matches a Logo varibale value."""
    if exp[0] == ":":
        return True
    return False


def isquoted(exp):
    """Determines if syntax of "exp" matches a Logo quoted value."""
    if exp[0] == '"':
        return True
    return False


def isdefinition(exp):
    """Determines if syntax of "exp" matches a Logo definition value."""

    # why do I need this if I could use just apply `to`
    # a: because you are accessing an undefined amount of operands which can't be done with
    #    the current implementation where operand count must be known.
    if exp == "to":
        return True
    return False


def tokenizer(text: str):
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
        b2 = _find_last_closed_bracket(text[b1:])
        print("Index of ]: {}".format(b2))
        nested_text = tokenizer(text[b1 + 1 : b1 + b2])
        data.append(nested_text)

    else:
        data.extend(text.split())

    return data


def _find_last_closed_bracket(text: str):
    """Find the last closed square bracket from a string of text."""
    for i in range(len(text)):
        if text[-i] == "]":
            return len(text) - i
    return None


def input_procedure() -> [str]:
    """Takes logo code as input for procedure creation."""
    pass


def eval_line(line: list, env: classes.Environment):
    """Evaluates all expressions in a line of code and returns the resulting value."""
    evals = []

    def exp_eval(exp):
        nonlocal evals  # gives write access to evals inside this scope

        if isprimitive(exp):
            return exp
        elif isvariable(exp):
            _, v = env.get_var(exp[1:])
            return v
        elif isquoted(exp):
            return eval_quoted(exp)
        elif isdefinition(exp):
            proc_name = evals[0]
            proc_args = evals[1:]

            body = input_procedure()

            env.add_proc(
                proc_name=proc_name,
                body=body,
                args=proc_args,
                args_count=len(proc_args),
            )

            evals = []
            return None
        else:
            proc = env.get_proc(exp)
            if proc.args_count != len(evals):
                raise TypeError(
                    "Invalid args provided for procedure: {}".format(proc.name)
                )
            print("'Evals' before apply_procedure: {}".format(evals))
            val = apply_procedure(proc, evals, env)
            evals = []
            print("Val to be added to 'evals' post apply_procedure: {}".format(val))
            return val

    while line:
        val = exp_eval(line.pop())

        if val is not None:
            evals.insert(0, val)


def eval_quoted(exp):
    return exp[1:]


def apply_procedure(proc: classes.Procedure, args: list, env: classes.Environment):
    """Orchestrates the applying of operands to a procedure."""

    if proc.user_defined:
        sub_env = classes.Environment(
            {}, {}, env, proc.name
        )  # new env that's dynamically scoped

        for i in len(args):
            sub_env.add_var(proc.args[i], args[i])  # bind operands in new env

        lines = proc.body

        try:
            while lines:
                line = tokenizer(lines.pop(0))  # turn a line into tokens
                eval_line(line, sub_env)  # call eval_line on each line of the body
        except classes.OuputException as e:
            return e.get_exp()

        return None

    else:
        if (
            proc.name == "make"
        ):  # sort of a workaround, more robust system for working with env would be better
            return proc.body(env, *args)
        return proc.body(
            *args
        )  # unpacks the list of args and applies them to the procedure.

        # do I need to create a new env for primitive procedures?


# <-------------------------------<%>------------------------------->#


def logo_cold_start(e: classes.Environment):
    """Starts a logo global environment."""
    e.add_proc("print", primitives.logo_print_procedure, ("text"), 1, False)
    e.add_proc(
        "sentence", primitives.logo_sentence_procedure, ("item1", "item2"), 2, False
    )
    e.add_proc("list", primitives.logo_list_procedure, ("item1", "item2"), 2, False)
    e.add_proc("fput", primitives.logo_fput_procedure, ("item1", "item2"), 2, False)
    e.add_proc("first", primitives.logo_first_procedure, ("setence"), 1, False)
    e.add_proc("last", primitives.logo_last_procedure, ("setence"), 1, False)
    e.add_proc("butfirst", primitives.logo_butfirst_procedure, ("setence"), 1, False)
    e.add_proc("make", primitives.logo_make_procedure, ("name", "value"), 2, False)
    return e


def logo_repl_loop():
    try:
        GLOBAL_ENV = logo_cold_start(GLOBAL_ENV)

        while True:
            tokens = tokenizer(input("? "))
            print("Tokens from parser: {}".format(tokens))
            eval_line(tokens, GLOBAL_ENV)
    except Exception as e:
        print("Found an Error of type {}: {}".format(type(e), e))


def logo_repl_debug_loop():
    global GLOBAL_ENV

    GLOBAL_ENV = logo_cold_start(GLOBAL_ENV)

    while True:
        tokens = tokenizer(input("? "))
        print("Tokens from parser: {}".format(tokens))
        eval_line(tokens, GLOBAL_ENV)


# <-------------------------------<%>------------------------------->#

if __name__ == "__main__":
    logo_repl_debug_loop()
