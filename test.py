from pylas import pylas
from pylas import units

t = pylas()

t.set_mnem('DT',[1,2,3,4],description="Depth",curve=True,unit=units.feet)
t.set_mnem('GR',[33.0,50.0,60.0,40.0],description="Gamma Ray",curve=True,unit=units.gammaray)
t.set_mnem('Dummy','Test',description="TestData")
print t.to_string()
