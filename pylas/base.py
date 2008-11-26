newline = '\n'

tab = '\t'

max_string_length = 21

max_line_length = 77

import string

from sections import sections

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
        
        self.set_mnem('VERS','2.0',description='CWLS log ASCII Standard -VERSION 2.0')
        self.set_mnem('NULL',null,description='NULL VALUE')
        
    def set_mnem(self,mnem,value,unit=None,description=None):
        if not self.data.has_key(mnem):
            self.data[mnem] = {}

        self.data[mnem]['value'] = value
        
        if unit:
            self.data[mnem]['unit'] = unit
        if description:
            self.data[mnem]['description'] = description

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
        for section in sections:
            las_data.append('~%s INFORMATION' % section)
            las_data.append(newline)
        
            for mnem in sections[section]:
                if self.data.has_key(mnem):
                    las_data.extend(flatten(self.data,mnem,sections[section][mnem]))
                    
            las_data.append(self.break_line)
            las_data.append(newline)
        
        return string.join(las_data,'')
