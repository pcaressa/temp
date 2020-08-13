#   put_parenthesys.py

"""
    Expressions are represented as lists: [b1, o1, b2, o2, ...]
    where bi are 'true', 'false' or subexpressions and oi are 'and',
    'or', 'xor'.
"""

def find_all(token_list):
    """ Associates in all possible ways parentheses in the token_list
        expression. TODO"""
    yield token_list

def compute(triple):
    """Computes the Boolean operation triple[0] triple[1] triple[2]."""
    b1 = triple[0] == 'true'
    b2 = triple[2] == 'true'
    if triple[1] == 'and':
        result = b1 and b2
    elif triple[1] == 'or':
        result = b1 or b2
    elif triple[1] == 'xor':
        result = b1 != b2
    return 'true' if result else 'false'

def find_false(token_list):
    """Recursively yields all associations of expressions which
        evaluates to false."""
    if len(token_list) == 1 and token_list[0] == 'false':
        yield token_list
    elif len(token_list) > 1:
        if token_list[1] == 'and' and token_list[0] == 'true'   \
        or token_list[1] == 'or' and token_list[0] == 'false'   \
        or token_list[1] == 'xor' and token_list[0] == 'false':
            for L in find_false(token_list[2:]):
                yield token_list[:2] + L
        elif token_list[1] == 'and' and token_list[0] == 'false':
            for L in find_all(token_list[2:]):
                yield token_list[:2] + L
        elif token_list[1] == 'xor' and token_list[0] == 'true':
            for L in find_true(token_list[2:]):
                yield token_list[:2] + L
        if len(token_list) > 3:
            for sublist in find_false([compute(token_list[:3])] + token_list[3:]):
                # Get to the first operand in the sublist and stores
                # instead of it token_list[:3]
                element = sublist
                while not isinstance(element[0], str):
                    element = element[0]
                element[0] = token_list[:3]
                yield sublist

def find_true(token_list):
    """Recursively yields all associations of expressions which
        evaluates to true."""
    if len(token_list) == 1 and token_list[0] == 'true':
        yield token_list
    elif len(token_list) > 1:
        if token_list[1] == 'and' and token_list[0] == 'true'   \
        or token_list[1] == 'or' and token_list[0] == 'false'   \
        or token_list[1] == 'xor' and token_list[0] == 'false':
            for L in find_true(token_list[2:]):
                yield token_list[:2] + [L]
        elif token_list[1] == 'or' and token_list[0] == 'true':
            for L in find_all(token_list[2:]):
                yield token_list[:2] + [L]
        elif token_list[1] == 'xor' and token_list[0] == 'true':
            for L in find_false(token_list[2:]):
                yield token_list[:2] + [L]
        if len(token_list) > 3:
            # tries also so associate the first operation and continue
            for sublist in find_true([compute(token_list[:3])] + token_list[3:]):
                # Get to the first operand in the sublist and stores
                # instead of it token_list[:3]
                element = sublist
                while not isinstance(element[0], str):
                    element = element[0]
                element[0] = token_list[:3]
                yield sublist

def print_token_list(token_list):
    """Prints the token list as a string with parentheses."""
    if len(token_list) > 0:
        if isinstance(token_list[0], list):
            if len(token_list[0]) == 1:
                print(token_list[0][0], end = "")
            else:
                print("(", end = "")
                print_token_list(token_list[0])
                print(")", end = " ")
        else:
            print(token_list[0], end = " ")
        if len(token_list) > 1:
            print(token_list[1], end = " ")
            print_token_list(token_list[2:])

#boolean_expression = input("Insert the expression: ")

boolean_expressions = ["true and false xor true",
                       "true or false xor true and false",
                       "false xor false and false"
]
for b in boolean_expressions:
    s = b.split()
    print("Dealing with ", end = "")
    print_token_list(s)
    print()
    for token_list in find_true(s):
        print_token_list(token_list)
        print()
