# -*- coding: utf-8 -*-

from datetime import date, datetime
import numpy as np
import win32com.client

class DaishinCybosEngine(PyKrStock):

    item2code = {}
    cpcybos = win32com.client.Dispatch("CpUtil.CpCybos")
    cpstockcode = win32com.client.Dispatch("CpUtil.CpStockCode")
    stockchart = win32com.client.Dispatch("CpSysdib.StockChart")

    def __init__(self):
        super(DaishinCybosEngine, self).__init__()
        
    def is_available(self):
        return DaishinCybosEngine.cpcybos.IsConnect == 1

    def cool_time(self):
        cpcybos = DaishinCybosEngine.cpcybos
        # GetLimitRemainCount(LT_NONTRADE_REQUEST)
        if cpcybos.GetLimitRemainCount(1) == 0:
            return cpcybos.LimitRequestRemainTime
        return 0

    def daily_stats(self, item, start, end):
        if not self.is_available():
            return None
        
        stockchart = DaishinCybosEngine.stockchart;
        code = self._get_item_code(item)
        start_date = int(start.strftime("%Y%m%d"))
        end_date = int(end.strftime("%Y%m%d"))
        requested_count = (end - start).days + 1

        self.standby_for_safe_request()
        stockchart.SetInputValue(0, code)
        stockchart.SetInputValue(1, '1') # by period, doesn't matter
        stockchart.SetInputValue(2, end_date) # YYYYMMDD
        stockchart.SetInputValue(3, start_date)
        # count of items requested
        stockchart.SetInputValue(4, requested_count)
        # fetch [date, start price, end price,
        #        max price, min price, volume]
        stockchart.SetInputValue(5, [0, 2, 5, 3, 4, 8])
        stockchart.SetInputValue(6, ord('D')) # daily
        stockchart.SetInputValue(9, '1') # adjusted price
        stockchart.BlockRequest()
        
        num = stockchart.GetHeaderValue(3) # count of result items
        rows = []
        for i in range(0, num):
            idate = stockchart.GetDataValue(0, i)
            start_price = stockchart.GetDataValue(1, i)
            end_price = stockchart.GetDataValue(2, i)
            max_price = stockchart.GetDataValue(3, i)
            min_price = stockchart.GetDataValue(4, i)
            volume = stockchart.GetDataValue(5, i)
            if idate < start_date:
                break
            rows.append((idate, start_price, end_price,
                         max_price, min_price, volume))
        ret = np.array(rows, dtype=[ # base['volume'] base.names
            ('date', 'i'), ('start price', 'i'), ('end price', 'i'),
            ('max price', 'i'), ('min price', 'i'), ('volume', 'i')])
        return ret

    def hourly_stats(self, item, start, end):
        if not self.is_available():
            return None
        
        stockchart = DaishinCybosEngine.stockchart;
        code = self._get_item_code(item)
        start_date = int(start.strftime("%Y%m%d"))
        end_date = int(end.strftime("%Y%m%d"))
        requested_count = ((end - start).days + 1) * 6 * 60
            # days * 6 (9~15 o'clock) * 60 (minutes/hour)

        self.standby_for_safe_request()
        stockchart.SetInputValue(0, code)
        stockchart.SetInputValue(1, '1') # by period, doesn't matter
        stockchart.SetInputValue(2, end_date) # YYYYMMDD
        stockchart.SetInputValue(3, start_date)
        # count of items requested
        stockchart.SetInputValue(4, requested_count)
        # fetch [date, time, start price, end price,
        #        max price, min price, volume]
        stockchart.SetInputValue(5, [0, 1, 2, 5, 3, 4, 8])
        stockchart.SetInputValue(6, ord('m')) # minutely
        stockchart.SetInputValue(9, '1') # adjusted price
        stockchart.BlockRequest()
        
        num = stockchart.GetHeaderValue(3) # count of result items
        rows = []
        if num != 0:
            last_date = stockchart.GetDataValue(0, 0)
            last_hour = int(stockchart.GetDataValue(1, 0) / 100)
            if last_hour == 15: last_hour = 14
            h_start_price = stockchart.GetDataValue(2, 0)
            h_end_price = h_max_price = h_min_price = h_volume = 0
        for i in range(0, num):
            idate = stockchart.GetDataValue(0, i)
            itime = stockchart.GetDataValue(1, i)
            start_price = stockchart.GetDataValue(2, i)
            end_price = stockchart.GetDataValue(3, i)
            max_price = stockchart.GetDataValue(4, i)
            min_price = stockchart.GetDataValue(5, i)
            volume = stockchart.GetDataValue(6, i)
            if last_date != idate or last_hour != int(itime / 100):
                rows.append((last_date, last_hour,
                             h_start_price, h_end_price,
                             h_max_price, h_min_price, h_volume))
                last_date = idate
                last_hour = int(itime / 100)
                if last_hour == 15: last_hour = 14
                h_start_price = start_price
                h_end_price = end_price
                h_max_price = max_price
                h_min_price = min_price
                h_volume = volume
            else:
                h_end_price = end_price
                if h_max_price < max_price: h_max_price = max_price
                if h_min_price < min_price: h_min_price = min_price
                h_volume += volume
            if idate < start_date:
                break
        ret = np.array(rows, dtype=[ # base['volume'] base.names
            ('date', 'i'), ('time', 'i'),
            ('start price', 'i'), ('end price', 'i'),
            ('max price', 'i'), ('min price', 'i'), ('volume', 'i')])
        return ret

    def _get_item_code(self, item):
        item2code = DaishinCybosEngine.item2code
        if item in item2code:
            return item2code[item]
        ret = DaishinCybosEngine.cpstockcode.NameToCode(item)
        item2code[item] = ret
        return ret

