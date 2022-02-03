from pytest import mark
from src.position import Position


@mark.parametrize('norm, size1, size2, weight, _100szt_kg, kg_100szt',[
    ('DIN931', '10.0', '55', 43.8, 0.228, 4.38)
])
class PositionTests:

    def test_norm(self, norm, size1, size2, weight, _100szt_kg, kg_100szt):
        print(norm, size1, size2, weight, _100szt_kg, kg_100szt)
        pass

    # def test_size1(self):
    #     pass

    # def test_size2(self):
    #     pass

    # def test_weight(self):
    #     pass

    # def test_full_name(self):
    #     pass

    # def test_calc_kg_to_100szt(self):
    #     pass

    # def test_calc_100szt_to_kg(self):
    #     pass

    # def test_weight_kg_per_1000szt(self):
    #     pass
