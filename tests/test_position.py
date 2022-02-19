from multiprocessing.context import assert_spawning
from pytest import mark, approx
from src.position import Position


# @mark.parametrize('norm, size1, size2, weight, _100szt_kg, kg_100szt',[
#     ('DIN931', '10.0', '55', 43.8, 0.228, 4.38)
# ])
@mark.position
class PositionTests:

    def test_calc_kg_to_100szt(self, position):
        assert 4.380 == round(position.calc_kg_to_100szt, 3)

    def test_calc_100szt_to_kg(self, position):
        assert 0.228 == round(position.calc_100szt_to_kg, 3)

    def test_weight_kg_per_1000szt(self, position):
        assert '43.8 kg/1000szt.' == position.weight_kg_per_1000szt

    def test_convert_weight_from_kg_to_szt(self, position):
        assert '273' == position.convert_weight_from_kg_to_szt(12)

    def test_convert_weight_from_szt_to_kg(self, position):
        assert '12.001' == position.convert_weight_from_szt_to_kg(274)

    def test_convert_price_from_kg_to_100szt(self, position):
        assert '52.56' == position.convert_price_from_kg_to_100szt(12)

    def test_convert_price_from_100szt_to_kg(self, position):
        assert '12.00' == position.convert_price_from_100szt_to_kg(52.56)
