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

from PyQt5 import QtWidgets
import aqt, os
import webbrowser

from ...path import ICONS_PATH, USER_FILES_PATH

# https://stackoverflow.com/a/30070664
ranges = [
    {"from": ord(u"\u3300"), "to": ord(u"\u33ff")},         # compatibility ideographs
    {"from": ord(u"\ufe30"), "to": ord(u"\ufe4f")},         # compatibility ideographs
    {"from": ord(u"\uf900"), "to": ord(u"\ufaff")},         # compatibility ideographs
    {"from": ord(u"\U0002F800"), "to": ord(u"\U0002fa1f")}, # compatibility ideographs
    #{'from': ord(u'\u3040'), 'to': ord(u'\u309f')},         # Japanese Hiragana
    #{"from": ord(u"\u30a0"), "to": ord(u"\u30ff")},         # Japanese Katakana
    {"from": ord(u"\u2e80"), "to": ord(u"\u2eff")},         # cjk radicals supplement
    {"from": ord(u"\u4e00"), "to": ord(u"\u9fff")},
    {"from": ord(u"\u3400"), "to": ord(u"\u4dbf")},
    {"from": ord(u"\U00020000"), "to": ord(u"\U0002a6df")},
    {"from": ord(u"\U0002a700"), "to": ord(u"\U0002b73f")},
    {"from": ord(u"\U0002b740"), "to": ord(u"\U0002b81f")},
    {"from": ord(u"\U0002b820"), "to": ord(u"\U0002ceaf")}  # included as of Unicode 8.0
]

def is_cjk(char):
    return any([range["from"] <= ord(char) <= range["to"] for range in ranges])

def on_setup_menus() -> None:
        icon = aqt.QIcon(os.path.join(ICONS_PATH, "nihongo_companion.png"))

        rtkDict = None
        rtkSet = None
        rtkIndex = None

        with open(os.path.join(USER_FILES_PATH,"dictionaries/rtk.txt"), encoding="UTF-8") as f :
            line = f.readline()
            rtkDict = {a:b for a,b in zip(line, range(1,3001))}
            rtkSet = set(c for c in line)
            rtkIndex = [c for c in line]

        def rtkKanjiStats() -> None :
            progress = aqt.mw.progress.start(immediate=True)
            progress.show()
            aqt.QApplication.processEvents()
            did = aqt.mw.col.decks.selected()
            deck = aqt.mw.col.decks.get(did)
            if not deck:
                aqt.utils.showInfo("Please select a deck!")
                return
            kanjis_rtk = set()
            kanjis_other = set()
            cache = set()
            cRTK1, cRTK3 = 0,0
            for noteId in aqt.mw.col.find_notes('"deck:{}"'.format(deck["name"])) :
                note = aqt.mw.col.getNote(noteId)
                for field in note.values() :
                    for c in field :
                        if c in cache : continue
                        if c in rtkSet :
                            if rtkDict[c]<=2200 : cRTK1+=1
                            else : cRTK3+=1
                            kanjis_rtk.add(c)
                        elif is_cjk(c) :
                            kanjis_other.add(c)
                        cache.add(c)
            
            html = """<h1>Stats:</h1><ul>
<li style="font-size: 1.5em">RTK 1: {}/2200 ({:.2f}%)</li>
<li style="font-size: 1.5em">RTK 3: {}/800 ({:.2f}%)</li>
<li style="font-size: 1.5em">Other: {}</li></ul>""".format(cRTK1, cRTK1/22, cRTK3, cRTK3/8, len(kanjis_other))
            i = 1
            html+='<h2>RTK 1:</h2>'
            for kanji in rtkIndex :
                if i == 2201 : html+='<h2>RTK 3:</h2>'
                styling = "background-color: {}; color: inherit; text-decoration: none; padding: 2px; border: 1px solid rgba(0,0,0,0.5); font-size: 1.5em; display: inline-block;".format("green" if kanji in kanjis_rtk else "red")
                html+='<a href="https://jisho.org/search/{1}%20%23kanji" style="{0}">{1}</a>'.format(styling, kanji)
                i+=1
            
            html+='<h2>Other kanji (not in RTK):</h2>'
            for kanji in kanjis_other :
                styling = "color: inherit; text-decoration: none; padding: 2px; border: 1px solid rgba(0,0,0,0.5); font-size: 1.5em; display: inline-block;"
                html+='<a href="https://jisho.org/search/{1}%20%23kanji" style="{0}">{1}</a>'.format(styling, kanji)

            app = aqt.QDialog(aqt.mw)
            app.setWindowTitle("NihongoMaster: RTK kanji stats")
            app.setWindowIcon(icon)
            app.resize(500, 350)
            layout = aqt.QVBoxLayout()
            layout.setContentsMargins(0,0,0,0)
            webview = aqt.webview.AnkiWebView()
            layout.addWidget(webview)
            webview.stdHtml(html)
            buttons = aqt.QDialogButtonBox(aqt.QDialogButtonBox.Close)
            layout.addWidget(buttons)
            buttons.rejected.connect(app.accept)
            app.setLayout(layout)
            aqt.utils.restoreGeom(app, "nc-rtkanji")
            aqt.mw.progress.finish()
            app.exec_()
            aqt.utils.saveGeom(app, "nc-rtkanji")

        menu = QtWidgets.QMenu("Nihongo companion", aqt.mw)
        menu.setIcon(icon)
        aqt.mw.form.menuTools.addMenu(menu)

        action = aqt.qt.QAction("Check kanjis in deck...", menu)
        aqt.qconnect(action.triggered, rtkKanjiStats)
        menu.addAction(action)

        action = aqt.qt.QAction("Help", menu)
        aqt.qconnect(action.triggered, lambda : webbrowser.open('https://northy.github.io/anki-nihongo-companion/'))
        menu.addAction(action)
