import openai
from openai import OpenAI
import pandas as pd
import csv
import os
import xlrd
import time
import requests


ArticleResearchlist = []
ArticleTypelist = []
high_entropy_elements_list = []
abstract_processedlist = []
title_processedlist = []
ArticleResearch = []
ArticleType = []
high_entropy_elements = []
abstract_processed = []
title_processed = []
GPToutputlist = []
GPToutput = []
a = 1
counts = 0


def extract_high_entropy_elements(abstract, ti):

    api_key = ""
    base_url = ""

    try:
        client = OpenAI(api_key=api_key,
                        base_url=base_url)
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": f"You are an expert in electrocatalysis literature analysis."},
                {"role": "user",
                 "content": f"Electrocatalyst materials are functional materials that lower energy barriers in electrochemical reactions, accelerate charge transfer, and enhance energy conversion efficiency. They are widely used in fuel cells, water splitting, and CO₂ reduction."},
                {"role": "user",
                 "content": f"The oxygen reduction reaction (ORR) is an electrocatalytic process in which oxygen (O2) is reduced to water (H2O) or hydrogen peroxide (H2O2) through multi-electron transfer at the catalyst surface."},
                {"role": "user",
                 "content": f"Research article (Research): A primary study presenting original experimental or theoretical results, including methods, data, and analysis. Review article (Review): A secondary study that summarizes, analyzes, and discusses existing research progress, without presenting substantial new experimental data."},
                {"role": "user", "content": f" Abstact:{abstract}"},
                {"role": "user", "content": f" title:{ti}"},
                {"role": "user",
                 "content": f"This is an Abstract and title from an article about electrocatalyst, analysis this abstract with title, fill the chart, all section should be fill, if you are uncertain about specify items, fill NULL."},
                {"role": "user",
                 "content": f"Please determine whether the article studies electrocatalyst materials. If yes, reply “Yes”; otherwise, reply “No”."},
                {"role": "user",
                 "content": f"Analyze whether the study focuses on oxygen reduction reaction (ORR). If yes, reply “Yes”; otherwise, reply “No”."},
                {"role": "user",
                 "content": f"If the article studies electrocatalyst materials, determine whether it is a review article or a research article. Reply “Review” or “Research”. If unclear, reply “NULL”."},
                {"role": "user",
                 "content": f"If this abstract from a research article, summarize the abstract and analysis the metal elements that authors choosen as the electrocatalyst materials they investigated, if there were no metal elements mentioned or Empty Input or any information is not provided or you are unsure, reply 'NULL'.To be noted, the elements should be symbolized with English abbreviation only, for example, if the elements are Iron, Cobalt, Nickel, please reply 'Fe, Co, Ni'."},
                {"role": "user", "content": f"""
                Now, output the results in **exactly** the following standardized format with line breaks and nothing else:

                Article research on electrocatalyst materials : [Yes or No]
                Article research on oxygen reduction reaction (ORR) : [Yes or No]
                Article Type: [Research or Review]
                Metal Elements: [Individual elements corresponding to all alloys or NULL]
            

                No extra commentary, markdown or quotation marks. Return only the formatted result.
                """},
                # {"role": "user",
                #  "content": f" Your answer should be standardized with the following chart: \nArticle research on intermetallic compounds or not:\nDetailed Research Field:\nSpecified Research Field:\nArticle Type: Research or Review\nElements: 1, 2, 3, \n. To be noted, if you are unsure, please reply 'NULL', and the elements should be symbolized with English abbreviation only, for example, if the elements are Iron, Cobalt, Nickel, please reply 'Fe, Co, Ni'"},
                {"role": "user",
                 "content": f" Please check your answer, read the abstract and title again and reply again"},
                                ],
            timeout=60.0, 
        )

        return response.choices[0].message.content.strip()
    except:
        return "API请求超时"


datapath = r''
save_dir = r''
os.makedirs(save_dir, exist_ok=True)


for file in os.listdir(datapath):
    file_path = os.path.join(datapath, file)
    print(f"正在处理文件：{file_path}")

    reader = pd.read_excel(file_path, sheet_name=0, header=0, index_col=0)
    title_list = reader['Article Title'].values
    abstract_list = reader['Abstract'].values

    for row in range(len(abstract_list)):
        abstract = abstract_list[row]
        ti = title_list[row]
        counts += 1

        GPToutput = extract_high_entropy_elements(abstract, a)
        a = 1 if a == 3 else a + 1

        while GPToutput == "API请求超时":
            time.sleep(20)
            GPToutput = extract_high_entropy_elements(abstract, a)
            print("API请求超时，等待20秒后再次请求")

        GPToutputlist.append(GPToutput)
        abstract_processedlist.append(abstract)
        title_processedlist.append(ti)

        print(f"标题：{ti}")
        print(f"GPToutput：{GPToutput}")
        print(f"已提取{counts}条文献摘要")
        print("-" * 50)

