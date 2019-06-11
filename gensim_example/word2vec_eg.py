import gensim
path=r'F:\陶士来文件\downloads\news_12g_baidubaike_20g_novel_90g_embedding_64.model'
model = gensim.models.Word2Vec.load(path)
