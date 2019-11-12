import sys
import psutil
from PyQt5.QtChart import QChartView, QChart, QSplineSeries, QValueAxis
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

__version__ = "0.0.1"


class DynamicSpline(QChart):
    def __init__(self,coreNumber,color=QColor(54, 213, 206)):
        super().__init__()
        self.setTitleFont(QFont("Microsoft YaHei"))
        self.setFont(QFont("Microsoft YaHei"))
        self.setAnimationOptions(QChart.AllAnimations)
        self.legend().hide()
        self.m_step = 0
        self.m_x = 5
        self.m_y = 1
        # 初始化图像
        self.series = QSplineSeries(self)
        green_pen = QPen(color)
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
        self.axisX.setTickCount(5)
        self.axisX.setRange(0, 10)
        self.axisX.setLabelsVisible(False)
        self.axisY.setRange(0, 100)

        self.timer = QTimer(self)
        self.timer.setInterval(1000)
        self.timer.timeout.connect(lambda:self.handleTimeout(coreNumber))
        self.timer.start()

    def handleTimeout(self, coreNumber=0):
        x = self.plotArea().width() / self.axisX.tickCount()
        y = (self.axisX.max() - self.axisX.min()) / self.axisX.tickCount()
        self.m_x += y
        self.m_y = psutil.cpu_percent(percpu=True)[coreNumber]
        # if self.m_y < 25:
        #     self.axisY.setRange(0, 25)
        # if self.m_y >= 25:
        #     self.axisY.setRange(0, 50)
        # if self.m_y >= 50:
        #     self.axisY.setRange(0, 75)
        # if self.m_y >= 75:
        #     self.axisY.setRange(0, 100)
        self.series.append(self.m_x+4.9, self.m_y)
        self.scroll(x, 0)



# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     chart = DynamicSpline()
#     chart.setTitle("CPU real time usage")
    
#     view = QChartView(chart)
#     view.setRenderHint(QPainter.Antialiasing)  # 抗锯齿
#     view.resize(300, 200)
#     view.show()
#     sys.exit(app.exec_())