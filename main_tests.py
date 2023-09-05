
import main
import classes

GLOBAL_ENV = classes.Environment({}, {}, None, "Global")
GLOBAL_ENV = main.logo_cold_start(GLOBAL_ENV)

def tokenizer_test():
    single_nested_input = 'print sentence "this [is a deep list]'
    double_nested_input = 'print sentence "this [is a [deep] list]'

    single_nested_input_whitespace = '   print  sentence "this [  is a  deep list   ]'
    double_nested_input_whitespace = '   print  sentence "this [  is a  [ deep] list   ]'

    single_nested_output = ['print', 'sentence', '"this', ['is', 'a', 'deep', 'list']]
    double_nested_output = ['print', 'sentence', '"this', ['is', 'a', ['deep'], 'list']]
    
    assert main.tokenizer(single_nested_input) == single_nested_output, "Output should be {} but instead was: {}".format(single_nested_output, main.tokenizer(single_nested_input))
    # assert main.tokenizer(double_nested_input) == double_nested_output, "Output should be {} but instead was: {}".format(double_nested_output, main.tokenizer(double_nested_input))
    
    assert main.tokenizer(single_nested_input_whitespace) == single_nested_output, "Single nested input did not pass the whitespace test. Output was {}".format(main.tokenizer(single_nested_input_whitespace))
    # assert main.tokenizer(double_nested_input_whitespace) == double_nested_output, "Double nested input did not pass the whitespace test. Output was {}".format(main.tokenizer(double_nested_input_whitespace))



def print_test():
    single_print_input = "print 5"

    assert main.eval_line(main.parse_text(single_print_input), GLOBAL_ENV) == None

def make_test():
    make_input_one = 'make "x 555'
    make_input_two = 'make "x 777'
    make_input_three = 'make "y "hello'

    #<-------------------------------<%>------------------------------->#    

    assert GLOBAL_ENV.procedures["make"] == True, 'No "make" procedure added to the environment.'
    main.eval_line(make_input_one, GLOBAL_ENV)

    assert GLOBAL_ENV.variables["x"] == "555", 'Variable not bound to expected value in env: {}'.format(GLOBAL_ENV.name)

    #<-------------------------------<%>------------------------------->#    
    
    sub_env = classes.Environment({}, {}, GLOBAL_ENV, "Test Env 1")
    main.eval_line(make_input_two, sub_env)

    assert sub_env.get_var("x") == "777"
    assert sub_env.variables["x"] == False
    assert GLOBAL_ENV.variables["x"] == "777"

    #<-------------------------------<%>------------------------------->#  

    main.eval_line(make_input_three, sub_env)

    assert sub_env.get_var("y") == "hello", '"get_var" method not returning expected value for y.'
    assert sub_env.variables["y"] == False, 'Variable "y" incorrectly found in {}'.format(sub_env.name)
    assert GLOBAL_ENV.variables["y"] == "hello", 'Variable "y" not added to Global env via "make" procedure.'

if __name__ == "__main__":
    tokenizer_test()
    print_test()
    make_test()