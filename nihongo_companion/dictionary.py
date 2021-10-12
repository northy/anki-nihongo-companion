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

import requests
from bs4 import BeautifulSoup
from urllib.parse import quote

from typing import Generator, List

class Dict(object) :
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

class NihongoMaster(WebDict) :
    def search(self, query:str) -> Generator[list,int,int] :
        return_results = []

        query = quote(query)
        page = 1
        while True : #page
            soup = self.__urlGet__(f"https://nihongomaster.com/japanese/dictionary/search?type=j&q={query}&p={str(page)}")
            if soup==None : yield None, None, None; break
            results = soup.find("div", class_="results")
            if results==None : yield None, None, None; break
            for result in results.find_all("div") :
                return_results.append({
                    "title": result.find("h2").text,
                    "kana": result.find("h3").text if result.find("h3")!=None else result.find("h2").text, #may not have kana
                    "type": result.find("dt").text,
                    "english": list(map(lambda x : x.text, result.find_all("li"))),
                    "uri": result.find("a", href=True)["href"]
                })

            count = soup.find("h1", class_='text-lg md:text-2xl xl:text-4xl font-bold text-center md:text-left mt-4').text.strip().split()
            cur,tot = int(count[4]), int(count[6])

            yield return_results, cur, tot
            return_results.clear()

            if cur==tot : break
            page+=1

    def get_examples(self, uri:str) -> List[dict] :
        return_results = []

        soup = self.__urlGet__(uri)
        if soup==None : return None
        results = soup.find("div", id="examples")
        if results==None : return None
        try :
            for result in results.find("div", class_="w-full").find_all("div", class_="flex") :
                return_results.append({
                    "japanese": ''.join(map(lambda x : x.strip(),result.find("div", class_="p-2 font-bold").find_all(text=True))),
                    "english": result.find_all("div")[1].text.strip()
                })
        except :
            return None
        
        return return_results

if __name__=="__main__" :
    print("(Using nihongoMaster webdict as dictionary)")
    nm = NihongoMaster()
    query = input("What to search? ")
    results = nm.search(query)
    if results!=None :
        i=1
        for result in results :
            print(str(i)+')')
            print(result["title"])
            print(result["kana"])
            print(result["type"])
            for english in result["english"] :
                print(' -',english)
            print()
            i+=1
    else :
        print("Nothing found")
        exit(1)
    option = int(input("which one? "))
    examples = nm.get_examples(results[option-1]["uri"])
    if examples!=None :
        for example in examples :
            print(example["japanese"])
            print(example["english"])
            print()
    else :
        print("No examples")
        exit(1)
