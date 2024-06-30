# -*- coding: utf-8 -*-

from tool import Tool
from ex_iterator import ExIterator
from benchmark import Benchmark


class BenchmarkBasedRebalanceTool(Tool):
    
    def __init__(self, data_source: ExIterator, stock_amount: int, cash_amount: int, benchmark: Benchmark, output_path) -> None:
        super().__init__()
        self.data_source = data_source
        self.stock_amount = stock_amount * 1000000
        self.stock_count = 0
        self.cash_amount = cash_amount * 1000000
        self.benchmark = benchmark
        self.output_path = output_path
        self.init = False

    def get_data_sources(self) -> set[ExIterator]:
        return self.benchmark.get_data_sources().union([self.data_source])

    def execute(self) -> None:
        pass

    def _init_amount(self):
        if not self.init:
            
            self.init = True



