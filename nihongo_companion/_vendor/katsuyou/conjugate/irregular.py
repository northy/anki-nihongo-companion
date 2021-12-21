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
from . import i_adjective, ichidan_verb, godan_verb

#為る、する
SURU = (lambda word : Bundle(
    stem = Bundle(
        neutral = Bundle(
            te_form = word[:-2]+("為" if word[-2]=="為" else "し")+"て",
            i_stem = word[:-2]+("為" if word[-2]=="為" else "し")
        )
    ),
    plain = Bundle(
        positive = Bundle(
            receptive = word[:-2]+("為" if word[-2]=="為" else "さ")+"れる",
            causative = word[:-2]+("為" if word[-2]=="為" else "さ")+"せる",
            potential = word[:-2]+("出来" if word[-2]=="為" else "でき")+"る",
            imperative = word[:-2]+("為" if word[-2]=="為" else "し")+"ろ"
        )
    )
), ichidan_verb.lookup)

#くる、来る
KURU = (lambda word : Bundle(
    stem = Bundle(
        neutral = Bundle(
            te_form = word[:-2]+("来" if word[-2]=="来" else "き")+"て",
            i_stem = word[:-2]+("来" if word[-2]=="来" else "き")
        )
    ),
    plain = Bundle(
        positive = Bundle(
            presumptive = word[:-2]+("来" if word[-2]=="来" else "こ")+"よう",
            receptive = word[:-2]+("来" if word[-2]=="来" else "こ")+"られる",
            causative = word[:-2]+("来" if word[-2]=="来" else "こ")+"させる",
            potential = word[:-2]+("来" if word[-2]=="来" else "こ")+"られる",
            imperative = word[:-2]+("来" if word[-2]=="来" else "こ")+"い"
        ),
        negative = Bundle(
            nonpast = word[:-2]+("来" if word[-2]=="来" else "こ")+"ない"
        )
    )
), ichidan_verb.lookup)

#いい、良い
II = (lambda word : Bundle(
    stem = Bundle(
        neutral = Bundle(
            connective = word[:-2]+("良" if word[-2]=="良" else "よ")+"く"
        )
    ),
    plain = Bundle(
        positive = Bundle(
            past = word[:-2]+("良" if word[-2]=="良" else "よ")+"かった",
            assumptive = word[:-2]+("良" if word[-2]=="良" else "よ")+"さそう",
            ba_conditional = word[:-2]+("良" if word[-2]=="良" else "よ")+"ければ"
        )
    )
), i_adjective.lookup)

#御座る、ご座る、ござる
GOZARU = (lambda word : Bundle(
    stem = Bundle(
        neutral = Bundle(
            i_stem = word[:-1]+"い"
        )
    )
), godan_verb.lookup)

#ある、有る, 在る
ARU = (lambda word : Bundle(
    plain = Bundle(
        negative = Bundle(
            nonpast = word[:-2]+("ない" if word[-2]=="あ" else "無い"),
            assumptive = word[:-2]+("なさそう" if word[-2]=="あ" else "無さそう")
        )
    )
), godan_verb.lookup)

#Returns (object, lookup)
lookup = Bundle(
    verb = Bundle(
        為る = SURU,
        する = SURU,
        くる = KURU,
        来る = KURU,
        御座る = GOZARU,
        ご座る = GOZARU,
        ござる = GOZARU,
        ある = ARU,
        有る = ARU,
        在る = ARU
    ),
    adjective = Bundle(
        いい = II,
        良い = II
    )
)
