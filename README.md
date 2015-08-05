# PyKrStock
South Korea stock market interface

You need to install Numpy, Python for Windows Extensions and
one of Home Trading Systems (like Daishin Securities CYBOS 5).
And you should pass HTS authentication first.

```python
stock, err = PyKrStockEngine.daishin_cybos_engine()
daily = stock.daily_stats("LG화학", date(2015,1,15), date(2015,2,13))
hourly = stock.hourly_stats("LG화학", date(2015,2,6), date(2015,2,13))
print(hourly)
```

