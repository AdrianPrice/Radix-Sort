
def padding_length(string_list, b):
    '''
    This function adds zeros to the start of the string so that they are all the same length
    :param string_list: a list of strings
    :complexity: O(n), where n is the length of string_list
    :return: a list of strings all of the same length (padded with zeros)
    '''

    '''Find longest number'''
    max_length = len(string_list[0])
    for x in range(1, len(string_list)):
        if len(string_list[x]) > max_length:
            max_length = len(string_list[x])

    '''For each number add zeros to the start so the length is the same as the longest numbers'''
    for x in range (len(string_list)):
        for y in range(len(string_list[x]), max_length):
            string_list[x] = [0] + string_list[x]

    return string_list

def numbersToString(num_list):
    '''
    :param num_list: an list of integers
    :return: the same list but converted to string
    '''

    '''Convert num_list to strings'''
    string_list = []
    for x in range(len(num_list)):
        string_list.append(str(num_list[x]))

    return string_list

def convert_to_different_base_aux(decimal, base):
    '''
    This function converts a list of base 10 numbers to a different, specified base
    :param decimal: the base 10 number to convert to different base
    :param base: the base in which to convert decimal to
    :complexity: O(log_b(n)), where b is the base and n is the decimal (because its being divided by the base each time)
    :return: a list of strings representation of decimal in the specified base
    '''

    if decimal == 0:
        return []
    else:
        return convert_to_different_base_aux(decimal//base,base) + [decimal%base]

def convert_to_different_base(decimal_array, base):
    '''
    This function calls convert_to_different_base_aux to convert a list of base 10 numbers to a different, specified base
    :param decimal_array: a list of base 10 numbers to convert to different base
    :param base: the base in which to convert it to
    :complexity: O(mlog_b(n)), where m is the length of decimal array, for b and n see convert_to_different_base_aux
    :return: a list of strings representing the numbers in the specified base
    '''
    new_base_list = []
    for x in range (len(decimal_array)):
        assert isinstance(decimal_array[x], int), "Can't perform sort on non integer values"
        assert decimal_array[x] >= 1 and decimal_array[x] <=  2**64-1, "Can't perform sort on values less than 1 or greater than 2^64 -1"

        new_base_list.append(convert_to_different_base_aux(decimal_array[x], base))
    return new_base_list

def convert_from_different_base_aux(not_decimal, from_base):
    '''
    This function converts a number from a different base back into base 10
    :param not_decimal: a numbers in another base other than base 10
    :param from_base: the base that the number is being converted from
    :complexity: O(N), where N is the length of not_decimal
    :return: the equivalent number in base 10
    '''

    output = 0
    for x in range(0, len(not_decimal)):
        number_to_add_to_output = not_decimal[len(not_decimal)-x-1]
        output += (from_base ** x) * number_to_add_to_output
    return output

def convert_from_different_base(not_decimal_array, from_base):
    '''
    This function calls convert_from_different_base_aux to convert a number back to base 10
    :param not_decimal_array: a list of numbers in any base
    :param from_base: the base that the numbers are being converted from
    :complexity: O(MN), where M is the length of the array, for N see convert_from_different_base_aux
    :return: the list with all the numbers being base 10
    '''
    new_base_list = []
    for x in range (len(not_decimal_array)):
        new_base_list.append(convert_from_different_base_aux(not_decimal_array[x], from_base))
    return new_base_list

def radix_sort(num_list, b):
    '''
    This function performs radix sort on a list of integers in a specified base
    :param num_list: a list of integers from 1 -  2^64 -1
    :param b: the base of the list of integers
    :complexity: O(MN), where M is the length of the longest number in num_list and N which is the length of num_list
    :return: a sorted list of integers based on num_list
    '''
    if len(num_list) == 0:
        return num_list

    '''Convert to specified base'''
    string_list = convert_to_different_base(num_list, b) # O(mlog_b(n)), where m is the length of decimal array, for b and n see convert_to_different_base_aux

    '''Pad the numbers so they are all the same length'''
    numbersSameLength = padding_length(string_list, b) #O(n), where n is the length of string_list


    '''For each grouping run an individual run of radix sort'''
    for x in range (len(numbersSameLength[0])): #O(M), where M is the length of the longest number
        numbersSameLength = counting_sort(numbersSameLength, b, len(numbersSameLength[0]) - x - 1) #O(N), where N is the length of numbersSameLength
    sorted_array = numbersSameLength

    int_sorted_array_ten = convert_from_different_base(sorted_array, b)  #O(MN), where M is the length of the array, for N see convert_from_different_base_aux


    return int_sorted_array_ten

def counting_sort(string_list, base, order_by_what_index):
    '''
    This function is called by radix_sort and performs counting sort on a set of numbers ordered by a specific index
    :param num_list: a list of numbers to be sorted
    :param base: the base in which the numbers are represented
    :param orderByWhatIndex: the index in which to order the numbers by
    :complexity: O(n), where n is the length of the array
    :return: the numbers in ascending order based on the orderByWhatIndex parameter
    '''

    '''Create list of just the indexes we are looking at this pass'''
    numbers_to_order = []
    for x in range (len(string_list)):
        numbers_to_order.append(int(string_list[x][order_by_what_index]))

    '''Count the occurrences of each number'''
    occurrences = count_occurrences(numbers_to_order, base) #O(n)

    '''Calculate the starting positions in the sorted array of each number'''
    positions = [0] * len(occurrences)
    for x in range(len(positions) - 1): #O(n)
        positions[x + 1] = positions[x] + occurrences[x]

    '''Using the starting positions insert each number into the sorted array'''
    sortedArray = [0] * len(string_list)
    for x in range(len(string_list)): #O(n)
        positionToPlace = positions[int(string_list[x][order_by_what_index])]
        sortedArray[positionToPlace] = string_list[x]
        positions[int(string_list[x][order_by_what_index])] += 1

    return sortedArray

def count_occurrences(array, base):
    '''
    This function is called by counting_sort and counts the number of occurrences of each number in the array
    :param array: an array of integers
    :complexity: Time - O(n), where n is the length of the array
                 Aux Space - O(k), where k is the max integer in the array
    :return: the number of occurrences of each number
    '''

    counter = [0] * base

    for x in range (len(array)):
        counter[array[x]] +=1

    return counter

