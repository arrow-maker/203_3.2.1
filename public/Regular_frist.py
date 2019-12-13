import re
def regular_findall(text1,left,right):      #取用text中的有前后的字符串列表
    a = re.findall(left + "(.+?)" + right, text1)    #这里的flags=re.IGNORECASE是忽略大小写的格式
    return a
def regular_findditer(text1,left,right):    #取用text中的有前后的字符串迭代展示
    aa =re.finditer(left + "(.+?)" + right, text1)
    return aa