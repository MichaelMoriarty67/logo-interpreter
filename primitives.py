# write all primitive functions here in python and then import them all to the global env upon startup
import utils
import classes

def logo_make_procedure(env: classes.Environment, name: str, value: str | list | int):
    """Binds a name to a value in the current environment."""
    print(env)
    env.add_var(name, value)
    return None

def logo_print_procedure(text):
    """Prints to the REL loop."""
    # if sentence, reformat
    # if word, determine what the word reps (number, string, boolean, etc) and  format correctly

    print(text)
    return None # maybe remove this?

def logo_show_procedure(text):
    """Prints to the REL without any syntax removed."""
    pass

def logo_sentence_procedure(item1, item2):
    """Creates a deconstructed Logo sentence from two variables."""
    # problem is that if I get '10' as a value, I am deconstructing the string. I only want to deconstruct lists

    return utils.str_friendly_unpack(item1, item2)

def logo_list_procedure(item1, item2):
    """Creates a Logo sentence from two variables."""
    return [item1, item2]

def logo_fput_procedure(item1, item2):
    """Creates a Logo sentence from one variable, and one deconstructed variable."""
    # this will break if item2 is a sole string with len > 1

    return [item1, *item2]

def logo_first_procedure(sentence):
    """Selects the first element in a sentence."""
    if len(sentence) == 0:
        raise Exception("Error. Cannot take first of a blank sentence.")
    return str(sentence[0])

def logo_last_procedure(sentence):
    """Selects the last element in a sentence."""
    if len(sentence) == 0:
        raise Exception("Error. Cannot take last of a blank sentence.")
    return str(sentence[-1])

def logo_butfirst_procedure(sentence):
    """Returns all but the first element in a sentence."""
    if len(sentence) == 0:
        raise Exception("Error. Cannot take butfirst of a blank sentence.")
    return str(sentence[1:])

def logo_to_procedure(name, args: tuple):
    """Creates a Logo procedure."""
    pass

def logo_run_procedure(sentence):
    """Runs a sentence as if it was line of Logo code."""
    # can I pass this to eval_line somehow?
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

