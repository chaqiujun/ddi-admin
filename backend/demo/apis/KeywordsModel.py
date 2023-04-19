import jieba
from textrank4ch.TextRank4Keyword import TextRank4Keywords
# 此條代碼解決警告Building prefix dict from the default dictionary ...Loading model from....解决方案
jieba.setLogLevel(jieba.logging.INFO)
def keywordsModel(text):
	# 准备预料, 输入时一个字符长串, 可含特殊字符
	corpus = text
	# 对输入进行分析、得到全量的关键词相关信息, 如权重(PR)、词性
	t4kw = TextRank4Keywords()
	t4kw.analyze(text=corpus)
	result=",".join(str(item[0]) for item in t4kw.get_key_words(5))
	return result
	# 再基于上述analyze的结果进行按需提取需要的关键字

import spacy
def kw():
	nlp = spacy.load('zh_core_web_sm')
	doc = nlp("原来的TextRank4ZH都近5年莫得更新了！个人感觉这个包还不错，当前项目里也在使用，只不过这个包有不少体验不好的地方,比如：1.句子分词会直接删除x类型，但是自定义词库不少人是只填了个词的，这个情况下词性为x,最终textrank4zh就把这个词删了。2.还有一些比如内部计算pagerank(默认最大迭代次数为100)时候会偶尔发生不收敛的情况, 这个异常也是没有捕捉处理的。既然没更新了，我就想着参考（chao xi）着开发优化更新一下咯，毕竟自己工作中也在用。 (竟然连名字都差不多, 希望那个大佬知道了不要打我)")
	word_freq = {}
	for token in doc:
		if token.is_stop or token.is_punct:
			continue
		if token.text not in word_freq:
			word_freq[token.text] = 1
		else:
			word_freq[token.text] += 1

	for word, freq in word_freq.items():
		print(word, freq)



if __name__ == '__main__':
    kw()
#    print(keywordsModel('如何以逗号为分隔符输出数组如何以逗号为分隔符输出数组如何以逗号为分隔符输出数组如何以逗号为分隔符输出数组如何以逗号为分隔符输出数组'))