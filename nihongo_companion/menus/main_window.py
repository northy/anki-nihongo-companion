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

def on_setup_menus() -> None:
        icon = aqt.QIcon(os.path.join(ICONS_PATH, "nihongo_companion.png"))

        rtkSet = None
        rtkIndex = None

        with open(os.path.join(USER_FILES_PATH,"dictionaries/rtk.txt"), encoding="UTF-8") as f :
            line = f.readline()
            rtkSet = set(c for c in line)
            rtkIndex = [c for c in line]

        def rtkKanjiStats() -> None :
            aqt.mw.progress.start(immediate=True)
            did = aqt.mw.col.decks.selected()
            deck = aqt.mw.col.decks.get(did)
            if not deck:
                aqt.utils.showInfo("Please select a deck!")
                return
            kanjis = set()
            for noteId in aqt.mw.col.find_notes('"deck:{}"'.format(deck["name"])) :
                note = aqt.mw.col.getNote(noteId)
                for field in note.values() :
                    for c in field :
                        if c in rtkSet : kanjis.add(c)
            html = '<p style="font-size: 1.5em;">RTK 1:</p>'
            i = 1
            for kanji in rtkIndex :
                if i == 2201 : html+='<p style="font-size: 1.5em;">RTK 3:</p>'
                styling = "background-color: {}; color: inherit; text-decoration: none; padding: 2px; border: 1px solid rgba(0,0,0,0.5); font-size: 1.5em; display: inline-block;".format("green" if kanji in kanjis else "red")
                html+='<a href="https://jisho.org/search/{1}%20%23kanji" style="{0}">{1}</a>'.format(styling, kanji)
                i+=1

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
