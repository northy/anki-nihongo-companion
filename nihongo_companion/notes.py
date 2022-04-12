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

import aqt
from anki import notes
from . import dictionary
from ._vendor.katsuyou import conjugate
from ._vendor.katsuyou.util import matcher

from typing import Dict, List, Set

def update(note:notes.Note, field:str, sentences:List[Dict], entry:Dict, extraReadings:Set, dictName:str, append:bool) :
    """update note's field adding sentences"""
    configObj = aqt.mw.addonManager.getConfig(__name__)

    highlight = configObj["highlight"]
    highlight_color = configObj["highlightColor"]
    useEnglish = configObj["useEnglish"]
    
    if highlight :
        highlight_html_begin = '<span style="color:{0};">'.format(highlight_color)
        highlight_html_end = '</span>'
        highlight_html_len = len(highlight_html_begin)+len(highlight_html_end)

        highlight_words = set(entry["title"].split(', ')).union(extraReadings)
        for x in entry["kana"].split(', ') : highlight_words.add(x)
        if '' in highlight_words : highlight_words.remove('')

        #conjugate
        #TODO: extract other ways of writing kanji words
        for x in list(highlight_words) :
            if len(x)<2 : continue
            #adjective-i possibility
            if x[-1] == "い" :
                highlight_words = highlight_words.union(conjugate.Adjective(x, True).forms.unpack())
                continue
            verb = False
            #verb-ichidan possibility
            if x[-1] == "る" and x[-2] in ["り", "み", "ひ", "に", "ち", "し", "き", "い", "れ", "め", "へ", "ね", "て", "せ", "け", "え"] :
                highlight_words = highlight_words.union(conjugate.Verb(x, True, True).forms.unpack())
                verb = True
            #verb-godan possibility
            if x[-1] in ["く", "ぐ", "す", "ぶ", "む", "ぬ", "う", "つ", "る"] :
                highlight_words = highlight_words.union(conjugate.Verb(x, False, True).forms.unpack())
                verb = True
            #verb-suru possibility
            if not verb : highlight_words = highlight_words.union(conjugate.Verb(x+"する", conjugateAll=True).forms.unpack())
        
        m = matcher.Matcher(words=highlight_words)

        for sentence in sentences :
            off = 0
            for s,e in m.longest_matches(sentence["japanese"]) :
                s+=off
                e+=off
                sentence["japanese"] = sentence["japanese"][:s]+highlight_html_begin+sentence["japanese"][s:e]+highlight_html_end+sentence["japanese"][e:]
                off+=highlight_html_len

    html = "<p>{0}{1}</p>"
    
    formattedHtml = "\n<hr>\n".join(map(lambda example : html.format(example["japanese"],("<br>"+example["english"] if useEnglish and example["english"] else '')), sentences))

    if append :
        note[field] += ("\n<hr>\n" if len(note[field]) and note[field][-1]!='\n' else "<hr>\n")+formattedHtml
    else :
        note[field] = formattedHtml

    dictName = dictName.replace(" (local)",'').replace(" ",'_')
    if not(append) :
        for x in dictionary.dictionaries.keys() : note.delTag(configObj["tagName"]+"::"+x)
    note.addTag(configObj["tagName"]+"::"+dictName)

    #update the menu
    note.flush()
