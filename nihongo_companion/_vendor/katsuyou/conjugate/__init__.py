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

from . import i_adjective, ichidan_verb, godan_verb, irregular
from .util.bundle import Bundle

class Adjective(object) :
    def __init__(self, word:str, conjugateAll:bool=False) :
        assert word[-1]=="い", "Word passed as argument is not an adjective"

        self._lookup = i_adjective.lookup
        self._word = word
        self._forms = Bundle()

        if conjugateAll : self.conjugate()

    @property
    def word(self) :
        return self._word
    
    @property
    def forms(self) :
        return self._forms
    
    def conjugate(self, type:str="*", polarity:str="*", form:str="*") :
        if self._word.endswith("いい") or self._word.endswith("良い") :
            self._forms.update(irregular.II(self._word))
        
        lookup = self._lookup

        if type=="*" :
            for t in lookup.items() :
                for p in t[1].items() :
                    if polarity!="*" and p[0]!=polarity : continue
                    for f in p[1].items() :
                        if form!="*" and f[0]!=form : continue
                        f[1](self._word, self._forms)
            return
        
        lookup = lookup[type]

        if polarity=="*" :
            for p in lookup.items() :
                for f in p[1].items() :
                    if form!="*" and f[0]!=form : continue
                    f[1](self._word, self._forms)
            return
        
        lookup = lookup[polarity]
        
        if form=="*" :
            for f in lookup.items() :
                f[1](self._word, self._forms)
            return
        
        lookup[form](self._word, self._forms)

class Verb(object) :
    def __init__(self, word:str, ichidan:bool=False, conjugateAll:bool=False) :
        assert word[-1] in ["く", "ぐ", "す", "ぶ", "む", "ぬ", "う", "つ", "る"], "Word passed as argument is not a verb"

        self._word = word
        self.irregular = irregular
        self._lookup = ichidan_verb.lookup if ichidan else godan_verb.lookup
        self._forms = Bundle()

        if conjugateAll : self.conjugate()
    
    @property
    def word(self) :
        return self._word
    
    @property
    def forms(self) :
        return self._forms
    
    def conjugate(self, type:str="*", polarity:str="*", form:str="*") :
        if self._word.endswith("する") or self._word.endswith("為る") :
            self._forms.update(irregular.SURU(self._word))
            self._lookup = ichidan_verb.lookup
        elif self._word.endswith("くる") or self._word.endswith("来る") :
            self._forms.update(irregular.KURU(self._word))
            self._lookup = ichidan_verb.lookup
        elif self._word.endswith("御座る") or self._word.endswith("ござる") or self._word.endswith("ご座る") :
            self._forms.update(irregular.GOZARU(self._word))

        lookup = self._lookup

        if type=="*" :
            for t in lookup.items() :
                for p in t[1].items() :
                    if polarity!="*" and p[0]!=polarity : continue
                    for f in p[1].items() :
                        if form!="*" and f[0]!=form : continue
                        f[1](self._word, self._forms)
            return
        
        lookup = lookup[type]
        if type not in self._forms : self._forms[type] = Bundle()

        if polarity=="*" :
            for p in lookup.items() :
                for f in p[1].items() :
                    if form!="*" and f[0]!=form : continue
                    f[1](self._word, self._forms)
            return
        
        lookup = lookup[polarity]
        if polarity not in self._forms[type] : self._forms[type][polarity] = Bundle()
        
        if form=="*" :
            for f in lookup.items() :
                f[1](self._word, self._forms)
            return
        
        lookup[form](self._word, self.forms)
