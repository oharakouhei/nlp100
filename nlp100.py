
# coding: utf-8

# # 言語処理100本ノック

# ## 00. 文字列の逆順

# In[ ]:

str = "stressed"
print str[::-1]


# ## 01. 「パタトクカシーー」

# In[ ]:

str = u"パタトクカシーー"
print str[::2]


# ## 02. 「パトカー」＋「タクシー」＝「パタトクカシーー」

# In[ ]:

str1 = u"パトカー"
str2 = u"タクシー"
result = "".join([a + b for a, b in zip(str1, str2)])
print result


# In[ ]:



