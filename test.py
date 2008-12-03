from pylas import pylas
t = pylas()

t.set_mnem('DT',[1,2,3,4],description="Depth",curve=True)
print t.to_string()
