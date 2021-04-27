# CISC 465 project
# produced by Ruikang Luo
# 2021/04/19

from PicException import *
from copy import deepcopy
import os
import sys



def findMatchRP(str1):
    if str1[0] != '(': 
        return -1
    str2 = str1
    i2 = str2.find(')')
    if i2 == -1:
        raise InvalidPiCalculusSyntax
    while True:   
        str2 = str2[0:i2]
        i1 = str2.rfind('(')
        if i1 == 0: 
            return i2
        i1 = str2.rfind('(')
        str2 = list(str1)
        str2[i1] = '0'
        str2[i2] = '0'
        str2 = ''.join(str2)
        i2 = str2.find(')')
        if i2 == -1:
            raise InvalidPiCalculusSyntax

def removeOuterParentheses(str1):
    if len(str1) == 0: 
        return str1
    if str1[0] != '(': 
        return str1
    str1 = str1.strip()
    if(str1[0] == '('):
        left = 0
        i = 0
        balance = 0
        for c in str1:
            if c == '(':
                if( balance ==  0):
                    left = i
                balance += 1
            if c == ')':
                balance -= 1
                
            i += 1
        if balance == 0 and left == 0 and str1[-1] == ')':
            str1 = str1[:-1]
            str1 = str1[1:]
                   
    return str1

def computePicExpr(text):
    pic_global_name_list = []
    p_name_list = []
    for line in text:
        if '::=' in line:
            name, value = line.split('::=')
            value2 = value
            name = name.strip()
            value = value.strip()
            if name == 'picExpr': 
                p_name_list = value2.split('|')
                pic_expr = ''
                len1 = len(p_name_list )
                for i in range(len1):
                    name1 = p_name_list[i]
                    name2 = removeOuterParentheses(name1)
                    p_name_list[i] = name2  
                    x1 = ""
                    x2a = ""
                    x2b = ""
                    x2 = name2
                    if name2.find('@') != -1:
                        va = name2.rpartition('@') #use the last occurrence of '@'
                        x1 = va[0]+va[1]       
                        x2 = va[2]  
                        if x2[0] == '(' and x2[-1] != ')':
                            x2a = x2[0]
                            x2 = x2[1:]
                        if x2[0] == '(' and x2[-1] == ')':
                            x2a = x2[0]
                            x2b = x2[-1]
                            x2 = x2[1:]
                            x2 = x2[:-1]
                    else:
                        if name2[-1] == ')':
                            x2b = x2[-1]
                            x2 = x2[0:-1]
                    
                    if x2[0] == '!':   
                        x2a = x2a+'!'
                        x2 = x2 = x2[1:]
                        
                    p_name_list[i] = x2   
                    
                    x2 = x2.replace('!','"!"+') 
                    
                    if x2[0] == '(' and x2.find(')') == -1:
                        raise InvalidPiCalculusSyntax
                        x2 = x2.replace('(','"("+')
                    if x2[-1] == ')' and x2.find('(') == -1:
                        raise InvalidPiCalculusSyntax
                        x2 = x2.replace('(','+")"')    
                    value2 = x1+x2a+eval(x2)+x2b
                    
                    if i>0:
                        pic_expr = pic_expr + '|' +value2
                    else:
                        pic_expr = pic_expr + value2      
                globals()[name] = pic_expr  
                break  
            globals()[name] = eval(value)
            pic_global_name_list.append(name)     
        elif ':=' in line:     
            name, value = line.split(':=')
            name = name.strip()
            value = value.strip()
            globals()[name] = value 
            pic_global_name_list.append(name)
    for item in pic_global_name_list:
        if item != 'picExpr':
            del globals()[item]    
    if name != 'picExpr':
        return  'InvalidPiCalculusSyntax', p_name_list  
        
    return picExpr, p_name_list


def createSimulatorExpr(msg, picExprFile):
    expr4show = ''
    p_name_list = []
    cur_path=os.getcwd()
    file1 = open(picExprFile,"r")
    lines = []
    line = 'msgMU1:= '+msg+'\n'
    lines.append(line)
    while True:
        line = file1.readline()
        if not line:
            file1.close()
            break  
        lines.append(line)    
    try:    
        picExpr, p_name_list = computePicExpr(lines)
    except NameError:
        raise InvalidPiCalculusSyntax
        return  'InvalidPiCalculusSyntax', p_name_list, expr4show 
    expr4show = ''
    for line in lines:
        expr4show = expr4show + line 
    return picExpr, p_name_list, expr4show