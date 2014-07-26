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
from getpass import getuser
from os import path
from configparser import ConfigParser
from json import loads
from subprocess import call
from urllib import parse, request
from webbrowser import open_new_tab

from PyQt5.Qsci import QsciLexerPython, QsciScintilla
from PyQt5.QtGui import QColor, QIcon, QFont
from PyQt5.QtWidgets import (QApplication, QCheckBox, QComboBox, QCompleter,
                             QDialogButtonBox, QFileDialog,
                             QGraphicsDropShadowEffect, QGridLayout, QGroupBox,
                             QLabel, QMainWindow, QMessageBox,
                             QPushButton, QShortcut, QVBoxLayout, QWidget)


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
        self.setMinimumSize(400, 400)
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
        font = QFont()  # Set the default font
        font.setFamily('Monospace')
        font.setFixedPitch(True)
        font.setPointSize(12)
        self.setFont(font)
        self.setMarginsFont(font)
        self.marginClicked.connect(self.on_margin_clicked)
        self.markerDefine(QsciScintilla.Circle, self.ARROW_MARKER_NUM)
        # Set Python lexer,set style for Python comments (number 1) fixed-width
        self.lexer = QsciLexerPython()
        self.lexer.setFont(font)
        self.lexer.setDefaultFont(font)
        self.lexer.setPaper(QColor('#D5D8DB'))
        self.lexer.setDefaultPaper(QColor('#D5D8DB'))
        self.setLexer(self.lexer)
        self.SendScintilla(QsciScintilla.SCI_SETHSCROLLBAR, 0)
        self.setEdgeMode(QsciScintilla.EdgeLine)
        self.setEdgeColumn(80)
        # default colors
        self.setPaper(QColor('#272822'))
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
            if config['charset']:
                self.setUtf8('utf-8' in str(config['charset']))
            if config['indent_size']:
                self.setTabWidth(int(config['indent_size']))
            if config['end_of_line']:
                self.setEolMode(eol_dict[str(config['end_of_line']).lower()])
            if config['indent_style']:
                self.setIndentationsUseTabs('tab' in config['indent_style'])
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
        # self.statusBar().showMessage(__doc__.strip().capitalize())
        self.setWindowTitle(__doc__.strip().capitalize())
        self.setMinimumSize(480, 600)
        self.setMaximumSize(600, 1024)
        self.resize(self.minimumSize())
        self.setWindowIcon(QIcon.fromTheme("start-here"))
        self.center()
        QShortcut("Ctrl+q", self, activated=lambda: self.close())
        self.menuBar().addMenu("&File").addAction("Exit", self.close)
        windowMenu = self.menuBar().addMenu("&Window")
        windowMenu.addAction("Minimize", lambda: self.showMinimized())
        windowMenu.addAction("Maximize", lambda: self.showMaximized())
        windowMenu.addAction("Restore", lambda: self.showNormal())
        windowMenu.addAction("Center", lambda: self.center())
        windowMenu.addAction("To Mouse", lambda: self.move_to_mouse_position())
        self.menuBar().addMenu("&Config").addAction(
            "Open and load .editorconfig file",
            lambda: self.code_editor.set_editorconfig(self.get_editorconfig()))
        self.menuBar().addMenu("&Skin").addAction(
            "Open and load .color file",
            lambda: self.code_editor.set_color(self.get_color()))
        helpMenu = self.menuBar().addMenu("&Help")
        helpMenu.addAction("About Qt 5", lambda: QMessageBox.aboutQt(self))
        helpMenu.addAction("About Python 3",
                           lambda: open_new_tab('https://www.python.org'))
        helpMenu.addAction("About" + __doc__,
                           lambda: QMessageBox.about(self, __doc__, HELP))
        helpMenu.addSeparator()
        helpMenu.addAction("Keyboard Shortcut", lambda: QMessageBox.information(
            self, __doc__, "<b>Quit = CTRL+Q"))
        if sys.platform.startswith("linux"):
            helpMenu.addAction("View Source Code",
                               lambda: call('xdg-open ' + __file__, shell=True))
        helpMenu.addAction("View GitHub Repo", lambda: open_new_tab(__url__))
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
        QVBoxLayout(group0).addWidget(self.code_editor)
        # Graphic effect
        self.glow = QGraphicsDropShadowEffect(self)
        self.glow.setOffset(0)
        self.glow.setBlurRadius(99)
        self.glow.setColor(QColor(99, 255, 255))
        self.glow.setEnabled(True)
        self.code_editor.setGraphicsEffect(self.glow)
        # options
        self.strp, self.lowr = QCheckBox("Strip"), QCheckBox("Lower")
        self.newl, self.sheb = QCheckBox("Add a line"), QCheckBox("Add SheBang")
        self.mini, self.clea = QCheckBox("Auto minimize"), QCheckBox("Clean up")
        self.clip = QCheckBox("Copy URL to clipboard")
        self.open = QCheckBox("Open URL with browser")
        self.bttn = QPushButton("Create Linkode")
        self.bttn.clicked.connect(lambda: self.run(self.code_editor.text()))
        self.text_type = QComboBox()
        self.text_type.addItems(LINKODE_SUPPORTED_LANGUAGES)
        self.text_type.currentIndexChanged.connect(
            lambda: self.text_type.setToolTip(self.text_type.currentText()))
        self.text_type.setToolTip(self.text_type.currentText())
        self.strp.setToolTip("Strip the text at the end and beggining")
        self.newl.setToolTip("Add a new line at the end of text before posting")
        self.lowr.setToolTip("Lowercase all the text before posting")
        self.clip.setToolTip("Copy the full URL to Clipboard after posting")
        self.open.setToolTip("Open the new URL with a web browser on a new tab")
        self.mini.setToolTip("Automatically minimize the window after posting")
        self.clea.setToolTip("Clean up all the textarea after posting")
        self.sheb.setToolTip("Add a Python SheBang as the first line of text")
        self.strp.setChecked(True)
        self.clip.setChecked(True)
        self.newl.setChecked(True)
        self.mini.setChecked(True)
        self.clea.setChecked(True)
        self.open.setChecked(True)
        group1_layout = QGridLayout(self.group1)
        group1_layout.addWidget(self.strp, 0, 0)
        group1_layout.addWidget(self.newl, 0, 1)
        group1_layout.addWidget(self.mini, 0, 2)
        group1_layout.addWidget(self.open, 0, 3)
        group1_layout.addWidget(self.lowr, 1, 0)
        group1_layout.addWidget(self.sheb, 1, 1)
        group1_layout.addWidget(self.clea, 1, 2)
        group1_layout.addWidget(self.clip, 1, 3)
        group1_layout.addWidget(self.text_type, 2, 2)
        group1_layout.addWidget(self.bttn, 2, 3)

    def run(self, text=None):
        """Run the main method and create bash script."""
        if not text or not len(text.strip()):
            return  # If we got no text or text is just spaces then do nothing
        text = text.strip() if self.strp.isChecked() else text  # strip text
        text = text.lower() if self.lowr.isChecked() else text  # lowercase text
        text = text + "\n" if self.newl.isChecked() else text  # add new line
        text = SHEBANG + text if self.sheb.isChecked() else text  # add shebang
        text_type = str(self.text_type.currentText()).strip().lower()
        dict_data_to_send = {'content': text, 'text_type': text_type}
        raw_data_to_send = parse.urlencode(dict_data_to_send).encode("ascii")
        http_request = request.urlopen(LINKODE_API_URL, data=raw_data_to_send)
        if http_request.code == 201:  # if the request created the linkode
            jsony = loads(http_request.read().decode("utf8"))  # loads response
        else:  # else tell the user something weird happen
            QMessageBox.information(self, __doc__, "<b>Error posting Linkode!")
            return
        linkode_url = LINKODE_API_URL.replace("/api/1/linkodes/", "/{}/{}")
        linkode_url = linkode_url.format(jsony['linkode_id'], jsony['revno'])
        if self.open.isChecked():
            open_new_tab(linkode_url)  # open browser tab
        if self.clip.isChecked():
            QApplication.clipboard().setText(linkode_url)  # copy to clipboard
        if self.clea.isChecked():
            self.code_editor.clear()  # clean out the text
        if self.mini.isChecked():
            self.showMinimized()  # minimize the window
        return linkode_url

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

    def get_half_of_resolution(self):
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
