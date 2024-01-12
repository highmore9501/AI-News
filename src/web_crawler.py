from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from typing import Tuple
import time
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class WebCrawler:
    def __init__(self) -> None:
        # 设置 ChromeDriver 的路径
        self.driver_path = "C:/chromedriver/chromedriver.exe"

        # 设置浏览器选项
        self.chrome_options = Options()
        self.chrome_options.add_argument("--no-sandbox")  # 非沙盒模式运行，避免部分环境下出现问题
        self.chrome_options.add_argument("--disable-dev-shm-usage")  # 禁用虚拟内存

        # 设置浏览器标头信息
        self.chrome_options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6099.217 Safari/537.36")  # 替换为合适的 Chrome 版本号

        # 创建 ChromeDriver 实例
        self.driver = webdriver.Chrome(options=self.chrome_options)

    def get_page_content(self, url: str) -> str:
        # 打开指定的URL
        self.driver.get(url)
        # 获取页面源代码
        page_content = self.driver.page_source
        return page_content

    def get_href_by_keyword(self, page_content, keyword: str, match_case: bool) -> Tuple[str, str]:
        result = []
        # 寻找所有带有href属性的a标签
        soup = BeautifulSoup(page_content, "html.parser")
        a_tags = soup.find_all("a", href=True)

        for tag in a_tags:
            if match_case:
                if keyword in tag.text:
                    # 简化tag.text
                    tag.text = self.simplify_text(tag.text)
                    result.append(
                        {
                            "href": tag["href"],
                            "text": tag.text,
                        }
                    )
            else:
                if keyword.lower() in tag.text.lower():
                    tag.text = self.simplify_text(tag.text)
                    result.append(
                        {
                            "href": tag["href"],
                            "text": tag.text,
                        }
                    )

        return result

    def simplify_text(self, text: str) -> str:
        # 将tag.text的长度控制在256以内
        if len(text) > 256:
            text = text[:256]

        # 并且确保最后一个字符是空格或者逗号，句号
        if text[-1] not in [" ", ",", "."]:
            # 从tag.text中找到最后一个空格的位置
            last_space_index = text.rfind(" ")
            # 从tag.text中找到最后一个逗号的位置
            last_comma_index = text.rfind(",")
            # 从tag.text中找到最后一个句号的位置
            last_period_index = text.rfind(".")
            # 选择三个位置中最大的一个
            max_index = max(last_space_index,
                            last_comma_index, last_period_index)
            # 截取tag.text的前max_index个字符
            text = text[:max_index+1]

        return text

    def close(self):
        # 关闭浏览器
        self.driver.quit()