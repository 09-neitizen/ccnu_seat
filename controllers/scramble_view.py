from PyQt5.QtWidgets import QWidget
from PyQt5 import QtCore, QtGui
from PyQt5 import QtWidgets
import json
import os
# 导入QMainWindow类
from PyQt5.QtWidgets import QMainWindow
# 导入QWebEngineView和QWebEngineProfile类
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineProfile

# 浏览器控件


class MyWebEngineView(QWebEngineView):
    # 加一个参数model，用于保存cookie
    def __init__(self,model, *args, **kwargs):
        self.cookies = model.cookies
        self.model=model
        super(MyWebEngineView, self).__init__(*args, **kwargs)
        # 绑定cookie被添加的信号槽
        QWebEngineProfile.defaultProfile().cookieStore().cookieAdded.connect(self.onCookieAdd)
        # 设置窗口标题
        self.setWindowTitle('华师登录页面')
        # 加一个保存按钮，点击时保存页面上的username和password
        self.save_button = QtWidgets.QPushButton(self)
        self.save_button.setGeometry(QtCore.QRect(350, 345, 150, 41))
        self.save_button.setObjectName("save_button")
        self.save_button.setText("保存")
        # 创建两个输入框，用于输入用户名和密码
        self.username_input = QtWidgets.QLineEdit(self)
        self.username_input.setGeometry(QtCore.QRect(50, 100, 200, 30))
        self.username_input.setObjectName("username")
        self.password_input = QtWidgets.QLineEdit(self)
        self.password_input.setGeometry(QtCore.QRect(50, 150, 200, 30))
        self.password_input.setObjectName("password")
        self.password_input.setEchoMode(QtWidgets.QLineEdit.Password)
        # 创建两个label，用于显示提示信息
        self.username_label = QtWidgets.QLabel(self)
        self.username_label.setGeometry(QtCore.QRect(50, 80, 200, 20))
        self.username_label.setObjectName("username_label")
        self.username_label.setText("学号")
        self.password_label = QtWidgets.QLabel(self)
        self.password_label.setGeometry(QtCore.QRect(50, 130, 200, 20))
        self.password_label.setObjectName("password_label")
        self.password_label.setText("密码")
        # 将按钮添加到布局
        self.hlayout = QtWidgets.QHBoxLayout()
        self.hlayout.addWidget(self.username_label)
        self.hlayout.addWidget(self.username_input)
        self.hlayout2 = QtWidgets.QHBoxLayout()
        self.hlayout2.addWidget(self.password_label)
        self.hlayout2.addWidget(self.password_input)
        self.layout().addWidget(self.save_button)
        self.layout().addLayout(self.hlayout)
        self.layout().addLayout(self.hlayout2)

    def onCookieAdd(self, cookie):  # 处理cookie添加的事件
        name = cookie.name().data().decode('utf-8')  # 先获取cookie的名字，再把编码处理一下
        value = cookie.value().data().decode('utf-8')  # 先获取cookie值，再把编码处理一下
        # 将name和value保存到Ui_Dialog里的cookies
        self.cookies[name] = value  # 将cookie保存到字典里
        return self.cookies

class ScrambleView(QMainWindow):
    def __init__(self):
        super().__init__()
    
    # 设置内容窗口（已整合）
    def setupContentWidget(self):
        # 创建一个内容小部件
        content_widget = QtWidgets.QWidget(self)
        # 将内容小部件添加到主布局中
        content_layout = QtWidgets.QVBoxLayout(content_widget)
        # 提示小部件
        # 创建一个水平布局用于放置 tishi
        hotishi_layout = QtWidgets.QHBoxLayout()
        hotishi_layout.addWidget(self.tishi)
        hotishi_container = QtWidgets.QWidget()
        hotishi_container.setLayout((hotishi_layout))
        hotishi_container.setFixedHeight(170)

        # 信息小部件
        horizontal_layout = QtWidgets.QHBoxLayout()
        horizontal_layout.addWidget(self.label_xinxi)
        horizontal_layout.addWidget(self.applyseatid)
        horizontal_layout.addWidget(self.label_findname)
        horizontal_layout.addWidget(self.applyname)
        # 创建一个容器小部件来容纳水平布局
        horizontal_container = QtWidgets.QWidget()
        horizontal_container.setLayout(horizontal_layout)

        # 日期小部件
        hodate_layout = QtWidgets.QHBoxLayout()
        hodate_layout.addWidget(self.label_3)
        hodate_layout.addWidget(self.applydate)
        hodate_container = QtWidgets.QWidget()
        hodate_container.setLayout((hodate_layout))

        # 座位小部件
        hoseat_layout = QtWidgets.QHBoxLayout()
        hoseat_layout.addWidget(self.label)
        hoseat_layout.addWidget(self.comboBox)
        hoseat_container = QtWidgets.QWidget()
        hoseat_container.setLayout((hoseat_layout))

        # 时间小部件
        hotime_layout = QtWidgets.QHBoxLayout()
        hotime_layout.addWidget(self.label_4)
        hotime_layout.addWidget(self.applystarttime)
        hotime_layout.addWidget(self.applyendtime)
        hotime_container = QtWidgets.QWidget()
        hotime_container.setLayout((hotime_layout))

        # 限时秒杀小部件
        homiaosha_layout = QtWidgets.QHBoxLayout()
        homiaosha_layout.addWidget(self.open_webpage_button)
        homiaosha_layout.addWidget(self.submitbutton)
        homiaosha_container = QtWidgets.QWidget()
        homiaosha_container.setLayout((homiaosha_layout))
        # 将小部件添加到内容布局中
        content_layout.addWidget(self.labelyuyue)
        content_layout.addWidget(hotishi_container)
        content_layout.addWidget(horizontal_container)
        content_layout.addWidget(hodate_container)
        content_layout.addWidget(hoseat_container)
        content_layout.addWidget(hotime_container)
        content_layout.addWidget(homiaosha_container)
        content_layout.addWidget(self.reselect)
        # 设置内容小部件的布局
        content_widget.setLayout(content_layout)
        # 设置主布局
        self.setCentralWidget(content_widget)
    
    # 设置主窗口
    def setupMainWindow(self):
        self.setObjectName("MainWindow")
        self.resize(1000, 1100)
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei")
        font.setPointSize(12)
        self.setFont(font)
        self.setInputMethodHints(QtCore.Qt.ImhNone)

    # 设置ui控件
    def setupUiControl(self):
        self.labelyuyue = QtWidgets.QLabel(self)
        self.labelyuyue.setGeometry(QtCore.QRect(20, 20, 101, 31))
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei")
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.labelyuyue.setFont(font)
        self.labelyuyue.setObjectName("labelyuyue")
        # 申请时间
        self.applystarttime = QtWidgets.QComboBox(self)
        self.applystarttime.setGeometry(QtCore.QRect(140, 280, 50, 31))
        self.applystarttime.setObjectName("applystarttime")
        # 申请信息
        self.label_xinxi = QtWidgets.QLabel(self)
        self.label_xinxi.setGeometry(QtCore.QRect(20, 155, 71, 31))
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei")
        font.setPointSize(12)
        self.label_xinxi.setFont(font)
        self.label_xinxi.setObjectName("label_xinxi")
        # 申请信息
        self.label_3 = QtWidgets.QLabel(self)
        self.label_3.setGeometry(QtCore.QRect(50, 195, 54, 21))
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei")
        font.setPointSize(12)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self)
        self.label_4.setGeometry(QtCore.QRect(50, 290, 54, 21))
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei")
        font.setPointSize(12)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.submitbutton = QtWidgets.QPushButton(self)
        self.submitbutton.setGeometry(QtCore.QRect(50, 345, 101, 41))
        self.submitbutton.setObjectName("submitbutton")
        self.tishi = QtWidgets.QTextBrowser(self)
        self.tishi.setGeometry(QtCore.QRect(20, 70, 421, 61))
        self.tishi.setObjectName("tishi")
        self.reselect = QtWidgets.QPushButton(self)
        self.reselect.setGeometry(QtCore.QRect(270, 345, 101, 41))
        self.reselect.setObjectName("reselect")
        self.applyendtime = QtWidgets.QComboBox(self)
        self.applyendtime.setGeometry(QtCore.QRect(270, 285, 50, 31))
        self.applyendtime.setObjectName("applyendtime")
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei")
        font.setPointSize(30)
        self.applyseatid = QtWidgets.QLabel(self)
        self.applyseatid.setGeometry(QtCore.QRect(130, 150, 71, 31))
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei")
        font.setPointSize(12)
        self.applyseatid.setFont(font)
        self.applyseatid.setObjectName("applyseatid")
        self.label_findname = QtWidgets.QLabel(self)
        self.label_findname.setGeometry(QtCore.QRect(200, 150, 71, 31))
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei")
        font.setPointSize(12)
        self.label_findname.setFont(font)
        self.label_findname.setObjectName("label_findname")
        self.applyname = QtWidgets.QLabel(self)
        self.applyname.setGeometry(QtCore.QRect(270, 150, 71, 31))
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei")
        font.setPointSize(12)
        self.applyname.setFont(font)
        self.applyname.setObjectName("applyname")
        self.applydate = QtWidgets.QDateEdit(self)
        self.applydate.setGeometry(QtCore.QRect(130, 190, 110, 22))
        self.applydate.setObjectName("applydate")
        self.label = QtWidgets.QLabel(self)
        self.label.setGeometry(QtCore.QRect(50, 240, 61, 16))
        self.label.setObjectName("label")
        # 创建一个下拉框，表示座位号
        self.comboBox = QtWidgets.QComboBox(self)
        self.comboBox.setGeometry(QtCore.QRect(130, 240, 91, 21))
        self.comboBox.setObjectName("comboBox")
        # 添加一个按钮，当点击时打开Web页面窗口
        self.open_webpage_button = QtWidgets.QPushButton(self)
        self.open_webpage_button.setGeometry(QtCore.QRect(350, 345, 150, 41))
        self.open_webpage_button.setObjectName("open_webpage_button")
        self.open_webpage_button.setText("华师登录")
        # self.open_webpage_button.clicked.connect(self.openWebPage)
        # self.reselect.clicked.connect(self.reselect_seat)
    
    # 设置界面
    def setupUi(self):
        # 设置主窗口
        self.setupMainWindow()
        # 设置ui控件
        self.setupUiControl()
        # 设置小部件
        self.setupContentWidget()
        # 重新设置内容窗口
        self.retranslateUi()
        # 信号与槽
        # QtCore.QMetaObject.connectSlotsByName()
    
    # 重新设置内容窗口
    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("self", "华师图书馆抢座系统"))
        # self.setupComboBox(self)
        self.labelyuyue.setText(_translate("self", "预约申请"))
        self.label_xinxi.setText(_translate("self", "申请信息"))
        self.label_3.setText(_translate("self", "日期"))
        self.label_4.setText(_translate("self", "时间"))
        self.submitbutton.setText(_translate("self", "提交"))
        self.tishi.setHtml(_translate("self", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                      "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                      "p, li { white-space: pre-wrap; }\n"
                                      "</style></head><body style=\" font-family:\'Microsoft YaHei\'; font-size:12pt; font-weight:400; font-style:normal;\">\n"
                                      "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Helvetica Neue\',\'Helvetica\',\'Arial\',\'sans-serif\'; font-size:11pt; color:#8a6d3b;\">当日开放：</span><span style=\" font-family:\'Helvetica Neue\',\'Helvetica\',\'Arial\',\'sans-serif\'; font-size:11pt; color:#c7254e;\">07:30</span><span style=\" font-family:\'Helvetica Neue\',\'Helvetica\',\'Arial\',\'sans-serif\'; font-size:11pt; color:#8a6d3b;\"> - </span><span style=\" font-family:\'Helvetica Neue\',\'Helvetica\',\'Arial\',\'sans-serif\'; font-size:11pt; color:#c7254e;\">22:00</span><span style=\" font-family:\'Helvetica Neue\',\'Helvetica\',\'Arial\',\'sans-serif\'; font-size:11pt; color:#8a6d3b;\">；预约至少提前：</span><span style=\" font-family:\'Helvetica Neue\',\'Helvetica\',\'Arial\',\'sans-serif\'; font-size:11pt; color:#c7254e;\">0</span><span style=\" font-family:\'Helvetica Neue\',\'Helvetica\',\'Arial\',\'sans-serif\'; font-size:11pt; color:#8a6d3b;\"> 最长提前：</span><span style=\" font-family:\'Helvetica Neue\',\'Helvetica\',\'Arial\',\'sans-serif\'; font-size:11pt; color:#c7254e;\">1天</span><span style=\" font-family:\'Helvetica Neue\',\'Helvetica\',\'Arial\',\'sans-serif\'; font-size:11pt; color:#8a6d3b;\">；允许时长：</span><span style=\" font-family:\'Helvetica Neue\',\'Helvetica\',\'Arial\',\'sans-serif\'; font-size:11pt; color:#c7254e;\">1小时</span><span style=\" font-family:\'Helvetica Neue\',\'Helvetica\',\'Arial\',\'sans-serif\'; font-size:11pt; color:#8a6d3b;\"> - </span><span style=\" font-family:\'Helvetica Neue\',\'Helvetica\',\'Arial\',\'sans-serif\'; font-size:11pt; color:#c7254e;\">14小时</span><span style=\" font-family:\'Helvetica Neue\',\'Helvetica\',\'Arial\',\'sans-serif\'; font-size:11pt; color:#8a6d3b;\">；迟到 </span><span style=\" font-family:\'Helvetica Neue\',\'Helvetica\',\'Arial\',\'sans-serif\'; font-size:11pt; color:#c7254e;\">30分钟</span><span style=\" font-family:\'Helvetica Neue\',\'Helvetica\',\'Arial\',\'sans-serif\'; font-size:11pt; color:#8a6d3b;\"> 取消预约。<br />人数限制：</span><span style=\" font-family:\'Helvetica Neue\',\'Helvetica\',\'Arial\',\'sans-serif\'; font-size:11pt; color:#c7254e;\">1</span><span style=\" font-family:\'Helvetica Neue\',\'Helvetica\',\'Arial\',\'sans-serif\'; font-size:11pt; color:#8a6d3b;\">；</span></p></body></html>"))
        self.reselect.setText(_translate("self", "定点秒杀"))
        self.applyseatid.setText(_translate("self", "座位号"))
        self.label_findname.setText(_translate("self", "申请人"))
        self.applyname.setText(_translate("self", "姓名"))
        self.label.setText(_translate("self", "座位"))
