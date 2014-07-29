#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PEP8:OK, LINT:OK, PY3:OK


# metadata
""" Linkode GUI """
__version__ = ' 0.0.1 '
__license__ = ' GPLv3+ '
__author__ = ' JuanCarlos '
__email__ = ' juancarlospaco@gmail.com '
__url__ = 'https://github.com/juancarlospaco/linkode-gui#linkode-gui'
__docformat__ = 'html'


# imports
import sys
from getopt import getopt
from json import loads
from os import path
from subprocess import call
from urllib import parse, request
from webbrowser import open_new_tab
from configparser import ConfigParser
from random import choice

from PyQt5.Qsci import QsciLexerPython, QsciScintilla
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QColor, QFont, QIcon
from PyQt5.QtNetwork import QNetworkProxyFactory
from PyQt5.QtWidgets import (QApplication, QCheckBox, QComboBox, QFileDialog,
                             QGraphicsDropShadowEffect, QGridLayout, QGroupBox,
                             QMainWindow, QMessageBox, QPushButton, QShortcut,
                             QVBoxLayout, QWidget, QInputDialog)


LINKODE_API_URL = "http://linkode.org/api/1/linkodes/"
SHEBANG = "#!/usr/bin/env python\n# -*- coding: utf-8 -*-\n#\n\n\n"
HELP = """<h3>Linkode GUI</h3><b>Linkode Desktop App!</b><br>Version {}, {}.
DEV: <a href=https://github.com/juancarlospaco>JuanCarlos</a>
""".format(__version__, __license__)
LINKODE_SUPPORTED_LANGUAGES = sorted((
    'Auto', 'C', 'C#', 'C++', 'CSS', 'Clojure', 'CoffeeScript', 'D', 'Diff',
    'Erlang', 'Go', 'HTML', 'HTMLmixed', 'Haskell', 'JSON', 'Java',
    'JavaScript', 'Lua', 'MarkDown', 'PHP', 'Perl', 'Plain Text', 'Python', 'R',
    'Ruby', 'Rust', 'Scala', 'Shell', 'XML', 'http', 'sql', 'tex'))


###############################################################################


class Simpleditor(QsciScintilla):
    ARROW_MARKER_NUM = 8

    def __init__(self, parent=None):
        super(Simpleditor, self).__init__(parent)
        self.setMinimumSize(300, 300)
        self.setEdgeMode(QsciScintilla.EdgeLine)
        self.setEdgeColumn(80)
        self.setFolding(QsciScintilla.BoxedTreeFoldStyle)
        self.setBraceMatching(QsciScintilla.SloppyBraceMatch)
        self.setCaretLineVisible(True)
        self.setMarginLineNumbers(1, True)
        self.setMarginWidth(1, 35)
        self.setMarginSensitivity(1, True)
        self.setAutoCompletionCaseSensitivity(False)
        self.setAutoCompletionSource(QsciScintilla.AcsAll)
        self.setAutoCompletionThreshold(2)
        self.setAutoIndent(True)
        self.setBackspaceUnindents(True)
        self.setIndentationGuides(True)
        self.setIndentationsUseTabs(False)
        self.setWhitespaceVisibility(True)
        self.setUtf8(True)
        self.setTabWidth(4)
        self.setEolMode(QsciScintilla.EolUnix)
        self.lexer, font = QsciLexerPython(), QFont()  # Set the font and lexer
        font.setFamily('Monospace')
        font.setFixedPitch(True)
        font.setPointSize(12)
        self.setFont(font)
        self.setMarginsFont(font)
        self.marginClicked.connect(self.on_margin_clicked)
        self.markerDefine(QsciScintilla.Circle, self.ARROW_MARKER_NUM)
        self.lexer.setFont(font)
        self.lexer.setDefaultFont(font)
        self.lexer.setPaper(QColor('#D5D8DB'))
        self.lexer.setDefaultPaper(QColor('#D5D8DB'))
        self.setLexer(self.lexer)
        self.SendScintilla(QsciScintilla.SCI_SETHSCROLLBAR, 0)
        self.setEdgeMode(QsciScintilla.EdgeLine)
        self.ensureCursorVisible()
        self.setEdgeColumn(80)
        self.setPaper(QColor('#272822'))  # default colors
        self.setEdgeColor(QColor("#00FFFF"))
        self.setSelectionBackgroundColor(QColor('#FFF'))
        self.setSelectionForegroundColor(QColor('#000'))
        self.setCaretLineBackgroundColor(QColor('#FFF'))
        self.setMarginsBackgroundColor(QColor('#292C2F'))
        self.setMarginsForegroundColor(QColor('#FFF'))
        self.setCaretForegroundColor(QColor('#000'))
        self.setFoldMarginColors(QColor("#00FFFF"), QColor("#333300"))
        self.setMarkerBackgroundColor(QColor("#00FFFF"), self.ARROW_MARKER_NUM)

    def on_margin_clicked(self, nmargin, nline, modifiers):
        """Toggle marker for the line the margin was clicked on."""
        if self.markersAtLine(nline) != 0:
            self.markerDelete(nline, self.ARROW_MARKER_NUM)
        else:
            self.markerAdd(nline, self.ARROW_MARKER_NUM)

    def set_editorconfig(self, config):
        """Take a parsed .editorconfig dict object and apply it."""
        eol_dict = {'cr': QsciScintilla.EolWindows, 'lf': QsciScintilla.EolUnix,
                    'crlf': QsciScintilla.EolMac}
        try:
            if config['indent_size']:
                self.setTabWidth(int(config['indent_size']))
            if config['end_of_line']:
                self.setEolMode(eol_dict[str(config['end_of_line']).lower()])
            if config['indent_style']:
                self.setIndentationsUseTabs('tab' in config['indent_style'])
            if config['charset']:
                self.setUtf8('utf-8' in str(config['charset']))
        except Exception as errors:
            print((" ERROR: " + errors))

    def set_color(self, colors):
        """Take a parsed .color dict object and apply it."""
        self.lexer.setPaper(QColor(colors["editor-background"]))
        self.lexer.setDefaultPaper(QColor(colors["editor-background"]))
        self.lexer.setColor(QColor(colors["editor-text"]))
        self.setPaper(QColor(colors["editor-background"]))
        self.setEdgeColor(QColor(colors["editor-background"]))
        self.setCaretLineBackgroundColor(QColor(colors["current-line"]))
        self.setMarginsBackgroundColor(QColor(colors["fold-area"]))
        self.setMarginsForegroundColor(QColor(colors["fold-arrow"]))
        self.setCaretForegroundColor(QColor(colors["editor-text"]))
        self.setColor(QColor(colors["editor-text"]))
        self.setMatchedBraceBackgroundColor(colors["brace"])
        self.setIndentationGuidesForegroundColor(colors["extras"])
        self.setFoldMarginColors(
            QColor(colors["string2"]), QColor(colors["string"]))
        self.setSelectionBackgroundColor(
            QColor(colors["editor-selection-background"]))
        self.setSelectionForegroundColor(
            QColor(colors["editor-selection-color"]))
        self.setMarkerBackgroundColor(
            QColor(colors["editor-background"]), self.ARROW_MARKER_NUM)


###############################################################################


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__()
        QNetworkProxyFactory.setUseSystemConfiguration(True)
        self.father = None  # linkode id of the root linkode if any
        self.the_last_of_us = None  # revno revision number of the last linkode
        # self.statusBar().showMessage(__doc__.strip().capitalize())
        self.setWindowTitle(__doc__.strip().capitalize())
        self.setMinimumSize(480, 480)
        self.setMaximumSize(800, 1024)
        self.resize(self.minimumSize().width(), self.get_half_resolution()[1])
        self.setWindowIcon(QIcon.fromTheme("start-here"))
        self.center()
        QShortcut("Ctrl+q", self, activated=lambda: self.close())
        fileMenu = self.menuBar().addMenu("&File")
        fileMenu.addAction(
            "Open", lambda: self.code_editor.setText(self.open()))
        fileMenu.addAction("Save", lambda: self.save(self.code_editor.text()))
        fileMenu.addSeparator()
        fileMenu.addAction("Exit", self.close)
        editMenu = self.menuBar().addMenu("&Edit")
        editMenu.addAction("Undo", lambda: self.code_editor.undo())
        editMenu.addAction("Redo", lambda: self.code_editor.redo())
        editMenu.addSeparator()
        editMenu.addAction("Cut", lambda: self.code_editor.cut())
        editMenu.addAction("Copy", lambda: self.code_editor.copy())
        editMenu.addAction("Paste", lambda: self.code_editor.paste())
        editMenu.addAction(
            "Delete", lambda: self.code_editor.removeSelectedText())
        editMenu.addSeparator()
        editMenu.addAction("Select all", lambda: self.code_editor.selectAll())
        editMenu.addSeparator()
        editMenu.addAction(
            "lower all",
            lambda: self.code_editor.setText(self.code_editor.text().lower()))
        editMenu.addAction(
            "UPPER all",
            lambda: self.code_editor.setText(self.code_editor.text().upper()))
        editMenu.addAction(
            "Title Word all",
            lambda: self.code_editor.setText(self.code_editor.text().title()))
        editMenu.addAction(
            "Capitalize all", lambda:
            self.code_editor.setText(self.code_editor.text().capitalize()))
        editMenu.addAction(
            "InvertCase all", lambda:
            self.code_editor.setText(self.code_editor.text().swapcase()))
        editMenu.addAction(
            "RaNdOmIzeCaSe all", lambda: self.code_editor.setText(
                ''.join(choice((str.upper, str.lower))(x)
                        for x in self.code_editor.text())))
        editMenu.addSeparator()
        editMenu.addAction("Clear all !", lambda: self.code_editor.clear())
        editMenu.addAction("Focus Editor", lambda: self.code_editor.setFocus())
        viewMenu = self.menuBar().addMenu("&View")
        viewMenu.addAction("Zoom In", lambda: self.code_editor.zoomIn())
        viewMenu.addAction("Zoom Out", lambda: self.code_editor.zoomOut())
        viewMenu.addAction(
            "Zoom To...", lambda: self.code_editor.zoomTo(QInputDialog.getInt(
                None, __doc__, "<b>Zoom factor ?:", 1, 1, 9)[0]))
        viewMenu.addAction("Zoom Reset", lambda: self.code_editor.zoomTo(1))
        self.menuBar().addMenu("&Config").addAction(
            "Open and load .editorconfig file",
            lambda: self.code_editor.set_editorconfig(self.get_editorconfig()))
        self.menuBar().addMenu("&Skin").addAction(
            "Open and load .color file",
            lambda: self.code_editor.set_color(self.get_color()))
        windowMenu = self.menuBar().addMenu("&Window")
        windowMenu.addAction("Minimize", lambda: self.showMinimized())
        windowMenu.addAction("Maximize", lambda: self.showMaximized())
        windowMenu.addAction("Restore", lambda: self.showNormal())
        windowMenu.addAction("Center", lambda: self.center())
        windowMenu.addAction("To Mouse", lambda: self.move_to_mouse_position())
        helpMenu = self.menuBar().addMenu("&Help")
        helpMenu.addAction("About Qt 5", lambda: QMessageBox.aboutQt(self))
        helpMenu.addAction("About Python 3",
                           lambda: open_new_tab('https://www.python.org'))
        helpMenu.addAction("About" + __doc__,
                           lambda: QMessageBox.about(self, __doc__, HELP))
        helpMenu.addAction("About Linkode",
                           lambda: open_new_tab('http://linkode.org/about'))
        helpMenu.addSeparator()
        helpMenu.addAction("Keyboard Shortcut", lambda: QMessageBox.information(
            self, __doc__, "<b>Quit = CTRL + Q"))
        if not sys.platform.startswith("win"):
            helpMenu.addAction("View Source Code", lambda: call(
                ('xdg-open ' if sys.platform.startswith("linux") else 'open ') +
                __file__, shell=True))
        helpMenu.addAction("View GitHub Repo", lambda: open_new_tab(__url__))
        helpMenu.addAction("Report Bugs", lambda: open_new_tab(
            'https://github.com/juancarlospaco/linkode-gui/issues?state=open'))
        # widgets
        container = QWidget()
        container_layout = QVBoxLayout(container)
        self.setCentralWidget(container)
        group0, self.group1 = QGroupBox("Code"), QGroupBox("Options")
        # option to show or hide some widgets on the gui
        self.guimode = QComboBox()
        self.guimode.addItems(('Full UX / UI', 'Simple UX / UI'))
        self.guimode.setCurrentIndex(1)
        self._set_guimode()
        self.guimode.setStyleSheet("""QComboBox{background:transparent;border:0;
            margin-left:25px;color:gray;text-decoration:underline}""")
        self.guimode.currentIndexChanged.connect(self._set_guimode)
        container_layout.addWidget(self.guimode)
        container_layout.addWidget(group0)
        container_layout.addWidget(self.group1)
        # source code area editor
        self.code_editor = Simpleditor()
        self.code_editor.textChanged.connect(self._on_code_editor_text_changed)
        QVBoxLayout(group0).addWidget(self.code_editor)
        # Graphic effect
        self.glow = QGraphicsDropShadowEffect(self)
        self.glow.setOffset(0)
        self.glow.setBlurRadius(75)
        self.glow.setColor(QColor(99, 255, 255))
        self.glow.setEnabled(False)
        self.code_editor.setGraphicsEffect(self.glow)
        # Timer to start
        self.code_editor_timer = QTimer(self)
        self.code_editor_timer.setSingleShot(True)
        self.code_editor_timer.timeout.connect(self._code_editor_timer_timeout)
        # options
        self.strp, self.lowr = QCheckBox("Strip"), QCheckBox("Lower")
        self.newl, self.sheb = QCheckBox("Add a line"), QCheckBox("Add SheBang")
        self.mini, self.clea = QCheckBox("Auto minimize"), QCheckBox("Clean up")
        self.clip = QCheckBox("Copy URL to clipboard")
        self.webo = QCheckBox("Open URL with browser")
        self.bttn = QPushButton("Create Linkode")
        self.bttn.clicked.connect(
            lambda: self.post_to_linkode(self.code_editor.text()))
        self.text_type = QComboBox()
        self.text_type.addItems(LINKODE_SUPPORTED_LANGUAGES)
        self.text_type.currentIndexChanged.connect(
            lambda: self.text_type.setToolTip(self.text_type.currentText()))
        self.text_type.setToolTip(self.text_type.currentText())
        self.strp.setToolTip("Strip the text at the end and beggining")
        self.newl.setToolTip("Add a new line at the end of text before posting")
        self.lowr.setToolTip("Lowercase all the text before posting")
        self.clip.setToolTip("Copy the full URL to Clipboard after posting")
        self.webo.setToolTip("Open the new URL with a web browser on a new tab")
        self.mini.setToolTip("Automatically minimize the window after posting")
        self.clea.setToolTip("Clean up all the text, start new Linkode tree !")
        self.sheb.setToolTip("Add a Python SheBang as the first line of text")
        self.strp.setChecked(True)
        self.clip.setChecked(True)
        self.newl.setChecked(True)
        self.mini.setChecked(True)
        self.webo.setChecked(True)
        group1_layout = QGridLayout(self.group1)
        group1_layout.addWidget(self.strp, 0, 0)
        group1_layout.addWidget(self.newl, 0, 1)
        group1_layout.addWidget(self.mini, 0, 2)
        group1_layout.addWidget(self.webo, 0, 3)
        group1_layout.addWidget(self.lowr, 1, 0)
        group1_layout.addWidget(self.sheb, 1, 1)
        group1_layout.addWidget(self.clea, 1, 2)
        group1_layout.addWidget(self.clip, 1, 3)
        group1_layout.addWidget(self.text_type, 2, 2)
        group1_layout.addWidget(self.bttn, 2, 3)

    def post_to_linkode(self, text=None):
        """Take text str if any and process to post it to linkode,returns url"""
        if not text or not len(text.strip()):
            return  # If we got no text or text is just spaces then do nothing
        text = text.strip() if self.strp.isChecked() else text  # strip text
        text = text.lower() if self.lowr.isChecked() else text  # lowercase text
        text = text + "\n" if self.newl.isChecked() else text  # add new line
        text = SHEBANG + text if self.sheb.isChecked() else text  # add shebang
        text_type = str(self.text_type.currentText()).strip().lower()  # type
        dict_data_to_send = {'content': text, 'text_type': text_type}  # dict
        if self.father:  # this linkode is child of a grand parent root linkode
            dict_data_to_send['parent'] = str(self.the_last_of_us).strip()
            linkode_api_url = LINKODE_API_URL + self.father
        else:  # poor orphan child :(
            linkode_api_url = LINKODE_API_URL
        raw_data_to_send = parse.urlencode(dict_data_to_send).encode("ascii")
        http_request = request.urlopen(linkode_api_url, data=raw_data_to_send)
        if http_request.code == 201:  # if the request created the linkode
            jsony = loads(http_request.read().decode("utf8"))  # loads response
        else:  # else tell the user something weird happen
            QMessageBox.information(self, __doc__, "<b>Error posting Linkode!")
            return
        linkodeurl = LINKODE_API_URL.replace("/api/1/linkodes/", "/{}/{}")
        if self.father:
            linkodeurl = linkodeurl.format(self.father, jsony['revno'])
        else:
            linkodeurl = linkodeurl.format(jsony['linkode_id'], jsony['revno'])
        if self.webo.isChecked():
            open_new_tab(linkodeurl)  # open browser tab
        if self.clip.isChecked():
            QApplication.clipboard().setText(linkodeurl)  # copy to clipboard
        if self.mini.isChecked():
            self.showMinimized()  # minimize the window
        if not self.father and not self.clea.isChecked():
            self.father = jsony['linkode_id']  # orphan get adopted by father :)
            self.the_last_of_us = jsony['revno']  # the last of linkodes revno
        if self.clea.isChecked():  # this is like a full Reset
            self.code_editor.clear()  # clean out the text
            self.father, self.the_last_of_us = None, None  # Start a new tree
        self.glow.setEnabled(False)
        return linkodeurl

    def _on_code_editor_text_changed(self):
        """Start or stop the Timer based on itself."""
        if self.code_editor_timer.isActive():
            self.code_editor_timer.stop()
        self.glow.setEnabled(True)
        self.code_editor_timer.start(60 * 1000)  # 60 seconds * 1000 = milisec

    def _code_editor_timer_timeout(self):
        """Post to Linkode callbacky when the timer timeouts."""
        self.post_to_linkode(self.code_editor.text())

    def get_editorconfig(self, config_file=None):
        """Open, read and parse a .editorconfig file and return dict object."""
        if not config_file:
            config_file = str(QFileDialog.getOpenFileName(
                self, __doc__ + " - Open .editorconfig !", path.expanduser("~"),
                "Open Source Editor Config files (*.editorconfig)")[0]).strip()
        if config_file and path.isfile(config_file):
            config = ConfigParser()
            config.read(config_file)
            return config

    def get_color(self, color_file=None):
        """Open, read and parse a .color file and return dict object."""
        if not color_file:
            color_file = str(QFileDialog.getOpenFileName(
                self, __doc__ + " - Open .color file !", path.expanduser("~"),
                "Ninja-IDE Editor Color files (*.color)")[0]).strip()
        if color_file and path.isfile(color_file):
            with open(color_file, 'r') as json_file:
                return loads(json_file.read().strip())

    def _set_guimode(self):
        """Switch between simple and full UX."""
        for widget in (self.group1, self.statusBar(), self.menuBar()):
            widget.hide() if self.guimode.currentIndex() else widget.show()
        self.resize(self.minimumSize()
                    if self.guimode.currentIndex() else self.maximumSize())
        self.center()

    def save(self, text=None, filename=None):
        """Save text as filename, if no text return False, if no filename ask"""
        if not text:
            return False
        if not filename:
            filename = str(QFileDialog.getSaveFileName(
                self, __doc__ + "- Save source code file", path.expanduser("~"),
                "Python (*.py);;JavaScript (*.js);;TXT (*.txt);;All (*.*)")[0])
        if filename:
            with open(filename, 'w') as file_to_write:
                file_to_write.write(text)
        return path.isfile(filename)

    def open(self, filename=None):
        """Open text from filename,if no text return None,if no filename ask"""
        if not filename:
            filename = str(QFileDialog.getOpenFileName(
                self, __doc__ + "- Open source code file", path.expanduser("~"),
                "Python (*.py);;JavaScript (*.js);;TXT (*.txt);;All (*.*)")[0])
        if filename and path.isfile(filename):
            with open(filename, 'r') as file_to_read:
                text = file_to_read.read()
        if text:
            return text

    def center(self):
        """Center the Window on the Current Screen,with Multi-Monitor support"""
        window_geometry = self.frameGeometry()
        mousepointer_position = QApplication.desktop().cursor().pos()
        screen = QApplication.desktop().screenNumber(mousepointer_position)
        centerPoint = QApplication.desktop().screenGeometry(screen).center()
        window_geometry.moveCenter(centerPoint)
        self.move(window_geometry.topLeft())

    def move_to_mouse_position(self):
        """Center the Window on the Current Mouse position."""
        window_geometry = self.frameGeometry()
        window_geometry.moveCenter(QApplication.desktop().cursor().pos())
        self.move(window_geometry.topLeft())

    def get_half_resolution(self):
        """Get half of the screen resolution."""
        mouse_pointer_position = QApplication.desktop().cursor().pos()
        screen = QApplication.desktop().screenNumber(mouse_pointer_position)
        widt = QApplication.desktop().screenGeometry(screen).size().width() // 2
        hei = QApplication.desktop().screenGeometry(screen).size().height() // 2
        return (widt, hei)

    def closeEvent(self, event):
        ' Ask to Quit '
        the_conditional_is_true = QMessageBox.question(
            self, __doc__.title(), 'Quit ?.', QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No) == QMessageBox.Yes
        event.accept() if the_conditional_is_true else event.ignore()


###############################################################################


def main():
    ' Main Loop '
    application = QApplication(sys.argv)
    application.setApplicationName(__doc__.strip().lower())
    application.setOrganizationName(__doc__.strip().lower())
    application.setOrganizationDomain(__doc__.strip())
    application.setWindowIcon(QIcon.fromTheme("start-here"))
    try:
        opts, args = getopt(sys.argv[1:], 'hv', ('version', 'help'))
    except:
        pass
    for o, v in opts:
        if o in ('-h', '--help'):
            print(''' Usage:
                  -h, --help        Show help informations and exit.
                  -v, --version     Show version information and exit.''')
            return sys.exit(1)
        elif o in ('-v', '--version'):
            print(__version__)
            return sys.exit(1)
    mainwindow = MainWindow()
    mainwindow.show()
    sys.exit(application.exec_())


if __name__ in '__main__':
    main()
