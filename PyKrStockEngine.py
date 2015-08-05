# -*- coding: utf-8 -*-

class PyKrStockEngine:
    
    @classmethod
    def daishin_cybos_engine(cls):
        reason = ""
        try:
            import numpy
        except ImportError:
            reason += "install NumPy\n"
        try:
            import win32com.client
        except ImportError:
            reason += "install Python for Windows Extensions\n"
        try:
            win32com.client.Dispatch("CpUtil.CpCybos")
        except:
            reason += "install Daishin Securities CYBOS 5\n"

        reason = reason.strip()
        if len(reason) == 0:
            return DaishinCybosEngine(), None
        else:
            return None, reason

