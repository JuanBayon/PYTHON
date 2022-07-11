def input_check_range(a, b):
    """
    The function ask the user to enter a number and checks for rank membership
    between a and b given as arguments. Returns the value.
    """
    while True:
        num = ask_number(f'Please choose a number between {a} an {b - 1}')
        try:
            if num in range(a, b):
                break
            else: 
                raise ValueError
        except ValueError:
            print(f'Please enter a number between {a} and {b - 1}')

    return num



def not_same_option(a, b):
    """
    Given two numbers representing an option in a list,
    the function checks if it is the same election.
    Returns true or false.
    """
    not_same = True
    if a == b:
        print('You have already chosen this option')
        not_same = False

    return not_same


def ask_number(text):
    """
    Given a text as an argument to ask the user to enter an input number,
    the function check it as integer and return the value.
    """
    while True:
        num = input(text)
        try:
            num = int(num)
        except ValueError:
            print('You can only choose characters [0, 9]') 
        else:
            return num