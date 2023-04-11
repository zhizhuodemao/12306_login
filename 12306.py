from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import base64
import requests
import json

# 如果你的浏览器版本是88以前, 要去执行一段js代码
# web.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
#   "source": """
#   navigator.webdriver = undefined
#     Object.defineProperty(navigator, 'webdriver', {
#       get: () => undefined
#     })
#   """
# })


# 88以后的版本用下面的方案
opt = Options()
opt.add_argument("--disable-blink-features=AutomationControlled")


def base64_api(uname, pwd, img, typeid):
    """
    # 一、图片文字类型(默认 3 数英混合)：
        # 1 : 纯数字
        # 1001：纯数字2
        # 2 : 纯英文
        # 1002：纯英文2
        # 3 : 数英混合
        # 1003：数英混合2
        #  4 : 闪动GIF
        # 7 : 无感学习(独家)
        # 11 : 计算题
        # 1005:  快速计算题
        # 16 : 汉字
        # 32 : 通用文字识别(证件、单据)
        # 66:  问答题
        # 49 :recaptcha图片识别
    # 二、图片旋转角度类型：
        # 29 :  旋转类型
        #
    # 三、图片坐标点选类型：
        # 19 :  1个坐标
        # 20 :  3个坐标
        # 21 :  3 ~ 5个坐标
        # 22 :  5 ~ 8个坐标
        # 27 :  1 ~ 4个坐标
        # 48 : 轨迹类型
        #
    # 四、缺口识别
        # 18 : 缺口识别（需要2张图 一张目标图一张缺口图）
        # 33 : 单缺口识别（返回X轴坐标 只需要1张图）
        # 五、拼图识别
        # 53：拼图识别
    :param uname:
    :param pwd:
    :param img:
    :param typeid:
    :return:
    """
    data = {"username": uname, "password": pwd, "typeid": typeid, "image": img}
    result = json.loads(requests.post("http://api.ttshitu.com/predict", json=data).text)
    if result['success']:
        return result["data"]["result"]
    else:
        return result["message"]
    return ""


url = "https://kyfw.12306.cn/otn/resources/login.html"
web = Chrome(options=opt, executable_path="./chromedriver.exe")
web.maximize_window()
web.get(url)

web.implicitly_wait(10)

username_input = web.find_element_by_xpath('//*[@id="J-userName"]')
password_input = web.find_element_by_xpath('//*[@id="J-password"]')

username_input.send_keys("username")
password_input.send_keys("password")

login_btn = web.find_element_by_xpath('//*[@id="J-login"]')
login_btn.click()

verify_img = web.find_element_by_xpath('//*[@id="modal"]')
verify_img_base64 = verify_img.screenshot_as_base64
print(verify_img.location)

span = web.find_element_by_xpath('//*[@id="nc_1_n1z"]')
ActionChains(web).drag_and_drop_by_offset(span, xoffset=380, yoffset=0).perform()
web.quit()
# 总体来说 12306的登陆还是比较简单 没什么太大难度
