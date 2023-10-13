import json
import requests
from PyQt5.QtCore import QDate
import logging
from PyQt5 import QtCore
from PyQt5 import QtWidgets

# 配置日志记录器
logging.basicConfig(filename='myapp.log', level=logging.INFO)
class ReservationModel:
    data_changed = QtCore.pyqtSignal(str)  # 自定义信号，用于通知view更新数据
    def __init__(self):
        self.cookies = {
            'ASP.NET_SessionId': ""
        }
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        self.username=""
        self.password=""
        self.seat_list = []
        self.time_list = []
        self.seat_data = None
        self.date = QDate.currentDate()
        self.start_time = "08:20"
        self.end_time = "21:45"
        self.dev_id = "101700156"
        self.dev_name = "K2076"

    def load_seat_data(self):
        self.seat_data={
            "K2001": "101700081",
            "K2002": "101700082",
            "K2003": "101700083",
            "K2004": "101700084",
            "K2005": "101700085",
            "K2006": "101700086",
            "K2007": "101700087",
            "K2008": "101700088",
            "K2009": "101700089",
            "K2010": "101700090",
            "K2011": "101700091",
            "K2012": "101700092",
            "K2013": "101700093",
            "K2014": "101700094",
            "K2015": "101700095",
            "K2016": "101700096",
            "K2017": "101700097",
            "K2018": "101700098",
            "K2019": "101700099",
            "K2020": "101700100",
            "K2021": "101700101",
            "K2022": "101700102",
            "K2023": "101700103",
            "K2024": "101700104",
            "K2025": "101700105",
            "K2026": "101700106",
            "K2027": "101700107",
            "K2028": "101700108",
            "K2029": "101700109",
            "K2030": "101700110",
            "K2031": "101700111",
            "K2032": "101700112",
            "K2033": "101700113",
            "K2034": "101700114",
            "K2035": "101700115",
            "K2036": "101700116",
            "K2037": "101700117",
            "K2038": "101700118",
            "K2039": "101700119",
            "K2040": "101700120",
            "K2041": "101700121",
            "K2042": "101700122",
            "K2043": "101700123",
            "K2044": "101700124",
            "K2045": "101700125",
            "K2046": "101700126",
            "K2047": "101700127",
            "K2048": "101700128",
            "K2049": "101700129",
            "K2050": "101700130",
            "K2051": "101700131",
            "K2052": "101700132",
            "K2053": "101700133",
            "K2054": "101700134",
            "K2055": "101700135",
            "K2056": "101700136",
            "K2057": "101700137",
            "K2058": "101700138",
            "K2059": "101700139",
            "K2060": "101700140",
            "K2061": "101700141",
            "K2062": "101700142",
            "K2063": "101700143",
            "K2064": "101700144",
            "K2065": "101700145",
            "K2066": "101700146",
            "K2067": "101700147",
            "K2068": "101700148",
            "K2069": "101700149",
            "K2070": "101700150",
            "K2071": "101700151",
            "K2072": "101700152",
            "K2073": "101700153",
            "K2074": "101700154",
            "K2075": "101700155",
            "K2076": "101700156",
            "K2077": "101700157",
            "K2078": "101700158",
            "K2079": "101700159",
            "K2080": "101700160",
            "K2081": "101700161",
            "K2082": "101700162",
            "K2083": "101700163",
            "K2084": "101700164",
            "K2085": "101700165",
            "K2086": "101700166",
            "K2087": "101700167",
            "K2088": "101700168",
            "K2089": "101700169",
            "K2090": "101700170",
            "K2091": "101700171",
            "K2092": "101700172",
            "K2093": "101700173",
            "K2094": "101700174",
            "K2095": "101700175",
            "K2096": "101700176",
            "N1017": "101699621"
        }

    def get_cookie(self):
        return self.cookies["ASP.NET_SessionId"]

    def send_reservation_request(self, dev_id,isTupong):
        try:
            # 构造提交的URL
            date_str = self.date.toString("yyyy-MM-dd")
            url = f"http://kjyy.ccnu.edu.cn/ClientWeb/pro/ajax/reserve.aspx?dialogid=&dev_id={dev_id}&lab_id=&kind_id=&room_id=&type=dev&prop=&test_id=&term=&Vnumber=&classkind=&test_name=&start={date_str} {self.start_time}&end={date_str} {self.end_time}&start_time={self.start_time.replace(':', '')}&end_time={self.end_time.replace(':', '')}&up_file=&memo=&act=set_resv&_="

            # 伪装成浏览器
            cookies = {'ASP.NET_SessionId': self.get_cookie()}

            # # 弹出一个提示框，显示提交的信息，点击确认后关闭提示框
            Dialog = QtWidgets.QDialog()
            # if isTupong == 1:
            #     QtWidgets.QMessageBox.information(Dialog, "提示","您将预约" + self.date + " " + self.start_time + "到" + self.date + " " + self.end_time + "的" + self.dev_name + "号座位")
            #     Dialog.close()
            
            # 发送请求
            response = requests.get(url, headers=self.headers, cookies=cookies,timeout=10)

            # 如果响应码为200，表示请求成功
            if response.status_code == 200:
                data = response.json()
                if isTupong == 1:
                    QtWidgets.QMessageBox.information(
                        Dialog, "提示", data["msg"])
                    Dialog.close()
                # 若返回的数据中的ret大于0，则表示预约成功
                if data["ret"] > 0:
                    print(data["msg"])
                    logging.info(data["msg"])
                    return True
                else:
                    print(data["msg"])
                    logging.error("预约失败: " + data["msg"])
            else:
                logging.error("请求失败，状态码：" + str(response.status_code))

        except requests.exceptions.Timeout:
            # 处理连接超时异常
            logging.error("请求超时，停止请求或采取其他措施")

        except requests.exceptions.RequestException as e:
            # 处理其他请求异常
            logging.error("请求发生错误：" + str(e))

        return False

