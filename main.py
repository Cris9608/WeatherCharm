from interface import *
from data import Data

d = Data()

app = Screen()
app.app(statii=d.station_names())
