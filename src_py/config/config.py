'''
Author: tansen
Date: 2024-10-20 19:15:08
LastEditors: 
LastEditTime: 2024-10-20 19:44:42
'''
'''
Description: 配置文件
usage:
    from src_py.config.config import Config
    print(Config.rootDir)
'''

import os
import sys
import getpass
import platform


class Config:
    '''配置文件'''

    ##
    # 程序基础配置信息
    ##
    appName = 'csv-tool'  # 应用名称
    appNameEN = 'csv-tool'    # 应用名称-英文（用于生成缓存文件夹，必须是英文）
    appVersion = "V0.1.0"  # 应用版本号
    appDeveloper = "tansen"  # 应用开发者
    appBlogs = "https://github.com/tansen87"  # github
    appPackage = 'csv-tool'    # 应用包名，用于在本地电脑生成 pywebview-toolkit.ppx 唯一文件夹
    appUpdateUrl = 'https://github.com/tansen87'
    appISSID = '56CD5B56-61AB-8E1A-DB2D-3311562E5350'    # Inno Setup 打包唯一编号。在执行 pnpm run init 之前，请设置为空，程序会自动生成唯一编号，生成后请勿修改！！！

    ##
    # 系统配置信息（不需要修改，可以自动获取）
    ##
    appSystem = platform.system()    # 本机系统类型
    appIsMacOS = appSystem == 'Darwin'    # 是否为macOS系统
    codeDir = sys.path[0].replace('base_library.zip', '')    # 代码根目录
    appDir = codeDir.replace(appName+'.app/Contents/MacOS/', '')    # 程序所在绝对目录
    staticDir = os.path.join(codeDir, 'static')    # 程序包中的static文件夹的绝对路径
    storageDir = ''    # 电脑上的存储目录
    downloadDir = ''    # 电脑上的下载目录

    ##
    # 其他配置信息
    ##
    devPort = '5173'    # 开发环境中的前端页面端口
    devEnv = True    # 是否为开发环境，不需要手动更改，在程序运行的时候自动判断
    ifCoverDB = False    # 是否覆盖电脑上存储的数据库，默认不覆盖。只有在数据库改动非常大，不得已的情况下才建议覆盖数据库

    ##
    # 函数
    ##
    def init(self):
        '''初始化'''
        # 获取电脑上的目录
        self.getDir()

    def getDir(self):
        '''获取电脑上的目录'''
        if Config.appSystem == 'Darwin':
            # Mac系统
            user = getpass.getuser()
            storageDir = os.path.join('/', 'Users', user, 'Library', 'Application Support')
            downloadDir = os.path.join('/', 'Users', user, 'Downloads')
        else:
            # win系统
            storageDir = os.getenv('APPDATA')
            downloadDir = os.path.join(os.getenv('USERPROFILE'), 'Downloads')
        storageDir = os.path.join(storageDir, Config.appPackage+'.'+Config.appNameEN)
        if not os.path.isdir(storageDir):
            os.mkdir(storageDir)
        Config.storageDir = storageDir    # 电脑上的存储目录
        Config.downloadDir = downloadDir    # 电脑上的下载目录
