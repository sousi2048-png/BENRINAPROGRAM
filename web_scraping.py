# ウェブクローリングと内容抽出のためのライブラリをインポート
import requests
from bs4 import BeautifulSoup
import trafilatura
import time
from urllib.parse import urljoin, urlparse, urldefrag
import csv

# パラメータの設定
# クローリング開始URL（複数可）
start_urls = ["https://ss64.com/ps/"]

max_crawl_count = 10000  # 最大クローリングページ数
ng_words = []  # クローリング除外ワード
ok_words = []  # クローリング指定ワード
specific_path_only = True  # 指定したURLの階層以降のみをクローリング対象とする

# クロール済みURLと抽出したコンテンツを格納するリスト
visited_urls = set()
content_list = []


# 抽出したコンテンツをファイルに保存する関数
def save_content_to_file(data, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        for content in data:
            f.write("------------------------------------------------------\n")
            f.write(f"<url>{content['url']}</url>\n\n")
            f.write("<content>\n")
            f.write(content['text'])
            f.write("\n</content>\n\n")

# クロールしたURLをCSVファイルに保存する関数
def save_urls_to_csv(urls, filename):
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['URL'])
        for url in urls:
            writer.writerow([url])

# URLが許可されているかチェックする関数（NGワードを含まないか）
def is_url_allowed(url, ng_words):
    return not any(ng_word in url for ng_word in ng_words)

# URLが指定ワードを含むかチェックする関数
def is_url_included(url, ok_words):
    return not ok_words or any(ok_word in url for ok_word in ok_words)

# URLが指定されたパス以降かチェックする関数
def is_within_specific_path(url, start_url, specific_path_only):
    if not specific_path_only:
        return True
    start_path = urlparse(start_url).path
    return urlparse(url).path.startswith(start_path)

# 再帰的にウェブページをクロールする関数
def crawl(url, max_crawl_count, start_url):
    if url not in visited_urls and len(visited_urls) < max_crawl_count:
        visited_urls.add(url)
        print(f"Crawling {len(visited_urls)}: {url}")
        try:
            response = requests.get(url)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'html.parser')
            title_tag = soup.title.string if soup.title else 'No Title'
            raw_content = trafilatura.extract(response.text, output_format='markdown')
            if raw_content:
                content_list.append({
                    'url': url,
                    'title': title_tag,
                    'text': raw_content
                })

            # このページ内のリンクを取得
            links = [a['href'] for a in soup.find_all('a', href=True)]

            # さらにリンク先をクロール
            for link in links:
                if len(visited_urls) >= max_crawl_count:
                    break
                absolute_url = urljoin(url, link)
                absolute_url, _ = urldefrag(absolute_url)  # フラグメントを除去
                parsed_url = urlparse(absolute_url)

                if (parsed_url.hostname == urlparse(start_url).hostname
                        and absolute_url not in visited_urls
                        and is_url_allowed(absolute_url, ng_words)
                        and is_url_included(absolute_url, ok_words)
                        and is_within_specific_path(absolute_url, start_url, specific_path_only)):
                    time.sleep(0.1)  # クロール先の負荷調整
                    crawl(absolute_url, max_crawl_count, start_url)

        except requests.RequestException as e:
            print(f"Error crawling {url}: {e}")

# メインの処理：各開始URLに対してクローリングを実行
for start_url in start_urls:
    crawl(start_url, max_crawl_count, start_url)

# 抽出したコンテンツとURLをファイルに保存
save_content_to_file(content_list, 'crawled_content.txt')
save_urls_to_csv(visited_urls, 'crawled_urls.csv')

# クローリング結果の統計を出力
total_word_count = sum(len(content['text'].split()) for content in content_list)
print(f"Crawled {len(content_list)} pages.")
print(f"Total word count: {total_word_count}")