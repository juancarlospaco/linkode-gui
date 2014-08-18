#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PEP8:OK, LINT:OK, PY3:OK


#############################################################################
## This file may be used under the terms of the GNU General Public
## License version 2.0 or 3.0 as published by the Free Software Foundation
## and appearing in the file LICENSE.GPL included in the packaging of
## this file.  Please review the following information to ensure GNU
## General Public Licensing requirements will be met:
## http:#www.fsf.org/licensing/licenses/info/GPLv2.html and
## http:#www.gnu.org/copyleft/gpl.html.
##
## This file is provided AS IS with NO WARRANTY OF ANY KIND, INCLUDING THE
## WARRANTY OF DESIGN, MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.
#############################################################################


# metadata
""" Linkode GUI """
__version__ = ' 0.0.1 '
__license__ = ' GPLv3+ '
__author__ = ' JuanCarlos '
__email__ = ' juancarlospaco@gmail.com '
__url__ = 'https://github.com/juancarlospaco/linkode-gui#linkode-gui'
__docformat__ = 'html'
__source__ = ('https://raw.githubusercontent.com/juancarlospaco/'
              'linkode-gui/master/linkode-gui.py')


# imports
import sys
from sys import builtin_module_names
from pkgutil import iter_modules
from base64 import b64encode, urlsafe_b64encode
from datetime import datetime
from getopt import getopt
from json import loads
from os import nice, path
from random import choice, sample
from re import sub
from subprocess import call
from urllib import parse, request
from webbrowser import open_new_tab
from string import ascii_letters
from tempfile import mkstemp
from getpass import getuser
from platform import linux_distribution
import codecs

from configparser import ConfigParser
from PyQt5.Qsci import QsciLexerPython, QsciScintilla, QsciAPIs
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QColor, QFont, QIcon
from PyQt5.QtNetwork import QNetworkProxyFactory
from PyQt5.QtWidgets import (QApplication, QCheckBox, QColorDialog, QComboBox,
                             QFileDialog, QGraphicsDropShadowEffect,
                             QGridLayout, QGroupBox, QInputDialog, QMainWindow,
                             QMessageBox, QPushButton, QShortcut, QVBoxLayout,
                             QWidget, QFontDialog)


###############################################################################


LINKODE_API_URL = "http://linkode.org/api/1/linkodes/"
SHEBANG = "#!/usr/bin/env python\n# -*- coding: utf-8 -*-\n#\n\n\n"
HELP = """<h3>Linkode GUI</h3><b>Linkode Desktop App!</b><br>Version {}, {}.
DEV: <a href=https://github.com/juancarlospaco>JuanCarlos</a>
""".format(__version__, __license__)
LINKODE_SUPPORTED_LANGUAGES = tuple(sorted((
    'Auto', 'C', 'C#', 'C++', 'CSS', 'Clojure', 'CoffeeScript', 'D', 'Diff',
    'Erlang', 'Go', 'HTML', 'HTMLmixed', 'Haskell', 'JSON', 'Java',
    'JavaScript', 'Lua', 'MarkDown', 'PHP', 'Perl', 'Plain Text', 'Python', 'R',
    'Ruby', 'Rust', 'Scala', 'Shell', 'XML', 'http', 'sql', 'tex')))
CSS_SNIPPET = """@charset 'utf-8';
@import url(//netdna.bootstrapcdn.com/bootstrap/3.2.0/css/bootstrap.min.css);
@import url(//fonts.googleapis.com/css?family=Oxygen);*{font-family:Oxygen};"""
IMPSUM = tuple(sorted(("""at vero eos et accusamus et iusto odio dignissimos
ducimus qui blanditiis praesentium voluptatum deleniti atque corrupti quos in e
dolores et quas molestias excepturi sint occaecati cupiditate non provident,
similique sunt culpa qui officia deserunt mollitia animi, id est laborum et
dolorum fuga. Et ne harum quidem rerum facilis est et expedita distinctio. Nam
libero tempore, cum soluta nobis est eligendi optio cumque nihil impedit quo
minus id quod maxime te placeat facere possimus, omnis voluptas assumenda est,
omnis dolor repellendus. Temporibus autem quibusdam et aut officiis debitis aut
rerum necessitatibus ur y saepe eveniet ut et voluptates repudiandae sint et
molestiae non recusandae. a Itaque earum rerum hic tenetur a sapiente delectus,
ut aut reiciendis repellat. voluptatibus maiores alias consequatur aut illum aut
perferendis doloribus asperiores et o voluptate""".strip().lower().split(" "))))
# http://standards.freedesktop.org/icon-naming-spec/icon-naming-spec-latest.html
STD_ICON_NAMES = tuple(sorted(("""address-book-new application-exit weather-snow
appointment-new call-start call-stop contact-new document-new document-open
document-open-recent document-page-setup document-print document-print-preview
document-properties document-revert document-save document-save-as document-send
edit-clear edit-copy edit-cut edit-delete edit-find edit-find-replace edit-paste
edit-redo edit-select-all edit-undo folder-new format-indent-less user-idle
format-indent-more format-justify-center format-justify-fill format-justify-left
format-justify-right format-text-direction-ltr format-text-direction-rtl
format-text-bold format-text-italic format-text-underline weather-showers
format-text-strikethrough go-bottom go-down go-first go-home go-jump go-last
go-next go-previous go-top go-up help-about help-contents help-faq insert-image
insert-link insert-object insert-text list-add list-remove mail-forward
mail-mark-important mail-mark-junk mail-mark-notjunk mail-mark-read user-offline
mail-mark-unread mail-message-new mail-reply-all mail-reply-sender mail-send
mail-send-receive media-eject media-playback-pause media-playback-start
media-playback-stop media-record media-seek-backward media-seek-forward
media-skip-backward media-skip-forward object-flip-horizontal weather-clear
object-flip-vertical object-rotate-left object-rotate-right process-stop
system-lock-screen system-log-out system-run system-search system-reboot
system-shutdown tools-check-spelling view-fullscreen view-refresh view-restore
view-sort-ascending view-sort-descending window-close window-new zoom-fit-best
zoom-in zoom-original zoom-out process-working accessories-calculator user-away
accessories-character-map accessories-dictionary accessories-text-editor
help-browser multimedia-volume-control preferences-desktop-accessibility
preferences-desktop-font preferences-desktop-keyboard preferences-desktop-locale
preferences-desktop-multimedia preferences-desktop-screensaver sync-error
preferences-desktop-theme preferences-desktop-wallpaper system-file-manager
system-software-install system-software-update utilities-system-monitor
utilities-terminal applications-accessories applications-development task-due
applications-engineering applications-games applications-graphics printer-error
applications-internet applications-multimedia applications-office network-idle
applications-other applications-science applications-system security-high
applications-utilities preferences-desktop preferences-desktop-peripherals
preferences-desktop-personal preferences-other preferences-system folder-open
preferences-system-network system-help audio-card audio-input-microphone battery
camera-photo camera-video camera-web computer drive-harddisk drive-optical
drive-removable-media input-gaming input-keyboard input-mouse input-tablet
media-flash media-floppy media-optical media-tape modem multimedia-player
network-wired network-wireless pda phone printer scanner video-display text-html
emblem-default emblem-documents emblem-downloads emblem-favorite mail-signed
emblem-important emblem-mail emblem-photos emblem-readonly emblem-shared
emblem-symbolic-link emblem-synchronized emblem-system emblem-unreadable
face-angel face-angry face-crying face-devilish face-embarrassed face-cool
face-kiss face-laugh face-monkey face-plain face-raspberry face-sad face-sick
face-smile face-smile-big face-smirk face-surprise face-tired face-uncertain
face-wink face-worried application-x-executable audio-x-generic font-x-generic
image-x-generic package-x-generic text-x-generic weather-storm network-server
text-x-generic-template text-x-script video-x-generic x-office-address-book
x-office-calendar x-office-document x-office-presentation x-office-spreadsheet
folder folder-remote network-workgroup start-here user-bookmarks user-desktop
user-home user-trash appointment-missed appointment-soon audio-volume-high
audio-volume-low audio-volume-medium audio-volume-muted battery-caution
battery-low dialog-error dialog-information dialog-password dialog-question
dialog-warning folder-drag-accept folder-visiting image-loading image-missing
mail-attachment mail-unread mail-read mail-replied mail-signed-verified
media-playlist-repeat media-playlist-shuffle network-error network-offline
network-receive network-transmit network-transmit-receive printer-printing
security-medium security-low software-update-available software-update-urgent
sync-synchronizing task-past-due user-available user-trash-full weather-fog
weather-clear-night weather-few-clouds weather-few-clouds-night weather-overcast
weather-severe-alert weather-showers-scattered
""".strip().lower().replace("\n", " ").split(" "))))


###############################################################################


class Simpleditor(QsciScintilla):
    ARROW_MARKER_NUM = 8

    def __init__(self, parent=None):
        super(Simpleditor, self).__init__(parent)
        self.setMinimumSize(100, 100)
        self.setEdgeMode(QsciScintilla.EdgeLine)
        self.setEdgeColumn(80)
        self.setFolding(QsciScintilla.BoxedTreeFoldStyle)
        self.setBraceMatching(QsciScintilla.SloppyBraceMatch)
        self.setCaretLineVisible(True)
        self.setMarginLineNumbers(1, True)
        self.setMarginWidth(1, 50)
        self.setMarginSensitivity(1, True)
        self.setAutoCompletionCaseSensitivity(False)
        self.setAutoCompletionSource(QsciScintilla.AcsAll)
        self.setAutoCompletionThreshold(1)
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
        autocompletion_api = QsciAPIs(self.lexer)
        for word_for_autocomplete in builtin_module_names:
            autocompletion_api.add(word_for_autocomplete)
        for word_for_autocomplete in iter_modules():
            autocompletion_api.add(word_for_autocomplete[1])
        for word_for_autocomplete in tuple(__builtins__.__dict__.keys()):
            autocompletion_api.add(word_for_autocomplete)
        for word_for_autocomplete in tuple(dir(__builtins__)):
            autocompletion_api.add(word_for_autocomplete)
        autocompletion_api.add(getuser())
        autocompletion_api.prepare()
        self.setLexer(self.lexer)
        # self.SendScintilla(QsciScintilla.SCI_SETHSCROLLBAR, 0)
        self.setEdgeMode(QsciScintilla.EdgeLine)
        self.ensureCursorVisible()
        self.setEdgeColumn(80)
        self.setPaper(QColor('#272822'))  # default colors
        self.setEdgeColor(QColor("#00FFFF"))
        self.setSelectionBackgroundColor(QColor('#000'))
        self.setSelectionForegroundColor(QColor('#FFF'))
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
        self.setMatchedBraceBackgroundColor(QColor(colors["brace"]))
        self.setIndentationGuidesForegroundColor(QColor(colors["extras"]))
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
        self.setMinimumSize(525, 400)
        self.setMaximumSize(1024, 1024)
        self.resize(1024, 768)
        self.setWindowIcon(QIcon.fromTheme("start-here"))
        self.center()
        QShortcut("Ctrl+q", self, activated=lambda: self.close())
        fileMenu = self.menuBar().addMenu("&File")
        fileMenu.addAction(
            "Open", lambda: self.code_editor.setText(self.open()))
        fileMenu.addAction("Save", lambda: self.save(self.code_editor.text()))
        fileMenu.addSeparator()
        fileMenu.addAction("Open from Web URL",
                           lambda: self.code_editor.setText(self.fetch()))
        fileMenu.addAction("Preview on Web Browser",
                           lambda: self.previeweb(self.code_editor.text()))
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
        editMenu.addAction("Clear all!", lambda: self.code_editor.clear())
        editMenu.addSeparator()
        editMenu.addAction("Focus editor", lambda: self.code_editor.setFocus())
        editMenu.addAction(
            "Jump to Line...", lambda: self.code_editor.setCursorPosition(int(
                QInputDialog.getInt(self, __doc__, "Line ?:", 1, 1)[0]) - 1, 0))
        editMenu.addSeparator()
        editMenu.addAction("Count code lines", lambda: QMessageBox.information(
            self, __doc__, self.count_code_lines(self.code_editor.text())))
        editMenu.addAction("Force ignore modifications", lambda:
                           self.code_editor.setModified(False))
        formatMenu = self.menuBar().addMenu("&Format")
        formatMenu.addAction(
            "lower selected text", lambda: self.code_editor.replaceSelectedText(
                self.code_editor.selectedText().lower()))
        formatMenu.addAction(
            "UPPER selected text", lambda: self.code_editor.replaceSelectedText(
                self.code_editor.selectedText().upper()))
        formatMenu.addAction(
            "Title selected text", lambda: self.code_editor.replaceSelectedText(
                self.code_editor.selectedText().title()))
        formatMenu.addAction("Capitalize selected text", lambda:
                             self.code_editor.replaceSelectedText(
                                 self.code_editor.selectedText().capitalize()))
        formatMenu.addAction("Swapcase selected text", lambda:
                             self.code_editor.replaceSelectedText(
                                 self.code_editor.selectedText().swapcase()))
        formatMenu.addAction(
            "RaNdOmCaSe selected text", lambda:
            self.code_editor.replaceSelectedText(
                self.ramdomcase(self.code_editor.selectedText())))
        # http://en.wikipedia.org/wiki/Letter_case
        formatMenu.addAction(
            "CamelCase selected text", lambda:
            self.code_editor.replaceSelectedText(
                self.code_editor.selectedText().title().replace(" ", "")))
        formatMenu.addAction(
            "Snake_case selected text", lambda:
            self.code_editor.replaceSelectedText(
                self.code_editor.selectedText().replace(" ", "_")))
        formatMenu.addAction(
            "Spinal-case selected text", lambda:
            self.code_editor.replaceSelectedText(
                self.code_editor.selectedText().replace(" ", "-")))
        formatMenu.addSeparator()
        formatMenu.addAction(
            "Split words from CamelCase", lambda:
            self.code_editor.replaceSelectedText(sub(
                r'([A-Z])', r' \1', self.code_editor.selectedText()).lower()))
        formatMenu.addAction(
            "Merge words to CamelCase", lambda:
            self.code_editor.replaceSelectedText("".join((
                self.code_editor.selectedText().title().split()))))
        formatMenu.addAction(
            "CamelCase to under_score", lambda:
            self.code_editor.replaceSelectedText("_".join((
                sub(r'([A-Z])', r' \1',
                    self.code_editor.selectedText()).lower().split()))))
        sourceMenu = self.menuBar().addMenu("&Source")
        sourceMenu.addAction(
            "Sort selected text", lambda: self.code_editor.replaceSelectedText(
                "".join(sorted(self.code_editor.selectedText()))))
        sourceMenu.addAction("Reverse selected text", lambda:  # not same [::-1]
                             self.code_editor.replaceSelectedText("".join(
                                 reversed(self.code_editor.selectedText()))))
        sourceMenu.addAction(  # randomize the selected characters
            "Randomize selected text", lambda:
            self.code_editor.replaceSelectedText("".join(sample(
                self.code_editor.selectedText(),
                len(self.code_editor.selectedText())))))
        sourceMenu.addAction(  # cleans up and sanitize all weird characters
            "Sanitize weird characters from selected text", lambda:
            self.code_editor.replaceSelectedText(
                sub("[^\x00-\x7F]+", "", self.code_editor.selectedText())))
        sourceMenu.addAction(
            "Base64 encode selected text", lambda:
            self.code_editor.replaceSelectedText(str(b64encode(bytes(
                self.code_editor.selectedText(), "utf-8")))))
        sourceMenu.addAction(
            "URL Safe Base64 encode selected text", lambda:
            self.code_editor.replaceSelectedText(str(urlsafe_b64encode(bytes(
                self.code_editor.selectedText(), "utf-8")))))
        sourceMenu.addAction(
            "URLencode selected text", lambda:
            self.code_editor.replaceSelectedText(parse.quote_plus(
                self.code_editor.selectedText(), encoding="utf-8")))
        sourceMenu.addAction(
            "ROT13 encode selected text", lambda:
            self.code_editor.replaceSelectedText(
                codecs.encode(self.code_editor.selectedText(), "rot-13")))
        sourceMenu.addAction(
            "Replace Tabs with Spaces", lambda: self.code_editor.setText(
                self.code_editor.text().replace("\t", "    ")))
        sourceMenu.addAction(
            "Invert HEX color on selected text", lambda:
            self.code_editor.replaceSelectedText(
                self.code_editor.selectedText().lower().translate(
                    str.maketrans('0123456789abcdef', 'fedcba9876543210'))))
        sourceMenu.addSeparator()
        sourceMenu.addAction("Join lines of selected text", lambda:
                             self.code_editor.replaceSelectedText("".join(
                                 self.code_editor.selectedText().splitlines())))
        sourceMenu.addAction(
            "Join lines with semicolon of selected text", lambda:
            self.code_editor.replaceSelectedText("; ".join(
                self.code_editor.selectedText().splitlines())))
        sourceMenu.addSeparator()
        sourceMenu.addAction("Google selected text", lambda: open_new_tab(
            "https://google.com/search?q=" + self.code_editor.selectedText()))
        sourceMenu.addAction("PyPI Search selected text", lambda: open_new_tab(
            "https://pypi.python.org/pypi?%3Aaction=search&term=" +
            self.code_editor.selectedText()))
        sourceMenu.addAction(
            "StackOverflow Search selected text", lambda: open_new_tab(
                "https://stackoverflow.com/search?q=" +
                self.code_editor.selectedText()))
        insertMenu = self.menuBar().addMenu("&Insert")
        insertMenu.addAction(
            "Lorem Impsum...", lambda: self.code_editor.insert(self.lorem()))
        insertMenu.addAction("Horizontal line",
                             lambda: self.code_editor.insert(self.comment()))
        insertMenu.addAction("Comment Title", lambda:
                             self.code_editor.insert(self.commentitle()))
        insertMenu.addAction("Python SheBang",
                             lambda: self.code_editor.insert(SHEBANG))
        insertMenu.addAction("Base CSS Snippet",
                             lambda: self.code_editor.insert(self.cssnippet()))
        insertMenu.addAction(
            "Date and Time", lambda: self.code_editor.insert(
                datetime.now().strftime(" %A %B %d-%m-%Y %H:%M:%S %p ")))
        insertMenu.addAction(
            "HEX Color from picker...", lambda: self.code_editor.insert(
                '"{}"'.format(QColorDialog.getColor().name())))
        insertMenu.addAction("CSS Font from picker...", lambda:
                             self.code_editor.insert(self.cssfont()))
        insertMenu.addAction("Qt Standard Icon...",
                             lambda: self.code_editor.insert(self.std_icon()))
        insertMenu.addAction("Random Password...",
                             lambda: self.code_editor.insert(self.rnd_pass()))
        insertMenu.addSeparator()
        insertSubmenu = insertMenu.addMenu("Debugging tricks")
        insertSubmenu.addAction(
            "wdb.set_trace()", lambda:
            self.code_editor.insert("__import__('wdb').set_trace()  #FIXME"))
        insertSubmenu.addAction(
            "pudb.set_trace()", lambda:
            self.code_editor.insert("__import__('pudb').set_trace()  #FIXME"))
        insertSubmenu.addAction(
            "ipdb.set_trace()", lambda:
            self.code_editor.insert("__import__('ipdb').set_trace()  #FIXME"))
        insertSubmenu.addAction(
            "pdb.set_trace()", lambda:
            self.code_editor.insert("__import__('pdb').set_trace()  #FIXME"))
        insertSubmenu.addSeparator()
        insertSubmenu.addAction(
            "print('#' * 80)", lambda:
            self.code_editor.insert("print('#' * 80)  #FIXME"))
        insertSubmenu.addAction(
            "print('BEGIN METHOD / FUNCTION')", lambda:
            self.code_editor.insert("print('BEGIN METHOD / FUNCTION')  #FIXME"))
        insertSubmenu.addAction(
            "print('END METHOD / FUNCTION')", lambda:
            self.code_editor.insert("print('END METHOD / FUNCTION')  #FIXME"))
        insertSubmenu.addSeparator()
        insertSubmenu.addAction(
            "Array(80).join('#'); debugger;", lambda:
            self.code_editor.insert("Array(80).join('#'); debugger;  //FIXME"))
        insertSubmenu.addAction(
            "console.log('BEGIN FUNCTION');", lambda:
            self.code_editor.insert("console.log('BEGIN FUNCTION');  //FIXME"))
        insertSubmenu.addAction(
            "console.log('END FUNCTION');", lambda:
            self.code_editor.insert("console.log('END FUNCTION');  //FIXME"))
        insertSubmenu2 = insertMenu.addMenu("Code Comments")
        insertSubmenu2.addAction("FIXME", lambda:
                                 self.code_editor.insert("  #FIXME "))
        insertSubmenu2.addAction("TODO", lambda:
                                 self.code_editor.insert("  #TODO "))
        insertSubmenu2.addAction("OPTIMIZE", lambda:
                                 self.code_editor.insert("  #OPTIMIZE "))
        insertSubmenu2.addSeparator()
        insertSubmenu2.addAction("lint:enable", lambda:
                                 self.code_editor.insert("  # lint:enable"))
        insertSubmenu2.addAction("lint:disable", lambda:
                                 self.code_editor.insert("  # lint:disable"))
        insertSubmenu2.addAction("lint:ok", lambda:
                                 self.code_editor.insert("  # lint:ok"))
        insertSubmenu2.addSeparator()
        insertSubmenu2.addAction("isort:skip", lambda:
                                 self.code_editor.insert("  # isort:skip"))
        insertSubmenu2.addAction("isort:skip_file", lambda:
                                 self.code_editor.insert("  # isort:skip_file"))
        insertSubmenu2.addSeparator()
        insertSubmenu2.addAction("pylint:disable", lambda:
                                 self.code_editor.insert("  # pylint:disable"))
        insertSubmenu2.addAction("pylint:enable", lambda:
                                 self.code_editor.insert("  # pylint:enable"))
        insertSubmenu2.addSeparator()
        insertSubmenu2.addAction("pragma: no cover", lambda:
                                 self.code_editor.insert("  # pragma:no cover"))
        insertSubmenu2.addAction("pyflakes:ignore", lambda:
                                 self.code_editor.insert("  # pyflakes:ignore"))
        viewMenu = self.menuBar().addMenu("&View")
        viewMenu.addAction("Zoom In", lambda: self.code_editor.zoomIn())
        viewMenu.addAction("Zoom Out", lambda: self.code_editor.zoomOut())
        viewMenu.addAction(
            "Zoom To...", lambda: self.code_editor.zoomTo(QInputDialog.getInt(
                self, __doc__, "<b>Zoom factor ?:", 1, 1, 9)[0]))
        viewMenu.addAction("Zoom Reset", lambda: self.code_editor.zoomTo(1))
        configMenu = self.menuBar().addMenu("&Config")
        configMenu.addAction(
            "Load .editorconfig Settings",
            lambda: self.code_editor.set_editorconfig(self.get_editorconfig()))
        configMenu.addAction(
            "Load .color Theme",
            lambda: self.code_editor.set_color(self.get_color()))
        configMenu.addAction(
            "Load .qss Skin", lambda: self.setStyleSheet(self.skin()))
        windowMenu = self.menuBar().addMenu("&Window")
        windowMenu.addAction("Minimize", lambda: self.showMinimized())
        windowMenu.addAction("Maximize", lambda: self.showMaximized())
        windowMenu.addAction("Restore", lambda: self.showNormal())
        windowMenu.addAction("FullScreen", lambda: self.showFullScreen())
        windowMenu.addAction("Center", lambda: self.center())
        windowMenu.addAction("Top-Left", lambda: self.move(0, 0))
        windowMenu.addAction("To Mouse", lambda: self.move_to_mouse_position())
        windowMenu.addSeparator()
        windowMenu.addAction(
            "Increase size", lambda:
            self.resize(self.size().width() * 1.3, self.size().height() * 1.3))
        windowMenu.addAction("Decrease size", lambda:
                             self.resize(self.size().width() // 1.3,
                                         self.size().height() // 1.3))
        windowMenu.addAction("Minimum size", lambda:
                             self.resize(self.minimumSize()))
        windowMenu.addAction("Maximum size", lambda:
                             self.resize(self.maximumSize()))
        windowMenu.addAction("Horizontal Wide", lambda: self.resize(
            self.maximumSize().width(), self.minimumSize().height()))
        windowMenu.addAction("Vertical Tall", lambda: self.resize(
            self.minimumSize().width(), self.maximumSize().height()))
        windowMenu.addSeparator()
        windowMenu.addAction("Disable Resize", lambda:
                             self.setFixedSize(self.size()))
        windowMenu.addAction("Set Font Family...", lambda:
                             self.setFont(QFontDialog.getFont()[0]))
        helpMenu = self.menuBar().addMenu("&Help")
        helpMenu.addAction("About Qt 5", lambda: QMessageBox.aboutQt(self))
        helpMenu.addAction("About Python 3",
                           lambda: open_new_tab('https://www.python.org'))
        helpMenu.addAction("About" + __doc__,
                           lambda: QMessageBox.about(self, __doc__, HELP))
        helpMenu.addAction("About Linkode",
                           lambda: open_new_tab('http://linkode.org/about'))
        helpMenu.addSeparator()
        helpMenu.addAction("Learn Python", lambda:
                           open_new_tab('https://docs.python.org/3/tutorial'))
        if not sys.platform.startswith("win"):
            helpMenu.addAction("View Source Code", lambda: call(
                ('xdg-open ' if sys.platform.startswith("linux") else 'open ') +
                __file__, shell=True))
        helpMenu.addAction("View GitHub Repo", lambda: open_new_tab(__url__))
        helpMenu.addSeparator()
        helpMenu.addAction("Keyboard Shortcut", lambda: QMessageBox.information(
            self, __doc__, "<b>Quit = CTRL + Q"))
        helpMenu.addAction("Report Bugs", lambda: open_new_tab(
            'https://github.com/juancarlospaco/linkode-gui/issues?state=open'))
        helpMenu.addAction("Check Updates", lambda: self.check_for_updates())
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
        self.glow.setBlurRadius(50)
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
        self.auto = QCheckBox("Auto Save")
        self.bttn = QPushButton("Create Linkode")
        self.bttn.setToolTip(self.bttn.text())
        self.bttn.setStatusTip(self.bttn.toolTip())
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
        self.auto.setToolTip("Auto Save to Linkode (60sec since last modified)")
        self.strp.setStatusTip(self.strp.toolTip())
        self.newl.setStatusTip(self.newl.toolTip())
        self.lowr.setStatusTip(self.lowr.toolTip())
        self.clip.setStatusTip(self.clip.toolTip())
        self.webo.setStatusTip(self.webo.toolTip())
        self.mini.setStatusTip(self.mini.toolTip())
        self.clea.setStatusTip(self.clea.toolTip())
        self.sheb.setStatusTip(self.sheb.toolTip())
        self.auto.setStatusTip(self.auto.toolTip())
        self.strp.setChecked(True)
        self.clip.setChecked(True)
        self.newl.setChecked(True)
        self.mini.setChecked(True)
        self.webo.setChecked(True)
        self.auto.setChecked(True)
        group1_layout = QGridLayout(self.group1)
        group1_layout.addWidget(self.strp, 0, 0)
        group1_layout.addWidget(self.newl, 0, 1)
        group1_layout.addWidget(self.mini, 0, 2)
        group1_layout.addWidget(self.webo, 0, 3)
        group1_layout.addWidget(self.lowr, 1, 0)
        group1_layout.addWidget(self.sheb, 1, 1)
        group1_layout.addWidget(self.clea, 1, 2)
        group1_layout.addWidget(self.clip, 1, 3)
        group1_layout.addWidget(self.auto, 2, 0)
        group1_layout.addWidget(self.text_type, 2, 2)
        group1_layout.addWidget(self.bttn, 2, 3)

    def post_to_linkode(self, text=None):
        """Take text str if any and process to post it to linkode,returns url"""
        if not text or not len(text.strip()) or not self.auto.isChecked():
            self.glow.setEnabled(False)
            return  # If we got no text or text is just spaces then do nothing
        if text and len(text.strip()) < 5:  # No Spamm,show a message,but allow
            QMessageBox.information(self, __doc__, """<b>Anti-Spamm!:<br>Your
            text is less than 5 Characters long, please dont Spamm Linkode!.""")
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
        self.bttn.setText(  # change the text on the button like on linkode web
            "Save new version" if self.father else "Create Linkode")
        self.bttn.setToolTip(self.bttn.text())
        self.bttn.setStatusTip(self.bttn.toolTip())
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
        """Open, read and parse a .editorconfig file and return dict object.
        >>> isinstance(MainWindow().get_editorconfig("./linkode.editorconfig"),\
                       ConfigParser)
        True"""
        if not config_file:
            config_file = str(QFileDialog.getOpenFileName(
                self, __doc__ + " - Open .editorconfig !", path.expanduser("~"),
                "Open Source Editor Config files (*.editorconfig)")[0]).strip()
        if config_file and path.isfile(config_file):
            config = ConfigParser()
            config.read(config_file)
            return config

    def get_color(self, color_file=None):
        """Open, read and parse a .color file and return dict object.
        >>> isinstance(MainWindow().get_color("./monokai.color"), dict)
        True"""
        if not color_file:
            color_file = str(QFileDialog.getOpenFileName(
                self, __doc__ + " - Open .color file !", path.expanduser("~"),
                "Ninja-IDE Editor Color files (*.color)")[0]).strip()
        if color_file and path.isfile(color_file):
            with open(color_file, 'r') as json_file:
                return loads(json_file.read().strip())

    def std_icon(self, icon=None):
        """Return a string with opendesktop standard icon name for Qt.
        >>> MainWindow().std_icon('folder')
        'PyQt5.QtGui.QIcon.fromTheme("folder")'"""
        if not icon:
            icon = QInputDialog.getItem(self, __doc__, "<b>Choose Icon name ?:",
                                        STD_ICON_NAMES, 0, False)[0]
        if icon:
            return 'PyQt5.QtGui.QIcon.fromTheme("{}")'.format(icon)

    def _set_guimode(self):
        """Switch between simple and full UX."""
        for widget in (self.group1, self.statusBar(), self.menuBar()):
            widget.hide() if self.guimode.currentIndex() else widget.show()
        self.resize(self.minimumSize()
                    if self.guimode.currentIndex() else self.maximumSize())
        self.center()

    def save(self, text=None, filename=None):
        """Save text as filename, if no text return False, if no filename ask.
        >>> MainWindow().save('X', __import__('tempfile').mkstemp(text=True)[1])
        True"""
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
        """Open text from filename,if no text return None,if no filename ask.
        >>> isinstance(MainWindow().open(__file__), str)
        True"""
        if not filename:
            filename = str(QFileDialog.getOpenFileName(
                self, __doc__ + "- Open source code file", path.expanduser("~"),
                "Python (*.py);;JavaScript (*.js);;TXT (*.txt);;All (*.*)")[0])
        if filename and path.isfile(filename):
            with open(filename, 'r') as file_to_read:
                text = file_to_read.read()
        if text:
            return text

    def fetch(self, url=None):
        """Get a text file from a remote HTTP/HTTPS URL.
        >>> isinstance(MainWindow().fetch(__source__), str)
        True"""
        if not url:
            url = str(QInputDialog.getText(self, __doc__, "<b>HTTP URL?:")[0])
        if url and url.lower().startswith("http"):
            text = str(request.urlopen(url).read().decode("utf8"))
        else:
            QMessageBox.warning(self, __doc__, "<b>URL is not HTTP/HTTPS !")
            text = None
        if text:
            return text

    def skin(self, filename=None):
        """Open QSS from filename,if no QSS return None,if no filename ask.
        >>> isinstance(MainWindow().skin('./styleshit.qss'), str)
        True"""
        if not filename:
            filename = str(QFileDialog.getOpenFileName(
                self, __doc__ + "- Open QSS Skin file", path.expanduser("~"),
                "CSS Cascading Style Sheet for Qt 5 (*.qss);;All (*.*)")[0])
        if filename and path.isfile(filename):
            with open(filename, 'r') as file_to_read:
                text = file_to_read.read().strip()
        if text:
            return text

    def count_code_lines(self, stringy=None):
        """Count approximate lines of code on the text string,returns string.
        >>> isinstance(MainWindow().count_code_lines('foo bar baz'), str)
        True"""
        code_lines_count = "<b>Current text is Empty or has no Source Code !."
        if stringy:
            stringy_tuple = tuple(stringy.splitlines())
            code = len([_ for _ in stringy_tuple
                        if _.strip() != "" and not _.startswith("#")])
            comments = len(stringy_tuple) - code
            code_lines_count = """<b>Lines of Code:{}<br>Blanks and Comments:{}
            <br><br>Total Lines:{}""".format(code, comments, len(stringy_tuple))
        return code_lines_count

    def lorem(self, how_many=None):
        """Take an integer and return a Lorem Impsum string.
        >>> isinstance(MainWindow().lorem(1), str)
        True"""
        lorem_impsum = "Lorem ipsum dolor sit amet, "
        if not how_many or not isinstance(how_many, int):
            how_many = QInputDialog.getInt(self, __doc__, "<b>How many words?:",
                                           len(IMPSUM) // 2, 1, len(IMPSUM))[0]
        lorem_impsum += " ".join((sample(IMPSUM, how_many))) + "\n\n"
        return lorem_impsum

    def rnd_pass(self, length=None):
        """Take an Int and return a random password string of that length.
        >>> isinstance(MainWindow().rnd_pass(8), str)
        True"""
        if not length:
            length = QInputDialog.getInt(self, __doc__, "<b>Character length?:",
                                         8, 4, len(ascii_letters))[0]
        if length and length > 2:
            return "".join((sample(ascii_letters, length)))

    def cssnippet(self):
        """Return str with basic CSS snippet for a new stylesheet from scratch.
        >>> isinstance(MainWindow().cssnippet(), str)
        True"""
        comment = """\n/* {} by {} using {} */ \n\n    Type your styles here...
        """.format(datetime.now().strftime("%A %B %d-%m-%Y %H:%M:%S %p"),
                   getuser().title(), " ".join((linux_distribution())))
        return CSS_SNIPPET + comment

    def commentitle(self, lang=None, text=None):
        """Make a named comment title.
        >>> isinstance(MainWindow().commentitle('python', 'test'), str)
        True"""
        comment_title = "#" * 80 + "\n#    {}\n" + "#" * 80
        if not lang or not len(lang.strip()):
            lang = QInputDialog.getItem(self, __doc__, "<b>Choose Language ?:",
                                        ("Python", "JS / CSS", "HTML"), 0, 0)[0]
        if not text or not len(text.strip()):
            text = str(QInputDialog.getText(self, __doc__, "<b>Title ?:")[0])
        if "js" in lang.lower():
            comment_title = "/*\n" + comment_title + "\n*/\n\n"
        elif "html" in lang.lower():
            comment_title = "<!--\n" + comment_title + "\n-->\n\n"
        if text and lang:
            return comment_title.format(text.strip().upper())

    def comment(self, lang=None):
        """Return a commented out horizontal line for multiple coding languages.
        >>> isinstance(MainWindow().comment('python'), str)
        True"""
        comment_horizontal_line = "#" * 80
        if not lang or not len(lang.strip()):
            lang = QInputDialog.getItem(self, __doc__, "<b>Choose Language ?:",
                                        ("Python", "JS / CSS", "HTML"), 0, 0)[0]
        if "js" in lang.lower():
            comment_horizontal_line = "/*  " + comment_horizontal_line + "  */"
        elif "html" in lang.lower():
            comment_horizontal_line = "<!-- " + comment_horizontal_line + " -->"
        return comment_horizontal_line + "\n\n"

    def previeweb(self, text=None):
        """Take a str and write to tempfile to preview it on web browsers."""
        if not text or not len(text.strip()):
            return
        temp_filename = mkstemp(suffix='.html')[1]
        with open(temp_filename, 'w') as temp_file_to_write:
            temp_file_to_write.write(text)
        open_new_tab("file://" + temp_filename)
        return temp_filename

    def cssfont(self):
        """Return CSS from a font picker(HTML and X11 fonts arent compatible)"""
        font = QFontDialog.getFont()[0]
        css = "font-family: '{}';\nfont-size: {}px;\n".format(font.family(),
                                                              font.pointSize())
        font_weight = font.styleName().split(" ")[0].lower()
        if font_weight in ('normal', 'bold', 'bolder', 'light', 'lighter'):
            css += "font-weight: {};\n".format(font_weight)
        if len(font.styleName().split(" ")) > 1:
            font_style = font.styleName().split(" ")[1].lower()
            if font_style in ('normal', 'italic', 'oblique'):
                css += "font-style: {};\n".format(font_style)
        if font.underline():
            css += "text-decoration: underline;\n"
        if font.strikeOut():
            css += "text-decoration: line-through;\n"
        return css.strip()

    def ramdomcase(self, stringy=None):
        """Return the same string but with random lettercase.
        >>> isinstance(MainWindow().ramdomcase('foo bar baz'), str)
        True"""
        if stringy and len(stringy) and isinstance(stringy, str):
            return "".join(choice((str.upper, str.lower))(x) for x in stringy)

    def check_for_updates(self):
        """Method to check for updates from Git repo versus this version."""
        this_version = str(open(__file__).read())
        last_version = str(request.urlopen(__source__).read().decode("utf8"))
        if this_version != last_version:
            m = "Theres new Version available!<br>Download update from the web"
        else:
            m = "No new updates!<br>You have the lastest version of this app"
        return QMessageBox.information(self, __doc__.title(), "<b>" + m)

    def center(self):
        """Center the Window on the Current Screen,with Multi-Monitor support.
        >>> MainWindow().center()
        True"""
        window_geometry = self.frameGeometry()
        mousepointer_position = QApplication.desktop().cursor().pos()
        screen = QApplication.desktop().screenNumber(mousepointer_position)
        centerPoint = QApplication.desktop().screenGeometry(screen).center()
        window_geometry.moveCenter(centerPoint)
        return bool(not self.move(window_geometry.topLeft()))

    def move_to_mouse_position(self):
        """Center the Window on the Current Mouse position.
        >>> MainWindow().move_to_mouse_position()
        True"""
        window_geometry = self.frameGeometry()
        window_geometry.moveCenter(QApplication.desktop().cursor().pos())
        return bool(not self.move(window_geometry.topLeft()))

    def get_half_resolution(self):
        """Get half of the screen resolution.
        >>> isinstance(MainWindow().get_half_resolution(), tuple)
        True"""
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
    nice(19)
    application = QApplication(sys.argv)
    application.setApplicationName(__doc__.strip().lower())
    application.setOrganizationName(__doc__.strip().lower())
    application.setOrganizationDomain(__doc__.strip())
    application.setWindowIcon(QIcon.fromTheme("start-here"))
    try:
        opts, args = getopt(sys.argv[1:], 'hvt', ('version', 'help', 'tests'))
    except:
        pass
    for o, v in opts:
        if o in ('-h', '--help'):
            print(''' Usage:
                  -h, --help        Show help informations and exit.
                  -v, --version     Show version information and exit.
                  -t, --tests       Run Unit Tests on DocTests if any.''')
            return sys.exit(1)
        elif o in ('-v', '--version'):
            print(__version__)
            return sys.exit(1)
        elif o in ('-t', '--tests'):
            from doctest import testmod
            testmod(verbose=True, report=True, exclude_empty=True)
            exit(1)
    mainwindow = MainWindow()
    mainwindow.show()
    sys.exit(application.exec_())


if __name__ in '__main__':
    main()
