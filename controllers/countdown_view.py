from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QVBoxLayout, QWidget
from PyQt5.QtCore import QThread, pyqtSignal
# 导入QLable模块
from PyQt5.QtWidgets import QLabel
# 导入QDialog模块
from PyQt5.QtWidgets import QDialog
import sys
from PyQt5 import QtWidgets
sys.path.insert(0, r'D:\Desktop\vsFindSeat')
from reservation_model import logging
import time
from PyQt5.QtWidgets import QTimeEdit

class TimerThread(QThread):
    # 定义一个信号
    timeout_signal = pyqtSignal(int, int, int, bool, bool)

    def __init__(self, target_time):
        super().__init__()
        self.stopped = False
        self.alloexecute = False
        self.openLogin = False
        self.target_time = time.mktime(
            time.strptime(target_time, "%Y-%m-%d %H:%M:%S"))
    # 停止线程
    def stop(self):
        self.stopped = True
    # 线程执行函数
    # 每隔一秒发送一次距离目标时间还有多长时间的信号
    def run(self):
        while not self.stopped:
            # 获取当前时间
            current_time = time.time()
            # 计算当前时间与目标时间的时间差
            time_difference = self.target_time - current_time
            # 若时间差在2到5分钟以内，则发送信号
            if time_difference == 120 or time_difference == 50:
                self.openLogin = True
                self.timeout_signal.emit(0, 0, 0,self.alloexecute,self.openLogin)
                self.openLogin = False
            # 如果时间差小于等于0，则发送信号
            if time_difference <= 0:
                #################若到达时间，则执行操作
                self.alloexecute = True
                self.timeout_signal.emit(0, 0, 0,self.alloexecute,self.openLogin)
                break
            # 将时间差转换为时、分、秒
            hours, remainder = divmod(time_difference, 3600)
            minutes, seconds = divmod(remainder, 60)
            # 发送信号
            self.timeout_signal.emit(int(hours),int(minutes),int(seconds),self.alloexecute,self.openLogin)
            # 线程休眠1秒
            time.sleep(1)


class CountDownView(QDialog):  # 修改为QDialog
    def __init__(self,model,controller):
        super().__init__()
        self.controller = controller
        self.model = model
        self.miaosha_time_list = []
        # 设置目标时间为每天的时间为18:00:00，要求获取当前日期
        # 获取当前日期
        self.current_date = time.strftime("%Y-%m-%d", time.localtime())
        # 拼接目标时间
        self.target_time = self.current_date + " 18:00:00"
        self.initUI()

    def closeEvent(self, event):
            # 在这里执行你希望在窗口关闭时执行的操作
        if self.controller:
            self.controller.stop_timer()

        event.accept()  # 确认关闭

    # 初始化用户界面
    def initUI(self):
        # 设置窗口标题
        self.setWindowTitle("秒杀系统")
        # 设置窗口大小
        self.resize(600, 400)
        # 创建一个垂直布局
        self.layout = QVBoxLayout()
        # 设置布局
        self.setLayout(self.layout)

        # 创建开始计时和停止计时按钮以及显示时间的标签
        self.start_button = QPushButton("Start Timer")
        # 设置按钮大小
        self.start_button.setFixedSize(600, 80)
        self.stop_button = QPushButton("Stop Timer")
        # 设置按钮大小
        self.stop_button.setFixedSize(600, 80)
        self.label = QLabel("")
        self.target_time_select = QtWidgets.QComboBox(self)
        self.target_time_select.setFixedSize(600, 80)
        # 设置标签的字体大小
        self.start_button.setStyleSheet("font-size:30px")
        self.stop_button.setStyleSheet("font-size:30px")
        self.target_time_select.setStyleSheet("font-size:30px")
        self.label.setStyleSheet("font-size:30px")
        # 设置标签的默认文本
        self.label.setText("距离下一次秒杀还有:  你猜！")
        for hour in range(7, 22):
            for minute in range(0, 60, 1):
                self.miaosha_time_list.append("%02d:%02d" % (hour, minute))
        self.target_time_select.addItems(self.miaosha_time_list)
        # 将下拉框的信号与槽函数进行连接
        self.target_time_select.currentIndexChanged.connect(self.change_target_time)
        # 将按钮和标签添加到布局中
        self.layout.addWidget(self.target_time_select)
        self.layout.addWidget(self.start_button)
        self.layout.addWidget(self.stop_button)
        self.layout.addWidget(self.label)

    def change_target_time(self):
        # 获取下拉框中的时间,并拼接成目标时间
        self.target_time = self.current_date + " " + self.target_time_select.currentText() + ":00"
        print(self.target_time)