import sys
import os
sys.path.insert(0, os.path.abspath("src"))
from pytest import fixture, mark
from src.moduls.position import Position
from src.moduls.sqlite import Sqlite


@fixture(scope='session')
def sql():
    with Sqlite() as sql:
        yield sql


@fixture(scope='session', params=[
    ('DIN931', '10', '55', 43.8),
    ('DIN931', '10', '55', 0)
])
def position(request):
    norm, size1, size2, weight = request.param
    position = Position(
        norm=norm,
        size1=size1,
        size2=size2,
        weight=weight
    )
    return position