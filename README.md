# XJTU-DHA-auto-complete
西安交通大学健康每日报自动打卡/Xi'an Jiaotong University Daily Health Assessment Auto Complete

## 西安交通大学健康每日报自动打卡
* 使用python3编写的一个小程序，可以帮你每天自动打卡  
* **使用前需手动打卡过**，确保除体温及健康码颜色之外的其他信息能自动加载  
* 建议部署在Linux上并使用crontab定时执行  

## 以CentOS 7为例的Linux部署方法
1. 安装Chrome
2. 前往 https://chromedriver.storage.googleapis.com/index.html 下载最新Chrome自动控制驱动，解压后在SSH输入

    mv chromedriver /usr/bin/
3. 设定crontab定时任务，执行如下shell脚本

    #!/bin/bash  
    /path/to/python /path/to/XJTU.py
    
   将上方两个路径分别改为python解释器路径和py文件存放路径
4. Chrome安装方法和crontab设置方法可自行百度
