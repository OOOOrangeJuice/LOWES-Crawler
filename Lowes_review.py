import requests as rs
import re
import time
import pandas as pd

ids = ["1001299116", "1075959", "1001155988", "1001155954"]                                                                          #change to target ID list
result_add = "C:\\Users\\Jonny_Chen\\Desktop\\橙汁\\常规任务\\不定期爬虫\\Tasks\\20200907 LOWES for Checky"                            #change to output address

header = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36"}

for id in ids:
    rating_list = []
    time_list = []
    review_list = []
    title_list = []

    # 读取真正储存LOWES评论的地址
    req = rs.get("https://www.lowes.com/rnr/r/get-by-product/" + id + "/pdp/prod",headers=header)
    resp = req.text

    # 获取相关信息
    ratings = re.findall(r'"Rating":(.)',resp)
    times = re.findall(r'"SubmissionTime":"(.*?)"',resp)
    reviews = re.findall(r'"ReviewText":(.*?),"',resp)
    titles = re.findall(r'"Title":(.*?),"',resp)

    # 存入List中
    rating_list.extend(ratings)
    time_list.extend(times)
    review_list.extend(reviews)
    title_list.extend(titles)

    page = 0

    while len(times) != 0:

        # 翻页、查询
        page += 10

        print(page)
        print(ratings[0])

        req = rs.get("https://www.lowes.com/rnr/r/get-by-product/" + id + "/pdp/prod?offset=" + str(page),headers=header)
        resp = req.text

        # 获取相关信息
        ratings = re.findall(r'"Rating":(.)',resp)
        times = re.findall(r'"SubmissionTime":"(.*?)"',resp)
        reviews = re.findall(r'"ReviewText":(.*?),"',resp)
        titles = re.findall(r'"Title":(.*?),"',resp)

        # 获取相关信息
        rating_list.extend(ratings)
        time_list.extend(times)
        review_list.extend(reviews)
        title_list.extend(titles)
        time.sleep(1)

    id_list = [id]*len(title_list)

    # 处理Title及eview body的格式
    for i in range(len(title_list)):
        # 删去左右引号
        title_list[i] = title_list[i].strip('"')
        review_list[i] = review_list[i].strip('"')

        # 处理部分格式异常的无内容评论
        if title_list[i][:5] == "null}":
            title_list[i] = 'null'

    # 导出
    result_dic = {'ID':id_list,'Review Title':title_list,'Review Body':review_list,'Rating':rating_list,'Time':time_list}
    result_df = pd.DataFrame(result_dic)
    result_df.to_excel(result_add + '\\' + id + ".xlsx")           #修改为目标保存路径
