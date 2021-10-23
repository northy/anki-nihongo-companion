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

from . import ui_SelectWord, ui_SelectExamples
from .. import dictionary

class SelectWord(aqt.QDialog) :
    """Select which word from a dictionary query to use"""

    def __init__(self, parent, dictionaries, note, internal_config) :
        #init window
        super(SelectWord,self).__init__(parent)
        self.setWindowFlags(aqt.Qt.Dialog | aqt.Qt.MSWindowsFixedSizeDialogHint)

        #data and methods
        self.closed = False #window is closed (bool)
        self.skipped = False #user skipped (bool)
        self.searchResults = None #search result rows (List[dict])
        self.selected = None #selected row (int)
        
        self.dictionaries = dictionaries
        self.note = note
        self.internal_config = internal_config

        #setup UI
        self.ui = ui_SelectWord.Ui_diagSelectWord()
        self.ui.setupUi(self)
        self.ui.pbSearch.setHidden(True)
        self.__updateDropdowns()

        #hooks
        self.ui.bSearch.clicked.connect(self.__search)
        self.ui.bCancel.clicked.connect(self.__cancel)
        self.ui.bSkip.clicked.connect(self.__skip)
        self.ui.bConfirm.clicked.connect(self.__confirm)
        self.ui.listResults.doubleClicked.connect(self.__confirm)
        self.ui.cbDict.currentTextChanged.connect(self.__changeDict)

        #begin search
        if self.internal_config["auto_search"] and self.dictionaries[self.internal_config["dict"]].needsSearch : self.__search()

    def __changeDict(self, value) :
        self.ui.listResults.setEnabled(False)
        self.ui.listResults.clear()
        self.ui.bConfirm.setEnabled(False if self.dictionaries[value].needsSearch else True)
        self.ui.bSearch.setEnabled(True if self.dictionaries[value].needsSearch else False)

    def __updateDropdowns(self) -> None :
        for field,_ in self.note.items() :
            self.ui.cbField_in.addItem(field)
        self.ui.cbField_in.setCurrentIndex(self.internal_config["in_field"])

        for field,_ in self.dictionaries.items() :
            self.ui.cbDict.addItem(field)
        self.ui.cbDict.setCurrentText(self.internal_config["dict"])

    def __search(self) -> None :
        self.ui.bSearch.setEnabled(False)

        query = self.note.values()[self.ui.cbField_in.currentIndex()]

        self.ui.listResults.setEnabled(False)
        self.ui.bConfirm.setEnabled(False)
        self.ui.listResults.clear()

        self.ui.pbSearch.setValue(0)
        self.ui.pbSearch.setHidden(False)

        gen = self.dictionaries[self.ui.cbDict.currentText()].search(query)
        self.searchResults = []

        for results, cur, tot in gen :
            if self.closed : return
            elif results!=None and len(results)>0 :
                aqt.QApplication.processEvents() #update
                self.ui.pbSearch.setValue(100*cur//tot)
                self.searchResults += results
                for result in results :
                    item = aqt.QListWidgetItem()
                    item.setText(
                        result["title"]+'\n'+
                        result["kana"]+" ["+result["type"]+"]\n - "+
                        "\n - ".join(result["english"])
                    )
                    self.ui.listResults.addItem(item)
                    if self.selected == None :
                        self.selected = 0
                        self.ui.listResults.setCurrentItem(item)
                aqt.QApplication.processEvents() #update
            else :
                self.searchResults = None
                self.ui.pbSearch.setValue(0)
                self.ui.bSearch.setEnabled(True)
                self.ui.pbSearch.setHidden(True)
                aqt.utils.showInfo("Nothing found!")
                return
        
        self.ui.listResults.setEnabled(True)
        self.ui.bConfirm.setEnabled(True)
        self.ui.bSearch.setEnabled(True)
    
    #overload close event if needed
    def closeEvent(self, a0) -> None:
        return super().closeEvent(a0)

    def __cancel(self) -> None :
        self.closed = True
        self.close()
    
    def __confirm(self) -> None :
        if self.dictionaries[self.ui.cbDict.currentText()].needsSearch :
            if len(self.ui.listResults.selectedIndexes())==0 :
                aqt.utils.showInfo("No word selected!")
                return
            self.selected = self.ui.listResults.selectedIndexes()[0].row()
        else :
            sel = self.note.values()[self.ui.cbField_in.currentIndex()]
            self.searchResults = [{
                "title": sel,
                "uri": sel,
                "kana": ''
            }]
            self.selected = 0
        self.internal_config["in_field"] = self.ui.cbField_in.currentIndex()
        self.internal_config["auto_search"] = True
        self.internal_config["dict"] = self.ui.cbDict.currentText()
        self.accept()
    
    def __skip(self) -> None :
        self.skipped = True
        self.__cancel()

class SelectExamples(aqt.QDialog) :
    """Select which examples from a dictionary query to use"""

    def __init__(self, parent, dictionary, queryWord:dict, note, internal_config) :
        #init window
        super(SelectExamples,self).__init__(parent)
        self.setWindowFlags(aqt.Qt.Dialog | aqt.Qt.MSWindowsFixedSizeDialogHint)

        #data and methods
        self.closed = False
        self.dictionary = dictionary
        self.queryWord = queryWord
        self.internal_config = internal_config
        self.searchResults = None
        self.selected = None
        self.error = False
        self.field = None
        self.note = note

        #setup UI
        self.ui = ui_SelectExamples.Ui_diagSelectExamples()
        self.ui.setupUi(self)
        self.__resizeHeaders()
        self.__updateDropdowns()
        self.ui.cbField_out.setCurrentIndex(self.internal_config["out_field"])

        #hooks
        self.ui.bCancel.clicked.connect(self.__cancel)
        self.ui.bConfirm.clicked.connect(self.__confirm)
        quit = aqt.QAction("Quit", self)
        quit.triggered.connect(self.__cancel)
    
    def __updateDropdowns(self) -> None :
        for field,_ in self.note.items() :
            self.ui.cbField_out.addItem(field)
    
    def __resizeHeaders(self) -> None:
        #TODO: Wrap text
        header = self.ui.tExamples.horizontalHeader()
        header.setSectionResizeMode(aqt.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(0, aqt.QHeaderView.Stretch)
        header.setSectionResizeMode(1, aqt.QHeaderView.Stretch)

        self.ui.tExamples.setSelectionBehavior(aqt.QAbstractItemView.SelectRows)

    def search(self) -> None :
        self.ui.pbSearch.setValue(50)

        self.searchResults = self.dictionary.get_examples(self.queryWord['uri'])
        if self.searchResults!=None and len(self.searchResults)>0 :
            if self.closed : return
            self.ui.tExamples.setRowCount(len(self.searchResults))
            i = 0
            for example in self.searchResults :
                item = aqt.QTableWidgetItem()
                item.setText(example['japanese'])
                self.ui.tExamples.setItem(i,0,item)
                item = aqt.QTableWidgetItem()
                item.setText(example['english'])
                self.ui.tExamples.setItem(i,1,item)
                i+=1
                aqt.QApplication.processEvents() #update
            self.ui.tExamples.selectRow(0)
            self.ui.pbSearch.setValue(100)
            self.ui.tExamples.setEnabled(True)
            self.ui.bConfirm.setEnabled(True)
            self.ui.tExamples.resizeRowsToContents()
        else :
            self.error = True

    def __cancel(self) -> None :
        self.closed = True
        self.close()
    
    def __confirm(self) -> None :
        if len(self.ui.tExamples.selectedIndexes())==0 :
            aqt.utils.showInfo("No example selected!")
            return
        self.field = self.note.keys()[self.ui.cbField_out.currentIndex()]
        self.selected = list(sorted(set(map(lambda index : index.row(), self.ui.tExamples.selectedIndexes()))))
        self.internal_config["out_field"] = self.ui.cbField_out.currentIndex()
        self.accept()
