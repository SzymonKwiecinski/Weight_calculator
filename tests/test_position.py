from pytest import mark
from pytest import fixture
from src.position import Position


@fixture('norm, size1, size2, weight, 100szt_kg, kg_100szt',[
    ('DIN931', '10.0', '55', 43.8, 0.228, 4.38)
])
@mark.position
class PositionTests:

    def test_norm(self, norm):
        assert 

    def test_size1(position):
        pass

    def test_size2(position):
        pass

    def test_weight(position):
        pass

    def test_full_name(position):
        pass

    def test_calc_kg_to_100szt(position):
        pass

    def test_calc_100szt_to_kg(position):
        pass

    def test_weight_kg_per_1000szt(position):
        pass
