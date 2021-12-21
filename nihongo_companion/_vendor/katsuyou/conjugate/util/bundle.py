# -*- coding: utf-8 -*-

# MIT License

# Copyright (c) 2021 Alexsandro Thomas

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from typing import Dict


def dict_unpack(d:dict) :
    for v in d.values() :
        if isinstance(v, Bundle) :
            yield from v.unpack()
        elif isinstance(v, dict) :
            yield from dict_unpack(v)
        else :
            yield v

class Bundle(dict):
    def __init__(self, *args, **kwargs):
        super(Bundle, self).__init__(*args, **kwargs)

    def __getattr__(self, attr):
        return self.get(attr)
    
    def __setattr__(self, key, value):
        self.__setitem__(key, value)

    def __setitem__(self, key, value):
        super(Bundle, self).__setitem__(key, value)

    def unpack(self) :
        for v in self.values() :
            if isinstance(v, Bundle) :
                yield from v.unpack()
            elif isinstance(v, dict) :
                yield from dict_unpack(v)
            else :
                yield v

    def update(self, other):
        for k, v in other.items() :
            if isinstance(v, dict):
                if k not in self or not isinstance(self[k],Bundle) : self[k] = Bundle()
                self[k].update(v)
            else:
                self[k] = v
    
    def recursive_set(self, *args) :
        assert len(args)>=2, "No key and element"
        ptr = self
        for i in range(len(args)-2) :
            k = args[i]
            if k not in ptr or not isinstance(ptr[k],Bundle) : ptr[k] = Bundle()
            ptr = ptr[k]
        ptr[args[-2]] = args[-1]
    
    def recursive_get(self, *args) :
        assert len(args)>=1, "No key"

        ptr = self
        for k in args :
            if k not in ptr : return None
            if not isinstance(ptr[k], dict) : return ptr[k]
            ptr = ptr[k]
        return ptr.setdefault(k, None)
    
    def assert_equal(self, other:dict, path:str="") :
        keys = set().union(self.keys()).union(other.keys())
        for k in keys :
            assert k in self and k in other, "missing: "+path+str(k)
            if isinstance(self[k], Bundle) : self[k].assert_equal(other[k], path+k+"::")
            else : assert self[k]==other[k], "different: "+path+str(k)+" - "+str(self[k])+" | "+str(other[k])
