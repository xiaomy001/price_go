# -*- coding: utf-8 -*-

class ExIterator:

    def __init__(self, origin_iter: iter) -> None:
        self.origin_iter = origin_iter
        self.current_item = None

    def next(self):
        val = next(self.origin_iter, None)
        self.current_item = val
        return val
    
    def current(self):
        return self.current_item

if __name__ == '__main__':
    iterator = ExIterator(iter([1,2,3]))
    while iterator.next():
        print(iterator.current())
