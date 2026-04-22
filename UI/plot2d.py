from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QMenu, QAction, QVBoxLayout, \
    QWidget, QFileDialog, QDialog, QLineEdit
from PyQt5.QtCore import Qt
import sys
import pandas as pd
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import *
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import seaborn as sns
from PyQt5.QtCore import QFile, QTextStream
from PyQt5.QtGui import *
import json

class Plot2DDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('2D Plot Options')

        layout = QVBoxLayout()

        self.plot_type_label = QLabel('Select Plot Type:')
        self.plot_type_combo = QComboBox()
        self.plot_type_combo.addItem('Histogram')
        self.plot_type_combo.addItem('Kernel Density Estimation (KDE)')
        self.plot_type_combo.addItem('Box Plot')
        self.plot_type_combo.addItem('ECDF Plot')
        self.plot_type_combo.addItem('Bar Plot')
        self.plot_type_combo.addItem('count Plot')
        self.plot_type_combo.addItem('Violin Plot')
        self.plot_type_combo.addItem('Scatter Plot')
        self.plot_type_combo.addItem('Swarm Plot')
        self.plot_type_combo.addItem('Line Plot')
        self.plot_type_combo.addItem('Heatmap Plot')
        self.plot_type_combo.addItem('Pair Plot')

        layout.addWidget(self.plot_type_label)
        layout.addWidget(self.plot_type_combo)

        self.rugplot_checkbox_x = QCheckBox('Add x Rugplot?')
        layout.addWidget(self.rugplot_checkbox_x)

        self.rugplot_checkbox_y = QCheckBox('Add y Rugplot?')
        layout.addWidget(self.rugplot_checkbox_y)

        self.reverse_checkbox = QCheckBox('Reverse?')
        layout.addWidget(self.reverse_checkbox)

        self.plot_button = QPushButton('Plot')
        self.plot_button.clicked.connect(self.plot)
        layout.addWidget(self.plot_button)

        self.setLayout(layout)

    def plot(self):
        plot_type = self.plot_type_combo.currentText()

        if plot_type == 'Histogram':
            histogram_dialog = HistogramDialog_2d(self)
            if histogram_dialog.exec_() == QDialog.Accepted:
                params = histogram_dialog.get_parameters()



                # 데이터 가져오기 (예: 현재 열의 데이터)
                column_names = [self.parent().tableWidget.horizontalHeaderItem(col).text() for col in
                range(self.parent().tableWidget.columnCount())]
                x_col, ok1 = QInputDialog.getItem(self, "Select X-Axis Column for 2D Plot", "Select X-axis column:",
                                                  self.parent().column_names, 0, False)
                y_col, ok2 = QInputDialog.getItem(self, "Select Y-Axis Column for 2D Plot", "Select Y-axis column:",
                                                  self.parent().column_names, 0, False)


                if ok1 and ok2 and x_col and y_col:
                    try:

                        x_data = []
                        y_data = []
                        x_col_index = column_names.index(x_col)
                        y_col_index = column_names.index(y_col)

                        for row in range(self.parent().tableWidget.rowCount()):
                            x_item = self.parent().tableWidget.item(row, x_col_index)
                            y_item = self.parent().tableWidget.item(row, y_col_index)

                            if x_item is not None and x_item.text() and y_item is not None and y_item.text():
                                x_value = x_item.text()
                                y_value = y_item.text()

                                # 숫자로 변환 가능한지 확인
                                if x_value.replace('.', '', 1).isdigit() and y_value.replace('.', '', 1).isdigit():
                                    x_data.append(float(x_value))
                                    y_data.append(float(y_value))
                                else:
                                    # 숫자로 변환할 수 없는 경우에는 문자열 데이터로 처리
                                    x_data.append(x_value)
                                    y_data.append(y_value)


                        if x_data and y_data:
                            df = pd.DataFrame(zip(x_data, y_data))
                            print(df)
                            if self.reverse_checkbox.isChecked():
                                sns.histplot(data=df, y = x_data, kde=True, **params)
                            else:
                                sns.histplot(x=x_data, y=y_data, kde=True, **params)
                            if self.rugplot_checkbox_x.isChecked():
                                sns.rugplot(x_data, color='yellow')
                            if self.rugplot_checkbox_y.isChecked():
                                sns.rugplot(y_data, color='yellow')
                            plt.xlabel(x_col)
                            plt.ylabel(y_col)
                            plt.title(f"Histogram")

                            plt.show()

                            # 현재 다이얼로그를 닫음
                            self.accept()
                        else:
                            print(f"No numeric data found in column '{x_data}' or '{y_data}'")
                    except Exception as e:
                        print(e)
        # 나머지 그래프 유형에 대한 처리 코드는 여기에 추가
        elif plot_type == 'Kernel Density Estimation (KDE)':
            kde_dialog = KDEDialog_2d(self)
            if kde_dialog.exec_() == QDialog.Accepted:
                params = kde_dialog.get_parameters()

                # 데이터 가져오기 (예: 현재 열의 데이터)
                column_names = [self.parent().tableWidget.horizontalHeaderItem(col).text() for col in
                                range(self.parent().tableWidget.columnCount())]
                x_col, ok1 = QInputDialog.getItem(self, "Select X-Axis Column for 2D Plot", "Select X-axis column:",
                                                  self.parent().column_names, 0, False)
                y_col, ok2 = QInputDialog.getItem(self, "Select Y-Axis Column for 2D Plot", "Select Y-axis column:",
                                                  self.parent().column_names, 0, False)

                if ok1 and ok2 and x_col and y_col:
                    try:
                        x_data = []
                        y_data = []
                        x_col_index = column_names.index(x_col)
                        y_col_index = column_names.index(y_col)

                        for row in range(self.parent().tableWidget.rowCount()):
                            x_item = self.parent().tableWidget.item(row, x_col_index)
                            y_item = self.parent().tableWidget.item(row, y_col_index)

                            if x_item is not None and x_item.text() and y_item is not None and y_item.text():
                                x_value = x_item.text()
                                y_value = y_item.text()

                                # 숫자로 변환 가능한지 확인
                                if x_value.replace('.', '', 1).isdigit() and y_value.replace('.', '', 1).isdigit():
                                    x_data.append(float(x_value))
                                    y_data.append(float(y_value))
                                else:
                                    # 숫자로 변환할 수 없는 경우에는 문자열 데이터로 처리
                                    x_data.append(x_value)
                                    y_data.append(y_value)


                        if x_data and y_data:
                            df = pd.DataFrame(zip(x_data, y_data))
                            if self.reverse_checkbox.isChecked():
                                sns.kdeplot(data=df, y = x_data, **params)
                            else:
                                sns.kdeplot(x=x_data, y=y_data, **params)
                            if self.rugplot_checkbox_x.isChecked():
                                sns.rugplot(x=x_data, color='yellow')
                            if self.rugplot_checkbox_y.isChecked():
                                sns.rugplot(y=y_data, color='yellow')
                            plt.xlabel(x_col)
                            plt.ylabel(y_col)
                            plt.title(f"KDE Plot")

                            plt.show()

                            # 현재 다이얼로그를 닫음
                            self.accept()
                        else:
                            print(f"No numeric data found in column '{x_data}' or '{y_data}'")
                    except Exception as e:
                        print(e)
        elif plot_type == 'Box Plot':
            boxplot_dialog = BoxPlotDialog_2d(self)
            if boxplot_dialog.exec_() == QDialog.Accepted:
                params = boxplot_dialog.get_parameters()
                # 데이터 가져오기 (예: 현재 열의 데이터)
                column_names = [self.parent().tableWidget.horizontalHeaderItem(col).text() for col in
                                range(self.parent().tableWidget.columnCount())]
                x_col, ok1 = QInputDialog.getItem(self, "Select X-Axis Column for 2D Plot", "Select X-axis column:",
                                                  self.parent().column_names, 0, False)
                y_col, ok2 = QInputDialog.getItem(self, "Select Y-Axis Column for 2D Plot", "Select Y-axis column:",
                                                  self.parent().column_names, 0, False)

                if ok1 and ok2 and x_col and y_col:
                    try:
                        x_data = []
                        y_data = []
                        x_col_index = column_names.index(x_col)
                        y_col_index = column_names.index(y_col)

                        for row in range(self.parent().tableWidget.rowCount()):
                            x_item = self.parent().tableWidget.item(row, x_col_index)
                            y_item = self.parent().tableWidget.item(row, y_col_index)

                            if x_item is not None and x_item.text() and y_item is not None and y_item.text():
                                x_value = x_item.text()
                                y_value = y_item.text()

                                # 숫자로 변환 가능한지 확인
                                if x_value.replace('.', '', 1).isdigit() and y_value.replace('.', '', 1).isdigit():
                                    x_data.append(float(x_value))
                                    y_data.append(float(y_value))
                                else:
                                    # 숫자로 변환할 수 없는 경우에는 문자열 데이터로 처리
                                    x_data.append(x_value)
                                    y_data.append(y_value)


                        if x_data and y_data:
                            df = pd.DataFrame(zip(x_data, y_data))
                            if self.reverse_checkbox.isChecked():
                                sns.boxplot(data=df, y=x_data, **params)
                            else:
                                sns.boxplot(x=x_data, y=y_data, **params)
                            if self.rugplot_checkbox_x.isChecked():
                                sns.rugplot(x=x_data, color='yellow')
                            if self.rugplot_checkbox_y.isChecked():
                                sns.rugplot(y=y_data, color='yellow')
                            plt.xlabel(x_col)
                            plt.ylabel(y_col)
                            plt.title(f"Box Plot")

                            plt.show()

                            # 현재 다이얼로그를 닫음
                            self.accept()
                        else:
                            print(f"No numeric data found in column '{x_data}' or '{y_data}'")
                    except Exception as e:
                        print(e)
        elif plot_type == 'ECDF Plot':
            plot_dialog = ECDFPlotDialog_2d(self)
            if plot_dialog.exec_() == QDialog.Accepted:
                params = plot_dialog.get_parameters()
                # 데이터 가져오기 (예: 현재 열의 데이터)
                column_names = [self.parent().tableWidget.horizontalHeaderItem(col).text() for col in
                                range(self.parent().tableWidget.columnCount())]
                x_col, ok1 = QInputDialog.getItem(self, "Select X-Axis Column for 2D Plot", "Select X-axis column:",
                                                  self.parent().column_names, 0, False)
                y_col, ok2 = QInputDialog.getItem(self, "Select Y-Axis Column for 2D Plot", "Select Y-axis column:",
                                                  self.parent().column_names, 0, False)

                if ok1 and ok2 and x_col and y_col:
                    try:
                        x_data = []
                        y_data = []
                        x_col_index = column_names.index(x_col)
                        y_col_index = column_names.index(y_col)

                        for row in range(self.parent().tableWidget.rowCount()):
                            x_item = self.parent().tableWidget.item(row, x_col_index)
                            y_item = self.parent().tableWidget.item(row, y_col_index)

                            if x_item is not None and x_item.text() and y_item is not None and y_item.text():
                                x_value = x_item.text()
                                y_value = y_item.text()

                                # 숫자로 변환 가능한지 확인
                                if x_value.replace('.', '', 1).isdigit() and y_value.replace('.', '', 1).isdigit():
                                    x_data.append(float(x_value))
                                    y_data.append(float(y_value))
                                else:
                                    # 숫자로 변환할 수 없는 경우에는 문자열 데이터로 처리
                                    x_data.append(x_value)
                                    y_data.append(y_value)



                        if x_data and y_data:
                            df = pd.DataFrame(zip(x_data, y_data))
                            if self.reverse_checkbox.isChecked():
                                sns.ecdfplot(data=df, y=x_data, **params)
                            else:
                                sns.ecdfplot(x=x_data, y=y_data, **params)
                            if self.rugplot_checkbox_x.isChecked():
                                sns.rugplot(x=x_data, color='yellow')
                            if self.rugplot_checkbox_y.isChecked():
                                sns.rugplot(y=y_data, color='yellow')
                            plt.xlabel(x_col)
                            plt.ylabel(y_col)
                            plt.title(f"ECDF Plot")

                            plt.show()

                            # 현재 다이얼로그를 닫음
                            self.accept()
                        else:
                            print(f"No numeric data found in column '{x_data}' or '{y_data}'")
                    except Exception as e:
                        print(e)
        elif plot_type == 'Bar Plot':
            plot_dialog = BarPlotDialog_2d(self)
            if plot_dialog.exec_() == QDialog.Accepted:
                params = plot_dialog.get_parameters()
                # 데이터 가져오기 (예: 현재 열의 데이터)
                column_names = [self.parent().tableWidget.horizontalHeaderItem(col).text() for col in
                                range(self.parent().tableWidget.columnCount())]
                x_col, ok1 = QInputDialog.getItem(self, "Select X-Axis Column for 2D Plot", "Select X-axis column:",
                                                  self.parent().column_names, 0, False)
                y_col, ok2 = QInputDialog.getItem(self, "Select Y-Axis Column for 2D Plot", "Select Y-axis column:",
                                                  self.parent().column_names, 0, False)

                if ok1 and ok2 and x_col and y_col:
                    try:
                        x_data = []
                        y_data = []
                        x_col_index = column_names.index(x_col)
                        y_col_index = column_names.index(y_col)

                        for row in range(self.parent().tableWidget.rowCount()):
                            x_item = self.parent().tableWidget.item(row, x_col_index)
                            y_item = self.parent().tableWidget.item(row, y_col_index)

                            if x_item is not None and x_item.text() and y_item is not None and y_item.text():
                                x_value = x_item.text()
                                y_value = y_item.text()

                                # 숫자로 변환 가능한지 확인
                                if x_value.replace('.', '', 1).isdigit() and y_value.replace('.', '', 1).isdigit():
                                    x_data.append(float(x_value))
                                    y_data.append(float(y_value))
                                else:
                                    # 숫자로 변환할 수 없는 경우에는 문자열 데이터로 처리
                                    x_data.append(x_value)
                                    y_data.append(y_value)


                        if x_data and y_data:
                            df = pd.DataFrame(zip(x_data, y_data))
                            if self.reverse_checkbox.isChecked():
                                sns.barplot(data=df, y=x_data, **params)
                            else:
                                sns.barplot(data = df, x=x_data, y=y_data, **params)
                            if self.rugplot_checkbox_x.isChecked():
                                sns.rugplot(x=x_data, color='yellow')
                            if self.rugplot_checkbox_y.isChecked():
                                sns.rugplot(y=y_data, color='yellow')
                            plt.xlabel(x_col)
                            plt.ylabel(y_col)
                            plt.title(f"Bar Plot")

                            plt.show()

                            # 현재 다이얼로그를 닫음
                            self.accept()
                        else:
                            print(f"No numeric data found in column '{x_data}' or '{y_data}'")
                    except Exception as e:
                        print(e)
        elif plot_type == 'Count Plot':
            plot_dialog = CountPlotDialog_2d(self)
            if plot_dialog.exec_() == QDialog.Accepted:
                params = plot_dialog.get_parameters()
                # 데이터 가져오기 (예: 현재 열의 데이터)
                column_names = [self.parent().tableWidget.horizontalHeaderItem(col).text() for col in
                                range(self.parent().tableWidget.columnCount())]
                x_col, ok1 = QInputDialog.getItem(self, "Select X-Axis Column for 2D Plot", "Select X-axis column:",
                                                  self.parent().column_names, 0, False)
                y_col, ok2 = QInputDialog.getItem(self, "Select Y-Axis Column for 2D Plot", "Select Y-axis column:",
                                                  self.parent().column_names, 0, False)

                if ok1 and ok2 and x_col and y_col:
                    try:
                        x_data = []
                        y_data = []
                        x_col_index = column_names.index(x_col)
                        y_col_index = column_names.index(y_col)

                        for row in range(self.parent().tableWidget.rowCount()):
                            x_item = self.parent().tableWidget.item(row, x_col_index)
                            y_item = self.parent().tableWidget.item(row, y_col_index)

                            if x_item is not None and x_item.text() and y_item is not None and y_item.text():
                                x_value = x_item.text()
                                y_value = y_item.text()

                                # 숫자로 변환 가능한지 확인
                                if x_value.replace('.', '', 1).isdigit() and y_value.replace('.', '', 1).isdigit():
                                    x_data.append(float(x_value))
                                    y_data.append(float(y_value))
                                else:
                                    # 숫자로 변환할 수 없는 경우에는 문자열 데이터로 처리
                                    x_data.append(x_value)
                                    y_data.append(y_value)


                        if x_data and y_data:
                            df = pd.DataFrame(zip(x_data, y_data))
                            if self.reverse_checkbox.isChecked():
                                sns.countplot(data=df, y=x_data, **params)
                            else:
                                sns.countplot(x=x_data, y=y_data, **params)
                            if self.rugplot_checkbox_x.isChecked():
                                sns.rugplot(x=x_data, color='yellow')
                            if self.rugplot_checkbox_y.isChecked():
                                sns.rugplot(y=y_data, color='yellow')
                            plt.xlabel(x_col)
                            plt.ylabel(y_col)
                            plt.title(f"Count Plot")

                            plt.show()

                            # 현재 다이얼로그를 닫음
                            self.accept()
                        else:
                            print(f"No numeric data found in column '{x_data}' or '{y_data}'")
                    except Exception as e:
                        print(e)
        elif plot_type == 'Violin Plot':
            plot_dialog = ViolinPlotDialog_2d(self)
            if plot_dialog.exec_() == QDialog.Accepted:
                params = plot_dialog.get_parameters()
                # 데이터 가져오기 (예: 현재 열의 데이터)
                column_names = [self.parent().tableWidget.horizontalHeaderItem(col).text() for col in
                                range(self.parent().tableWidget.columnCount())]
                x_col, ok1 = QInputDialog.getItem(self, "Select X-Axis Column for 2D Plot", "Select X-axis column:",
                                                  self.parent().column_names, 0, False)
                y_col, ok2 = QInputDialog.getItem(self, "Select Y-Axis Column for 2D Plot", "Select Y-axis column:",
                                                  self.parent().column_names, 0, False)

                if ok1 and ok2 and x_col and y_col:
                    try:
                        x_data = []
                        y_data = []
                        x_col_index = column_names.index(x_col)
                        y_col_index = column_names.index(y_col)

                        for row in range(self.parent().tableWidget.rowCount()):
                            x_item = self.parent().tableWidget.item(row, x_col_index)
                            y_item = self.parent().tableWidget.item(row, y_col_index)

                            if x_item is not None and x_item.text() and y_item is not None and y_item.text():
                                x_value = x_item.text()
                                y_value = y_item.text()

                                # 숫자로 변환 가능한지 확인
                                if x_value.replace('.', '', 1).isdigit() and y_value.replace('.', '', 1).isdigit():
                                    x_data.append(float(x_value))
                                    y_data.append(float(y_value))
                                else:
                                    # 숫자로 변환할 수 없는 경우에는 문자열 데이터로 처리
                                    x_data.append(x_value)
                                    y_data.append(y_value)


                        if x_data and y_data:
                            df = pd.DataFrame(zip(x_data, y_data))
                            if self.reverse_checkbox.isChecked():
                                sns.violinplot(data=df, y=x_data, **params)
                            else:
                                sns.violinplot(x=x_data, y=y_data, **params)
                            if self.rugplot_checkbox_x.isChecked():
                                sns.rugplot(x=x_data, color='yellow')
                            if self.rugplot_checkbox_y.isChecked():
                                sns.rugplot(y=y_data, color='yellow')
                            plt.xlabel(x_col)
                            plt.ylabel(y_col)
                            plt.title(f"Violin Plot")

                            plt.show()

                            # 현재 다이얼로그를 닫음
                            self.accept()
                        else:
                            print(f"No numeric data found in column '{x_data}' or '{y_data}'")
                    except Exception as e:
                        print(e)
        elif plot_type == 'Scatter Plot':
            plot_dialog = ScatterPlotDialog_2d(self)
            if plot_dialog.exec_() == QDialog.Accepted:
                params = plot_dialog.get_parameters()
                # 데이터 가져오기 (예: 현재 열의 데이터)
                column_names = [self.parent().tableWidget.horizontalHeaderItem(col).text() for col in
                                range(self.parent().tableWidget.columnCount())]
                x_col, ok1 = QInputDialog.getItem(self, "Select X-Axis Column for 2D Plot", "Select X-axis column:",
                                                  self.parent().column_names, 0, False)
                y_col, ok2 = QInputDialog.getItem(self, "Select Y-Axis Column for 2D Plot", "Select Y-axis column:",
                                                  self.parent().column_names, 0, False)

                if ok1 and ok2 and x_col and y_col:
                    try:
                        x_data = []
                        y_data = []
                        x_col_index = column_names.index(x_col)
                        y_col_index = column_names.index(y_col)

                        for row in range(self.parent().tableWidget.rowCount()):
                            x_item = self.parent().tableWidget.item(row, x_col_index)
                            y_item = self.parent().tableWidget.item(row, y_col_index)

                            if x_item is not None and x_item.text() and y_item is not None and y_item.text():
                                x_value = x_item.text()
                                y_value = y_item.text()

                                # 숫자로 변환 가능한지 확인
                                if x_value.replace('.', '', 1).isdigit() and y_value.replace('.', '', 1).isdigit():
                                    x_data.append(float(x_value))
                                    y_data.append(float(y_value))
                                else:
                                    # 숫자로 변환할 수 없는 경우에는 문자열 데이터로 처리
                                    x_data.append(x_value)
                                    y_data.append(y_value)


                        if x_data and y_data:
                            df = pd.DataFrame(zip(x_data, y_data))
                            if self.reverse_checkbox.isChecked():
                                sns.scatterplot(data=df, y=x_data, **params)
                            else:
                                sns.scatterplot(x=x_data, y=y_data, **params)
                            if self.rugplot_checkbox_x.isChecked():
                                sns.rugplot(x=x_data, color='yellow')
                            if self.rugplot_checkbox_y.isChecked():
                                sns.rugplot(y=y_data, color='yellow')
                            plt.xlabel(x_col)
                            plt.ylabel(y_col)
                            plt.title(f"Scatter")

                            plt.show()

                            # 현재 다이얼로그를 닫음
                            self.accept()
                        else:
                            print(f"No numeric data found in column '{x_data}' or '{y_data}'")
                    except Exception as e:
                        print(e)
        elif plot_type == 'Swarm Plot':
            plot_dialog = SwarmPlotDialog_2d(self)
            if plot_dialog.exec_() == QDialog.Accepted:
                params = plot_dialog.get_parameters()
                # 데이터 가져오기 (예: 현재 열의 데이터)
                column_names = [self.parent().tableWidget.horizontalHeaderItem(col).text() for col in
                                range(self.parent().tableWidget.columnCount())]
                x_col, ok1 = QInputDialog.getItem(self, "Select X-Axis Column for 2D Plot", "Select X-axis column:",
                                                  self.parent().column_names, 0, False)
                y_col, ok2 = QInputDialog.getItem(self, "Select Y-Axis Column for 2D Plot", "Select Y-axis column:",
                                                  self.parent().column_names, 0, False)

                if ok1 and ok2 and x_col and y_col:
                    try:
                        x_data = []
                        y_data = []
                        x_col_index = column_names.index(x_col)
                        y_col_index = column_names.index(y_col)

                        for row in range(self.parent().tableWidget.rowCount()):
                            x_item = self.parent().tableWidget.item(row, x_col_index)
                            y_item = self.parent().tableWidget.item(row, y_col_index)

                            if x_item is not None and x_item.text() and y_item is not None and y_item.text():
                                x_value = x_item.text()
                                y_value = y_item.text()

                                # 숫자로 변환 가능한지 확인
                                if x_value.replace('.', '', 1).isdigit() and y_value.replace('.', '', 1).isdigit():
                                    x_data.append(float(x_value))
                                    y_data.append(float(y_value))
                                else:
                                    # 숫자로 변환할 수 없는 경우에는 문자열 데이터로 처리
                                    x_data.append(x_value)
                                    y_data.append(y_value)

                        if x_data and y_data:
                            df = pd.DataFrame(zip(x_data, y_data))
                            if self.reverse_checkbox.isChecked():
                                sns.swarmplot(data=df, y=x_data, **params)
                            else:
                                sns.swarmplot(x=x_data, y=y_data, **params)
                            if self.rugplot_checkbox_x.isChecked():
                                sns.rugplot(x=x_data, color='yellow')
                            if self.rugplot_checkbox_y.isChecked():
                                sns.rugplot(y=y_data, color='yellow')
                            plt.xlabel(x_col)
                            plt.ylabel(y_col)
                            plt.title(f"Swarm Plot")

                            plt.show()

                            # 현재 다이얼로그를 닫음
                            self.accept()
                        else:
                            print(f"No numeric data found in column '{x_data}' or '{y_data}'")
                    except Exception as e:
                        print(e)
        elif plot_type == 'Line Plot':
            plot_dialog = LinePlotDialog_2d(self)
            if plot_dialog.exec_() == QDialog.Accepted:
                params = plot_dialog.get_parameters()
                # 데이터 가져오기 (예: 현재 열의 데이터)
                column_names = [self.parent().tableWidget.horizontalHeaderItem(col).text() for col in
                                range(self.parent().tableWidget.columnCount())]
                x_col, ok1 = QInputDialog.getItem(self, "Select X-Axis Column for 2D Plot", "Select X-axis column:",
                                                  self.parent().column_names, 0, False)
                y_col, ok2 = QInputDialog.getItem(self, "Select Y-Axis Column for 2D Plot", "Select Y-axis column:",
                                                  self.parent().column_names, 0, False)

                if ok1 and ok2 and x_col and y_col:
                    try:
                        x_data = []
                        y_data = []
                        x_col_index = column_names.index(x_col)
                        y_col_index = column_names.index(y_col)

                        for row in range(self.parent().tableWidget.rowCount()):
                            x_item = self.parent().tableWidget.item(row, x_col_index)
                            y_item = self.parent().tableWidget.item(row, y_col_index)

                            if x_item is not None and x_item.text() and y_item is not None and y_item.text():
                                x_value = x_item.text()
                                y_value = y_item.text()

                                # 숫자로 변환 가능한지 확인
                                if x_value.replace('.', '', 1).isdigit() and y_value.replace('.', '', 1).isdigit():
                                    x_data.append(float(x_value))
                                    y_data.append(float(y_value))
                                else:
                                    # 숫자로 변환할 수 없는 경우에는 문자열 데이터로 처리
                                    x_data.append(x_value)
                                    y_data.append(y_value)

                        if x_data and y_data:
                            df = pd.DataFrame(zip(x_data, y_data))
                            if self.reverse_checkbox.isChecked():
                                sns.lineplot(data=df, y=x_data, **params)
                            else:
                                sns.lineplot(x=x_data, y=y_data, **params)
                            if self.rugplot_checkbox_x.isChecked():
                                sns.rugplot(x=x_data, color='yellow')
                            if self.rugplot_checkbox_y.isChecked():
                                sns.rugplot(y=y_data, color='yellow')
                            plt.xlabel(x_col)
                            plt.ylabel(y_col)
                            plt.title(f"Line Plot")

                            plt.show()

                            # 현재 다이얼로그를 닫음
                            self.accept()
                        else:
                            print(f"No numeric data found in column '{x_data}' or '{y_data}'")
                    except Exception as e:
                        print(e)
        elif plot_type == 'Heatmap Plot':
            plot_dialog = HeatPlotDialog_2d(self)
            if plot_dialog.exec_() == QDialog.Accepted:
                params = plot_dialog.get_parameters()
                # 데이터 가져오기 (예: 현재 열의 데이터)
                column_names = [self.parent().tableWidget.horizontalHeaderItem(col).text() for col in
                                range(self.parent().tableWidget.columnCount())]
                x_col, ok1 = QInputDialog.getItem(self, "Select X-Axis Column for 2D Plot", "Select X-axis column:",
                                                  self.parent().column_names, 0, False)
                y_col, ok2 = QInputDialog.getItem(self, "Select Y-Axis Column for 2D Plot", "Select Y-axis column:",
                                                  self.parent().column_names, 0, False)

                if ok1 and ok2 and x_col and y_col:
                    try:
                        x_data = []
                        y_data = []
                        x_col_index = column_names.index(x_col)
                        y_col_index = column_names.index(y_col)

                        for row in range(self.parent().tableWidget.rowCount()):
                            x_item = self.parent().tableWidget.item(row, x_col_index)
                            y_item = self.parent().tableWidget.item(row, y_col_index)

                            if x_item is not None and x_item.text() and y_item is not None and y_item.text():
                                x_value = x_item.text()
                                y_value = y_item.text()

                                # 숫자로 변환 가능한지 확인
                                if x_value.replace('.', '', 1).isdigit() and y_value.replace('.', '', 1).isdigit():
                                    x_data.append(float(x_value))
                                    y_data.append(float(y_value))
                                else:
                                    # 숫자로 변환할 수 없는 경우에는 문자열 데이터로 처리
                                    x_data.append(x_value)
                                    y_data.append(y_value)

                        if x_data and y_data:
                            df = pd.DataFrame(zip(x_data, y_data))
                            if self.reverse_checkbox.isChecked():
                                sns.heatmap(data=df, y=x_data, **params)
                            else:
                                sns.heatmap(x=x_data, y=y_data, **params)
                            if self.rugplot_checkbox_x.isChecked():
                                sns.rugplot(x=x_data, color='yellow')
                            if self.rugplot_checkbox_y.isChecked():
                                sns.rugplot(y=y_data, color='yellow')
                            plt.xlabel(x_col)
                            plt.ylabel(y_col)
                            plt.title(f"Heatmap PLot")

                            plt.show()

                            # 현재 다이얼로그를 닫음
                            self.accept()
                        else:
                            print(f"No numeric data found in column '{x_data}' or '{y_data}'")
                    except Exception as e:
                        print(e)
        elif plot_type == 'Pair Plot':
            plot_dialog = PairPlotDialog_2d(self)
            if plot_dialog.exec_() == QDialog.Accepted:
                params = plot_dialog.get_parameters()
                # 데이터 가져오기 (예: 현재 열의 데이터)
                column_names = [self.parent().tableWidget.horizontalHeaderItem(col).text() for col in
                                range(self.parent().tableWidget.columnCount())]
                x_col, ok1 = QInputDialog.getItem(self, "Select X-Axis Column for 2D Plot", "Select X-axis column:",
                                                  self.parent().column_names, 0, False)
                y_col, ok2 = QInputDialog.getItem(self, "Select Y-Axis Column for 2D Plot", "Select Y-axis column:",
                                                  self.parent().column_names, 0, False)

                if ok1 and ok2 and x_col and y_col:
                    try:
                        x_data = []
                        y_data = []
                        x_col_index = column_names.index(x_col)
                        y_col_index = column_names.index(y_col)

                        for row in range(self.parent().tableWidget.rowCount()):
                            x_item = self.parent().tableWidget.item(row, x_col_index)
                            y_item = self.parent().tableWidget.item(row, y_col_index)

                            if x_item is not None and x_item.text() and y_item is not None and y_item.text():
                                x_value = x_item.text()
                                y_value = y_item.text()

                                # 숫자로 변환 가능한지 확인
                                if x_value.replace('.', '', 1).isdigit() and y_value.replace('.', '', 1).isdigit():
                                    x_data.append(float(x_value))
                                    y_data.append(float(y_value))
                                else:
                                    # 숫자로 변환할 수 없는 경우에는 문자열 데이터로 처리
                                    x_data.append(x_value)
                                    y_data.append(y_value)

                        if x_data and y_data:
                            df = pd.DataFrame(zip(x_data, y_data))
                            if self.reverse_checkbox.isChecked():
                                sns.pairplot(data=df, **params)
                            else:
                                sns.pairplot(data=df, **params)
                            if self.rugplot_checkbox_x.isChecked():
                                sns.rugplot(x=x_data, color='yellow')
                            if self.rugplot_checkbox_y.isChecked():
                                sns.rugplot(y=y_data, color='yellow')
                            plt.xlabel(x_col)
                            plt.ylabel(y_col)
                            plt.title(f"Pair PLot")

                            plt.show()

                            # 현재 다이얼로그를 닫음
                            self.accept()
                        else:
                            print(f"No numeric data found in column '{x_data}' or '{y_data}'")
                    except Exception as e:
                        print(e)


class HistogramDialog_2d(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Histogram Parameters')
        self.setGeometry(200, 200, 400, 300)

        layout = QVBoxLayout()

        self.num_bins_label = QLabel('Number of Bins:')
        self.num_bins_spinbox = QSpinBox()
        self.num_bins_spinbox.setMinimum(1)
        layout.addWidget(self.num_bins_label)
        layout.addWidget(self.num_bins_spinbox)

        self.num_binswidth_label = QLabel('Number of Binwidths:')
        self.num_binswidth_spinbox = QSpinBox()
        self.num_binswidth_spinbox.setMinimum(1)
        layout.addWidget(self.num_binswidth_label)
        layout.addWidget(self.num_binswidth_spinbox)

        # 추가 파라미터 입력 위젯 추가


        self.color_label = QLabel('Color:')
        self.color_line_edit = QLineEdit('black')
        layout.addWidget(self.color_label)
        layout.addWidget(self.color_line_edit)

        self.legend_checkbox = QCheckBox('Show Legend')
        layout.addWidget(self.legend_checkbox)




        self.accept_button = QPushButton('OK')
        self.accept_button.clicked.connect(self.accept)
        layout.addWidget(self.accept_button)

        self.setLayout(layout)

    def get_parameters(self):
        params = {
            'color': self.color_line_edit.text(),
            'legend': self.legend_checkbox.isChecked(),
            'binwidth': self.num_binswidth_spinbox.value()
            # 여기에 추가 파라미터를 수집하는 코드 추가 가능
        }
        return params



class KDEDialog_2d(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('KDE Parameters')
        self.setGeometry(200, 200, 400, 300)

        layout = QVBoxLayout()



        self.vertical_checkbox = QCheckBox('Vertical')
        layout.addWidget(self.vertical_checkbox)

        self.color_label = QLabel('Color:')
        self.color_line_edit = QLineEdit('black')
        layout.addWidget(self.color_label)
        layout.addWidget(self.color_line_edit)

        self.accept_button = QPushButton('OK')
        self.accept_button.clicked.connect(self.accept)
        layout.addWidget(self.accept_button)

        self.setLayout(layout)

    def get_parameters(self):
        params = {
            'color': self.color_line_edit.text(),
            'vertical': self.vertical_checkbox.isChecked(),
        }
        return params



class BoxPlotDialog_2d(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Box Plot Parameters')
        self.setGeometry(200, 200, 400, 300)

        layout = QVBoxLayout()


        self.color_label = QLabel('Color:')
        self.color_line_edit = QLineEdit('black')
        layout.addWidget(self.color_label)
        layout.addWidget(self.color_line_edit)



        self.accept_button = QPushButton('OK')
        self.accept_button.clicked.connect(self.accept)
        layout.addWidget(self.accept_button)

        self.setLayout(layout)

    def get_parameters(self):
        params = {
            'color': self.color_line_edit.text(),
        }
        return params

class ECDFPlotDialog_2d(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('ECDF Plot Parameters')
        self.setGeometry(200, 200, 400, 300)

        layout = QVBoxLayout()


        self.color_label = QLabel('Color:')
        self.color_line_edit = QLineEdit('black')
        layout.addWidget(self.color_label)
        layout.addWidget(self.color_line_edit)



        self.accept_button = QPushButton('OK')
        self.accept_button.clicked.connect(self.accept)
        layout.addWidget(self.accept_button)

        self.setLayout(layout)

    def get_parameters(self):
        params = {
            'color': self.color_line_edit.text(),

        }
        return params

class BarPlotDialog_2d(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('bar Plot Parameters')
        self.setGeometry(200, 200, 400, 300)

        layout = QVBoxLayout()


        self.color_label = QLabel('Color:')
        self.color_line_edit = QLineEdit('black')
        layout.addWidget(self.color_label)
        layout.addWidget(self.color_line_edit)



        self.accept_button = QPushButton('OK')
        self.accept_button.clicked.connect(self.accept)
        layout.addWidget(self.accept_button)

        self.setLayout(layout)

    def get_parameters(self):
        params = {
            'color': self.color_line_edit.text(),

        }
        return params

class CountPlotDialog_2d(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Count Plot Parameters')
        self.setGeometry(200, 200, 400, 300)

        layout = QVBoxLayout()


        self.color_label = QLabel('Color:')
        self.color_line_edit = QLineEdit('black')
        layout.addWidget(self.color_label)
        layout.addWidget(self.color_line_edit)



        self.accept_button = QPushButton('OK')
        self.accept_button.clicked.connect(self.accept)
        layout.addWidget(self.accept_button)

        self.setLayout(layout)

    def get_parameters(self):
        params = {
            'color': self.color_line_edit.text(),

        }
        return params

class ViolinPlotDialog_2d(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Violin Plot Parameters')
        self.setGeometry(200, 200, 400, 300)

        layout = QVBoxLayout()


        self.color_label = QLabel('Color:')
        self.color_line_edit = QLineEdit('black')
        layout.addWidget(self.color_label)
        layout.addWidget(self.color_line_edit)



        self.accept_button = QPushButton('OK')
        self.accept_button.clicked.connect(self.accept)
        layout.addWidget(self.accept_button)

        self.setLayout(layout)

    def get_parameters(self):
        params = {
            'color': self.color_line_edit.text(),

        }
        return params

class ScatterPlotDialog_2d(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Scatter Plot Parameters')
        self.setGeometry(200, 200, 400, 300)

        layout = QVBoxLayout()


        self.color_label = QLabel('Color:')
        self.color_line_edit = QLineEdit('black')
        layout.addWidget(self.color_label)
        layout.addWidget(self.color_line_edit)



        self.accept_button = QPushButton('OK')
        self.accept_button.clicked.connect(self.accept)
        layout.addWidget(self.accept_button)

        self.setLayout(layout)

    def get_parameters(self):
        params = {
            'color': self.color_line_edit.text(),

        }
        return params

class SwarmPlotDialog_2d(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Swarm Plot Parameters')
        self.setGeometry(200, 200, 400, 300)

        layout = QVBoxLayout()


        self.color_label = QLabel('Color:')
        self.color_line_edit = QLineEdit('black')
        layout.addWidget(self.color_label)
        layout.addWidget(self.color_line_edit)



        self.accept_button = QPushButton('OK')
        self.accept_button.clicked.connect(self.accept)
        layout.addWidget(self.accept_button)

        self.setLayout(layout)

    def get_parameters(self):
        params = {
            'color': self.color_line_edit.text(),

        }
        return params

class LinePlotDialog_2d(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Line Plot Parameters')
        self.setGeometry(200, 200, 400, 300)

        layout = QVBoxLayout()


        self.color_label = QLabel('Color:')
        self.color_line_edit = QLineEdit('black')
        layout.addWidget(self.color_label)
        layout.addWidget(self.color_line_edit)



        self.accept_button = QPushButton('OK')
        self.accept_button.clicked.connect(self.accept)
        layout.addWidget(self.accept_button)

        self.setLayout(layout)

    def get_parameters(self):
        params = {
            'color': self.color_line_edit.text(),

        }
        return params

class HeatPlotDialog_2d(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Heat Plot Parameters')
        self.setGeometry(200, 200, 400, 300)

        layout = QVBoxLayout()


        self.color_label = QLabel('Color:')
        self.color_line_edit = QLineEdit('black')
        layout.addWidget(self.color_label)
        layout.addWidget(self.color_line_edit)



        self.accept_button = QPushButton('OK')
        self.accept_button.clicked.connect(self.accept)
        layout.addWidget(self.accept_button)

        self.setLayout(layout)

    def get_parameters(self):
        params = {
            'cmap': self.color_line_edit.text(),

        }
        return params

class PairPlotDialog_2d(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Pair Plot Parameters')
        self.setGeometry(200, 200, 400, 300)

        layout = QVBoxLayout()


        self.color_label = QLabel('Color:')
        self.color_line_edit = QLineEdit('black')
        layout.addWidget(self.color_label)
        layout.addWidget(self.color_line_edit)



        self.accept_button = QPushButton('OK')
        self.accept_button.clicked.connect(self.accept)
        layout.addWidget(self.accept_button)

        self.setLayout(layout)

    def get_parameters(self):
        params = {
            'color': self.color_line_edit.text(),

        }
        return params



