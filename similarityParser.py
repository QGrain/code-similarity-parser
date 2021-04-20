import os
import sys
from getFunc import getFunc, getOutCalls, getInCalls, getComCalls, print_line

def parseHeaders(fname):
    '''
    输入：参数名：fname。类型：str。含义：待解析源文件的路径
    返回：header_list，记录了该源文件中include的所有头文件
    '''
    fp = open(fname, "r")
    lines = fp.readlines()
    header_list = list()
    for i, line in enumerate(lines):
        if "#include " in line:
            # print("line", i+1, line)
            hname = line.split(" ")[1][1:-2]
            if hname not in header_list:
                header_list.append(hname)
    # print(header_list)
    return header_list

def statHeaders(fname_list):
    '''
    输入：参数名：fname_list。类型：list[str]。含义：多个待解析源文件的路径列表
    功能：统计并打印列表源文件的include头文件的相似点
    '''
    fname_list_len = len(fname_list)
    headers_list = list()
    headers_cnt = dict()
    headers_2_source = dict()

    # 尽量过滤掉常见的头文件
    pass_list = ["config.h", "defines.h", "common.h", "fcntl.h", "sys/types.h", "unistd.h", 
                "sys/stat.h", "stdio.h", "string.h", "errno.h", "ctype.h", "stdlib.h"]
    for fname in fname_list:
        headers = parseHeaders(fname)
        source_name = fname.split("/")[-1]
        for hname in headers:
            if hname in pass_list:
                continue
            if hname in headers_2_source:
                headers_2_source[hname].append(source_name)
            else:
                headers_2_source[hname] = [source_name]
            if hname in headers_cnt:
                headers_cnt[hname] += 1
            else:
                headers_cnt[hname] = 1
        headers_list.append(headers)
    for hname in headers_cnt:
        if headers_cnt[hname] > 1:
            print("%s has appeared %d times in these %d source files" %(hname, headers_cnt[hname], fname_list_len), headers_2_source[hname])
    # print(headers_list)


def parseSimilarity(P1, P2, L):
    '''
    输入：参数名：P1, P2, L。类型：str。含义：程序1，程序2和Library的源码路径
    功能：解析头文件的相似性，解析函数调用的共同性
    '''
    statHeaders([P1, P2, L])

    (calls_1, defs_1) = getFunc(P1)
    out_calls_1 = getOutCalls(calls_1, defs_1)
    (calls_2, defs_2) = getFunc(P2)
    out_calls_2 = getOutCalls(calls_2, defs_2)
    (calls_L, defs_L) = getFunc(L)

    P1_name = P1.split("/")[-1]
    P2_name = P2.split("/")[-1]
    L_name = L.split("/")[-1]

    print("\n\n============%s calls the following funcs from %s==========="%(P1_name, L_name))
    in_calls_1 = getInCalls(out_calls_1, defs_L)
    print_line(in_calls_1)

    print("\n\n============%s calls the following funcs from %s==========="%(P2_name, L_name))
    in_calls_2 = getInCalls(out_calls_2, defs_L)
    print_line(in_calls_2)

    print("\n\n============Similarity between %s and %s==========="%(P1_name, P2_name))
    com_calls_1_2 = getComCalls(out_calls_1, out_calls_2)
    print_line(com_calls_1_2)



if __name__ == "__main__":
    if len(sys.argv) == 4:
        P1 = sys.argv[1]
        P2 = sys.argv[2]
        L = sys.argv[3]
    else:
        P1 = "../tcpdump-4.9.2/tcpdump.c"
        P2 = "../tcpreplay-4.3.1/src/tcpreplay.c"
        L = "../libpcap-1.8.1/pcap.c"
    parseSimilarity(P1, P2, L)