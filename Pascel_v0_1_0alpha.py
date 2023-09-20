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
from io import StringIO
import scipy.stats as stats
import statsmodels.api as sm

class Plot1DDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('1D Plot Options')

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
        layout.addWidget(self.plot_type_label)
        layout.addWidget(self.plot_type_combo)

        self.rugplot_checkbox = QCheckBox('Add Rugplot?')
        layout.addWidget(self.rugplot_checkbox)

        self.plot_button = QPushButton('Plot')
        self.plot_button.clicked.connect(self.plot)
        layout.addWidget(self.plot_button)

        self.setLayout(layout)

    def plot(self):
        plot_type = self.plot_type_combo.currentText()

        if plot_type == 'Histogram':
            histogram_dialog = HistogramDialog_1d(self)
            if histogram_dialog.exec_() == QDialog.Accepted:
                params = histogram_dialog.get_parameters()

                hist_params = {
                      # 커널 밀도 추정 여부
                    'color': params['color'],
                    'legend': params['legend'],
                    'binwidth': params['binwidth']


                    # 여기에 원하는 추가 파라미터 추가 가능
                }

                # 데이터 가져오기 (예: 현재 열의 데이터)
                column_names = [self.parent().tableWidget.horizontalHeaderItem(col).text() for col in
                                range(self.parent().tableWidget.columnCount())]
                selected_column, ok = QInputDialog.getItem(self, "Select Column for 1D Plot", "Select a column:",
                                                           column_names, 0, False)

                if ok and selected_column:
                    try:
                        column_index = self.parent().column_names.index(selected_column)
                        data = []

                        for row in range(self.parent().tableWidget.rowCount()):
                            item = self.parent().tableWidget.item(row, column_index)
                            if item is not None:
                                text = item.text()
                                if text:
                                    # 데이터가 비어 있지 않으면서, 숫자로 변환 가능한 경우에만 숫자로 처리
                                    if text.replace('.', '', 1).isdigit():
                                        data.append(float(text))
                                    else:
                                        # 숫자로 변환할 수 없는 경우에는 문자열로 처리
                                        data.append(text)
                                else:
                                    # 데이터가 비어 있는 경우에는 None 또는 빈 문자열("")로 처리
                                    data.append(None)

                        if data:
                            sns.histplot(data, bins=params['num_bins'], kde=True, **hist_params)
                            if self.rugplot_checkbox.isChecked():
                                sns.rugplot(data, color='yellow')
                            plt.xlabel(selected_column)
                            plt.ylabel('Frequency')
                            plt.title(f'1D Plot of {selected_column}')

                            plt.show()

                            # 현재 다이얼로그를 닫음
                            self.accept()
                        else:
                            print(f"No numeric data found in column '{selected_column}'")
                    except Exception as e:
                        print(e)
        # 나머지 그래프 유형에 대한 처리 코드는 여기에 추가
        elif plot_type == 'Kernel Density Estimation (KDE)':
            kde_dialog = KDEDialog_1d(self)
            if kde_dialog.exec_() == QDialog.Accepted:
                params = kde_dialog.get_parameters()

                # 선택한 열(column)의 데이터를 가져옴
                selected_column, ok = QInputDialog.getItem(self, "Select Column for 1D Plot", "Select a column:",
                                                           self.parent().column_names, 0, False)

                if ok and selected_column:
                    try:
                        column_index = self.parent().column_names.index(selected_column)
                        data = []

                        for row in range(self.parent().tableWidget.rowCount()):
                            item = self.parent().tableWidget.item(row, column_index)
                            if item is not None:
                                text = item.text()
                                if text:
                                    # 데이터가 비어 있지 않으면서, 숫자로 변환 가능한 경우에만 숫자로 처리
                                    if text.replace('.', '', 1).isdigit():
                                        data.append(float(text))
                                    else:
                                        # 숫자로 변환할 수 없는 경우에는 문자열로 처리
                                        data.append(text)
                                else:
                                    # 데이터가 비어 있는 경우에는 None 또는 빈 문자열("")로 처리
                                    data.append(None)

                        if data:
                            sns.kdeplot(data, **params)  # 'kde' 파라미터가 설정된 params를 전달
                            if self.rugplot_checkbox.isChecked():
                                sns.rugplot(data, color='yellow')
                            plt.xlabel(selected_column)
                            plt.ylabel('Density')
                            plt.title(f'KDE Plot of {selected_column}')

                            plt.show()

                            # 현재 다이얼로그를 닫음
                            self.accept()
                        else:
                            print(f"No numeric data found in column '{selected_column}'")
                    except Exception as e:
                        print(e)
        elif plot_type == 'Box Plot':
            boxplot_dialog = BoxPlotDialog_1d(self)
            if boxplot_dialog.exec_() == QDialog.Accepted:
                params = boxplot_dialog.get_parameters()
                selected_column, ok = QInputDialog.getItem(self, "Select Column for 1D Plot", "Select a column:",
                                                           self.parent().column_names, 0, False)

                if ok and selected_column:
                    try:
                        column_index = self.parent().column_names.index(selected_column)
                        data = []

                        for row in range(self.parent().tableWidget.rowCount()):
                            item = self.parent().tableWidget.item(row, column_index)
                            if item is not None:
                                text = item.text()
                                if text:
                                    # 데이터가 비어 있지 않으면서, 숫자로 변환 가능한 경우에만 숫자로 처리
                                    if text.replace('.', '', 1).isdigit():
                                        data.append(float(text))
                                    else:
                                        # 숫자로 변환할 수 없는 경우에는 문자열로 처리
                                        data.append(text)
                                else:
                                    # 데이터가 비어 있는 경우에는 None 또는 빈 문자열("")로 처리
                                    data.append(None)

                        if data:
                            sns.boxplot(data, **params)
                            if self.rugplot_checkbox.isChecked():
                                sns.rugplot(data, color='yellow')
                            plt.xlabel(selected_column)
                            plt.ylabel('Density')
                            plt.title(f'KDE Plot of {selected_column}')

                            plt.show()

                            # 현재 다이얼로그를 닫음
                            self.accept()
                        else:
                            print(f"No numeric data found in column '{selected_column}'")
                    except Exception as e:
                        print(e)
        elif plot_type == 'ECDF Plot':
            plot_dialog = ECDFPlotDialog_1d(self)
            if plot_dialog.exec_() == QDialog.Accepted:
                params = plot_dialog.get_parameters()
                selected_column, ok = QInputDialog.getItem(self, "Select Column for 1D Plot", "Select a column:",
                                                           self.parent().column_names, 0, False)

                if ok and selected_column:
                    try:
                        column_index = self.parent().column_names.index(selected_column)
                        data = []

                        for row in range(self.parent().tableWidget.rowCount()):
                            item = self.parent().tableWidget.item(row, column_index)
                            if item is not None:
                                text = item.text()
                                if text:
                                    # 데이터가 비어 있지 않으면서, 숫자로 변환 가능한 경우에만 숫자로 처리
                                    if text.replace('.', '', 1).isdigit():
                                        data.append(float(text))
                                    else:
                                        # 숫자로 변환할 수 없는 경우에는 문자열로 처리
                                        data.append(text)
                                else:
                                    # 데이터가 비어 있는 경우에는 None 또는 빈 문자열("")로 처리
                                    data.append(None)

                        if data:
                            sns.ecdfplot(data, **params)
                            if self.rugplot_checkbox.isChecked():
                                sns.rugplot(data, color='yellow')
                            plt.xlabel(selected_column)
                            plt.ylabel('Proportion')
                            plt.title(f'ECDF Plot of {selected_column}')

                            plt.show()

                            # 현재 다이얼로그를 닫음
                            self.accept()
                        else:
                            print(f"No numeric data found in column '{selected_column}'")
                    except Exception as e:
                        print(e)
        elif plot_type == 'Bar Plot':
            plot_dialog = BarPlotDialog_1d(self)
            if plot_dialog.exec_() == QDialog.Accepted:
                params = plot_dialog.get_parameters()
                selected_column, ok = QInputDialog.getItem(self, "Select Column for 1D Plot", "Select a column:",
                                                           self.parent().column_names, 0, False)

                if ok and selected_column:
                    try:
                        column_index = self.parent().column_names.index(selected_column)
                        data = []

                        for row in range(self.parent().tableWidget.rowCount()):
                            item = self.parent().tableWidget.item(row, column_index)
                            if item is not None:
                                text = item.text()
                                if text:
                                    # 데이터가 비어 있지 않으면서, 숫자로 변환 가능한 경우에만 숫자로 처리
                                    if text.replace('.', '', 1).isdigit():
                                        data.append(float(text))
                                    else:
                                        # 숫자로 변환할 수 없는 경우에는 문자열로 처리
                                        data.append(text)
                                else:
                                    # 데이터가 비어 있는 경우에는 None 또는 빈 문자열("")로 처리
                                    data.append(None)

                        if data:
                            sns.barplot(data, **params)
                            if self.rugplot_checkbox.isChecked():
                                sns.rugplot(data, color='yellow')
                            plt.xlabel(selected_column)
                            plt.ylabel('Frequency')
                            plt.title(f'Bar Plot of {selected_column}')

                            plt.show()

                            # 현재 다이얼로그를 닫음
                            self.accept()
                        else:
                            print(f"No numeric data found in column '{selected_column}'")
                    except Exception as e:
                        print(e)
        elif plot_type == 'Count Plot':
            plot_dialog = CountPlotDialog_1d(self)
            if plot_dialog.exec_() == QDialog.Accepted:
                params = plot_dialog.get_parameters()
                selected_column, ok = QInputDialog.getItem(self, "Select Column for 1D Plot", "Select a column:",
                                                           self.parent().column_names, 0, False)

                if ok and selected_column:
                    try:
                        column_index = self.parent().column_names.index(selected_column)
                        data = []

                        for row in range(self.parent().tableWidget.rowCount()):
                            item = self.parent().tableWidget.item(row, column_index)
                            if item is not None:
                                text = item.text()
                                if text:
                                    # 데이터가 비어 있지 않으면서, 숫자로 변환 가능한 경우에만 숫자로 처리
                                    if text.replace('.', '', 1).isdigit():
                                        data.append(float(text))
                                    else:
                                        # 숫자로 변환할 수 없는 경우에는 문자열로 처리
                                        data.append(text)
                                else:
                                    # 데이터가 비어 있는 경우에는 None 또는 빈 문자열("")로 처리
                                    data.append(None)

                        if data:
                            sns.countplot(data, **params)
                            if self.rugplot_checkbox.isChecked():
                                sns.rugplot(data, color='yellow')
                            plt.xlabel(selected_column)
                            plt.ylabel('Frequency')
                            plt.title(f'Count Plot of {selected_column}')

                            plt.show()

                            # 현재 다이얼로그를 닫음
                            self.accept()
                        else:
                            print(f"No numeric data found in column '{selected_column}'")
                    except Exception as e:
                        print(e)
        elif plot_type == 'Violin Plot':
            plot_dialog = ViolinPlotDialog_1d(self)
            if plot_dialog.exec_() == QDialog.Accepted:
                params = plot_dialog.get_parameters()
                selected_column, ok = QInputDialog.getItem(self, "Select Column for 1D Plot", "Select a column:",
                                                           self.parent().column_names, 0, False)

                if ok and selected_column:
                    try:
                        column_index = self.parent().column_names.index(selected_column)
                        data = []

                        for row in range(self.parent().tableWidget.rowCount()):
                            item = self.parent().tableWidget.item(row, column_index)
                            if item is not None:
                                text = item.text()
                                if text:
                                    # 데이터가 비어 있지 않으면서, 숫자로 변환 가능한 경우에만 숫자로 처리
                                    if text.replace('.', '', 1).isdigit():
                                        data.append(float(text))
                                    else:
                                        # 숫자로 변환할 수 없는 경우에는 문자열로 처리
                                        data.append(text)
                                else:
                                    # 데이터가 비어 있는 경우에는 None 또는 빈 문자열("")로 처리
                                    data.append(None)

                        if data:
                            sns.violinplot(data, **params)
                            if self.rugplot_checkbox.isChecked():
                                sns.rugplot(data, color='yellow')
                            plt.xlabel(selected_column)
                            plt.ylabel('Frequency')
                            plt.title(f'Violin Plot of {selected_column}')

                            plt.show()

                            # 현재 다이얼로그를 닫음
                            self.accept()
                        else:
                            print(f"No numeric data found in column '{selected_column}'")
                    except Exception as e:
                        print(e)
        elif plot_type == 'Scatter Plot':
            plot_dialog = ScatterPlotDialog_1d(self)
            if plot_dialog.exec_() == QDialog.Accepted:
                params = plot_dialog.get_parameters()
                selected_column, ok = QInputDialog.getItem(self, "Select Column for 1D Plot", "Select a column:",
                                                           self.parent().column_names, 0, False)

                if ok and selected_column:
                    try:
                        column_index = self.parent().column_names.index(selected_column)
                        data = []

                        for row in range(self.parent().tableWidget.rowCount()):
                            item = self.parent().tableWidget.item(row, column_index)
                            if item is not None:
                                text = item.text()
                                if text:
                                    # 데이터가 비어 있지 않으면서, 숫자로 변환 가능한 경우에만 숫자로 처리
                                    if text.replace('.', '', 1).isdigit():
                                        data.append(float(text))
                                    else:
                                        # 숫자로 변환할 수 없는 경우에는 문자열로 처리
                                        data.append(text)
                                else:
                                    # 데이터가 비어 있는 경우에는 None 또는 빈 문자열("")로 처리
                                    data.append(None)

                        if data:
                            sns.scatterplot(data, **params)
                            if self.rugplot_checkbox.isChecked():
                                sns.rugplot(data, color='yellow')
                            plt.xlabel(selected_column)
                            plt.ylabel('Frequency')
                            plt.title(f'Scatter Plot of {selected_column}')

                            plt.show()

                            # 현재 다이얼로그를 닫음
                            self.accept()
                        else:
                            print(f"No numeric data found in column '{selected_column}'")
                    except Exception as e:
                        print(e)
        elif plot_type == 'Swarm Plot':
            plot_dialog = SwarmPlotDialog_1d(self)
            if plot_dialog.exec_() == QDialog.Accepted:
                params = plot_dialog.get_parameters()
                selected_column, ok = QInputDialog.getItem(self, "Select Column for 1D Plot", "Select a column:",
                                                           self.parent().column_names, 0, False)

                if ok and selected_column:
                    try:
                        column_index = self.parent().column_names.index(selected_column)
                        data = []

                        for row in range(self.parent().tableWidget.rowCount()):
                            item = self.parent().tableWidget.item(row, column_index)
                            if item is not None:
                                text = item.text()
                                if text:
                                    # 데이터가 비어 있지 않으면서, 숫자로 변환 가능한 경우에만 숫자로 처리
                                    if text.replace('.', '', 1).isdigit():
                                        data.append(float(text))
                                    else:
                                        # 숫자로 변환할 수 없는 경우에는 문자열로 처리
                                        data.append(text)
                                else:
                                    # 데이터가 비어 있는 경우에는 None 또는 빈 문자열("")로 처리
                                    data.append(None)

                        if data:
                            sns.swarmplot(data, **params)
                            if self.rugplot_checkbox.isChecked():
                                sns.rugplot(data, color='yellow')
                            plt.xlabel(selected_column)
                            plt.ylabel('Frequency')
                            plt.title(f'Swarm Plot of {selected_column}')

                            plt.show()

                            # 현재 다이얼로그를 닫음
                            self.accept()
                        else:
                            print(f"No numeric data found in column '{selected_column}'")
                    except Exception as e:
                        print(e)
        elif plot_type == 'Line Plot':
            plot_dialog = LinePlotDialog_1d(self)
            if plot_dialog.exec_() == QDialog.Accepted:
                params = plot_dialog.get_parameters()
                selected_column, ok = QInputDialog.getItem(self, "Select Column for 1D Plot", "Select a column:",
                                                           self.parent().column_names, 0, False)

                if ok and selected_column:
                    try:
                        column_index = self.parent().column_names.index(selected_column)
                        data = []

                        for row in range(self.parent().tableWidget.rowCount()):
                            item = self.parent().tableWidget.item(row, column_index)
                            if item is not None:
                                text = item.text()
                                if text:
                                    # 데이터가 비어 있지 않으면서, 숫자로 변환 가능한 경우에만 숫자로 처리
                                    if text.replace('.', '', 1).isdigit():
                                        data.append(float(text))
                                    else:
                                        # 숫자로 변환할 수 없는 경우에는 문자열로 처리
                                        data.append(text)
                                else:
                                    # 데이터가 비어 있는 경우에는 None 또는 빈 문자열("")로 처리
                                    data.append(None)

                        if data:
                            sns.lineplot(data, **params)
                            if self.rugplot_checkbox.isChecked():
                                sns.rugplot(data, color='yellow')
                            plt.xlabel(selected_column)
                            plt.ylabel('Count')
                            plt.title(f'Line Plot of {selected_column}')

                            plt.show()

                            # 현재 다이얼로그를 닫음
                            self.accept()
                        else:
                            print(f"No numeric data found in column '{selected_column}'")
                    except Exception as e:
                        print(e)






class HistogramDialog_1d(QDialog):
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

        # hue 파라미터를 위한 콤보 박스 추가
        self.hue_label = QLabel('Hue:')
        self.hue_combo = QComboBox()
        self.hue_combo.addItem('None')
        self.hue_combo.addItem('Category Column 1')
        self.hue_combo.addItem('Category Column 2')
        # 필요한 만큼 카테고리 열을 추가
        layout.addWidget(self.hue_label)
        layout.addWidget(self.hue_combo)

        self.accept_button = QPushButton('OK')
        self.accept_button.clicked.connect(self.accept)
        layout.addWidget(self.accept_button)

        self.setLayout(layout)

    def get_parameters(self):
        params = {
            'num_bins': self.num_bins_spinbox.value(),
            'color': self.color_line_edit.text(),
            'legend': self.legend_checkbox.isChecked(),
            'hue': self.hue_combo.currentText(),
            'binwidth': self.num_binswidth_spinbox.value()
            # 여기에 추가 파라미터를 수집하는 코드 추가 가능
        }
        return params



class KDEDialog_1d(QDialog):
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



class BoxPlotDialog_1d(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Box Plot Parameters')
        self.setGeometry(200, 200, 400, 300)

        layout = QVBoxLayout()

        self.orientation_label = QLabel('Orientation:')
        self.orientation_combo = QComboBox()
        self.orientation_combo.addItem('Vertical')
        self.orientation_combo.addItem('Horizontal')
        layout.addWidget(self.orientation_label)
        layout.addWidget(self.orientation_combo)

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
            'orient': self.orientation_combo.currentText()
        }
        return params

class ECDFPlotDialog_1d(QDialog):
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

class BarPlotDialog_1d(QDialog):
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

class CountPlotDialog_1d(QDialog):
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

class ViolinPlotDialog_1d(QDialog):
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

class ScatterPlotDialog_1d(QDialog):
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

class SwarmPlotDialog_1d(QDialog):
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

class LinePlotDialog_1d(QDialog):
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

class mul_dialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle('Not support yet')
        self.setGeometry(200, 200, 400, 300)

        layout = QVBoxLayout()

        self.accept_button = QPushButton('OK')
        self.accept_button.clicked.connect(self.accept)
        layout.addWidget(self.accept_button)

        self.setLayout(layout)

#dialog to check descriptive statistics

class Univariate(QDialog):
    def __init__(self, parent=None, data=None):
        super().__init__(parent)
        self.setWindowTitle('check your needs')
        self.data = data
        self.setGeometry(100, 200, 400, 300)

        self.stdout_capture = StringIO()

        layout = QVBoxLayout()

        self.text_input = QLineEdit(self)
        self.text_input.setPlaceholderText("column_name + (==, <, >, ....) + (and, or, .... +another")
        layout.addWidget(self.text_input)

        self.stdout_capture = StringIO()

        self.Mean_check = QCheckBox('Mean')
        layout.addWidget(self.Mean_check)

        self.Median = QCheckBox('Median')
        layout.addWidget(self.Median)

        self.Mode = QCheckBox('Mode')
        layout.addWidget(self.Mode)

        self.std = QCheckBox('STD')
        layout.addWidget(self.std)

        self.var = QCheckBox('Var')
        layout.addWidget(self.var)

        self.Q = QCheckBox('Quantile')
        layout.addWidget(self.Q)

        self.Sk = QCheckBox('Skewness')
        layout.addWidget(self.Sk)

        self.Kurt = QCheckBox('Kurtosis')
        layout.addWidget(self.Kurt)

        self.Histo = QCheckBox('need Histogram?')
        layout.addWidget(self.Histo)

        self.Box_Plot = QCheckBox('need Box_Plot?')
        layout.addWidget(self.Box_Plot)

        self.accept_button = QPushButton('Show Output')
        self.accept_button.clicked.connect(self.accept)
        layout.addWidget(self.accept_button)

        self.setLayout(layout)
    def accept(self):
        if self.text_input.text() != '' and self.text_input.text() != 'column_name + (==, <, >, ....) + (and, or, .... +another':
            self.data = self.data.query(self.text_input.text())

        self.data = self.data.select_dtypes(include=[np.number])



        output_dialog = Univariate_Output(self)
        '''
        captured_output = self.stdout_capture.getvalue()
        output_dialog.set_output_text(captured_output)
        '''
        output_dialog.exec_()




class Univariate_Output(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Output')
        self.setGeometry(200, 200, 400, 300)
        '''
                self.text_edit = QTextEdit(self)
                layout.addWidget(self.text_edit)

                # 텍스트 출력 위젯 생성
        '''

        layout = QVBoxLayout()

        self.setLayout(layout)

        output_string = ''

        # 콘솔 출력을 캡처할 StringIO 객체 생성

        if self.parent().Mean_check.isChecked():
            output_string = output_string + ('Mean : ' + str(self.parent().data.mean()) + '\n')
        if self.parent().Median.isChecked():
            output_string = output_string +('Median : ' + str(self.parent().data.median()) + '\n')
        if self.parent().Mode.isChecked():
            output_string = output_string +('Mode : ' + str(self.parent().data.mode())+ '\n')
        if self.parent().std.isChecked():
            output_string = output_string +('STD : ' + str(self.parent().data.std())+ '\n')
        if self.parent().var.isChecked():
            output_string = output_string +('Var : ' + str(self.parent().data.var())+ '\n')
        if self.parent().Q.isChecked():
            output_string = output_string +('Q1 : ' + str(self.parent().data.quantile(0.25))+ '\n')
            output_string = output_string +('Q2 : ' + str(self.parent().data.quantile(0.5))+ '\n')
            output_string = output_string +('Q3 : ' + str(self.parent().data.quantile(0.75))+ '\n')
        if self.parent().Sk.isChecked():
            output_string = output_string +('Skewness : ' + str(self.parent().data.skew())+ '\n')
        if self.parent().Kurt.isChecked():
            output_string = output_string +('Kurtosis : ' + str(self.parent().data.kurtosis())+ '\n')

        '''
        self.stdout_capture = StringIO()
        sys.stdout = self.stdout_capture
        '''
        label_output = QLabel(output_string,self)
        layout.addWidget(label_output)




        if self.parent().Histo.isChecked():
            sns.histplot(self.parent().data)

            plt.show()

        if self.parent().Box_Plot.isChecked():
            sns.boxplot(self.parent().data)

            plt.show()


'''
        captured_output = self.stdout_capture.getvalue()
        self.text_edit.setPlainText(captured_output)
    def closeEvent(self, event):
        # 애플리케이션 종료 시 콘솔 출력 복원
        sys.stdout = sys.__stdout__

    def set_output_text(self, output_text):
        self.text_edit.setPlainText(output_text)

'''


class C_or_D(QDialog):
    def __init__(self, parent=None, data=None):
        super().__init__(parent)
        self.setWindowTitle('Settings')
        self.data = data
        self.setGeometry(100, 200, 400, 300)


        layout = QVBoxLayout()

        self.text_input = QLineEdit(self)
        self.text_input.setPlaceholderText("column_name + (==, <, >, ....) + (and, or, .... +another")
        layout.addWidget(self.text_input)


        self.type_d_c = QLabel('D : discrete, C : continue')
        self.C_D = QComboBox(self)
        self.C_D.addItem('D_bernoulli')#베르누이
        self.C_D.addItem('D_binom')#이항분포
        self.C_D.addItem('D_poisson')#포아송분포
        self.C_D.addItem('D_multinomial')#다항분포
        self.C_D.addItem('C_uniform')#균일분포
        self.C_D.addItem('C_norm')#정규분포
        self.C_D.addItem('C_beta')#베타분포
        self.C_D.addItem('C_gamma')#감마분포
        self.C_D.addItem('C_t')#t분포
        self.C_D.addItem('C_chi2')#카이 제곱분포
        self.C_D.addItem('C_f')#F분포
        #아래는 미구현
        self.C_D.addItem('C_dirichlet')#디리클리분포
        self.C_D.addItem('C_multivariate_normal')#다변수 정규분포
        layout.addWidget(self.type_d_c)
        layout.addWidget(self.C_D)


        self.Plot = QCheckBox('need Plot?')
        layout.addWidget(self.Plot)

        self.CDF_Plot = QCheckBox('need CDF?')
        layout.addWidget(self.CDF_Plot)

        self.PDF_Plot = QCheckBox('need PDF?')
        layout.addWidget(self.PDF_Plot)







        self.accept_button = QPushButton('Show Output')
        self.accept_button.clicked.connect(self.accept)
        layout.addWidget(self.accept_button)

        self.setLayout(layout)
    def accept(self):
        if self.text_input.text() != '' and self.text_input.text() != 'column_name + (==, <, >, ....) + (and, or, .... +another':
            self.data = self.data.query(self.text_input.text())
        if self.C_D == 'D_poisson' or self.C_D == 'C_norm':
            column_names = [self.parent().tableWidget.horizontalHeaderItem(col).text() for col in
                        range(self.parent().tableWidget.columnCount())]
            self.x_col, ok1 = QInputDialog.getItem(self, "Select Column", "Select  column:",
                                          column_names, 0, False)
        if self.C_D == 'C_beta' or self.C_D == 'C_gamma':
            column_names = [self.parent().tableWidget.horizontalHeaderItem(col).text() for col in
                        range(self.parent().tableWidget.columnCount())]
            self.alpha, ok1 = QInputDialog.getItem(self, "Select Column", "Select  column:",
                                          column_names, 0, False)
            self.beta, ok1 = QInputDialog.getItem(self, "Select Column", "Select  column:",
                                          column_names, 0, False)





        output_dialog = C_or_D_Output(self,self.C_D)
        output_dialog.exec_()

class C_or_D_Output(QDialog):
    def __init__(self, parent=None, distribution_type=None):
        super().__init__(parent)
        self.setWindowTitle('Output')
        self.setGeometry(200, 200, 400, 300)
        self.distribution_type = distribution_type


        layout = QVBoxLayout()
        self.output_str = ''
        '''
        self.text_edit = QTextEdit(self)
        layout.addWidget(self.text_edit)
        self.setLayout(layout)
        self.stdout_capture = StringIO()
        sys.stdout = self.stdout_capture
        '''
        self.show_output()

        label_output = QLabel(self.output_str,self)
        layout.addWidget(label_output)



    '''
    def closeEvent(self, event):
        # 애플리케이션 종료 시 콘솔 출력 복원
        sys.stdout = sys.__stdout__
    '''
    def show_output(self):
        if self.parent().C_D.currentText() == 'D_bernoulli':

            p, ok = QInputDialog.getDouble(self, 'Input', 'Success Probability (0 - 1):')

            if ok:
                rv = stats.bernoulli(p)
                probability_success = rv.pmf(1)
                probability_failure = rv.pmf(0)
                self.output_str = self.output_str + ('Success Probability : ' + str(probability_success) + '\n')
                self.output_str = self.output_str +('Failure Probability : ' +  str(probability_failure) + '\n')
                if self.parent().Plot.isChecked():
                    x = [0, 1]
                    pmf = [rv.pmf(val) for val in x]
                    plt.bar(x, pmf, tick_label=x)
                    plt.xlabel('Outcome')
                    plt.ylabel('Probability')
                    plt.title('Bernoulli PMF')
                    plt.show()

            if self.parent().Plot.isChecked():
                x = [0, 1]
                pmf = [rv.pmf(val) for val in x]

                plt.bar(x, pmf, tick_label=x)
                plt.xlabel('Outcome')
                plt.ylabel('Probability')
                plt.title('Bernoulli PMF')
                plt.show()
        elif self.parent().C_D.currentText() == 'D_binom':
            while True:
                n, ok = QInputDialog.getInt(self, 'Input', 'Number of Trials (n):')
                if not ok:
                    break
                p, ok = QInputDialog.getDouble(self, 'Input', 'Success Probability (0 - 1):')
                if not ok:
                    break
                x, ok = QInputDialog.getInt(self, 'Input', 'Success Count (x):')
                if not ok:
                    break
                binom_dist = stats.binom(n, p)
                probability = binom_dist.pmf(x)
                self.output_str = self.output_str + ("Probability of successes being" + str(x) + ' : ' + str(probability) +  "\n")
                if self.parent().Plot.isChecked():
                    x_values = range(n + 1)
                    pmf_values = binom_dist.pmf(x_values)
                    plt.bar(x_values, pmf_values)
                    plt.xlabel("Success count")
                    plt.ylabel("Probability")
                    plt.title("Probability Mass Function (PMF) of the Binomial Distribution")
                    plt.show()
                if self.parent().CDF_Plot.isChecked():
                    x = np.arange(0, n + 1)
                    cdf = stats.binom.cdf(x, n, p)
                    plt.plot(x, cdf, marker='o', linestyle='--', color='b')
                    plt.xlabel('Success Count')
                    plt.ylabel('Cumulative Probability')
                    plt.title('Binomial Distribution CDF')
                    plt.grid(True)
                    plt.show()
        elif self.parent().C_D == 'D_poisson':
            data = self.parent().data[str(self.parent()._col)]

            data['lambda'] = self.parent().data[str(self.parent().x_col)].mean()

            data['probability'] = stats.poisson.pmf(self.parent().data[str(self.parent().x_col)], self.parent().data['lambda'])

            for column in data.columns:
                self.output_str+= str(data[column]) + '\n'

            if self.parent().Plot.isChecked():
                # Poisson PMF 그리기
                plt.figure(figsize=(12, 4))
                plt.subplot(121)
                for index, row in data.iterrows():
                    x = np.arange(0, row['events'] + 1)
                    pmf = stats.poisson.pmf(x, row['lambda'])
                    plt.plot(x, pmf, marker='o', label=f"Row {index}")
                plt.title('Poisson PMF')
                plt.xlabel('X')
                plt.ylabel('Probability')
                plt.legend()
                plt.show()
            if self.parent().CDF_Plot.isChecked():
                # Poisson CDF 그리기
                plt.subplot(122)
                for index, row in data.iterrows():
                    x = np.arange(0, row['events'] + 1)
                    cdf = stats.poisson.cdf(x, row['lambda'])
                    plt.plot(x, cdf, marker='o', label=f"Row {index}")
                plt.title('Poisson CDF')
                plt.xlabel('X')
                plt.ylabel('Cumulative Probability')
                plt.legend()
                plt.tight_layout()
                plt.show()
        elif self.parent().C_D.currentText() == 'D_multinomial':
            df = self.parent().data

            n, ok = QInputDialog.getInt(self, 'Input', 'Number of Trials (n):')

            p = df.divide(df.sum(axis=1), axis=0)

            multinom_dist = stats.multinomial(n, p)

            # 각 행에 대한 확률 계산
            probabilities = multinom_dist.pmf(df.values)

            # 결과 출력
            for i, row in enumerate(probabilities):
                self.output_str += f'다항 분포 확률 (행 {i + 1}) : {row}\n'

        elif self.parent().C_D.currentText() == 'C_norm':
            data = self.parent().data[str(self.parent()._col)]



            # 데이터를 기반으로 정규분포 모수 추정 (평균과 표준편차)
            mu = data[str(self.parent()._col)].mean()
            sigma = data[str(self.parent()._col)].std()

            # 정규분포 객체 생성
            rv = stats.norm(loc=mu, scale=sigma)




            if self.parent().PDF_Plot.isChecked():
                x = np.linspace(mu - 3 * sigma, mu + 3 * sigma, 100)
                pdf = rv.pdf(x)  # PDF 값 계산
                plt.figure()  # 새 그래프 창 열기
                plt.plot(x, pdf, label='PDF')
                plt.xlabel('X')
                plt.ylabel('Probability Density')
                plt.title('Normal Distribution PDF')
                plt.legend()
                plt.show()

            if self.parent().CDF_Plot.isChecked():
                x = np.linspace(mu - 3 * sigma, mu + 3 * sigma, 100)  # 그래프 x 범위 설정
                cdf = rv.cdf(x)  # CDF 값 계산
                plt.plot(x, cdf, label='CDF')
                plt.xlabel('X')
                plt.ylabel('Cumulative Probability')
                plt.title('Normal Distribution CDF')
                plt.legend()

                plt.tight_layout()
                plt.show()
        elif self.parent().C_D.currentText() == 'C_beta':
            data = self.parent().data



            for index, row in data.iterrows():
                alpha = row[self.parent().alpha]
                beta = row[self.parent().beta]

                # 베타 분포 객체 생성
                rv = beta(alpha, beta)

                # [0, 1] 범위에서 x 값 생성
                x = np.linspace(0, 1, 100)

                # PDF 계산
                pdf = rv.pdf(x)

                # CDF 계산
                cdf = rv.cdf(x)

                # 그래프 그리기
                plt.figure(figsize=(12, 4))

                # PDF 그래프
                plt.subplot(121)
                plt.plot(x, pdf, label=f'PDF (Alpha={alpha}, Beta={beta})')
                plt.xlabel('x')
                plt.ylabel('Probability Density')
                plt.title(f'Beta Distribution PDF (Alpha={alpha}, Beta={beta})')
                plt.legend()

                # CDF 그래프
                plt.subplot(122)
                plt.plot(x, cdf, label=f'CDF (Alpha={alpha}, Beta={beta})')
                plt.xlabel('x')
                plt.ylabel('Cumulative Probability')
                plt.title(f'Beta Distribution CDF (Alpha={alpha}, Beta={beta})')
                plt.legend()

                plt.tight_layout()
                plt.show()
        elif self.parent().C_D.currentText() == 'C_gamma':
            data = self.parent().data

            a, ok = QInputDialog.getInt(self, 'Input', 'shape (a):')
            scale, ok = QInputDialog.getInt(self, 'Input', 'scale (scale):')
            gamma_dist = stats.gamma(a, scale=scale)

            # 각 행에 대한 CDF 및 PDF 값 계산
            data['cdf'] = data.apply(lambda row: gamma_dist.cdf(row[self.parent().alpha]), axis=1)
            data['pdf'] = data.apply(lambda row: gamma_dist.pdf(row[self.parent().alpha]), axis=1)

            # 결과 출력
            for index, row in data.iterrows():
                self.output_str += f'Index: {index}\n'
                self.output_str += f'CDF: {row["cdf"]}\n'
                self.output_str += f'PDF: {row["pdf"]}\n'
                self.output_str += '\n'


            # CDF 그래프 그리기
            plt.figure(figsize=(8, 4))
            plt.plot(data[self.parent().alpha], data['cdf'], marker='o', linestyle='-', color='b')
            plt.xlabel('Shape (형상) 매개 변수')
            plt.ylabel('누적 확률 (CDF)')
            plt.title('감마 분포 CDF')
            plt.grid(True)

            # PDF 그래프 그리기
            plt.figure(figsize=(8, 4))
            plt.plot(data[self.parent().alpha], data['pdf'], marker='o', linestyle='-', color='r')
            plt.xlabel('Shape (형상) 매개 변수')
            plt.ylabel('확률 밀도 (PDF)')
            plt.title('감마 분포 PDF')
            plt.grid(True)

            # 그래프 표시
            plt.show()
        elif self.parent().C_D.currentText() == 'C_t':
            degrees_of_freedom , ok = QInputDialog.getInt(self, 'Input', 'degree of freedom :')

            rv = stats.t(df=degrees_of_freedom)

            # 확률 밀도 함수 (PDF) 그래프 그리기
            x = np.linspace(-5, 5, 1000)
            pdf = rv.pdf(x)
            plt.plot(x, pdf, label='PDF')
            plt.xlabel('X')
            plt.ylabel('Probability Density')
            plt.title('Student\'s t-Distribution PDF')
            plt.legend()
            plt.grid(True)
            plt.show()

            # 누적 분포 함수 (CDF) 그래프 그리기
            x = np.linspace(-5, 5, 1000)
            cdf = rv.cdf(x)
            plt.plot(x, cdf, label='CDF', color='orange')
            plt.xlabel('X')
            plt.ylabel('Cumulative Probability')
            plt.title('Student\'s t-Distribution CDF')
            plt.legend()
            plt.grid(True)
            plt.show()

        elif self.parent().C_D.currentText() == 'C_chi2':
            df , ok = QInputDialog.getInt(self, 'Input', 'degree of freedom :')

            # 카이제곱 분포 객체 생성
            rv = stats.chi2(df)

            # 확률 밀도 함수 (PDF) 그래프
            x = np.linspace(0, 20, 1000)  # 분포의 범위를 설정
            pdf = rv.pdf(x)
            plt.plot(x, pdf, label=f"df={df}")
            plt.xlabel("X")
            plt.ylabel("Probability Density")
            plt.title("Chi-Square Probability Density Function (PDF)")
            plt.legend()
            plt.grid(True)
            plt.show()

            # 누적 분포 함수 (CDF) 그래프
            x = np.linspace(0, 20, 1000)
            cdf = rv.cdf(x)
            plt.plot(x, cdf, label=f"df={df}")
            plt.xlabel("X")
            plt.ylabel("Cumulative Probability")
            plt.title("Chi-Square Cumulative Distribution Function (CDF)")
            plt.legend()
            plt.grid(True)
            plt.show()
        elif self.parent().C_D.currentText() == 'C_f':
            df1 , ok = QInputDialog.getInt(self, 'Input', 'degree of freedom1 :')
            df2, ok = QInputDialog.getInt(self, 'Input', 'degree of freedom2 :')

            # F-분포 객체 생성
            rv = stats.f(df1, df2)

            # 확률 밀도 함수 (PDF) 그래프
            x = np.linspace(0, 5, 1000)  # 분포의 범위를 설정
            pdf = rv.pdf(x)
            plt.plot(x, pdf, label=f"df1={df1}, df2={df2}")
            plt.xlabel("X")
            plt.ylabel("Probability Density")
            plt.title("F-Distribution Probability Density Function (PDF)")
            plt.legend()
            plt.grid(True)
            plt.show()

            # 누적 분포 함수 (CDF) 그래프
            x = np.linspace(0, 5, 1000)
            cdf = rv.cdf(x)
            plt.plot(x, cdf, label=f"df1={df1}, df2={df2}")
            plt.xlabel("X")
            plt.ylabel("Cumulative Probability")
            plt.title("F-Distribution Cumulative Distribution Function (CDF)")
            plt.legend()
            plt.grid(True)
            plt.show()

class Estimation_or_test(QDialog):
    def __init__(self, parent=None, data=None):
        super().__init__(parent)
        self.setWindowTitle('Settings')
        self.data = data
        self.setGeometry(100, 200, 400, 300)
        self.alpha = None


        layout = QVBoxLayout()

        self.text_input = QLineEdit(self)
        self.text_input.setPlaceholderText("column_name + (==, <, >, ....) + (and, or, .... +another")
        layout.addWidget(self.text_input)


        self.type_d_c = QLabel('Estimation? or test?')
        self.C_D = QComboBox(self)
        self.C_D.addItem('Estimation')#구간 추정
        self.C_D.addItem('Test')#검정

        layout.addWidget(self.type_d_c)
        layout.addWidget(self.C_D)


        self.accept_button = QPushButton('Show Output')
        self.accept_button.clicked.connect(self.accept)
        layout.addWidget(self.accept_button)

        self.setLayout(layout)
    def accept(self):
        if self.text_input.text() != '' and self.text_input.text() != 'column_name + (==, <, >, ....) + (and, or, .... +another':
            self.data = self.data.query(self.text_input.text())

        if self.C_D.currentText() == 'Estimation':
            output_dialog = Estimation(self)
            output_dialog.exec_()
        if self.C_D.currentText() == 'Test':


            output_dialog = Test(self)
            output_dialog.exec_()




class Estimation(QDialog):
    def __init__(self,parent=None):
        super().__init__(parent)
        self.setWindowTitle('Output')
        self.setGeometry(200, 200, 400, 300)

        layout = QVBoxLayout()
        '''
        # 텍스트 출력 위젯 생성
        self.text_edit = QTextEdit(self)
        layout.addWidget(self.text_edit)
        '''
        self.setLayout(layout)
        self.output_str = ''

        '''
        # 콘솔 출력을 캡처할 StringIO 객체 생성
        self.stdout_capture = StringIO()
        sys.stdout = self.stdout_capture
        '''
        self.show_output()
        label_output = QLabel(self.output_str,self)
        layout.addWidget(label_output)




    def closeEvent(self, event):
        # 애플리케이션 종료 시 콘솔 출력 복원
        sys.stdout = sys.__stdout__

    def show_output(self):
        data = self.parent().data

        input_alpha, ok = QInputDialog.getDouble(self, 'Input', 'CIBASIC ALPHA(0 - 1) :', decimals=3)

        column_names = data.columns

        for column_name in column_names:
            data_column = data[column_name]
            mean = data_column.mean()
            std_dev = data_column.std()

            # 입력한 alpha 값을 보존하고 새로운 변수로 계산
            alpha = 1 - input_alpha
            z_score = stats.norm.ppf(1 - alpha / 2)  # 양측 검정의 경우

            margin_of_error = z_score * (std_dev / np.sqrt(len(data_column)))
            lower_bound = mean - margin_of_error
            upper_bound = mean + margin_of_error

            # 결과 출력
            self.output_str += f"{column_name}의 {input_alpha * 100}% 신뢰 구간: (신뢰 상한{lower_bound}, 신뢰 하한{upper_bound})\n"

class Test(QDialog):
    def __init__(self,parent=None):
        super().__init__(parent)
        self.setWindowTitle('Output')
        self.setGeometry(200, 200, 400, 300)
        self.data = self.parent().data
        print(self.data)

        layout = QVBoxLayout()
        '''
        # 텍스트 출력 위젯 생성
        self.text_edit = QTextEdit(self)
        layout.addWidget(self.text_edit)
        '''
        self.setLayout(layout)
        self.output_str = ''
        '''
        # 콘솔 출력을 캡처할 StringIO 객체 생성
        self.stdout_capture = StringIO()
        sys.stdout = self.stdout_capture
        '''
        self.show_output()

        label_output = QLabel(self.output_str,self)
        layout.addWidget(label_output)

    def closeEvent(self, event):
        # 애플리케이션 종료 시 콘솔 출력 복원
        sys.stdout = sys.__stdout__



    def show_output(self):
        input_column_name_1, ok = QInputDialog.getText(self, "Input", "Enter column name:")
        input_column_name_2, ok = QInputDialog.getText(self, "Input", "Enter column name:")


        t_stat, p_value = stats.ttest_ind(self.data[input_column_name_1], self.data[input_column_name_2])

        alpha, ok = QInputDialog.getDouble(self, 'Input', 'CIBASIC ALPHA :', decimals=3)

        if p_value < alpha:
            self.output_str+= "귀무 가설 기각: 두 그룹 간에 통계적으로 유의미한 차이가 있음"
        else:
            self.output_str+="귀무 가설 채택: 두 그룹 간에 통계적으로 유의미한 차이가 없음"





class reg_and_corr(QDialog):
    def __init__(self, parent=None, data=None):
        super().__init__(parent)
        self.setWindowTitle('Settings')
        self.data = data
        self.setGeometry(100, 200, 400, 300)

        layout = QVBoxLayout()

        self.text_input = QLineEdit(self)
        self.text_input.setPlaceholderText("column_name + (==, <, >, ....) + (and, or, .... +another")
        layout.addWidget(self.text_input)

        self.type_d_c = QLabel('regression? or corr?')
        self.C_D = QComboBox(self)
        self.C_D.addItem('regression')  # 구간 추정
        self.C_D.addItem('corr')  # 검정

        layout.addWidget(self.type_d_c)
        layout.addWidget(self.C_D)

        self.accept_button = QPushButton('Show Output')
        self.accept_button.clicked.connect(self.accept)
        layout.addWidget(self.accept_button)

        self.setLayout(layout)

    def accept(self):
        if self.text_input.text() != '' and self.text_input.text() != 'column_name + (==, <, >, ....) + (and, or, .... +another':
            self.data = self.data.query(self.text_input.text())

        if self.C_D.currentText() == 'corr':
            output_dialog = corr(self)
            output_dialog.exec_()
        if self.C_D.currentText() == 'regression':
            column_names = [self.parent().tableWidget.horizontalHeaderItem(col).text() for col in
                            range(self.parent().tableWidget.columnCount())]
            self.alpha, ok1 = QInputDialog.getItem(self, "Select Column", "Select test column:",
                                                   column_names, 0, False)

            output_dialog = reg(self)
            output_dialog.exec_()

class corr(QDialog):
    def __init__(self,parent = None):
        super().__init__(parent)
        self.setWindowTitle('Output')
        self.setGeometry(200, 200, 400, 300)

        layout = QVBoxLayout()
        '''
        # 텍스트 출력 위젯 생성
        self.text_edit = QTextEdit(self)
        layout.addWidget(self.text_edit)
        '''
        self.setLayout(layout)
        self.output_str = ''
        '''
        # 콘솔 출력을 캡처할 StringIO 객체 생성
        self.stdout_capture = StringIO()
        sys.stdout = self.stdout_capture
        '''
        self.show_output()
        label_output = QLabel(self.output_str,self)
        layout.addWidget(label_output)


    '''
    def closeEvent(self, event):
        # 애플리케이션 종료 시 콘솔 출력 복원
        sys.stdout = sys.__stdout__
    '''
    def show_output(self):
        data = self.parent().data
        correlation_method, ok = QInputDialog.getText(self, 'Input', 'correlation_method(pearson, spearman, kendall) :')

        if not ok or not correlation_method:
            correlation_method = 'pearson'


        result = data.corr(method=correlation_method)

        # 상관계수 결과 출력
        self.output_str = self.output_str + (f"선택한 상관계수 \n ({correlation_method}) 결과: {result}") + '\n'


class reg(QDialog):
    def __init__(self,parent = None):
        super().__init__(parent)
        self.setWindowTitle('Output')
        self.setGeometry(200, 200, 400, 300)

        layout = QVBoxLayout()
        '''
        # 텍스트 출력 위젯 생성
        self.text_edit = QTextEdit(self)
        layout.addWidget(self.text_edit)
        '''
        self.setLayout(layout)
        self.output_str = ''
        '''
        # 콘솔 출력을 캡처할 StringIO 객체 생성
        self.stdout_capture = StringIO()
        sys.stdout = self.stdout_capture
        '''
        self.show_output()
        label_output = QLabel(self.output_str,self)
        layout.addWidget(label_output)




    def closeEvent(self, event):
        # 애플리케이션 종료 시 콘솔 출력 복원
        sys.stdout = sys.__stdout__
    def show_output(self):
        data = self.parent().data

        X = data.drop(labels = str(self.parent().alpha),axis = 1)
        X = sm.add_constant(X)
        y = data[str(self.parent().alpha)]

        model = sm.OLS(y,X).fit()

        self.output_str += str(model.summary()) + '\n'




class FileDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Open Data File')
        self.setGeometry(200, 200, 400, 200)

        layout = QVBoxLayout()

        self.filepath = None

        self.file_button = QPushButton('Choose File')
        self.file_button.clicked.connect(self.openFile)
        layout.addWidget(self.file_button)

        self.open_button = QPushButton('Open')
        self.open_button.clicked.connect(self.accept)
        layout.addWidget(self.open_button)

        self.setLayout(layout)

    def openFile(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly

        filepath, _ = QFileDialog.getOpenFileName(self, 'Open Data File', '', 'CSV Files (*.csv);;Excel Files (*.xlsx)',
                                                  options=options)

        if filepath:
            self.filepath = filepath


class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Pascel v0.1.0-alpha")

        # 데이터를 저장할 변수 추가
        self.data = None

        self.initUI()

    def initUI(self):
        self.setGeometry(100, 100, 800, 600)

        self.initMenuBar()
        self.initTableWidget()

        self.show()

    def initMenuBar(self):
        menubar = self.menuBar()
        file_menu = menubar.addMenu('File')

        open_action = QAction('Open', self)
        open_action.triggered.connect(self.openFile)
        file_menu.addAction(open_action)

        # "Plot" 메뉴 추가
        plot_menu = menubar.addMenu('Plot')

        # "1D Plot" 액션 추가
        plot_1d_action = QAction('1D Plot', self)
        plot_1d_action.triggered.connect(self.plot_1d)
        plot_menu.addAction(plot_1d_action)

        # "2D Plot" 액션 추가
        plot_2d_action = QAction('2D Plot', self)
        plot_2d_action.triggered.connect(self.plot_2d)
        plot_menu.addAction(plot_2d_action)

        # "3D Plot" 액션 추가
        plot_3d_action = QAction('3D Plot', self)
        plot_3d_action.triggered.connect(self.plot_3d)
        plot_menu.addAction(plot_3d_action)

        #다중 그래프 추가

        plot_mul_action = QAction('Mul Plot', self)
        plot_mul_action.triggered.connect(self.plot_mul)
        plot_menu.addAction(plot_mul_action)

        # stats 메뉴추가
        stat_menu = menubar.addMenu('Stat')

        univariate_action = QAction('Univariate', self)
        univariate_action.triggered.connect(self.univeraite)
        stat_menu.addAction(univariate_action)

        C_D_action = QAction('Random variables and distributions', self)
        C_D_action.triggered.connect(self.C_D)
        stat_menu.addAction(C_D_action)

        #Estimation and Testing
        Estimation_Testing_action = QAction('Estimation and Testing', self)
        Estimation_Testing_action.triggered.connect(self.E_T)
        stat_menu.addAction(Estimation_Testing_action)

        #reggression and corr
        reggression_and_corr = QAction('reggression and corr', self)
        reggression_and_corr.triggered.connect(self.R_C)
        stat_menu.addAction(reggression_and_corr)


    def R_C(self):
        if self.data is not None:
            dialog = reg_and_corr(self, self.data)
            dialog.exec_()


    def E_T(self):
        if self.data is not None:
            dialog = Estimation_or_test(self, self.data)
            dialog.exec_()


    def univeraite(self):
        if self.data is not None:  # 데이터가 있는 경우에만 Univariate 창 열기
            univer_dialog = Univariate(self, self.data)  # 데이터프레임을 인자로 전달
            univer_dialog.exec_()

    def C_D(self):
        if self.data is not None:
            dialog = C_or_D(self, self.data)
            dialog.exec_()

    # 수정된 함수 시작
    def plot_1d(self):
        plot_dialog = Plot1DDialog(self)
        plot_dialog.exec_()

    def plot_2d(self):
        plot_dialog = Plot2DDialog(self)
        plot_dialog.exec_()


    def plot_3d(self):
        plot_dialog = Plot3DDialog(self)
        plot_dialog.exec_()

    def plot_mul(self):
        plot_dialog = mul_dialog(self)
        plot_dialog.exec_()

    def initTableWidget(self):
        self.tableWidget = QTableWidget()
        layout = QVBoxLayout()
        layout.addWidget(self.tableWidget)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # 우클릭 이벤트 연결
        self.tableWidget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tableWidget.customContextMenuRequested.connect(self.show_context_menu)

        # 컬럼 헤더 더블클릭 이벤트 연결
        self.tableWidget.horizontalHeader().sectionDoubleClicked.connect(self.change_column_name)

    def openFile(self):
        file_dialog = FileDialog(self)
        if file_dialog.exec_() == QDialog.Accepted:
            filepath = file_dialog.filepath
            if filepath:
                try:
                    self.data = pd.read_csv(filepath) if filepath.endswith('.csv') else pd.read_excel(filepath)
                    self.displayDataFrame(self.data)
                except Exception as e:
                    print(e)

    def displayDataFrame(self, df):
        self.tableWidget.clear()

        self.tableWidget.setRowCount(df.shape[0])
        self.tableWidget.setColumnCount(df.shape[1])

        self.tableWidget.setHorizontalHeaderLabels(df.columns)

        # column_names 정의
        self.column_names = df.columns.tolist()

        for row in range(df.shape[0]):
            for col in range(df.shape[1]):
                item = QTableWidgetItem(str(df.iat[row, col]))
                self.tableWidget.setItem(row, col, item)

    def show_context_menu(self, pos):
        context_menu = QMenu(self)
        add_row_action = QAction("Add Row", self)
        add_row_action.triggered.connect(self.add_row)
        context_menu.addAction(add_row_action)

        add_column_action = QAction("Add Column", self)
        add_column_action.triggered.connect(self.add_column)
        context_menu.addAction(add_column_action)

        save_data_action = QAction("Save Data", self)
        save_data_action.triggered.connect(self.save_data)
        context_menu.addAction(save_data_action)

        context_menu.exec_(self.tableWidget.mapToGlobal(pos))

    def add_row(self):
        row_position = self.tableWidget.rowCount()
        self.tableWidget.insertRow(row_position)

    def add_column(self):
        col_position = self.tableWidget.columnCount()
        self.tableWidget.insertColumn(col_position)
        for row in range(self.tableWidget.rowCount()):
            item = QTableWidgetItem("")
            self.tableWidget.setItem(row, col_position, item)

    def save_data(self):
        file_name, _ = QFileDialog.getSaveFileName(self, "Save Data", "", "CSV Files (*.csv)")

        if file_name:
            data = []
            for row in range(self.tableWidget.rowCount()):
                row_data = []
                for col in range(self.tableWidget.columnCount()):
                    item = self.tableWidget.item(row, col)
                    row_data.append(item.text())
                data.append(row_data)

            df = pd.DataFrame(data)
            df.to_csv(file_name, index=False)

    def change_column_name(self, index):
        new_name, ok = QInputDialog.getText(self, "Change Column Name", "Enter new column name:")
        if ok and new_name:
            self.tableWidget.setHorizontalHeaderItem(index, QTableWidgetItem(new_name))

class Output_window(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('OutputWindow')
        self.setGeometry(100, 100, 400, 300)

        # GUI 초기화
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # 텍스트 출력 위젯 생성
        self.text_edit = QTextEdit(self)
        layout.addWidget(self.text_edit)

        self.setLayout(layout)

        # 콘솔 출력을 캡처할 StringIO 객체 생성
        self.stdout_capture = StringIO()
        sys.stdout = self.stdout_capture


    def closeEvent(self, event):
        # 애플리케이션 종료 시 콘솔 출력 복원
        sys.stdout = sys.__stdout__


import html
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyWindow()
    window_output = Output_window()







    window.show()
    window_output.show()

    # 여기서 콘솔 출력 테스트
    print("This is Output Window you have to close MainWindow first (It will support next update!)")

    # 콘솔 출력 값을 GUI 텍스트 위젯에 전달
    captured_output = window_output.stdout_capture.getvalue()
    window_output.text_edit.setPlainText(captured_output)







    sys.exit(app.exec_())
