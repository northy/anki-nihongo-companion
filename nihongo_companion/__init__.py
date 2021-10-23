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

from PyQt5.QtCore import ws
import anki
import aqt

from . import gui, notes, dictionary

def registerMenu() -> None :
    """Create options on card browser's menu toolbar"""
    
    from PyQt5 import QtWidgets

    def on_setup_menus(browser) -> None:
        menu = QtWidgets.QMenu("Nihongo companion", browser.form.menubar)
        browser.form.menubar.addMenu(menu)

        def addExampleSentencesToSelected() -> None :
            configObj = aqt.mw.addonManager.getConfig(__name__)

            endIt = False
            i = 0
            cards_N = len(browser.selectedNotes())
            internal_config = {
                "in_field": 0,
                "out_field": 0,
                "auto_search": False,
                "dict": configObj["defaultDict"]
            }

            for note_id in browser.selectedNotes() :
                if endIt : break
                note = browser.mw.col.getNote(note_id)
                i+=1

                #Open any card's preview
                browser.card = note.cards()[0]
                browser.singleCard = note.cards()[0]
                browser._previewer = aqt.browser.PreviewDialog(browser, browser.mw, lambda : None)
                browser._previewer.open()

                while True : #Run until select word is cancelled or skipped
                    wSelection = gui.SelectWord(browser, dictionary.dictionaries, note, internal_config)
                    wSelection.setWindowTitle(wSelection.windowTitle()+' ({0}/{1})'.format(i, cards_N))
                    wSelection.show()
                    if wSelection.exec_() == QtWidgets.QDialog.Accepted :
                        wSelection.close()
                        wExamples = gui.SelectExamples(browser, dictionary.dictionaries[internal_config["dict"]], wSelection.searchResults[wSelection.selected], note, internal_config)
                        wExamples.setWindowTitle(wExamples.windowTitle()+' ({0}/{1})'.format(i, cards_N))
                        wExamples.show()
                        wExamples.search()
                        if not(wExamples.error) and wExamples.exec_() == QtWidgets.QDialog.Accepted :
                            notes.update(browser, note, wExamples.field, [wExamples.searchResults[x] for x in wExamples.selected], wSelection.searchResults[wSelection.selected])
                            break
                        else :
                            if wExamples.error :
                                wExamples.close()
                                aqt.utils.showInfo("Nothing found!")
                    else :
                        if not(wSelection.skipped) : endIt = True
                        break
                try : browser._previewer.close()
                except : pass
                browser._previewer=None
            browser.mw.reset()
                
        action = aqt.qt.QAction("Add example sentences to selected...", menu)
        aqt.qconnect(action.triggered, addExampleSentencesToSelected)
        menu.addAction(action)
    
    anki.hooks.addHook(
        'browser.setupMenus',
        on_setup_menus,
    )
