# -*- coding: UTF-8 -*-
##Copyleft@2020 Jerry Yang
##Licensed Under GNU GPLv3
##西交每日健康报自动打卡
##使用selenium库模拟Chrome浏览器
##可以使用crontab定时自动执行，为Linux命令行以headless模式运行Chrome设计

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time
import random

option = webdriver.ChromeOptions()
option.add_argument('--headless')  #设置为headless mode，win平台下调试的时候注释这行
option.add_argument('--no-sandbox') #Linux下root权限运行，win平台下调试的时候注释这行
option.add_argument('--window-size=1920,1080') #headless模式下指定窗口大小，win平台下调试的时候注释这行
capabilities = DesiredCapabilities.CHROME
capabilities['goog:loggingPrefs'] = { 'browser':'ALL' } #设置浏览器log读取等级
driver = webdriver.Chrome(desired_capabilities=capabilities,options=option)
#driver.maximize_window()  #最大化浏览器窗口

USERNAME = "" #用户名
PASSWORD = "" #密码
login = "http://jkrb.xjtu.edu.cn/EIP/user/index.htm"   #登录页面，带参跳转

##西交SSO登录操作
def user_login(account,password,url):
    driver.get(url)
    time.sleep(5)  #等待浏览器渲染js文件
    driver.find_element_by_xpath('//*[@id="form1"]/input[1]').send_keys(account) #输入用户名密码
    driver.find_element_by_xpath('//*[@id="form1"]/input[2]').send_keys(password)
    driver.find_element_by_xpath('//*[@id="account_login"]').click() #点击登录按钮
    time.sleep(5)

##健康报打卡操作
def daka():
    time.sleep(3)
    ##driver.find_element_by_link_text(u'本科生每日健康状况填报').click()
    ##driver.find_element_by_xpath('//*[@id="form"]/div[2]/div/ul[1]/li[2]/div/a').click()
    driver.switch_to.frame(driver.find_element_by_xpath('//*[@id="mini-17$body$2"]/iframe')) #进入页面主框架
    driver.switch_to.frame(1) #进入二级框架
    driver.find_element_by_xpath('//*[text()="本科生每日健康状况填报"]').click() #更新-尽量避免使用index确定按钮位置
    ##driver.execute_script('document.getElementsByClassName("service-hall-box-top-hover")[1].click()') #执行JavaScript点击“本科生每日健康状况填报”按钮
    time.sleep(3)
    driver.switch_to.default_content() #回退到页面主框架外
    driver.switch_to.frame(driver.find_element_by_xpath('//*[@id="mini-17$body$3"]/iframe')) #进入标签页框架
    driver.find_element_by_xpath('//*[text()="每日健康填报"]').click() #调试使用“漏填健康日报补录”，调试结束后改为“每日健康填报”
    ##driver.execute_script('document.getElementsByClassName("bl-item bl-link active")[0].click()') #js点击“每日健康填报”按钮（按钮位置index可能改变）
    time.sleep(5)
    if checkDakaStat():
        print('今日已打卡，无需重复')
    else:
        ##开始打卡-todo
        driver.switch_to.default_content() #回退到页面主框架外
        driver.switch_to.frame(driver.find_element_by_xpath('//*[@id="mini-17$body$4"]/iframe')) #进入标签页框架
        driver.switch_to.frame(0) #进入表格二级框架
        ##Step1 选择绿码选项
        driver.find_element_by_css_selector('[value="绿色"]').click() #调试结束改为绿色！！
        ##Step2 填入自动生成的体温数值
        driver.find_element_by_name('BRTW').send_keys(fakeTemperature())
        ##Step3 点击提交
        driver.switch_to.parent_frame() #退出到表格二级框架外
        driver.execute_script('document.getElementById("sendBtn").click()') #js点击提交按钮
        driver.find_element_by_xpath('//*[text()="确定"]').click() #操控点击确定按钮
        ## **在每个打卡时间段结束前1小时可以进行一个遍历检查，console.log返回“每天仅可填报一次，请勿重复！”即可判断自动填报成功

##自动生成36.0-36.9度之间的一个体温数值
def fakeTemperature():
    decimal = random.randint(0,9)
    srtDecimal = str(decimal)
    temp = "36." + srtDecimal
    print("已自动生成体温数值"+temp+"度")
    return temp

#检查打卡状态，console.log返回“每天仅可填报一次，请勿重复！”即可判断自动填报成功
def checkDakaStat():
    consoleLog = driver.get_log('browser')
    for logs in consoleLog:
        if logs['level'] == 'INFO':
            if logs['message'].find('每天仅可填报一次，请勿重复！') != -1:
                return True
    return False


##main
def main():
    print("开始自动打卡")
    print("正在自动登录")
    user_login(USERNAME,PASSWORD,login)  #登陆
    time.sleep(2)
    print("登陆成功，开始导向打卡页面")
    daka()
    print("提交完成")
    time.sleep(3)
    driver.quit()
    #cookies = driver.get_cookies()  #获取cookies，调试语句，正式上线时注释
    #print(cookies)

if __name__ == '__main__':
    main()
