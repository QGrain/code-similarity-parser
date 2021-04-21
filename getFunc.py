import os
import sys


def checkStart(string, start_list):
    for i, s in enumerate(start_list):
        l = len(s)
        if string[:l] == s:
            return i
    return -1


def trim(string):
    '''
    输入：参数名：string。类型：str。含义：所解析源代码的一行字符串
    返回：返回去掉string尾部换行符和首尾空格符的字符串，以及去掉while，if或者for等条件控制关键字的开头
    '''
    start_list = ["while", "if", "for", "else if", "switch", "(", "=", "+", "-", " "]

    if len(string) <= 1:
        return string
    while string[-1] == "\n":
        string = string[:-1]
    string = string.strip()

    while checkStart(string, start_list) != -1:
        i = checkStart(string, start_list)
        string = string[len(start_list[i]):]
    return string


def print_line(d):
    '''
    输入：参数名：d。类型：dict。含义：记录了所有function call的字典
    功能：逐行打印字典中所有的函数调用、所出现的行数以及总次数
    '''
    print("\nIn source file %s, there are %d functions:"%(d["fname"], len(d)-1))
    for l in d:
        if l == "fname":
            continue
        print("%s() \t\t\t appears at line" %l, d[l], "for %d times."%len(d[l]))


def extracFuncName(func_str):
    '''
    输入：参数名：func_str。类型：str。含义：包含函数名的字符串
    返回：解析后的函数名，字符串
    '''
    return func_str.split('(')[0].split(' ')[-1]
    

def getFunc(fname):
    '''
    输入：参数名：fname。类型：str。含义：目标源代码文件的路径
    返回：(func_calls, func_defs) 两个字典分别记录了该源码中的函数调用和函数定义
    '''
    func_defs = dict()
    func_calls = dict()
    func_calls["fname"] = fname.split("/")[-1]
    func_defs["fname"] = fname.split("/")[-1]
    fp = open(fname, "r")
    lines = list()
    line = fp.readline()
    while line:
        line = trim(line)
        lines.append(line)
        line = fp.readline()

    len_lines = len(lines)
    # 尽量剔除常见的函数调用或者C关键字
    keywords_list = ["while(", "if(", "for(", "do(", "switch(", "malloc(", " free(", " open(", " close(", " return(", "printf",  
                    "putc", "fputs", "fflush", "exit(", "error(", "atoi", "read(", "write(", "fgets", "*(", "memset(", "memcpy(",  
                    "strtol", "strdup", "strlen", "strncpy", "strcpy", "strncmp", "strftime", "dirname", "fcntl(", "fclose(", 
                    "sizeof("]
    for i in range(1, len_lines):
        go_next = 0
        if '(' in lines[i-1]:
            for k in keywords_list:
                if k in lines[i-1]:
                    go_next = 1
            if go_next == 1:
                continue
            func_name = extracFuncName(lines[i-1])
            if ';' in lines[i-1]:
                if func_name != '':
                    if func_name not in func_calls:
                        func_calls[func_name] = [i]
                    else:
                        func_calls[func_name].append(i)
            elif '{' in lines[i]:
                if func_name != '':
                    if func_name not in func_defs:
                        func_defs[func_name] = [i]
                    else:
                        func_defs[func_name].append(i)
            else:
                if func_name != '':
                    if func_name not in func_calls:
                        func_calls[func_name] = [i]
                    else:
                        func_calls[func_name].append(i)

    return (func_calls, func_defs)


def getOutCalls(calls_1, defs_1):
    '''
    输入：参数名：calls_1, defs_1。类型：dict。含义：分别是源码文件1中的函数调用和函数定义
    返回：out_calls字典，记录了源文件1中从外部库所调用的函数
    '''
    out_calls = dict()
    out_calls["fname"] = calls_1["fname"]
    for c in calls_1:
        if c not in defs_1:
            out_calls[c] = calls_1[c]
    return out_calls

def getInCalls(calls_1, defs_2):
    '''
    输入：参数名：calls_1, defs_2。类型：dict。含义：源码文件1中的(从外部的)函数调用和源码文件2中的函数定义
    返回：in_calls字典，记录了源文件1中从源文件2中所调用的函数
    '''
    in_calls = dict()
    in_calls["fname"] = calls_1["fname"]
    for c in calls_1:
        if c in defs_2:
            in_calls[c] = calls_1[c]
    return in_calls


def getComCalls(calls_1, calls_2):
    '''
    输入：参数名：calls_1, calls_2。类型：dict。含义：源码文件1和源码文件2中的函数调用
    返回：com_calls字典，源文件1和源文件2的共同调用的函数
    '''
    com_calls = dict()
    com_calls["fname"] = calls_1["fname"]
    for c in calls_1:
        if c in calls_2:
            com_calls[c] = calls_1[c]
    return com_calls

if __name__ == "__main__":
    if len(sys.argv) == 2:
        fname = sys.argv[1]
    else:
        print("Usage: python getFunc.py SourceFileName")
        fname = "../tcpdump-4.9.2/tcpdump.c"
    (func_calls, func_defs) = getFunc(fname)
    out_calls = getOutCalls(func_calls, func_defs)
    print("\nHere is the func calls")
    print_line(func_calls)
    print("\nHere is the func defs")
    print_line(func_defs)
    print("\nHere is the out calls")
    print_line(out_calls)
