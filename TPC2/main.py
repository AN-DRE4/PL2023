import re


def sum_numbers_in_string(input_string):
    if input_string is None:
        return 0
    # Use regular expressions to find all sequences of numbers in the input string
    numbers = re.findall(r'\d+', input_string)

    # Convert each string of numbers to an integer and sum them up
    total_sum = sum(int(num) for num in numbers)

    return total_sum


def stdin_sum_digits():
    print(sum_numbers_in_string(input("Write some text:")))


def sum_until_off(input_string):
    # Search for the index of the first occurrence of "Off" in the input string
    off_index = input_string.find("Off")

    # If "Off" sequence was found, only consider the string before it
    if off_index != -1:
        input_string = input_string[:off_index]

    # Use the original sum_numbers_in_string() function to sum all numbers in the remaining input string
    total_sum = sum_numbers_in_string(input_string)

    return total_sum


def sum_until_off_remade(input_string):
    # Search for the index of the first occurrence of "Off" in the input string
    off_index = input_string.find("Off")
    rest = None

    # If "Off" sequence was found, only consider the string before it
    if off_index != -1:
        rest = input_string[off_index + 3:]
        input_string = input_string[:off_index]

    # Use the original sum_numbers_in_string() function to sum all numbers in the remaining input string
    total_sum = sum_numbers_in_string(input_string) + sum_after_on(rest)

    return total_sum


def sum_after_on(input_string):
    if input_string is None:
        return 0
    # Search for the index of the first occurrence of "On" in the input string
    on_index = input_string.find("On")

    # If "On" sequence was found, only consider the string after it
    total_sum = 0
    if on_index != -1:
        input_string = input_string[on_index + 2:]
        total_sum = sum_until_off_remade(input_string)

    return total_sum


def sum_until_equals(input_str):
    if input_str is None:
        return 0
    equals_index = input_str.find("=")
    rest = None
    if equals_index != -1:
        sum_to_print = input_str[:equals_index]
        rest = input_str[equals_index + 1:]
        print(sum_numbers_in_string(sum_to_print))

    return sum_until_equals(rest)


def main():
    text = "abc12Off=123Onedf=2hv6=Off56On8="
    print(sum_until_off_remade(text))
    sum_until_equals(text)
    stdin_sum_digits()


if __name__ == "__main__":
    main()
