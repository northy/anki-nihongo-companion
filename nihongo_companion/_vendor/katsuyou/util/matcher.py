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

DEBUG = False

class Matcher(object) :
    def __init__(self, **kwargs) :
        """
        Creates an object able to check strings for the existence of the input word dictionary.

        Parameters:
        - words (iterable): The set of words to build the dictionary; OR:
        - bundle (conjugate.util.Bundle): A bundle object to build the dictionary.
    
        
        Returns:
        - Matcher object, with a built automata
        """

        self._set = None

        self._trie = None #chars (list[str])
        self._trie_d = None #depth (list[int])
        self._trie_c = None #children (list[dict[int]])
        if DEBUG : self._trie_s = None #complete string (list[str])
        self._trie_f = None #final (set)
        self._trie_p = None #parent (list[int])
        self._trie_fl = None #fail-link (list[int])
        self._trie_dl = None #dictionary-link (dict[int])

        if "words" in kwargs :
            try :
                it = iter(kwargs["words"])
            except:
                raise AttributeError("words argument is not iterable")
            self._set = kwargs["words"]
        elif "bundle" in kwargs :
            try :
                self._set = set(kwargs["bundle"].unpack())
            except :
                raise AttributeError("bundle argument does not have the unpack() method, is it really a bundle?")
        else :
            raise AttributeError("please supply the set or bundle of words")

    def _build_trie(self) :
        #implementation of the aho-corasick algorithm with fail-links
        self._trie = ['']
        if DEBUG : self._trie_s = ['']
        self._trie_d = [0]
        self._trie_c = [dict()]
        self._trie_f = set()
        self._trie_p = [0]

        i = 1
        for word in self._set :
            t = 0
            for c in word :
                if c not in self._trie_c[t] :
                    self._trie.append(c)
                    self._trie_c.append(dict())
                    self._trie_p.append(t)
                    self._trie_d.append(self._trie_d[t] + 1)
                    if DEBUG : self._trie_s.append(self._trie_s[t] + c)
                    self._trie_c[t][c] = i
                    t = i
                    i+=1
                else :
                    t = self._trie_c[t][c]
            self._trie_f.add(t)
        del self._set

        queue = []
        self._trie_fl = [0]*len(self._trie)
        self._trie_dl = dict()
        
        for x in self._trie_c[0].values() :
            queue.append(x)
            self._trie_fl[x] = 0  
        i=0
        while i<len(queue) :
            u = queue[i]
            uc = self._trie[u]

            #fail link
            v = self._trie_p[u]
            while v!=0 :
                link = self._trie_fl[v]
                if uc in self._trie_c[link] :
                    self._trie_fl[u] = self._trie_c[link][uc]
                    break
                v = link
            
            #dictionary link
            v = self._trie_fl[u]
            while v!=0 :
                if v in self._trie_f :
                    self._trie_dl[u] = v
                    break
                v = self._trie_fl[v]
            
            #add children to queue
            for v in self._trie_c[u].values() : queue.append(v)
            i+=1
        
    def matches(self, string:str) :
        if self._trie is None : self._build_trie()

        automaton = 0

        for i in range(len(string)) :
            #fail link
            while automaton!=0 :
                if string[i] in self._trie_c[automaton] : break
                automaton = self._trie_fl[automaton]
            if string[i] not in self._trie_c[automaton] : continue

            automaton = self._trie_c[automaton][string[i]]

            #got to final node
            if automaton in self._trie_f :
                start = i-self._trie_d[automaton]+1
                end = i+1
                yield start, end
            
            #dictionary link
            if automaton in self._trie_dl :
                dl = self._trie_dl[automaton]
                start = i-self._trie_d[dl]+1
                end = start+self._trie_d[dl]
                yield start, end

    def longest_matches(self, string:str) :
        if self._trie is None : self._build_trie()

        automaton = 0
        curLongest = 0
        curLongestAttrib = 0

        for i in range(len(string)) :
            while automaton!=0 :
                if string[i] in self._trie_c[automaton] : break
                automaton = self._trie_fl[automaton]
            
            if automaton==0 and curLongest!=0 :
                start = curLongestAttrib
                end = start+self._trie_d[curLongest]
                yield start, end
                curLongest = 0
                curLongestAttrib = 0

            if string[i] not in self._trie_c[automaton] : continue

            automaton = self._trie_c[automaton][string[i]]
            
            #got to final node
            if automaton in self._trie_f :
                if self._trie_d[curLongest]<=self._trie_d[automaton] :
                    curLongest = automaton
                    curLongestAttrib = i-self._trie_d[curLongest]+1
            else :
                #dictionary link
                if automaton in self._trie_dl :
                    dl = self._trie_dl[automaton]
                    if self._trie_d[curLongest]<self._trie_d[dl] :
                        curLongest = dl
                        curLongestAttrib = i-self._trie_d[curLongest]+1
        
        if curLongest!=0 :
            start = curLongestAttrib
            end = start+self._trie_d[curLongest]
            yield start, end
