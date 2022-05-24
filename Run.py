import sys
import os
# from src import filter
# import filter
from src import filter, parsing, graph, fitting
import warnings


'''찾고 싶은 파일의 Lot_id를 입력하세요.'''
Lot_id = ['HY202103']

'''찾고 싶은 파일의 Wafer_id를 입력하세요.'''
Wafer_id = ['D08']

'''찾고 싶은 파일의 행렬을 입력하세요. ex) [0,0]'''
xy_coord = ['(0,0)']

'''찾고 싶은 파일의 maskset을 입력하세요.'''
Mask_set = ['LION1']

'''찾고 싶은 파일의 devive_name을 입력하세요.'''
device_name =[]

'''그래프를 저장하고 싶다면 True, 저장하고 싶지 않다면 False를 입력하세요.'''
Opt_savefig = True

'''그래프를 보고 싶다면 True, 보고 싶지 않다면 False를 입력하세요.'''
Opt_showfig = False


filter.cmp(Lot_id,Wafer_id,xy_coord,Mask_set,device_name)
# print(str(filter.dlst[0]))
for i in range(len(filter.dlst)):
    warnings.filterwarnings('ignore')
    a = parsing.v(filter.dlst[i])
    b = parsing.i(filter.dlst[i])
    c = parsing.wvl(filter.dlst[i])
    d = parsing.itst(filter.dlst[i])
    e = parsing.lgds(filter.dlst[i])
    # s = str(filter.dlst[i])
    f = graph.figname(str(filter.dlst[i]))
    graph.grph(a,b,c,d,e,Opt_showfig,Opt_savefig,f)

print('제시하신 파일을 모두 찾았습니다. 이용해 주셔서 감사합니다.')
# print(a.pas())
# print(parsing.i)
# print(graph.v(filter.dlst))
# print(c)
# print(parsing.ps(c))
# (parsing.ps(c))[1]

