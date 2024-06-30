# -*- coding: utf-8 -*-

from ex_iterator import ExIterator


class Benchmark:

    def __init__(self) -> None:
        pass

    def get_data_sources(self) -> set[ExIterator]:
        pass

    def calculate_rebalance_percent(self) -> tuple[float, float]:
        pass


class ReferBenchmark(Benchmark):

    def __init__(self) -> None:
        super().__init__()

    def calculate_rebalance_percent(self) -> tuple[float, float]:
        pass

