#-*-coding:utf-8 -*-
__author__ = 'luohua139'
from py2neo import Node,Relationship
st = "学历"
n1 = Node("person",name="luohua",age=12,st="小学",id=1)
n2 = Node("person",name="haha",age=44,st="大学",id=2)
print(type(n1["st"]))
r = Relationship(n1,n2,rela = "朋友",)
n1.xstr()
print(n1)
print(n2)
print(r)