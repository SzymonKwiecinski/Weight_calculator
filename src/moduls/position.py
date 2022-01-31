import traceback


class Position:
    """Manages position attributes and methods

    Holds details about position in order to
    make operation on it and display in GUI
    interafec.
    In short is response for all logic.

    Attributes:
        norm: Norm or text describe product e.g. DIN933
        size1: First size of product e.g. 12
        size2: Second size of product e.g. 70
        weight: Weight of product e.g. 345.34
        full_name: e.g. DIN933 M12x70
        calc_kg_to_100szt: number allows to convert ? from kg to 100szt
        calc_100szt_to_kg: number allows to convert ? from 100szt to kg
        weight_kg_per_1000szt: weight of product per 1000szt

    """

    def __init__(self, norm: str = '', size1: str = '', size2: str = '', weight: float = 0) -> None:
        self.norm = norm
        self.size1 = size1
        self.size2 = size2
        self.weight = weight

    @property
    def norm(self) -> str:
        return self.__norm

    @norm.setter
    def norm(self, norm):
        if isinstance(norm, tuple):
            norm = norm[0]
        self.__norm = norm

    @norm.deleter
    def norm(self):
        self.norm = ''

    @property
    def size1(self) -> str:
        return self.__size1

    @size1.setter
    def size1(self, size1):
        if isinstance(size1, tuple):
            size1 = size1[0]
        self.__size1 = size1

    @size1.deleter
    def size1(self):
        self.size1 = ''

    @property
    def size2(self) -> str:
        return self.__size2

    @size2.setter
    def size2(self, size2):
        if isinstance(size2, tuple):
            size2 = size2[0]
        self.__size2 = size2

    @size2.deleter
    def size2(self):
        self.size2 = ''

    @property
    def weight(self) -> float | int:
        print(1)
        return self.__weight

    @weight.setter
    def weight(self, weight):
        weight = float(weight)
        if weight > 0:
            self.__weight = weight
        else:
            self.__weight = 0

    @property
    def full_name(self) -> str:
        if self.__size2 == '':
            return f'{self.__norm}  {self.__size1}'
        else:
            return f'{self.__norm}  {self.__size1}x{self.__size2}'

    @property
    def calc_kg_to_100szt(self) -> float:
        val = self.__weight * (100 / 1000)
        return val

    @property
    def calc_100szt_to_kg(self) -> float:
        try:
            val = (1000 / 100) * (1 / self.__weight)
            return val
        except ZeroDivisionError:
            traceback.print_exc()
            return 0

    @property
    def weight_kg_per_1000szt(self) -> str:
        return str(self.__weight) + ' kg/1000szt.'

    def __repr__(self) -> str:
        str_repl = (
            f"norm: {self.norm}\n"
            f"size 1: {self.size1}\n"
            f"size 2: {self.size2}\n"
            f"weight: {self.weight}\n"
            f"kg_to_100szt: {self.calc_kg_to_100szt}\n"
            f"100szt_to_kg: {self.calc_100szt_to_kg}\n")
        return str_repl
