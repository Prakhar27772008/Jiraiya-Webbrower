from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QApplication, QWidget, QShortcut, QLabel, QHBoxLayout
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtPrintSupport import *
import sys
from PyQt5 import QtGui
from playsound import playsound
class MainWindow(QMainWindow):
	def __init__(self, *args, **kwargs):
		super(MainWindow, self).__init__(*args, **kwargs)
		self.tabs = QTabWidget()
		self.setWindowIcon(QtGui.QIcon('logo.png'))
		self.tabs.setDocumentMode(True)
		self.tabs.tabBarDoubleClicked.connect(self.tab_open_doubleclick) 
		self.tabs.currentChanged.connect(self.current_tab_changed)
		self.tabs.setTabsClosable(True)
		self.tabs.tabCloseRequested.connect(self.close_current_tab)
		self.setCentralWidget(self.tabs)
		self.status = QStatusBar()
		self.setStatusBar(self.status)
		navtb = QToolBar("Navigation")
		self.addToolBar(navtb)

		back_btn = QAction("Back", self)
		back_btn.setStatusTip("Back to previous page")
		back_btn.setShortcut("ctrl+y") or back_btn.setShortcut("ctrl+Y")
		back_btn.setIcon(QIcon("img/BackwardArrow.png"))
		back_btn.triggered.connect(lambda: self.tabs.currentWidget().back())
		navtb.addAction(back_btn)

		next_btn = QAction("Forward", self)
		next_btn.setStatusTip("Forward to next page")
		next_btn.setIcon(QIcon("img/ForwardArrow.png"))
		next_btn.setShortcut("Ctrl+z") or next_btn.setShortcut("Ctrl+Z")
		next_btn.triggered.connect(lambda: self.tabs.currentWidget().forward())
		navtb.addAction(next_btn)

		reload_btn = QAction("Reload", self)
		reload_btn.setStatusTip("Reload page")
		reload_btn.setIcon(QIcon("img/Refresh.png"))
		reload_btn.setShortcut("ctrl+r") or reload_btn.setShortcut("ctrl+R")
		reload_btn.triggered.connect(lambda: self.tabs.currentWidget().reload())
		navtb.addAction(reload_btn)

		home_btn = QAction("Home", self)
		home_btn.setStatusTip("Go home")
		home_btn.setIcon(QIcon("img/Home.png"))
		home_btn.setShortcut("ctrl+h") or home_btn.setShortcut("ctrl+H")
		home_btn.triggered.connect(self.navigate_home)

		navtb.addAction(home_btn)
		navtb.addSeparator()
		self.urlbar = QLineEdit()
		self.urlbar.returnPressed.connect(self.navigate_to_url)
		navtb.addWidget(self.urlbar)

		stop_btn = QAction("Stop", self)
		stop_btn.setStatusTip("Stop loading current page")
		stop_btn.setShortcut("ctrl+W") or stop_btn.setShortcut("ctrl+w")
		stop_btn.triggered.connect(lambda: self.tabs.currentWidget().stop())
		navtb.addAction(stop_btn)

		self.add_new_tab(QUrl('http://www.google.com'), 'Homepage')
		self.show()
		self.setWindowTitle("Jiraiya")
		playsound("Opening.mp3")

	# method for adding new tab
	def add_new_tab(self, qurl = None, label ="Blank"):
		if qurl is None:
			qurl = QUrl('http://www.google.com')
		browser = QWebEngineView()
		browser.setUrl(qurl)

		i = self.tabs.addTab(browser, label)
		self.tabs.setCurrentIndex(i)

		browser.urlChanged.connect(lambda qurl, browser = browser:
								self.update_urlbar(qurl, browser))

		browser.loadFinished.connect(lambda _, i = i, browser = browser:
									self.tabs.setTabText(i, browser.page().title()))

	def tab_open_doubleclick(self, i):
		if i == -1:
			self.add_new_tab()
			playsound("NewTab.mp3")
	def current_tab_changed(self, i):
		qurl = self.tabs.currentWidget().url()
		self.update_urlbar(qurl, self.tabs.currentWidget())
		self.update_title(self.tabs.currentWidget())
	def close_current_tab(self, i):
		if self.tabs.count() < 2:
			return
		self.tabs.removeTab(i)
	def update_title(self, browser):
		if browser != self.tabs.currentWidget():
			return
		title = self.tabs.currentWidget().page().title()
		self.setWindowTitle("% s - Jiraiya" % title)

	def navigate_home(self):
		self.tabs.currentWidget().setUrl(QUrl("http://www.google.com"))

	# method for navigate to url
	def navigate_to_url(self):
		q = QUrl(self.urlbar.text())
		if q.scheme() == "":
			q.setScheme("http")
		self.tabs.currentWidget().setUrl(q)
	def update_urlbar(self, q, browser = None):
		if browser != self.tabs.currentWidget():
			return
		self.urlbar.setText(q.toString())
		self.urlbar.setCursorPosition(0)
app = QApplication(sys.argv)
app.setApplicationName("Jiraiya")
window=MainWindow()
app.exec_()
