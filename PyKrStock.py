# -*- coding: utf-8 -*-
#
# TODO: docstring

import threading

class PyKrStock:

    dummy_event = threading.Event()
    
    def is_available(self):
        raise NotImplementedError

    def cool_time(self):
        raise NotImplementedError

    def daily_stats(self, item, start, end):
        raise NotImplementedError

    def hourly_stats(self, item, start, end):
        raise NotImplementedError

    def register_handler(self, handler):
        raise NotImplementedError

    def add_items(self, item_list):
        raise NotImplementedError

    def remove_items(self, item_list):
        raise NotImplementedError

    def standby_for_safe_request(self):
        self.nonbusy_sleep(self.cool_time())
        
    def nonbusy_sleep(self, ms = None):
        if ms is None:
            PyKrStock.dummy_event.wait()
        else:
            PyKrStock.dummy_event.wait(ms / 1000.0)

