import os, sys, time, psutil, wmi, re
import subprocess,threading
import pandas as pd
from PyQt5.QtWidgets import *
from PyQt5 import *
from PyQt5.QtChart import QChartView, QChart, QSplineSeries, QValueAxis
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from Ui_cchan import Ui_MainWindow
from drawLine import *
from style import *

class mywindow(Ui_MainWindow, QMainWindow):
    def __init__(self):
        super(mywindow, self).__init__()
        self.setupUi(self)
        w = wmi.WMI()
        self.CPU = w.Win32_Processor()
        self.timer = QTimer()
        self.timer.start(500)
        self.timer.timeout.connect(self.setTotalUsage)
        self.pushButton_min.setStyleSheet(min_style)
        self.pushButton_close.setStyleSheet(close_style)
        self.pushButton_close.setIcon(QIcon("../icons/关闭.png"))
        self.pushButton_min.setIcon(QIcon("../icons/最小化.png"))
        self.pushButton_min.clicked.connect(self.showMinimized)
        self.pushButton_close.clicked.connect(self.close)
        

        self.setCoresGragh()
        self.setCPUBaseInfo()
        self.setCPUBrandImage()

    def getCPUInfo(self, searchBy="TDP", cpu="i5-7300HQ"):
        df = pd.read_csv("../datas/cpu.csv",encoding="gbk")
        data = df[["CPU",searchBy]]
        for i in range(len(data)):
            findpattern = data.iloc[i,:].tolist()
            if cpu in findpattern[0]:
                return findpattern[1]

    def setTotalUsage(self):
        self.lineEdit_total.setText("{}%".format(psutil.cpu_percent()))

    def setCPUBaseInfo(self):
        for i in self.CPU:
            cpu_name = i.Name
            NumberOfCores = str(i.NumberOfCores)
            ThreadCount = str(i.ThreadCount)
            VFE = str(i.VirtualizationFirmwareEnabled)
            VME = str(i.VMMonitorModeExtensions)
        self.cpu_name = re.sub(r'[(](.*?)[)]', '', " ".join(cpu_name.split()[:-3]))
        tdp = self.getCPUInfo(searchBy="TDP", cpu=self.cpu_name)
        L2 = self.getCPUInfo(searchBy="L2", cpu=self.cpu_name)
        L3 = self.getCPUInfo(searchBy="L3", cpu=self.cpu_name)
        clock = self.getCPUInfo(searchBy="实际频率", cpu=self.cpu_name)
        self.lineEdit_name.setText(self.cpu_name)
        if clock>100:
            self.lineEdit_clock.setText("@{}GHz".format(clock/1000))
        else:
            self.lineEdit_clock.setText("@{}MHz".format(clock))
        self.lineEdit_tdp.setText("{}w".format(tdp))
        self.lineEdit_physical.setText(NumberOfCores)
        self.lineEdit_threadcount.setText(ThreadCount)
        self.lineEdit_L2.setText("{}".format(L2))
        self.lineEdit_L3.setText("{}".format(L3))
        self.lineEdit_VFE.setText(VFE)
        self.lineEdit_VME.setText(VME)
        
    def setCPUBrandImage(self):
        #后续完成对CPU代数、产品系的识别
        for i in self.CPU:
            CPU_name = i.Name
        print(CPU_name)
        if "intel" in CPU_name or "Intel" in CPU_name or "INTEL" in CPU_name:
            cpu_name = "intel"
        elif "AMD" in CPU_name or "amd" in CPU_name or "Amd" in CPU_name:
            cpu_name = "amd"
        self.label_image.setStyleSheet("image: url(../icons/{}.png);".format(cpu_name))

    def setCoresGragh(self):
        self.chart = DynamicSpline(0)
        self.chart.setTitle("Core 1")
        view = QChartView(self.chart)
        view.setRenderHint(QPainter.Antialiasing)  # 抗锯齿
        view.show()   
        self.verticalLayout.addWidget(view)

        self.chart2 = DynamicSpline(1,QColor(39, 155, 218))
        self.chart2.setTitle("Core 2")
        view2 = QChartView(self.chart2)
        view2.setRenderHint(QPainter.Antialiasing)  # 抗锯齿
        view2.show()
        self.verticalLayout_2.addWidget(view2)

        self.chart3 = DynamicSpline(2,QColor(241, 168, 56))
        self.chart3.setTitle("Core 3")
        view3 = QChartView(self.chart3)
        view3.setRenderHint(QPainter.Antialiasing)  # 抗锯齿
        view3.show()
        self.verticalLayout_3.addWidget(view3)

        self.chart4 = DynamicSpline(3,QColor(241, 56, 129))
        self.chart4.setTitle("Core 4")
        view4 = QChartView(self.chart4)
        view4.setRenderHint(QPainter.Antialiasing)  # 抗锯齿
        self.verticalLayout_4.addWidget(view4)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = mywindow()
    w.show()
    sys.exit(app.exec_())
