#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Description: 系统类
usage: 调用window.pywebview.api.<methodname>(<parameters>)从Javascript执行
'''

import os
import codecs
import csv
import json
import time

import webview


class System():
    '''系统类'''
    window = None

    def __init__(self):
        self.file_path = None
        self.result = None

    def system_py2js(self, func, info):
        '''调用js中挂载到window的函数'''
        infoJson = json.dumps(info)
        System.window.evaluate_js(f"{func}('{infoJson}')")

    def system_open_file(self, read_encoding: str):
        '''打开文件对话框'''
        file_types=['全部文件 (*.*)']
        directory=''
        try:
            file_types = tuple(file_types)
            self.result = System.window.create_file_dialog(dialog_type=webview.OPEN_DIALOG, directory=directory, allow_multiple=False, file_types=file_types)
            self.file_path = self.result[0]

            # 判断csv的分割符
            with open(self.file_path, 'r', encoding=read_encoding) as csvfile:
                delimiter = csv.Sniffer().sniff(csvfile.read(5000)).delimiter
            
            # 打开CSV文件并读取前10行
            rows = []
            with open(self.file_path, mode='r', encoding=read_encoding) as file:
                reader = csv.DictReader(file, delimiter=delimiter)
                for i, row in enumerate(reader):
                    if i == 10:
                        break
                    rows.append(row)

            # 将读取的csv数据转换为JSON格式
            data = {
                'file_path': self.file_path,
                'json_data': json.dumps(rows, ensure_ascii=False, indent=4)
            }
            json_data = json.dumps(data, ensure_ascii=False, indent=4)
            return json_data

        except Exception as e:
            json_error = json.dumps(repr(e), ensure_ascii=False, indent=2)
            data = {
                'file_path': self.file_path,
                'json_data': json_error
            }
            json_data = json.dumps(data, ensure_ascii=False, indent=4)
            return json_data
    
    def convert_encoding(self, read_encoding: str, write_encoding: str):
        start_time = time.time()

        try:
            filename = os.path.splitext(self.file_path)[0]
            output_path = f'{filename}_{write_encoding}.csv'
            print(output_path)
            # 打开输入文件和输出文件
            with open(self.file_path, 'r', encoding=read_encoding, newline='') as infile, \
                    codecs.open(output_path, 'w', encoding=write_encoding) as outfile:
                # 创建CSV读取器
                reader = csv.reader(infile)
                # 创建CSV写入器
                writer = csv.writer(outfile)
                # 读取并写入数据
                for row in reader:
                    writer.writerow(row)
        except Exception as e:
            json_error = json.dumps(repr(e), ensure_ascii=False, indent=2)
            return json_error
        
        end_time = time.time()
        elapsed_time = round(end_time - start_time, 2)
        return elapsed_time
