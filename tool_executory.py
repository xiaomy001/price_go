# -*- coding: utf-8 -*-

from tool import Tool
from ex_iterator import ExIterator

class ToolExecutory:

    def __init__(self) -> None:
        self.data_sources: set[ExIterator] = set()
        self.tools: list[Tool] = list()

    def add_tool(self, tool: Tool):
        self.data_sources.update(tool.get_data_sources())
        self.tools.append(tool)

    def execute(self):
        while True:
            for data_source in self.data_sources:
                val = data_source.next()
                if val is None:
                    return

            for tool in self.tools:
                tool.execute()

    def report(self):
        for tool in self.tools:
            tool.report()
