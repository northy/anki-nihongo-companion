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

from .util.bundle import Bundle

def stem_neutral_connective(word:str, forms:Bundle) :
    if forms is not None :
        cache = forms.recursive_get("stem", "neutral", "connective")
        if cache is not None : return cache

    ret = word[:-1]+"く"
    if forms is not None : forms.recursive_set("stem", "neutral", "connective", ret)
    return ret

def plain_positive_nonpast(word:str, forms:Bundle) :
    if forms is not None :
        cache = forms.recursive_get("plain", "positive", "nonpast")
        if cache is not None : return cache

    ret = word
    if forms is not None : forms.recursive_set("plain", "positive", "nonpast", ret)
    return ret

def plain_positive_past(word:str, forms:Bundle) :
    if forms is not None :
        cache = forms.recursive_get("plain", "positive", "past")
        if cache is not None : return cache

    ret = word[:-1]+"かった"
    if forms is not None : forms.recursive_set("plain", "positive", "past", ret)
    return ret

def plain_positive_assumptive(word:str, forms:Bundle) :
    if forms is not None :
        cache = forms.recursive_get("plain", "positive", "assumptive")
        if cache is not None : return cache

    ret = word[:-1]+"そう"
    if forms is not None : forms.recursive_set("plain", "positive", "assumptive", ret)
    return ret

def plain_positive_presumptive(word:str, forms:Bundle) :
    if forms is not None :
        cache = forms.recursive_get("plain", "positive", "presumptive")
        if cache is not None : return cache

    ret = word+"だろう"
    if forms is not None : forms.recursive_set("plain", "positive", "presumptive", ret)
    return ret

def plain_positive_ba_conditional(word:str, forms:Bundle) :
    if forms is not None :
        cache = forms.recursive_get("plain", "positive", "ba_conditional")
        if cache is not None : return cache

    ret = word[:-1]+"ければ"
    if forms is not None : forms.recursive_set("plain", "positive", "ba_conditional", ret)
    return ret

def plain_positive_te_form(word:str, forms:Bundle) :
    if forms is not None :
        cache = forms.recursive_get("plain", "positive", "te_form")
        if cache is not None : return cache

    ret = stem_neutral_connective(word, forms)+"て"
    if forms is not None : forms.recursive_set("plain", "positive", "te_form", ret)
    return ret

def plain_negative_nonpast(word:str, forms:Bundle) :
    if forms is not None :
        cache = forms.recursive_get("plain", "negative", "nonpast")
        if cache is not None : return cache

    ret = stem_neutral_connective(word, forms)+"ない"
    if forms is not None : forms.recursive_set("plain", "negative", "nonpast", ret)
    return ret

def plain_negative_past(word:str, forms:Bundle) :
    if forms is not None :
        cache = forms.recursive_get("plain", "negative", "past")
        if cache is not None : return cache

    ret = plain_positive_past(plain_negative_nonpast(word, forms), None)
    if forms is not None : forms.recursive_set("plain", "negative", "past", ret)
    return ret

def plain_negative_assumptive(word:str, forms:Bundle) :
    if forms is not None :
        cache = forms.recursive_get("plain", "negative", "assumptive")
        if cache is not None : return cache

    ret = plain_negative_nonpast(word, forms)[:-1]+"さそう"
    if forms is not None : forms.recursive_set("plain", "negative", "assumptive", ret)
    return ret

def plain_negative_presumptive(word:str, forms:Bundle) :
    if forms is not None :
        cache = forms.recursive_get("plain", "negative", "presumptive")
        if cache is not None : return cache

    ret = plain_positive_presumptive(plain_positive_past(word, forms), None)
    if forms is not None : forms.recursive_set("plain", "negative", "presumptive", ret)
    return ret

def plain_negative_ba_conditional(word:str, forms:Bundle) :
    if forms is not None :
        cache = forms.recursive_get("plain", "negative", "ba_conditional")
        if cache is not None : return cache

    ret = plain_positive_ba_conditional(plain_negative_nonpast(word, forms), None)
    if forms is not None : forms.recursive_set("plain", "negative", "ba_conditional", ret)
    return ret

def plain_negative_te_form(word:str, forms:Bundle) :
    if forms is not None :
        cache = forms.recursive_get("plain", "negative", "te_form")
        if cache is not None : return cache

    ret = plain_positive_te_form(plain_negative_nonpast(word, forms), None)
    if forms is not None : forms.recursive_set("plain", "negative", "te_form", ret)
    return ret

def polite_positive_nonpast(word:str, forms:Bundle) :
    if forms is not None :
        cache = forms.recursive_get("polite", "positive", "nonpast")
        if cache is not None : return cache

    ret = word+"です"
    if forms is not None : forms.recursive_set("polite", "positive", "nonpast", ret)
    return ret

def polite_positive_past(word:str, forms:Bundle) :
    if forms is not None :
        cache = forms.recursive_get("polite", "positive", "past")
        if cache is not None : return cache

    ret = polite_positive_nonpast(plain_positive_past(word, forms), None)
    if forms is not None : forms.recursive_set("polite", "positive", "past", ret)
    return ret

def polite_positive_presumptive(word:str, forms:Bundle) :
    if forms is not None :
        cache = forms.recursive_get("polite", "positive", "presumptive")
        if cache is not None : return cache

    ret = word+"でしょう"
    if forms is not None : forms.recursive_set("polite", "positive", "presumptive", ret)
    return ret

def polite_negative_nonpast(word:str, forms:Bundle) :
    if forms is not None :
        cache = forms.recursive_get("polite", "negative", "nonpast")
        if cache is not None : return cache

    ret = stem_neutral_connective(word, forms)+"ありません"
    if forms is not None : forms.recursive_set("polite", "negative", "nonpast", ret)
    return ret

def polite_negative_past(word:str, forms:Bundle) :
    if forms is not None :
        cache = forms.recursive_get("polite", "negative", "past")
        if cache is not None : return cache

    ret = polite_negative_nonpast(word, forms)+"でした"
    if forms is not None : forms.recursive_set("polite", "negative", "past", ret)
    return ret

def polite_negative_presumptive(word:str, forms:Bundle) :
    if forms is not None :
        cache = forms.recursive_get("polite", "negative", "presumptive")
        if cache is not None : return cache

    ret = polite_positive_presumptive(plain_negative_nonpast(word, forms), None)
    if forms is not None : forms.recursive_set("polite", "negative", "presumptive", ret)
    return ret

lookup = Bundle(
    stem = Bundle(
        neutral = Bundle(
            connective = stem_neutral_connective
        )
    ),
    plain = Bundle(
        positive = Bundle(
            nonpast = plain_positive_nonpast,
            past = plain_positive_past,
            assumptive = plain_positive_assumptive,
            presumptive = plain_positive_presumptive,
            ba_conditional = plain_positive_ba_conditional,
            te_form = plain_positive_te_form
        ),
        negative = Bundle(
            nonpast = plain_negative_nonpast,
            past = plain_negative_past,
            assumptive = plain_negative_assumptive,
            presumptive = plain_negative_presumptive,
            ba_conditional = plain_negative_ba_conditional,
            te_form = plain_negative_te_form
        )
    ),

    polite = Bundle(
        positive = Bundle(
            nonpast = polite_positive_nonpast,
            past = polite_positive_past,
            presumptive = polite_positive_presumptive
        ),
        negative = Bundle(
            nonpast = polite_negative_nonpast,
            past = polite_negative_past,
            presumptive = polite_negative_presumptive
        )
    )
)
