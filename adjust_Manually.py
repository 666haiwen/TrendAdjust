import os
from adjust import AdjustTrend
from const import *

adjustProcess = AdjustTrend(templatePath, runPath, resPath, 1)
adjustProcess([])
