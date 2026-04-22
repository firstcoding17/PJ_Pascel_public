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


#we made it but not recommend
class Plot3DDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('3D Plot Options')

        layout = QVBoxLayout()

        self.plot_type_label = QLabel('Select Plot Type:')
        self.plot_type_combo = QComboBox()
        self.plot_type_combo.addItem('Scatter Plot')
        self.plot_type_combo.addItem('Line Plot')
        self.plot_type_combo.addItem('List Plot')
        self.plot_type_combo.addItem('Grid Plot')

        layout.addWidget(self.plot_type_label)
        layout.addWidget(self.plot_type_combo)

        self.plot_button = QPushButton('Plot')
        self.plot_button.clicked.connect(self.plot)
        layout.addWidget(self.plot_button)

        self.setLayout(layout)

    def plot(self):
        plot_type = self.plot_type_combo.currentText()

        if plot_type == 'Scatter Plot':
            histogram_dialog = PlotDialog_3d(self)
            if histogram_dialog.exec_() == QDialog.Accepted:
                params = histogram_dialog.get_parameters()

                column_names = [self.parent().tableWidget.horizontalHeaderItem(col).text() for col in
                                range(self.parent().tableWidget.columnCount())]
                x_col, ok1 = QInputDialog.getItem(self, "Select X-Axis Column for 3D Plot", "Select X-axis column:",
                                                  column_names, 0, False)
                y_col, ok2 = QInputDialog.getItem(self, "Select Y-Axis Column for 3D Plot", "Select Y-axis column:",
                                                  column_names, 0, False)
                z_col, ok3 = QInputDialog.getItem(self, "Select Z-Axis Column for 3D Plot", "Select Z-axis column:",
                                                  column_names, 0, False)

                if ok1 and ok2 and ok3 and x_col and y_col and z_col:
                    try:
                        x_data = []
                        y_data = []
                        z_data = []
                        x_col_index = column_names.index(x_col)
                        y_col_index = column_names.index(y_col)
                        z_col_index = column_names.index(z_col)

                        for row in range(self.parent().tableWidget.rowCount()):
                            x_item = self.parent().tableWidget.item(row, x_col_index)
                            y_item = self.parent().tableWidget.item(row, y_col_index)
                            z_item = self.parent().tableWidget.item(row, z_col_index)

                            if x_item is not None and x_item.text() and y_item is not None and y_item.text() and z_item is not None and z_item.text():
                                x_value = x_item.text()
                                y_value = y_item.text()
                                z_value = z_item.text()

                                # 숫자로 변환 가능한지 확인
                                if x_value.replace('.', '', 1).isdigit() and y_value.replace('.', '',
                                                                                             1).isdigit() and z_value.replace(
                                    '.', '', 1).isdigit():
                                    x_data.append(float(x_value))
                                    y_data.append(float(y_value))
                                    z_data.append(float(z_value))

                        if x_data and y_data and z_data:
                            fig = plt.figure()
                            ax = fig.add_subplot(111, projection='3d')
                            ax.scatter(x_data, y_data, z_data)
                            ax.set_xlabel(x_col)
                            ax.set_ylabel(y_col)
                            ax.set_zlabel(z_col)
                            ax.set_title(f'3D Plot of {x_col} vs {y_col} vs {z_col}')
                            plt.show()
                        else:
                            print(f"No numeric data found in selected columns.")
                    except Exception as e:
                        print(e)
        elif plot_type == 'Line Plot':
            histogram_dialog = PlotDialog_3d(self)
            if histogram_dialog.exec_() == QDialog.Accepted:
                params = histogram_dialog.get_parameters()

                column_names = [self.parent().tableWidget.horizontalHeaderItem(col).text() for col in
                                range(self.parent().tableWidget.columnCount())]
                x_col, ok1 = QInputDialog.getItem(self, "Select X-Axis Column for 3D Plot", "Select X-axis column:",
                                                  column_names, 0, False)
                y_col, ok2 = QInputDialog.getItem(self, "Select Y-Axis Column for 3D Plot", "Select Y-axis column:",
                                                  column_names, 0, False)
                z_col, ok3 = QInputDialog.getItem(self, "Select Z-Axis Column for 3D Plot", "Select Z-axis column:",
                                                  column_names, 0, False)

                if ok1 and ok2 and ok3 and x_col and y_col and z_col:
                    try:
                        x_data = []
                        y_data = []
                        z_data = []
                        x_col_index = column_names.index(x_col)
                        y_col_index = column_names.index(y_col)
                        z_col_index = column_names.index(z_col)

                        for row in range(self.parent().tableWidget.rowCount()):
                            x_item = self.parent().tableWidget.item(row, x_col_index)
                            y_item = self.parent().tableWidget.item(row, y_col_index)
                            z_item = self.parent().tableWidget.item(row, z_col_index)

                            if x_item is not None and x_item.text() and y_item is not None and y_item.text() and z_item is not None and z_item.text():
                                x_value = x_item.text()
                                y_value = y_item.text()
                                z_value = z_item.text()

                                # 숫자로 변환 가능한지 확인
                                if x_value.replace('.', '', 1).isdigit() and y_value.replace('.', '',
                                                                                             1).isdigit() and z_value.replace(
                                    '.', '', 1).isdigit():
                                    x_data.append(float(x_value))
                                    y_data.append(float(y_value))
                                    z_data.append(float(z_value))

                        if x_data and y_data and z_data:
                            fig = plt.figure()
                            ax = fig.add_subplot(111, projection='3d')

                            # 3D Line Plot 생성
                            ax.plot(x_data, y_data, z_data, label='3D Line Plot', marker='o')

                            ax.set_xlabel(x_col)
                            ax.set_ylabel(y_col)
                            ax.set_zlabel(z_col)
                            ax.set_title(f'3D Line Plot of {x_col} vs {y_col} vs {z_col}')

                            # 범례 추가
                            ax.legend()

                            plt.show()
                        else:
                            print(f"No numeric data found in selected columns.")
                    except Exception as e:
                        print(e)
        elif plot_type == 'list Plot':
            histogram_dialog = PlotDialog_3d(self)
            if histogram_dialog.exec_() == QDialog.Accepted:
                params = histogram_dialog.get_parameters()

                column_names = [self.parent().tableWidget.horizontalHeaderItem(col).text() for col in
                                range(self.parent().tableWidget.columnCount())]
                x_col, ok1 = QInputDialog.getItem(self, "Select X-Axis Column for 3D Plot", "Select X-axis column:",
                                                  column_names, 0, False)
                y_col, ok2 = QInputDialog.getItem(self, "Select Y-Axis Column for 3D Plot", "Select Y-axis column:",
                                                  column_names, 0, False)
                z_col, ok3 = QInputDialog.getItem(self, "Select Z-Axis Column for 3D Plot", "Select Z-axis column:",
                                                  column_names, 0, False)

                if ok1 and ok2 and ok3 and x_col and y_col and z_col:
                    try:
                        x_data = []
                        y_data = []
                        z_data = []
                        x_col_index = column_names.index(x_col)
                        y_col_index = column_names.index(y_col)
                        z_col_index = column_names.index(z_col)

                        for row in range(self.parent().tableWidget.rowCount()):
                            x_item = self.parent().tableWidget.item(row, x_col_index)
                            y_item = self.parent().tableWidget.item(row, y_col_index)
                            z_item = self.parent().tableWidget.item(row, z_col_index)

                            if x_item is not None and x_item.text() and y_item is not None and y_item.text() and z_item is not None and z_item.text():
                                x_value = x_item.text()
                                y_value = y_item.text()
                                z_value = z_item.text()

                                # 숫자로 변환 가능한지 확인
                                if x_value.replace('.', '', 1).isdigit() and y_value.replace('.', '',
                                                                                             1).isdigit() and z_value.replace(
                                    '.', '', 1).isdigit():
                                    x_data.append(float(x_value))
                                    y_data.append(float(y_value))
                                    z_data.append(float(z_value))

                        if x_data and y_data and z_data:
                            fig = plt.figure()
                            ax = fig.add_subplot(111, projection='3d')

                            # 3D List Plot 생성
                            ax.plot(x_data, y_data, z_data, label='3D List Plot', marker='o', linestyle='-')

                            ax.set_xlabel(x_col)
                            ax.set_ylabel(y_col)
                            ax.set_zlabel(z_col)
                            ax.set_title(f'3D List Plot of {x_col} vs {y_col} vs {z_col}')

                            # 범례 추가
                            ax.legend()

                            plt.show()
                        else:
                            print(f"No numeric data found in selected columns.")
                    except Exception as e:
                        print(e)
        elif plot_type == 'Grid Plot':
            histogram_dialog = PlotDialog_3d(self)
            if histogram_dialog.exec_() == QDialog.Accepted:
                params = histogram_dialog.get_parameters()

                column_names = [self.parent().tableWidget.horizontalHeaderItem(col).text() for col in
                                range(self.parent().tableWidget.columnCount())]
                x_col, ok1 = QInputDialog.getItem(self, "Select X-Axis Column for 3D Plot", "Select X-axis column:",
                                                  column_names, 0, False)
                y_col, ok2 = QInputDialog.getItem(self, "Select Y-Axis Column for 3D Plot", "Select Y-axis column:",
                                                  column_names, 0, False)
                z_col, ok3 = QInputDialog.getItem(self, "Select Z-Axis Column for 3D Plot", "Select Z-axis column:",
                                                  column_names, 0, False)

                if ok1 and ok2 and ok3 and x_col and y_col and z_col:
                    try:
                        x_data = []
                        y_data = []
                        z_data = []
                        x_col_index = column_names.index(x_col)
                        y_col_index = column_names.index(y_col)
                        z_col_index = column_names.index(z_col)

                        for row in range(self.parent().tableWidget.rowCount()):
                            x_item = self.parent().tableWidget.item(row, x_col_index)
                            y_item = self.parent().tableWidget.item(row, y_col_index)
                            z_item = self.parent().tableWidget.item(row, z_col_index)

                            if x_item is not None and x_item.text() and y_item is not None and y_item.text() and z_item is not None and z_item.text():
                                x_value = x_item.text()
                                y_value = y_item.text()
                                z_value = z_item.text()

                                # 숫자로 변환 가능한지 확인
                                if x_value.replace('.', '', 1).isdigit() and y_value.replace('.', '',
                                                                                             1).isdigit() and z_value.replace(
                                    '.', '', 1).isdigit():
                                    x_data.append(float(x_value))
                                    y_data.append(float(y_value))
                                    z_data.append(float(z_value))

                        if x_data and y_data and z_data:
                            fig = plt.figure()
                            ax = fig.add_subplot(111, projection='3d')

                            # 3D 그리드 생성
                            x_grid, y_grid = np.meshgrid(x_data, y_data)
                            z_grid = np.zeros_like(x_grid)  # 모든 Z 값을 0으로 설정 (3D 그리드 플롯의 예시)

                            # 3D 그리드 플롯 생성
                            ax.plot_surface(x_grid, y_grid, z_grid, cmap='viridis')

                            ax.set_xlabel(x_col)
                            ax.set_ylabel(y_col)
                            ax.set_zlabel(z_col)
                            ax.set_title(f'3D Grid Plot of {x_col} vs {y_col} vs {z_col}')

                            plt.show()
                        else:
                            print(f"No numeric data found in selected columns.")
                    except Exception as e:
                        print(e)



class PlotDialog_3d(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('3d Plot Parameters')
        self.setGeometry(200, 200, 400, 300)

        layout = QVBoxLayout()



        self.accept_button = QPushButton('OK')
        self.accept_button.clicked.connect(self.accept)
        layout.addWidget(self.accept_button)

        self.setLayout(layout)

    def get_parameters(self):
        params = {

        }
        return params




