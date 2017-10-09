# -*- coding: utf-8 -*- 
import io
import json
import logging
import random
import re
import sys
import time
import urllib
import urllib2

import PIL.Image as image
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains


# 根据位置对图片进行合并还原
# content:图片内容
# location_list:图片位置
# 内部两个图片处理函数的介绍
# crop函数带的参数为(起始点的横坐标，起始点的纵坐标，宽度，高度）
# paste函数的参数为(需要修改的图片，粘贴的起始点的横坐标，粘贴的起始点的纵坐标）
def __get_merge_image__(content, location_list):
    # 打开图片文件
    fp = io.BytesIO(content)
    try:
        im = image.open(fp)
    except:
        fp.close()
        raise (sys.exc_info()[0](sys.exc_info()[1]))

    # 创建新的图片,大小为260*116
    im_list_upper = []
    im_list_down = []

    # 拷贝图片
    for location in location_list:
        # 上面的图片
        if location["y"] == -58:
            im_list_upper.append(im.crop((abs(location["x"]), 58, abs(location["x"]) + 10, 116)))
        # 下面的图片
        if location["y"] == 0:
            im_list_down.append(im.crop((abs(location["x"]), 0, abs(location["x"]) + 10, 58)))
    new_im = image.new("RGB", (260, 116))
    x_offset = 0

    # Close resources
    im.close()
    fp.close()

    # 黏贴图片
    for im in im_list_upper:
        new_im.paste(im, (x_offset, 0))
        x_offset += im.size[0]
    x_offset = 0
    for im in im_list_down:
        new_im.paste(im, (x_offset, 58))
        x_offset += im.size[0]
    return new_im


# 下载并还原图片
# driver:webdriver
# div:图片的div
def __get_image__(driver, div, timeout=10):
    # 找到图片所在的div
    background_images = driver.find_elements_by_xpath(div)
    location_list = []
    imageurl = ""

    # 图片是被CSS按照位移的方式打乱的,我们需要找出这些位移,为后续还原做好准备
    for background_image in background_images:
        location = {}
        # 在html里面解析出小图片的url地址，还有长高的数值

        location["x"] = int(re.findall("background-image: url\(\"(.*)\"\); background-position: (.*)px (.*)px;",
                                       background_image.get_attribute("style"))[0][1])
        location["y"] = int(re.findall("background-image: url\(\"(.*)\"\); background-position: (.*)px (.*)px;",
                                       background_image.get_attribute("style"))[0][2])
        imageurl = re.findall("background-image: url\(\"(.*)\"\); background-position: (.*)px (.*)px;",
                              background_image.get_attribute("style"))[0][0]
        location_list.append(location)

    # 替换图片的后缀,获得图片的URL
    imageurl = imageurl.replace("webp", "jpg")

    # 获得图片的名字
    imageName = imageurl.split("/")[-1]

    # 获得图片
    request = urllib2.Request(imageurl)
    request.add_header("User-Agent", "Mozilla/5.0 (Windows NT 5.1; rv:33.0) Gecko/20100101 Firefox/33.0")
    response = urllib2.urlopen(request, timeout=timeout)
    result = response.read()

    # 重新合并还原图片
    return __get_merge_image__(result, location_list)


# 对比RGB值
def __is_similar__(image1, image2, x, y):
    # 获取指定位置的RGB值
    pixel1 = image1.getpixel((x, y))
    pixel2 = image2.getpixel((x, y))
    for i in range(0, 3):
        # 如果相差超过50则就认为找到了缺口的位置
        if abs(pixel1[i] - pixel2[i]) >= 50:
            return False
    return True


# 计算缺口的位置
def __get_diff_location__(image1, image2):
    # 两张原始图的大小都是相同的260*116
    # 那就通过两个for循环依次对比每个像素点的RGB值
    # 如果相差超过50则就认为找到了缺口的位置
    for i in range(0, 260):
        for j in range(0, 116):
            if not __is_similar__(image1, image2, i, j):
                return i


# 根据缺口的位置模拟x轴移动的轨迹
def __get_track__(length):
    data_list = []
    while True:
        x = length / 2 + random.randint(-2, 2)
        if length - x >= 5:
            data_list.append(x)
            length -= x
        else:
            break
    # 最后五步都是一步步移动
    for i in range(length):
        data_list.append(1)
    return data_list


# Crack and get token & sid
def __crack__():
    # 打开火狐浏览器
    driver = webdriver.PhantomJS()

    token = None

    # 从cookie中获得sid
    sid = None

    try:
        # 用火狐浏览器打开网页
        driver.get("http://nx.gsxt.gov.cn/")
        time.sleep(2)

        # 下载图片
        image1 = __get_image__(driver, '//div[@class="gt_cut_bg gt_show"]/div')
        image2 = __get_image__(driver, '//div[@class="gt_cut_fullbg gt_show"]/div')

        # 计算缺口位置
        loc = __get_diff_location__(image1, image2)

        # 生成x的移动轨迹点
        track_list = __get_track__(loc)

        # 找到滑动的圆球
        element = driver.find_element_by_xpath('//div[@class="gt_slider_knob gt_show"]')

        # 鼠标点击元素并按住不放
        ActionChains(driver).click_and_hold(on_element=element).perform()
        time.sleep(0.15)

        # 拖动元素
        radius = 22
        for track in track_list:
            y_offset = radius + random.randint(-3, 3)
            # xoffset与yoffset是相对于滑动圆球左上角的值，注意
            ActionChains(driver).move_to_element_with_offset(to_element=element, xoffset=track + radius,
                                                             yoffset=y_offset).perform()
            # 间隔时间也通过随机函数来获得,间隔不能太快,否则会被认为是程序执行
            time.sleep(random.randint(10, 50) / 100.0)

        # 本质就是向后退6格。这里退了6格是因为圆球的位置和滑动条的左边缘有6格的距离
        for i in range(6):
            ActionChains(driver).move_to_element_with_offset(to_element=element, xoffset=radius - 1,
                                                             yoffset=radius).perform()
        time.sleep(0.1)

        # 释放鼠标
        ActionChains(driver).release(on_element=element).perform()
        time.sleep(3)

        # 验证是否通过，并获得token
        submit = driver.find_element_by_xpath('//div[@class="gt_ajax_tip gt_success"]')
        validate = driver.find_element_by_xpath('//input[@class="geetest_seccode"]')
        token = validate.get_attribute("value")

        # 从cookie中获得sid
        sid = driver.get_cookie("sid")['value']
    except:
        logging.warning("%s: %s" % (sys.exc_info()[0], sys.exc_info()[1]))
        [token, sid] = ["", ""]
    finally:
        # 关闭浏览器
        driver.quit()
    return [token, sid]


# 如果登录成功则返回0
def __login__(account, password, token, sid, timeout):
    postdata = urllib.urlencode({"userAcct": account, "userPassword": password, "token": token})
    request = urllib2.Request("http://www.qixin.com/service/login", postdata)
    request.add_header("cookie", "sid=" + sid)
    response = urllib2.urlopen(request, timeout=timeout)
    content = response.read()
    result = json.loads(content)

    if result["data"]["status"] == 0:
        return 0

    logging.warning("Login fail result: %s" % (result["data"]["message"]))
    return -1


# 自动登录，如果登录成功则返回sid数据，如果失败则返回空值
def auto_crack(account, password, timeout):
    try:
        [token, sid] = __crack__()
    except:
        logging.warning("%s: %s" % (sys.exc_info()[0], sys.exc_info()[1]))
        return ""

    try:
        if __login__(account, password, token, sid, timeout) == 0:
            return sid
        else:
            return ""
    except:
        logging.warning("%s: %s" % (sys.exc_info()[0], sys.exc_info()[1]))
        return ""


def main():
    ####
    #### 账号和密码需要修改！！！
    ####

    # 日志设置
    logging.basicConfig(level=logging.WARNING,
                        format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                        datefmt='%d %b %Y %H:%M:%S',
                        filename='test.log',
                        filemode='a')

    # 用内存代替显存
    # display = Display(visible=0, size=(1280, 960))
    # display.start()

    sid = auto_crack("13532369240", "555556", 3)
    if sid != "":
        print "Crack and login success"
        request2 = urllib2.Request(
            "http://www.qixin.com/service/getInvestedCompaniesById?eid=d6fb218c-e0d3-45e2-9645-e7b6fa84ef5b")
        request2.add_header("cookie", "sid=" + sid)
        response2 = urllib2.urlopen(request2, timeout=3)
        result = response2.read()
        print(result)

        # 关闭display功能
        # display.stop()


if __name__ == '__main__':
    main()
