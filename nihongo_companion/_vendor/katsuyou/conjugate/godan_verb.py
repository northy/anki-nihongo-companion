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
from . import i_adjective, ichidan_verb

def stem_neutral_te_form(word:str, forms:Bundle) :
    if forms is not None :
        cache = forms.recursive_get("stem", "neutral", "te_form")
        if cache is not None : return cache

    if word=="行く" or word=="いく" :
        ret = word[:-1]+"って"
        if forms is not None : forms.recursive_set("stem", "neutral", "te_form", ret)
        return ret
    translate = {
        "く": "いて",
        "ぐ": "いで",
        "す": "して",
        "ぶ": "んで",
        "む": "んで",
        "ぬ": "んで",
        "う": "って",
        "つ": "って",
        "る": "って"
    }
    ret = word[:-1]+translate[word[-1]]
    if forms is not None : forms.recursive_set("stem", "neutral", "te_form", ret)
    return ret

def stem_neutral_a_stem(word:str, forms:Bundle) :
    if forms is not None :
        cache = forms.recursive_get("stem", "neutral", "a_stem")
        if cache is not None : return cache

    translate = {
        "く": "か",
        "ぐ": "が",
        "す": "さ",
        "ぶ": "ば",
        "む": "ま",
        "ぬ": "な",
        "う": "わ",
        "つ": "た",
        "る": "ら"
    }
    ret = word[:-1]+translate[word[-1]]
    if forms is not None : forms.recursive_set("stem", "neutral", "a_stem", ret)
    return ret

def stem_neutral_i_stem(word:str, forms:Bundle) :
    if forms is not None :
        cache = forms.recursive_get("stem", "neutral", "i_stem")
        if cache is not None : return cache

    translate = {
        "く": "き",
        "ぐ": "ぎ",
        "す": "し",
        "ぶ": "び",
        "む": "み",
        "ぬ": "に",
        "う": "い",
        "つ": "ち",
        "る": "り"
    }
    ret = word[:-1]+translate[word[-1]]
    if forms is not None : forms.recursive_set("stem", "neutral", "i_stem", ret)
    return ret

def stem_neutral_e_stem(word:str, forms:Bundle) :
    if forms is not None :
        cache = forms.recursive_get("stem", "neutral", "e_stem")
        if cache is not None : return cache

    translate = {
        "く": "け",
        "ぐ": "げ",
        "す": "せ",
        "ぶ": "べ",
        "む": "め",
        "ぬ": "ね",
        "う": "え",
        "つ": "て",
        "る": "れ"
    }
    ret = word[:-1]+translate[word[-1]]
    if forms is not None : forms.recursive_set("stem", "neutral", "e_stem", ret)
    return ret

def stem_neutral_o_stem(word:str, forms:Bundle) :
    if forms is not None :
        cache = forms.recursive_get("stem", "neutral", "o_stem")
        if cache is not None : return cache

    translate = {
        "く": "こ",
        "ぐ": "ご",
        "す": "そ",
        "ぶ": "ぼ",
        "む": "も",
        "ぬ": "の",
        "う": "お",
        "つ": "と",
        "る": "ろ"
    }
    ret = word[:-1]+translate[word[-1]]
    if forms is not None : forms.recursive_set("stem", "neutral", "o_stem", ret)
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

    translate = {
        "て": "た",
        "で": "だ"
    }
    stem = stem_neutral_te_form(word, forms)
    ret = stem[:-1]+translate[stem[-1]]
    if forms is not None : forms.recursive_set("plain", "positive", "past", ret)
    return ret

def plain_positive_assumptive(word:str, forms:Bundle) :
    if forms is not None :
        cache = forms.recursive_get("plain", "positive", "assumptive")
        if cache is not None : return cache

    ret = stem_neutral_i_stem(word, forms)+"そう"
    if forms is not None : forms.recursive_set("plain", "positive", "assumptive", ret)
    return ret

def plain_positive_optative(word:str, forms:Bundle) :
    if forms is not None :
        cache = forms.recursive_get("plain", "positive", "optative")
        if cache is not None : return cache

    ret = stem_neutral_i_stem(word, forms)+"たい"
    if forms is not None : forms.recursive_set("plain", "positive", "optative", ret)
    return ret

def plain_positive_past_optative(word:str, forms:Bundle) :
    if forms is not None :
        cache = forms.recursive_get("plain", "positive", "past_optative")
        if cache is not None : return cache

    ret = i_adjective.plain_positive_past(plain_positive_optative(word, forms), None)
    if forms is not None : forms.recursive_set("plain", "positive", "past_optative", ret)
    return ret

def plain_positive_optative_te_form(word:str, forms:Bundle) :
    if forms is not None :
        cache = forms.recursive_get("plain", "positive", "optative_te_form")
        if cache is not None : return cache

    ret = i_adjective.plain_positive_te_form(plain_positive_optative(word, forms), None)
    if forms is not None : forms.recursive_set("plain", "positive", "optative_te_form", ret)
    return ret

def plain_positive_volitional(word:str, forms:Bundle) :
    if forms is not None :
        cache = forms.recursive_get("plain", "positive", "volitional")
        if cache is not None : return cache

    ret = stem_neutral_o_stem(word, forms)+"う"
    if forms is not None : forms.recursive_set("plain", "positive", "volitional", ret)
    return ret

def plain_positive_ba_conditional(word:str, forms:Bundle) :
    if forms is not None :
        cache = forms.recursive_get("plain", "positive", "ba_conditional")
        if cache is not None : return cache

    ret = stem_neutral_e_stem(word, forms)+"ば"
    if forms is not None : forms.recursive_set("plain", "positive", "ba_conditional", ret)
    return ret

def plain_positive_tara_conditional(word:str, forms:Bundle) :
    if forms is not None :
        cache = forms.recursive_get("plain", "positive", "tara_conditional")
        if cache is not None : return cache

    ret = plain_positive_past(word, forms)+"ら"
    if forms is not None : forms.recursive_set("plain", "positive", "tara_conditional", ret)
    return ret

def plain_positive_receptive(word:str, forms:Bundle) :
    if forms is not None :
        cache = forms.recursive_get("plain", "positive", "receptive")
        if cache is not None : return cache

    ret = stem_neutral_a_stem(word, forms)+"れる"
    if forms is not None : forms.recursive_set("plain", "positive", "receptive", ret)
    return ret

def plain_positive_causative(word:str, forms:Bundle) :
    if forms is not None :
        cache = forms.recursive_get("plain", "positive", "causative")
        if cache is not None : return cache

    ret = stem_neutral_a_stem(word, forms)+"せる"
    if forms is not None : forms.recursive_set("plain", "positive", "causative", ret)
    return ret

def plain_positive_potential(word:str, forms:Bundle) :
    if forms is not None :
        cache = forms.recursive_get("plain", "positive", "potential")
        if cache is not None : return cache

    ret = stem_neutral_e_stem(word, forms)+"る"
    if forms is not None : forms.recursive_set("plain", "positive", "potential", ret)
    return ret

def plain_positive_imperative(word:str, forms:Bundle) :
    if forms is not None :
        cache = forms.recursive_get("plain", "positive", "imperative")
        if cache is not None : return cache

    ret = stem_neutral_e_stem(word, forms)
    if forms is not None : forms.recursive_set("plain", "positive", "imperative", ret)
    return ret

def plain_positive_progressive(word:str, forms:Bundle) :
    if forms is not None :
        cache = forms.recursive_get("plain", "positive", "progressive")
        if cache is not None : return cache

    ret = stem_neutral_te_form(word, forms)+"いる"
    if forms is not None : forms.recursive_set("plain", "positive", "progressive", ret)
    return ret

def plain_positive_past_progressive(word:str, forms:Bundle) :
    if forms is not None :
        cache = forms.recursive_get("plain", "positive", "past_progressive")
        if cache is not None : return cache

    ret = ichidan_verb.plain_positive_past(plain_positive_progressive(word, forms), None)
    if forms is not None : forms.recursive_set("plain", "positive", "past_progressive", ret)
    return ret

def plain_positive_past_presumptive(word:str, forms:Bundle) :
    if forms is not None :
        cache = forms.recursive_get("plain", "positive", "past_presumptive")
        if cache is not None : return cache

    ret = plain_positive_past(word, forms)+"ろう"
    if forms is not None : forms.recursive_set("plain", "positive", "past_presumptive", ret)
    return ret

def plain_negative_nonpast(word:str, forms:Bundle) :
    if forms is not None :
        cache = forms.recursive_get("plain", "negative", "nonpast")
        if cache is not None : return cache

    ret = stem_neutral_a_stem(word, forms)+"ない"
    if forms is not None : forms.recursive_set("plain", "negative", "nonpast", ret)
    return ret

def plain_negative_past(word:str, forms:Bundle) :
    if forms is not None :
        cache = forms.recursive_get("plain", "negative", "past")
        if cache is not None : return cache

    ret = i_adjective.plain_positive_past(plain_negative_nonpast(word, forms), None)
    if forms is not None : forms.recursive_set("plain", "negative", "past", ret)
    return ret

def plain_negative_assumptive(word:str, forms:Bundle) :
    if forms is not None :
        cache = forms.recursive_get("plain", "negative", "assumptive")
        if cache is not None : return cache

    ret = plain_negative_nonpast(word, forms)[:-1]+"そう"
    if forms is not None : forms.recursive_set("plain", "negative", "assumptive", ret)
    return ret

def plain_negative_te_form(word:str, forms:Bundle) :
    if forms is not None :
        cache = forms.recursive_get("plain", "negative", "te_form")
        if cache is not None : return cache

    ret = i_adjective.plain_positive_te_form(plain_negative_nonpast(word, forms), None)
    if forms is not None : forms.recursive_set("plain", "negative", "te_form", ret)
    return ret

def plain_negative_optative(word:str, forms:Bundle) :
    if forms is not None :
        cache = forms.recursive_get("plain", "negative", "optative")
        if cache is not None : return cache

    ret = i_adjective.plain_negative_nonpast(plain_positive_optative(word, forms), None)
    if forms is not None : forms.recursive_set("plain", "negative", "optative", ret)
    return ret

def plain_negative_past_optative(word:str, forms:Bundle) :
    if forms is not None :
        cache = forms.recursive_get("plain", "negative", "past_optative")
        if cache is not None : return cache

    ret = i_adjective.plain_negative_past(plain_positive_optative(word, forms), None)
    if forms is not None : forms.recursive_set("plain", "negative", "past_optative", ret)
    return ret

def plain_negative_optative_te_form(word:str, forms:Bundle) :
    if forms is not None :
        cache = forms.recursive_get("plain", "negative", "optative_te_form")
        if cache is not None : return cache

    ret = i_adjective.plain_negative_te_form(plain_positive_optative(word, forms), None)
    if forms is not None : forms.recursive_set("plain", "negative", "optative_te_form", ret)
    return ret

def plain_negative_ba_conditional(word:str, forms:Bundle) :
    if forms is not None :
        cache = forms.recursive_get("plain", "negative", "ba_conditional")
        if cache is not None : return cache

    ret = i_adjective.plain_positive_ba_conditional(plain_negative_nonpast(word, forms), None)
    if forms is not None : forms.recursive_set("plain", "negative", "ba_conditional", ret)
    return ret

def plain_negative_tara_conditional(word:str, forms:Bundle) :
    if forms is not None :
        cache = forms.recursive_get("plain", "negative", "tara_conditional")
        if cache is not None : return cache

    ret = plain_negative_past(word, forms)+"ら"
    if forms is not None : forms.recursive_set("plain", "negative", "tara_conditional", ret)
    return ret

def plain_negative_receptive(word:str, forms:Bundle) :
    if forms is not None :
        cache = forms.recursive_get("plain", "negative", "receptive")
        if cache is not None : return cache

    ret = ichidan_verb.plain_negative_nonpast(plain_positive_receptive(word, forms), None)
    if forms is not None : forms.recursive_set("plain", "negative", "receptive", ret)
    return ret

def plain_negative_causative(word:str, forms:Bundle) :
    if forms is not None :
        cache = forms.recursive_get("plain", "negative", "causative")
        if cache is not None : return cache

    ret = ichidan_verb.plain_negative_nonpast(plain_positive_causative(word, forms), None)
    if forms is not None : forms.recursive_set("plain", "negative", "causative", ret)
    return ret

def plain_negative_potential(word:str, forms:Bundle) :
    if forms is not None :
        cache = forms.recursive_get("plain", "negative", "potential")
        if cache is not None : return cache

    ret = ichidan_verb.plain_negative_nonpast(plain_positive_potential(word, forms), None)
    if forms is not None : forms.recursive_set("plain", "negative", "potential", ret)
    return ret

def plain_negative_imperative(word:str, forms:Bundle) :
    if forms is not None :
        cache = forms.recursive_get("plain", "negative", "imperative")
        if cache is not None : return cache

    ret = word+"な"
    if forms is not None : forms.recursive_set("plain", "negative", "imperative", ret)
    return ret

def plain_negative_progressive(word:str, forms:Bundle) :
    if forms is not None :
        cache = forms.recursive_get("plain", "negative", "progressive")
        if cache is not None : return cache

    ret = ichidan_verb.plain_negative_nonpast(plain_positive_progressive(word, forms), None)
    if forms is not None : forms.recursive_set("plain", "negative", "progressive", ret)
    return ret

def plain_negative_past_progressive(word:str, forms:Bundle) :
    if forms is not None :
        cache = forms.recursive_get("plain", "negative", "past_progressive")
        if cache is not None : return cache

    ret = ichidan_verb.plain_negative_past(plain_positive_progressive(word, forms), None)
    if forms is not None : forms.recursive_set("plain", "negative", "past_progressive", ret)
    return ret

def polite_positive_nonpast(word:str, forms:Bundle) :
    if forms is not None :
        cache = forms.recursive_get("polite", "positive", "nonpast")
        if cache is not None : return cache

    ret = stem_neutral_i_stem(word, forms)+"ます"
    if forms is not None : forms.recursive_set("polite", "positive", "nonpast", ret)
    return ret

def polite_positive_past(word:str, forms:Bundle) :
    if forms is not None :
        cache = forms.recursive_get("polite", "positive", "past")
        if cache is not None : return cache

    ret = plain_positive_past(polite_positive_nonpast(word, forms), None)
    if forms is not None : forms.recursive_set("polite", "positive", "past", ret)
    return ret

def polite_positive_volitional(word:str, forms:Bundle) :
    if forms is not None :
        cache = forms.recursive_get("polite", "positive", "volitional")
        if cache is not None : return cache

    ret = polite_positive_nonpast(word, forms)[:-1]+"しょう"
    if forms is not None : forms.recursive_set("polite", "positive", "volitional", ret)
    return ret

def polite_positive_tara_conditional(word:str, forms:Bundle) :
    if forms is not None :
        cache = forms.recursive_get("polite", "positive", "tara_conditional")
        if cache is not None : return cache

    ret = polite_positive_past(word, forms)+"ら"
    if forms is not None : forms.recursive_set("polite", "positive", "tara_conditional", ret)
    return ret

def polite_positive_receptive(word:str, forms:Bundle) :
    if forms is not None :
        cache = forms.recursive_get("polite", "positive", "receptive")
        if cache is not None : return cache

    ret = ichidan_verb.polite_positive_nonpast(plain_positive_receptive(word, forms), None)
    if forms is not None : forms.recursive_set("polite", "positive", "receptive", ret)
    return ret

def polite_positive_causative(word:str, forms:Bundle) :
    if forms is not None :
        cache = forms.recursive_get("polite", "positive", "causative")
        if cache is not None : return cache

    ret = ichidan_verb.polite_positive_nonpast(plain_positive_causative(word, forms), None)
    if forms is not None : forms.recursive_set("polite", "positive", "causative", ret)
    return ret

def polite_positive_potential(word:str, forms:Bundle) :
    if forms is not None :
        cache = forms.recursive_get("polite", "positive", "potential")
        if cache is not None : return cache

    ret = ichidan_verb.polite_positive_nonpast(plain_positive_potential(word, forms), None)
    if forms is not None : forms.recursive_set("polite", "positive", "potential", ret)
    return ret

def polite_positive_progressive(word:str, forms:Bundle) :
    if forms is not None :
        cache = forms.recursive_get("polite", "positive", "progressive")
        if cache is not None : return cache

    ret = ichidan_verb.polite_positive_nonpast(plain_positive_progressive(word, forms), None)
    if forms is not None : forms.recursive_set("polite", "positive", "progressive", ret)
    return ret

def polite_positive_past_progressive(word:str, forms:Bundle) :
    if forms is not None :
        cache = forms.recursive_get("polite", "positive", "past_progressive")
        if cache is not None : return cache

    ret = ichidan_verb.polite_positive_past(plain_positive_progressive(word, forms), None)
    if forms is not None : forms.recursive_set("polite", "positive", "past_progressive", ret)
    return ret

def polite_negative_nonpast(word:str, forms:Bundle) :
    if forms is not None :
        cache = forms.recursive_get("polite", "negative", "nonpast")
        if cache is not None : return cache

    ret = polite_positive_nonpast(word, forms)+"せん"
    if forms is not None : forms.recursive_set("polite", "negative", "nonpast", ret)
    return ret

def polite_negative_past(word:str, forms:Bundle) :
    if forms is not None :
        cache = forms.recursive_get("polite", "negative", "past")
        if cache is not None : return cache

    ret = polite_negative_nonpast(word, forms)+"でした"
    if forms is not None : forms.recursive_set("polite", "negative", "past", ret)
    return ret

def polite_negative_optative(word:str, forms:Bundle) :
    if forms is not None :
        cache = forms.recursive_get("polite", "negative", "optative")
        if cache is not None : return cache

    ret = i_adjective.polite_negative_nonpast(plain_positive_optative(word, forms), None)
    if forms is not None : forms.recursive_set("polite", "negative", "optative", ret)
    return ret

def polite_negative_tara_conditional(word:str, forms:Bundle) :
    if forms is not None :
        cache = forms.recursive_get("polite", "negative", "tara_conditional")
        if cache is not None : return cache

    ret = polite_negative_past(word, forms)+"ら"
    if forms is not None : forms.recursive_set("polite", "negative", "tara_conditional", ret)
    return ret

def polite_negative_receptive(word:str, forms:Bundle) :
    if forms is not None :
        cache = forms.recursive_get("polite", "negative", "receptive")
        if cache is not None : return cache

    ret = ichidan_verb.polite_negative_nonpast(plain_positive_receptive(word, forms), None)
    if forms is not None : forms.recursive_set("polite", "negative", "receptive", ret)
    return ret

def polite_negative_causative(word:str, forms:Bundle) :
    if forms is not None :
        cache = forms.recursive_get("polite", "negative", "causative")
        if cache is not None : return cache

    ret = ichidan_verb.polite_negative_nonpast(plain_positive_causative(word, forms), None)
    if forms is not None : forms.recursive_set("polite", "negative", "causative", ret)
    return ret

def polite_negative_potential(word:str, forms:Bundle) :
    if forms is not None :
        cache = forms.recursive_get("polite", "negative", "potential")
        if cache is not None : return cache

    ret = ichidan_verb.polite_negative_nonpast(plain_positive_potential(word, forms), None)
    if forms is not None : forms.recursive_set("polite", "negative", "potential", ret)
    return ret

def polite_negative_imperative(word:str, forms:Bundle) :
    if forms is not None :
        cache = forms.recursive_get("polite", "negative", "imperative")
        if cache is not None : return cache

    ret = plain_negative_nonpast(word, forms)+"で"
    if forms is not None : forms.recursive_set("polite", "negative", "imperative", ret)
    return ret

def polite_negative_progressive(word:str, forms:Bundle) :
    if forms is not None :
        cache = forms.recursive_get("polite", "negative", "progressive")
        if cache is not None : return cache

    ret = ichidan_verb.polite_negative_nonpast(plain_positive_progressive(word, forms), None)
    if forms is not None : forms.recursive_set("polite", "negative", "progressive", ret)
    return ret

def polite_negative_past_progressive(word:str, forms:Bundle) :
    if forms is not None :
        cache = forms.recursive_get("polite", "negative", "past_progressive")
        if cache is not None : return cache

    ret = ichidan_verb.polite_negative_past(plain_positive_progressive(word, forms), None)
    if forms is not None : forms.recursive_set("polite", "negative", "past_progressive", ret)
    return ret

lookup = Bundle(
    stem = Bundle(
        neutral = Bundle(
            te_form = stem_neutral_te_form,
            a_stem = stem_neutral_a_stem,
            i_stem = stem_neutral_i_stem,
            e_stem = stem_neutral_e_stem,
            o_stem = stem_neutral_o_stem,
        )
    ),
    plain = Bundle(
        positive = Bundle(
            nonpast = plain_positive_nonpast,
            past = plain_positive_past,
            assumptive = plain_positive_assumptive,
            optative = plain_positive_optative,
            past_optative = plain_positive_past_optative,
            optative_te_form = plain_positive_optative_te_form,
            volitional = plain_positive_volitional,
            ba_conditional = plain_positive_ba_conditional,
            tara_conditional = plain_positive_tara_conditional,
            receptive = plain_positive_receptive,
            causative = plain_positive_causative,
            potential = plain_positive_potential,
            imperative = plain_positive_imperative,
            progressive = plain_positive_progressive,
            past_progressive = plain_positive_past_progressive,
            past_presumptive = plain_positive_past_presumptive
        ),
        negative = Bundle(
            nonpast = plain_negative_nonpast,
            past = plain_negative_past,
            assumptive = plain_negative_assumptive,
            te_form = plain_negative_te_form,
            optative = plain_negative_optative,
            past_optative = plain_negative_past_optative,
            optative_te_form = plain_negative_optative_te_form,
            ba_conditional = plain_negative_ba_conditional,
            tara_conditional = plain_negative_tara_conditional,
            receptive = plain_negative_receptive,
            causative = plain_negative_causative,
            potential = plain_negative_potential,
            imperative = plain_negative_imperative,
            progressive = plain_negative_progressive,
            past_progressive = plain_negative_past_progressive
        )
    ),

    polite = Bundle(
        positive = Bundle(
            nonpast = polite_positive_nonpast,
            past = polite_positive_past,
            volitional = polite_positive_volitional,
            tara_conditional = polite_positive_tara_conditional,
            receptive = polite_positive_receptive,
            causative = polite_positive_causative,
            potential = polite_positive_potential,
            progressive = polite_positive_progressive,
            past_progressive = polite_positive_past_progressive
        ),
        negative = Bundle(
            nonpast = polite_negative_nonpast,
            past = polite_negative_past,
            optative = polite_negative_optative,
            tara_conditional = polite_negative_tara_conditional,
            receptive = polite_negative_receptive,
            causative = polite_negative_causative,
            potential = polite_negative_potential,
            imperative = polite_negative_imperative,
            progressive = polite_negative_progressive,
            past_progressive = polite_negative_past_progressive
        )
    )
)
