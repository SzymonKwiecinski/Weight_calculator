from pytest import mark
from src.moduls.tools import quick_sort, str_to_number


@mark.tools
@mark.parametrize('test, expected, type',
    [
        (
            ['DIN125', 'PN82005', 'ISO1234', 'DIN94','ISO7380-1'],
            ['DIN94', 'DIN125', 'ISO1234', 'ISO7380-1', 'PN82005'],
            'str'
        ),
        (
            [],
            [],
            'str'
        ),
        (
            ['sd'],
            ['sd'],
            'str'
        ),
        (
            [0],
            [0],
            'str'
        ),
        (
            [10.2, 3.4, 5],
            [3.4, 5, 10.2],
            'number'
        )
    ])
def test_quick_sort_with_str(test, expected, type):
    argument = quick_sort(test, type)
    assert argument == expected


@mark.tools
@mark.parametrize('test, expected',
    [
        ('100', 100),
        ('12.23', 12.23),
        ('12,2', 12.2),
        ('', 0)
    ]
)
def test_str_to_number(test, expected):
    argument = str_to_number(test)
    assert argument == expected