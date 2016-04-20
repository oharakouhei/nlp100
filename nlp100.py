
# coding: utf-8

# # 言語処理100本ノック

# ## No.1

# In[ ]:

str = "stressed"
print str[::-1]


# ## No.2

# In[ ]:

str = u"パタトクカシーー"
print str[::2]


# ## No.3

# In[ ]:

str1 = u"パトカー"
str2 = u"タクシー"
result = "".join([a + b for a, b in zip(str1, str2)])
print result


# In[ ]:



