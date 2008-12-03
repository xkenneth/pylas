from pylas import pylas
t = pylas()

t.set_mnem('DT',[1,2,3,4],description="Depth",curve=True)
t.set_mnem('Dummy','Test',description="TestData")
print t.to_string()
