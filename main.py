from .src.translater import Translater
from .src.web_crawler import WebCrawler
import json
import time

websites_info_file = './data/ai_websites.json'
result_file = './data/result.json'

# 创建一个空的result_file
with open(result_file, 'w') as f:
    json.dump({}, f, indent=4)


def search_info(key_word):
    crawler = WebCrawler()
    translater = Translater()
    with open(websites_info_file, 'r') as f:
        websites_info = json.load(f)
        ai_websites = websites_info['ai_websites']

    for site in ai_websites:
        url_list = site['url_list']
        website_name = site['name']

        with open(result_file, 'r') as f:
            result_dict = json.load(f)
            if website_name not in result_dict:
                result_dict[website_name] = []

        print(f"正在爬取{website_name}的数据...")
        for url in url_list:
            page_content = crawler.get_page_content(url)
            result = crawler.get_href_by_keyword(
                page_content, key_word, match_case=True)

        # 检测result的长度，如果为零就跳过后面的步骤
        if len(result) == 0:
            print(f'{website_name}没有找到关于{key_word}的内容！')
            continue

        for item in result:
            href = item['href']
            text = item['text']
            translated_text = translater.translate(text, "en", "zh")
            # 翻译api每秒最多只能调用5次，所以这里设置0.3秒的延迟
            time.sleep(0.3)
            result_dict[website_name].append(
                {
                    "href": href,
                    "title": translated_text
                }
            )

        with open(result_file, 'w') as f:
            json.dump(result_dict, f, indent=4)
        print(f'{website_name}的数据爬取完毕！')

    crawler.close()


if __name__ == "__main__":
    key_word = input("请输入关键词：")
    search_info(key_word)
