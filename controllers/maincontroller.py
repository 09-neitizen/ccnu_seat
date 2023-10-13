from PyQt5 import QtWidgets
from PyQt5.QtCore import QDate
from PyQt5.QtCore import QUrl
from PyQt5 import QtCore
import json
import os
from PyQt5.QtCore import QUrl
from PyQt5.QtQml import QQmlApplicationEngine
from PyQt5.QtQuick import QQuickView
from countdown_view import CountDownView
from reservation_model import ReservationModel
from scramble_view import ScrambleView
from scramble_view import MyWebEngineView
from countdown_view import TimerThread
import logging

class ReservationController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.cout_view = None
        self.time_list = []
        # 创建一个计时器线程
        self.timer_thread = None

    def run(self):
        self.view.show()

    # 设置下拉框默认值
    def set_default_value(self):
        # 设置座位号列表和座位号下拉框的默认值
        self.model.load_seat_data()
        # 从数据中提取座位号信息，假设座位号信息在字典的"data"键下
        for key in self.model.seat_data:
            self.model.seat_list.append(key)
        # 将座位号列表添加到下拉框
        self.view.comboBox.addItems(self.model.seat_list)
        self.view.comboBox.setCurrentIndex(75)
        self.model.dev_id = self.model.seat_data[self.view.comboBox.currentText()]
        self.model.dev_name = self.view.comboBox.currentText()

        # 设置日期下拉框的默认值为当天日期，当点击日期下拉框时，弹出日历选择日期
        self.view.applydate.setCalendarPopup(True)
        self.view.applydate.setDate(self.model.date)
        self.model.date = self.view.applydate.date()
        # 点击日期下拉框时，触发dateChanged信号，将日期设为全局变量
        self.view.applydate.dateChanged.connect(self.onComboBoxIndexChanged)
        for hour in range(7, 22):
            for minute in range(0, 60, 5):
                self.time_list.append("%02d:%02d" % (hour, minute))
        self.model.time_list = self.time_list
        # 将时间列表添加到下拉框
        self.view.applystarttime.addItems(self.model.time_list)
        self.view.applyendtime.addItems(self.model.time_list)
        # 设置时间下拉框的默认值为早上8:20到晚上9:55
        self.view.applystarttime.setCurrentIndex(16)
        self.model.start_time = self.view.applystarttime.currentText()
        self.view.applyendtime.setCurrentIndex(179) 
        self.model.end_time = self.view.applyendtime.currentText()
    # 设置下拉框和提交按钮的槽函数
    def setupComboBox(self):
        # 连接日期下拉框的选择事件到槽函数
        self.view.applydate.dateChanged.connect(self.onComboBoxIndexChanged)
        # 连接下拉框的选择事件到槽函数
        self.view.comboBox.currentIndexChanged.connect(self.onComboBoxIndexChanged)
        # 连接时间下拉框的选择事件到槽函数
        self.view.applystarttime.currentIndexChanged.connect(
            self.onComboBoxIndexChanged)
        self.view.applyendtime.currentIndexChanged.connect(
            self.onComboBoxIndexChanged)
        # 连接提交按钮的点击事件到槽函数
        self.view.submitbutton.clicked.connect(self.submit)
        self.view.reselect.clicked.connect(self.reselect_seat)
        self.view.open_webpage_button.clicked.connect(self.openWebPage)
     # 下拉框选择事件的槽函数
    # 选择的座位号、日期、开始时间、结束时间都将设为全局变量
    def onComboBoxIndexChanged(self):
        # 若选择的结束时间比开始时间早，则将结束时间设为开始时间
        if self.view.applystarttime.currentIndex() > self.view.applyendtime.currentIndex():
            self.view.applyendtime.setCurrentIndex(
                self.view.applystarttime.currentIndex())
        # 将选择的开始时间和结束时间设为全局变量
        self.model.start_time = self.view.applystarttime.currentText()
        self.model.end_time = self.view.applyendtime.currentText()
        # 将选择的日期设为全局变量
        self.model.date = self.view.applydate.date()
        # 将选择的座位号设为全局变量
        self.model.dev_id = self.model.seat_data[view.comboBox.currentText()]
        self.model.dev_name = self.view.comboBox.currentText()
        # 将选择的日期设为全局变量
        self.model.date = self.view.applydate.date()
        self.model.dev_name = self.view.comboBox.currentText()

   
    # 打开华师登录界面
    def openWebPage(self):
        self.web = MyWebEngineView(self.model)  # 创建浏览器组件对象
        # 绑定加载结束信号槽
        self.web.loadFinished.connect(self.page_loaded)
        self.web.save_button.clicked.connect(self.save)
        self.web.setGeometry(QtCore.QRect(300, 100, 800, 800))
        self.web.load(QUrl(
            "https://account.ccnu.edu.cn/cas/login?service=http://kjyy.ccnu.edu.cn/loginall.aspx?page="))
        self.web.show()
        self.save()
    # 网页加载完成后执行的槽函数
    def page_loaded(self,ok):
        if ok:
            self.judge()
    def judge(self):
        # 获取当前页面的 URL
        current_url = self.web.url()
        # 将你希望匹配的网址替换成你的目标网址
        target_url = QUrl(
               "http://kjyy.ccnu.edu.cn/clientweb/xcus/ic2/Default.aspx")
        if current_url == QUrl("https://account.ccnu.edu.cn/cas/login?service=http://kjyy.ccnu.edu.cn/loginall.aspx?page="):
            # 如果当前页面的 URL 与目标网址匹配，执行登录操作
            # 执行登录操作,elementid:username,id=password,elementname:submit
            if self.model.username != "" and self.model.password != "":
                # 将输入用户名和密码封装成两条JavaScript语句
                self.js_username = f"document.getElementById('username').value='{self.model.username}'"
                self.js_password = f"document.getElementById('password').value='{self.model.password}'"

                # 将点击登录按钮封装成一条JavaScript语句
                self.js_submit = "document.getElementsByName('submit')[0].click()"
                # 执行JavaScript语句
                self.web.page().runJavaScript(self.js_username)
                self.web.page().runJavaScript(self.js_password)
                self.web.page().runJavaScript(self.js_submit)
        elif current_url == target_url:
        # 如果当前页面的 URL 与目标网址匹配，关闭子窗口
        # 等执行完runJavaScript后再关闭窗口
            self.web.close()
    
    def save(self):
        # 获取输入框里的用户名和密码
        self.web.user = {
            "username": self.web.username_input.text(),
            "password": self.web.password_input.text()
        }
        # 初始化时，打开user.json文件，读取里面的用户名和密码
        self.web.file_path = "./user.json"
        # 若文件存在，则读里面的用户名和密码
        if os.path.exists(self.web.file_path):
            # 若username和password都不为空，则将用户名和密码设为全局变量
            if self.web.user["username"] != "" and self.web.user["password"] != "":
                with open(self.web.file_path, "w", encoding="utf-8") as input_file:
                    json.dump(self.web.user, input_file, ensure_ascii=False)
                    self.model.username = self.web.user["username"]
                    self.model.password = self.web.user["password"]
                    self.web.username_input.setText(self.web.user["username"])
                    self.web.password_input.setText(self.web.user["password"])
            else :
                with open(self.web.file_path, "r", encoding="utf-8") as input_file:
                    self.web.user = json.load(input_file)
                    self.model.username = self.web.user["username"]
                    self.model.password = self.web.user["password"]
                    self.web.username_input.setText(self.web.user["username"])
                    self.web.password_input.setText(self.web.user["password"])
        # 若文件不存在，则创建文件，并写入用户名和密码
        else:
            with open(self.web.file_path, "w", encoding="utf-8") as input_file:
                json.dump(self.web.user, input_file, ensure_ascii=False)
                self.model.username = self.web.user["username"]
                self.model.password = self.web.user["password"]
                self.web.username_input.setText(self.web.user["username"])
                self.web.password_input.setText(self.web.user["password"])
        self.judge()
        # print(self.model.username+","+self.model.password)

    # 提交按钮的槽函数
    def submit(self):
        self.model.send_reservation_request(self.model.dev_id,1)
    
    # 定时
    def reselect_seat(self):
        logging.info("定点秒杀系统启动")
        self.openWebPage()
        self.cout_view=CountDownView(self.model,self)
        # 为开始计时和停止计时按钮绑定槽函数
        self.cout_view.start_button.clicked.connect(self.start_timer)
        self.cout_view.stop_button.clicked.connect(self.stop_timer)
        self.cout_view.show()

    # 开始计时的槽函数
    def start_timer(self):
        # 如果计时器线程不存在，则创建一个
        if not self.timer_thread:
            self.timer_thread = TimerThread(self.cout_view.target_time)
            # 将timeout_signal信号绑定到update_time槽函数
            self.timer_thread.timeout_signal.connect(self.update_time)
            # 启动计时器线程
            self.timer_thread.start()
            # 弹出提示框用户你选择的日期、时间、座位号
            QtWidgets.QMessageBox.information(
                self.cout_view, "提示", f"你选择的日期是：{self.model.date.toString('yyyy-MM-dd')}\n你选择的时间是：{self.model.start_time}到{self.model.end_time}\n你选择的座位号是：{self.model.dev_name}")
    # 停止计时的槽函数
    def stop_timer(self):
        # 如果计时器线程存在，则停止计时器线程
        if self.timer_thread:
            # 停止计时器线程
            self.timer_thread.stop()
            # 等待计时器线程完成
            self.timer_thread.wait()
            # 重置计时器线程
            self.timer_thread = None
    # 执行操作的槽函数
    def execute(self):
        logging.info("秒杀操作已执行！")
        if self.cout_view:
            self.cout_view.close()
        if self.web:
            self.web.close()
        
        self.model.send_reservation_request(self.model.dev_id, 1)
        seat_d = ['101700152', '101700153', '101700154', '101700155', '101700156', '101700157', '101700158',
                  '101700124', '101700125', '101700126', '101700127', '101700128', '101700129']
        isFind=0
        for item in reversed(seat_d):
            if self.model.send_reservation_request(item, 0) == True:
                isFind=1
                break
        if (not isFind):
            # 弹出警告框，提示没有找到座位,并设置警告框大小
            QtWidgets.QMessageBox.warning(
                self.cout_view, "警告", "找不到座太恐怖了！", QtWidgets.QMessageBox.Yes)
        else:
            # 弹出提示框，提示找到座位
            QtWidgets.QMessageBox.information(
                self.cout_view, "提示", "抢到了，真不容易啊！")
        self.stop_timer()
    # 更新时间的槽函数
    def update_time(self, hours, minutes, seconds,alloexecute,openLogin):
        if self.cout_view:
            self.cout_view.label.setText(
                f"距离下一次秒杀还有: {hours} : {minutes} : {seconds} 秒！")
            if openLogin:
                self.openWebPage()
            if alloexecute:
                self.execute()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    # 实例化MVC三个对象
    model = ReservationModel()
    model.load_seat_data()
    view = ScrambleView()
    controller = ReservationController(model, view)
    # 设置view的UI界面和默认值
    view.setupUi()
    controller.set_default_value()
    controller.setupComboBox()
    controller.run()
    sys.exit(app.exec_())
