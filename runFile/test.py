import psutil
import wmi
import requests
import bs4
import re
import pandas as pd

# r= requests.get("http://itianti.sinaapp.com/index.php/mcpu").text
# soup = bs4.BeautifulSoup(r.replace('&nbsp;', ' '),"lxml")
# lst = []
# res = []
# count = 0
# for i in soup.find_all("td"):
#    lst.append(i.get_text())
#    count += 1
#    if len(lst) == 7:
#        res.append(lst)
#        count = 0
#        lst = []

# for i in range(len(res)):
#     res[i] = res[i][:-1]
#     res[i].extend(res[i].pop().split("/"))
#     res[i].extend(res[i].pop(2).split("+"))
# print(res)
# df = pd.DataFrame(res, columns=["排名","CPU","TDP","实际频率","核心","线程","L2","L3"])
# print(df)
# df.to_csv("cpu.csv",encoding="utf-8",index=False)

# def getInfo(searchBy="TDP",cpu="i5-7300HQ"):
#     df = pd.read_csv("cpu.csv",encoding="gbk")
#     data = df[["CPU",searchBy]]
#     for i in range(len(data)):
#         findpattern = data.iloc[i,:].tolist()
#         if cpu in findpattern[0]:
#             print(findpattern)
# getInfo(searchBy="实际频率")


import sys

from PyQt5.QtChart import QChartView, QChart, QSplineSeries, QValueAxis
from PyQt5.QtCore import Qt, QTimer, QRandomGenerator
from PyQt5.QtGui import QPainter, QPen
from PyQt5.QtWidgets import QApplication

__version__ = "0.0.1"


class DynamicSpline(QChart):
    def __init__(self):
        super().__init__()
        self.m_step = 0
        self.m_x = 5
        self.m_y = 1
        # 初始化图像
        self.series = QSplineSeries(self)
        green_pen = QPen(Qt.red)
        green_pen.setWidth(2)
        self.series.setPen(green_pen)
        self.axisX = QValueAxis()
        self.axisY = QValueAxis()
        self.series.append(self.m_x, self.m_y)

        self.addSeries(self.series)
        self.addAxis(self.axisX, Qt.AlignBottom)
        self.addAxis(self.axisY, Qt.AlignLeft)
        self.series.attachAxis(self.axisX)
        self.series.attachAxis(self.axisY)
        self.axisX.setTickCount(10)
        self.axisX.setRange(0, 10)
        self.axisY.setRange(-5, 10)

        self.timer = QTimer(self)
        self.timer.setInterval(500)
        self.timer.timeout.connect(self.handleTimeout)
        self.timer.start()

    def handleTimeout(self):
        x = self.plotArea().width() / self.axisX.tickCount()
        y = (self.axisX.max() - self.axisX.min()) / self.axisX.tickCount()
        self.m_x += y
        # 在PyQt5.11.3及以上版本中，QRandomGenerator.global()被重命名为global_()
        self.m_y = QRandomGenerator.global_().bounded(5) - 2.5
        self.series.append(self.m_x, self.m_y)
        self.scroll(x, 0)
        if self.m_x >= 100:
            self.timer.stop()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    chart = DynamicSpline()
    chart.setTitle("Dynamic spline chart")
    chart.legend().hide()
    chart.setAnimationOptions(QChart.AllAnimations)

    view = QChartView(chart)
    view.setRenderHint(QPainter.Antialiasing)  # 抗锯齿
    view.resize(400, 300)
    view.show()
    sys.exit(app.exec_())