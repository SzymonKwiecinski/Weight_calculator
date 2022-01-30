# from unittest import expectedFailure
# import pytest
# import src.main as main



# @pytest.mark.parametrize('test, expected',
#     [
#         (
#             ['DIN125', 'PN82005', 'ISO1234', 'DIN94','ISO7380-1'],
#             ['DIN94', 'DIN125', 'ISO1234', 'ISO7380-1', 'PN82005']
#         ),
#         (
#             [],
#             []
#         ),
#         (
#             ['sd'],
#             ['sd']
#         ),
#         (
#             [0],
#             [0]
#         )
#     ])
# def test_quick_sort_with_str(test, expected):
#     argument = main.Window.quick_sort_with_str(test)
#     message = f'For {test} should be {expected}'
#     assert argument == expected, message