import random
secret=random.randint(0,10)
print("start-----")
gucess=input("输入数字猜想 :")
temp=int(gucess)
while temp !=secret:
    gucess=input("错了，请重新输入")
    temp=int(gucess)
    if(temp==secret):
        print("你是对的")
    else:
        if temp > secret:
            print("大了")
        else:
            print("小了")
print("默认打印")
