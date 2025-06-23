import requests
from bs4 import BeautifulSoup
import csv

urlCourse="https://syllabus.s.isct.ac.jp/courses/2025/7/0-907-0-110100-0"#該当する科目群のURLをここに
urls = []

def get_link(url): #科目群から科目ごとのurlを抽出する
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception if the request was unsuccessful
        soup = BeautifulSoup(response.content, "html.parser")
        #divContent = soup.find_all("div")
        # Find the first element with class "my-class"
        content, tabZero, links=[],[],[]
        element = soup.find_all(attrs={"data-tab-panel-label": "すべて"}) #「すべて」のカテゴリーの中にあるリンクのみ抽出
        #print(element)
        # Get all inner HTML (including tags and text)
        for el in element:
            links=el.find_all("a")
        for link in links:
            link=link['href'] #hrefタグの内容（リンク本体）を抽出
            tabZero.append(link)
        #tabZero="test"
        #child = tabBody.children
        #subjectName = soup.find_all("h1", "c-h1")
        return tabZero
    except requests.exceptions.RequestException as e:
        return f"An error occurred while fetching the content: {e}"

def get_kamoku(soup):
    subjectName = soup.find("h1", "c-h1")
    nametext=subjectName.get_text(strip=True)
    nametext=" ".join(nametext.split())
    return nametext

urls=get_link(urlCourse)# ✅ 解析対象のURLリストをゲット
# 抽出したい項目名
target_labels = [
    "担当教員",
    "開講クォーター",
    "成績評価の方法及び基準"
]

# ✅ すべてのデータを格納するリスト
all_data = []

# 各URLごとに処理
for url in urls:
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    result={}
    for label in target_labels:
        elements = soup.find_all(string=lambda text: label in text)
        for el in elements:
            parent = el.find_parent()
            next_element = parent.find_next_sibling()
            if next_element:
                result[label] = next_element.get_text(strip=True)
                break
            else:
                result[label] = ""  # 見つからない場合は空白に
    result["URL"]=url  # URLも記録しておくと便利
    #科目の名前をゲット
    kamokuName=get_kamoku(soup)
    result["科目名"]=kamokuName
    print(kamokuName) #進捗状況を把握するため
    all_data.append(result) #抽出したものを全体のdictionaryに入れる
# ✅ CSVに保存（1ページ＝1行）
with open("syllabus_allV2.csv", "w", newline="", encoding="utf-8-sig") as f:
    fieldnames = ["科目名"] + target_labels + ["URL"]
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(all_data)
    print("書き込み中…")

print("✅ 複数ページのデータを syllabus_all.csv に保存しました！")
