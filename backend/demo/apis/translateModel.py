# # -*- coding: utf-8 -*-
# # NLPIR机器翻译
# import re
# import requests

# # 分句函数
# def split_sentences(text):
#     # 使用句号分段
#     # pattern = r'\. '
#     # 使用正则表达式来分句
#     pattern = r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s'
#     sentences = re.split(pattern, text)
#     return sentences

# # 翻译函数
# def translate_text(text):
#     url = "http://mt.9paper.com//as_client"
#     para_data = {'src_text': text, 'id_index': '3'}
#     try:
#         r = requests.post(url, data=para_data,timeout=3000)
#         print('本次翻译消耗时间:',r.elapsed)
#         res_json = r.json()
#         if 'result' in res_json:
#             return "".join(res_json['result'])
#         else:
#             print('翻译API返回的响应不是JSON格式或不包含"result"字段:', res_json)
#             return ''
#     except Exception as e:
#         print('翻译API请求失败:', e)
#         return ''

# # 分句翻译函数
# def translate_article(article):
#     # 分句
#     sentences = split_sentences(article)
#     # 翻译每个句子
#     translated_sentences = []
#     for sentence in sentences:
#         translated = translate_text(sentence)
#         translated_sentences.append(translated)
#     # 合并翻译后的句子
#     translated_article = ' '.join(translated_sentences)
#     return translated_article

# # 示例
# english_article = "This is the first sentence. This is the second sentence. This is the third sentence."
# chinese_article = translate_article(english_article)
# print(chinese_article)
