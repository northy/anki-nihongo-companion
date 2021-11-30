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

import requests, re, os
from bs4 import BeautifulSoup
from urllib.parse import quote

from typing import Generator, List

from ...path import USER_FILES_PATH

class Dict(object) :
    needsSearch = True

    def search(self, query:str) -> Generator[list,int,int] :
        pass

    def get_examples(self, uri:str) -> List[dict] :
        pass

class WebDict(Dict) :
    def __urlGet__(self, url) :
        r = requests.get(url)
        if r.status_code==200 :
            soup = BeautifulSoup(r.text, 'html.parser')
            soup.prettify()
            return soup
        else :
            return None

class LocalDict(Dict) :
    def __iterator__(self, file) :
        with open(os.path.join(USER_FILES_PATH,'dictionaries/'+file), encoding="UTF-8") as f :
            for line in f :
                yield line
