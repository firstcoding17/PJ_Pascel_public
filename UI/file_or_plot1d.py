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

        filepath, _ = QFileDialog.getOpenFileName(self, 'Open Data File', '',
                                                  'CSV Files (*.csv);;JSON Files (*.json);;Excel Files (*.xlsx)',
                                                  options=options)

        if filepath:
            self.filepath = filepath
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





