import json
import os
import time


def write_MD(src_file, websites_info_file, md_file):
    with open(websites_info_file, 'r', encoding='utf-8') as f1:
        websites_info = json.load(f1)['ai_websites']
    with open(src_file, 'r', encoding='utf-8') as f2:
        result_dict = json.load(f2)
    # 创建一个空的md_file
    with open(md_file, 'w', encoding='utf-8') as f3:
        f3.write(f'[toc]\n# News_{today}\n\n')

    for key, value in result_dict.items():
        website_info = [
            item for item in websites_info if item['name'] == key][0]
        description = website_info['description']
        with open(md_file, 'a', encoding='utf-8') as f:
            f.write(f'## {key}\n\n')
            f.write(f'{description}\n\n')
            for item in value:
                href = item['href']
                title = item['title']
                f.write(f'- [{title}]({href})\n')
            f.write('\n')

    print(f'写入{md_file}完成！')


if __name__ == "__main__":
    today = time.strftime("%Y-%m-%d", time.localtime())
    src_file = '../data/result.json'
    websites_info_file = '../data/ai_websites.json'
    md_file = f'../data/result/News_{today}.md'
    write_MD(src_file, websites_info_file, md_file)
