newline = '\n'

tab = '\t'

max_string_length = 21

max_line_length = 77

import string

from sections import version, well

def is_number(num):
    return isinstance(num,(float,int,long))

def cut_string(value):
    value = str(value)
    if len(value) > 21:
        return value[0:21]
    return value

def flatten(las_data,mnem,description=None):
    data = []
    #mnem
    data.append(mnem)
    #unit
    data.append(tab)
    unit = ''
    if las_data[mnem].has_key('unit'):
        unit = las_data[mnem]['unit']

    data.append('.%s' % unit)
    data.extend([tab,tab])

    val = las_data[mnem]['value']
    if val is not None:
        if is_number(val):
            data.append('%5.2f' % float(val))
        if hasattr(val,'__iter__'):
            pass
        else:
            data.append(cut_string(val))
    
    data.append(tab)
    data.append(': ')
    if las_data[mnem].has_key('description'):
        data.append(las_data[mnem]['description'])
    else:
        if description:
            data.append(description)

    data.append(newline)
    return data

def get_bool(value):
    if value:
        return 'YES'
    else:
        return 'NO'

class pylas:
    def __init__(self,wrap=False,null=-9999):
        #initializing the data
        self.data = {}
        #setting the wrap
        self.set_wrap(wrap)
        self.curves = {}
        self.index = None
        
        self.set_mnem('VERS','2.0',description='CWLS log ASCII Standard -VERSION 2.0')
        self.set_mnem('NULL',null,description='NULL VALUE')
        
    def set_mnem(self,mnem,value,unit=None,description=None,curve=False,api_code=None):
        if curve:
            self.curves[mnem] = description
            if self.index is None:
                self.index = mnem
        
        if not self.data.has_key(mnem):
            self.data[mnem] = {}

        self.data[mnem]['value'] = value
        
        if unit:
            self.data[mnem]['unit'] = unit
        if description:
            self.data[mnem]['description'] = description

        if api_code:
            self.data[mnem]['api_code'] = api_code

    def get_break_line(self):
        return '#' + '-'*max_line_length
    
    break_line = property(get_break_line)

    def set_wrap(self,value):
        self._wrap = value
        self.set_mnem('WRAP',get_bool(value))

    def get_wrap(self):
        return self._wrap

    wrap = property(set_wrap,get_wrap)

    def to_string(self):
        las_data = []
        
        #version section

        sections = {'VERSION':version,
                    'WELL':well,
                    'CURVE':self.curves}

        order = ['VERSION','WELL','CURVE']
        
        for section in order:
            las_data.append('~%s INFORMATION' % section)
            las_data.append(newline)
            
            for mnem in sections[section]:
                if self.data.has_key(mnem):
                    las_data.extend(flatten(self.data,mnem,sections[section][mnem]))
                    
            las_data.append(self.break_line)
            las_data.append(newline)

        #data section
        
        las_data.append('~A')
        
        if len(self.curves) > 0:
            #add the curve headers
            for curve in self.curves:
                las_data.extend(tab)
                las_data.extend(curve)
                
            las_data.append(newline)

            #add the curve data
            for i in range(len(self.data[self.index]['value'])):
                for curve in self.curves:
                    las_data.append(str(self.data[curve]['value'][i]))
                    las_data.append(tab)
                las_data.append(newline)
                        
                
            
        
        return string.join(las_data,'')
