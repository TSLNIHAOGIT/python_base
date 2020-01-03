from keras_bert import extract_embeddings
from keras.layers import *
from keras.models import Model
import keras.backend as K
from keras.optimizers import Adam
from keras_bert import load_trained_model_from_checkpoint, Tokenizer,get_model

bert_model = load_trained_model_from_checkpoint(config_path, checkpoint_path, seq_len=None)
for l in bert_model.layers:
    l.trainable = True

x1_in = Input(shape=(None,))
x2_in = Input(shape=(None,))

x = bert_model([x1_in, x2_in])

# Tokenization
from keras_bert import Tokenizer

tokenizer = Tokenizer(token_dict)
# text = '语言模型 chinese is great'
# text='商品名称及规格型号'
# text='境外收货人\nDERCOCHILEREPUESTOSS.A.'
# text='合同协议号\n2019CICSA473-A'
text='运抵国(地区）\n智利'
tokens = tokenizer.tokenize(text)
# ['[CLS]', '语', '言', '模', '型', '[SEP]']
print('tokens',tokens)
indices, segments = tokenizer.encode(first=text, max_len=512)
print(indices[:10])