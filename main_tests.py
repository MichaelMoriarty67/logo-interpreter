
import main

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
    assert main.tokenizer(double_nested_input_whitespace) == double_nested_output, "Double nested input did not pass the whitespace test. Output was {}".format(main.tokenizer(double_nested_input_whitespace))
if __name__ == "__main__":
    tokenizer_test()