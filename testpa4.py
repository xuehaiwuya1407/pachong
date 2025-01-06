import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
# 设置Chrome的启动选项，启用headless模式
options = webdriver.ChromeOptions()
options.add_argument('--headless')  # 启用无头模式
options.add_argument('--disable-gpu')  # 禁用GPU加速
options.add_argument('--no-sandbox')  # 禁用沙盒模式
# 初始化webdriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)
# 小说主页URL
mainurl = "https://www.beqege.cc/40988/"
# 打开首页获取章节链接
driver.get(mainurl)
time.sleep(2)  # 等待页面加载完毕
# 获取页面源代码
main_html = driver.page_source
# 使用BeautifulSoup解析HTML
soup = BeautifulSoup(main_html, 'html.parser')
# 获取章节列表（假设每章链接在<dd><a>标签内）
chapter_list = soup.find('div', id='list').find_all('dd')
chapter_data = [(mainurl + a.find('a')['href'], a.find('a').text.strip()) for a in chapter_list[:100]]  # 提取链接和标题，只取前100章
# 指定保存路径
save_dir = r"D:\武道宗师"  # 这里是目标文件夹路径
if not os.path.exists(save_dir):  # 如果文件夹不存在，则创建
    os.makedirs(save_dir)
# 函数：获取章节内容并去除广告
def get_chapter_content(chapter_url):
    driver.get(chapter_url)
    time.sleep(2)  # 等待页面加载
    chapter_html = driver.page_source
    # 使用BeautifulSoup解析章节页面
    chapter_soup = BeautifulSoup(chapter_html, 'html.parser')
    content = chapter_soup.find('div', id='content')  # 获取章节内容
    if content:
        # 获取章节文本
        text = content.get_text(separator='\n', strip=True)
        # 删除广告部分
        ad_text = "【告知书友，时代在变化，免费站点难以长存，手机app多书源站点切换看书大势所趋，站长给你推荐的这个换源APP，听书音色多、换源、找书都好使！】"
        # 删除前后广告
        text = text.replace(ad_text, "").strip()
        return text
    return ""
# 保存章节到文本文件（添加标题为第一行）
def save_chapter_to_file(chapter_title, chapter_subtitle, content):
    file_path = os.path.join(save_dir, f'{chapter_title}.txt')  # 保存路径
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(chapter_subtitle + "\n\n")  # 第一行写入章节标题
        f.write(content)  # 写入章节内容
# 遍历章节链接并获取内容（仅抓取前几章）
for index, (chapter_url, chapter_subtitle) in enumerate(chapter_data):
    print(f"正在抓取第 {index + 1} 章：{chapter_url}")
    chapter_title = f"第{index + 1}章"
    content = get_chapter_content(chapter_url)
    if content:
        save_chapter_to_file(chapter_title, chapter_subtitle, content)
        print(f"保存章节：{chapter_title} - {chapter_subtitle}")
    else:
        print(f"未能获取到章节内容：{chapter_url}")
# 关闭浏览器
driver.quit()