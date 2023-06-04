# write all primitive functions here in python and then import them all to the global env upon startup


def logo_make_procedure(name, value, env):
    """Binds a name to a value in the current environment."""
    env.add_var(name, value)
    return None

def logo_print_procedure(text):
    """Prints to the REL loop."""
    print(text)
    return None

def logo_show_procedure(text):
    """Prints to the REL without any syntax removed."""

def logo_sentence_procedure(item1, item2):
    """Creates a deconstructed Logo sentence from two variables."""
    return [*item1, *item2]

def logo_list_procedure(item1, item2):
    """Creates a Logo sentence from two variables."""
    return [item1, item2]

def logo_fput_procedure(item1, item2):
    """Creates a Logo sentence from one variable, and one deconstructed variable."""
    return [item1, *item2]

def logo_first_procedure(sentence):
    """Selects the first element in a sentence."""
    return 

def logo_last_procedure(sentence):
    """Selects the last element in a sentence."""
    pass

def logo_butfirst_procedure(sentence):
    """Returns all but the first element in a sentence."""
    pass

def logo_to_procedure(name, args: tuple):
    """Creates a Logo procedure."""
    pass

def logo_run_procedure(sentence):
    """Runs a sentence as if it was line of Logo code."""
    pass

def logo_sum_procedure(x, y):
    """Adds two primitive values."""
    return x + y

def logo_difference_procedure(x, y):
    """Subtracts two primitive values."""
    return x - y

def logo_product_procedure(x, y):
    """Multiplies two primitive values."""
    return x * y

def logo_quotient_procedure(x, y):
    """Divides two primitive values."""
    return x / y

