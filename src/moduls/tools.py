import re


def quick_sort(arr: list, type: str = 'number') -> list:
    """Sorts list of strings or numbers.

    If we given list of strings program will
    be looking for only number in those strings
    and will be sorting base on only first number
    in each string

    Args:
        arr (list):
        type (str): 'str' or 'number'

    Returns:
        list
    """

    if type not in ['str', 'number']:
        raise TypeError

    if type == 'str':
        lenght = len(arr)
        lo = []
        hi = []

        if lenght <= 1:
            return arr
        else:
            pivot_int = int(re.search('[0-9]+', arr[lenght-1]).group())
            pivot_str = arr.pop(lenght-1)

            table_int = [int(re.search('[0-9]+', din).group()) for din in arr]
            table_str = arr

            for i, item in enumerate(table_int):
                if item < pivot_int:
                    lo.append(table_str[i])
                else:
                    hi.append(table_str[i])

            return quick_sort(lo, type=type) + [pivot_str] + quick_sort(hi, type=type)

    if type == 'number':
        lenght = len(arr)
        lo = []
        hi = []

        if lenght <= 1:
            return arr
        else:
            pivot = arr.pop(lenght-1)

            for item in arr:

                if item < pivot:
                    lo.append(item)
                else:
                    hi.append(item)

            return quick_sort(lo, type=type) + [pivot] + quick_sort(hi, type=type)


def str_to_number(string: str) -> int | float:
    """Convert string to number.

    Agrs:
        string (str)

    Returns:
        float | int: converted sting
        0: if do not find number in string

    Examples:
        >>> str_to_number('234,23')
        234.23

    """
    pattern = r'[0-9,.]+'
    dot_number = re.findall('[,.]', string)
    if re.search(pattern, string) and len(dot_number) <= 1:
        if ',' in string:
            string = string.replace(',', '.')
        number = float(re.search(pattern, string).group())
        return number
    else:
        return 0
