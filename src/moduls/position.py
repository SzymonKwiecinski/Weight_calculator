class Position:

    def __init__(self, norm: str = '', size1: str = '', size2: str = '', weight: float = 0) -> None:
        self.norm = norm
        self.size1 = size1
        self.size2 = size2
        self.weight = weight

    @property
    def norm(self):
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
    def size1(self):
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
    def size2(self):
        return self.__size2

    @size2.setter
    def size2(self, size2):
        if isinstance(size2, tuple):
            size2 = size2[0]
        # if size2 == '':
        #     self.__size2 = 'NULL'
        self.__size2 = size2

    @size2.deleter
    def size2(self):
        self.size2 = ''

    @property
    def weight(self):
        return self.__weight

    @weight.setter
    def weight(self, weight):
        weight = float(weight)
        if weight > 0:
            self.__weight = weight
        else:
            self.__weight = 0

    @property
    def full_name(self):
        if self.__size2 == '':
            return f'{self.__norm}  {self.__size1}'
        else:
            return f'{self.__norm}  {self.__size1}x{self.__size2}'

    @property
    def calc_kg_to_100szt(self):
        val = self.__weight * (100 / 1000)
        return val

    @property
    def calc_100szt_to_kg(self):
        val = (1000 / 100) * (1 / self.__weight)
        return val

    @property
    def weight_kg_per_1000szt(self):
        return str(self.__weight) + ' kg/1000szt.'

    def __repr__(self) -> str:
        str_repl = f"""norm: {self.norm}
                        size 1: {self.size1}
                        size 2: {self.size2}
                        weight: {self.weight}
                        kg_to_100szt: {self.calc_kg_to_100szt}
                        100szt_to_kg: {self.calc_100szt_to_kg}"""
        return str_repl
