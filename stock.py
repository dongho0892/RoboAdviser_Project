
# coding: utf-8

# In[3]:


def cal_upper(price):
    increment = price * 0.3
    upper_price = price + increment
    return upper_price

def cal_lower(price):
    decrement = price * 0.3
    lower_price = price - decrement
    return lower_price

author = "pystock"

def run():
    print(cal_upper(10000))
    print(cal_lower(10000))
    print(__name__)


if __name__ = "__main__":
    run()


# import 하면 조용히 import 하게끔 설정도 가능함.

# 바로 실행하면   .py를 바로 실행할 경우