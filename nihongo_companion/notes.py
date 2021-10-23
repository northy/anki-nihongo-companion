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

import aqt

def update(browser, note, field, sentences, entry) :
    """update note's field adding sentences"""
    #TODO: Add option to append to field, instead of replace

    configObj = aqt.mw.addonManager.getConfig(__name__)

    highlight = configObj["highlight"]
    highlight_color = configObj["highlightColor"]
    useEnglish = configObj["useEnglish"]
    
    #TODO: improve taking conjugations
    if highlight :
        highlight_html = '<span style="color:{0};">{1}</span>'

        highlight_words = set(entry["title"].split(', '))
        for x in entry["kana"].split(', ') : highlight_words.add(x)
        if '' in highlight_words : highlight_words.remove('')

        for word in highlight_words :
            for s in sentences :
                s["japanese"] = s["japanese"].replace(word, highlight_html.format(highlight_color, word))
    
    html = "<p>{0}{1}</p>"
    
    note[field] = "\n<hr>\n".join(map(lambda example : html.format(example["japanese"],("<br>"+example["english"] if useEnglish and example["english"] else '')), sentences))

    #update the menu
    note.flush()
