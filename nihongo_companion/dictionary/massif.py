# -*- coding: utf-8 -*-

"""
MIT License

Copyright (c) 2021 Alexsandro Thomas

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from .base import *

class Massif(WebDict) :
    needsSearch = False

    def get_examples(self, uri:str) -> List[dict] :
        return_results = []

        uri = quote(uri)

        soup = self.__urlGet__(f"https://massif.la/ja/search?q={uri}")
        if soup==None : return None
        try :
            for result in soup.find_all("li", class_="text-japanese") :
                return_results.append({
                    "japanese": ''.join([x.strip() for x in result.find("div").find_all(text=True)]),
                    "english": ''
                })
        except :
            return None
        
        return return_results

if __name__=="__main__" :
    print("(Using Massif webdict as dictionary)")
    massif = Massif()
    query = input("What to search? ")
    examples = massif.get_examples(query)
    if examples!=None :
        for example in examples :
            print(example["japanese"])
            print()
    else :
        print("No examples")
        exit(1)
