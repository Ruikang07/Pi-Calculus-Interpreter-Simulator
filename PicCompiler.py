# CISC 465 project
# Modified from Ruslan Spivak's work 
# by Ruikang Luo
# 2021/04/19
from PicException import *
from PicExpressionFilter import findMatchRP, removeOuterParentheses

P_NORMAL, P_REPEAT, P_SUM, P_MIX = (0, 1, 2, 3)
class PicCompiler(BaseException):
    def __init__(self, text):
        self.text = text
        self.count_bound = 0

    def replaceBoundName(self,process,name1,name2):
        process = process.replace('<', ' '+'<'+' ')
        process = process.replace('>', ' '+'>'+' ')
        process = process.replace('.', ' '+'.'+' ')
        process = process.replace('+', ' '+'+'+' ')
        process = process.replace('!', ' '+'!'+' ')
        process = process.replace('|', ' '+'|'+' ')
        process = process.replace('(', ' '+'('+' ')
        process = process.replace(')', ' '+')'+' ')
        process = ' ' + process
        process = process.replace(' '+name1, ' '+name2)
        process = process.replace(" ", "")
        return process
 
 
    # handle BOUND(@) op 
    def boundPreprocess(self,text):
        if text.find('@') == -1:
            return text
        else:
            self.count_bound += 1
            count_bound1 = self.count_bound
            ua = text.rpartition('@') #use the last occurrence of '@'
            u0 = ua[0]
            u1 = ua[1]
            u2 = ua[2]
            if u0[-1] != ')' :
                raise InvalidPiCalculusSyntax
            if u0.rfind('(') == -1:
                raise InvalidPiCalculusSyntax             
            
            va = u0.rpartition('(') #use the last occurrence of '('  
            v0 = va[0]
            v1 = va[1]
            v2 = va[2]            
            v2 = v2[:-1] # extract bounding names
            nameOlds  = [v2]  
            if v2.find(',') != -1:
                nameOlds = v2.split(',')

            if u2[0] == '(':
                i2 = findMatchRP(u2)
                w0 = u2[1:i2]
                w1 = u2[i2+1:]
                w2 = ""
            else:
                if u2.find('|') == -1:
                    w0 = u2
                    w1 = ""
                    w2 = ""
                else:
                    wa = u0.partition('|') #use the first occurrence of '|' 
                    w0 = wa[0]
                    w1 = wa[1]
                    w2 = wa[2]

            for name1 in nameOlds:
                name2 = '_'+str(count_bound1)+'_'+name1
                w0 = self.replaceBoundName(w0,name1,name2)    
            
            u2 = w0+w1+w2 
            u2 = u2.strip()
            expr =  self.boundPreprocess(v0) + u2        
     
            return expr
 


    # handle REPEAT(!) op
    def handleRepeat(self,p_list):    
        p_list1 = []
        p_type_list = []
        for item in p_list:
            c1 = item.count('!')
            if c1 > 1:
                raise InvalidPiCalculusSyntax
            if c1 == 1: 
                i1 = item.index('!')
                if i1 != 0:
                    raise InvalidPiCalculusSyntax
                item =item[1:]  
                p_list1.append(item)
                p_type_list.append(P_REPEAT)
            else:         
                p_list1.append(item)
                p_type_list.append(P_NORMAL)   
        return  p_list1, p_type_list        


    def handleSum(self,p_list1, p_type_list):
        p_list2 = []
        count = -1
        for item in p_list1:
            count += 1
            item = removeOuterParentheses(item)
            boundFlag = False
            
            # handle SUM(+) op
            if item.count('+') > 0:#with '+' op
                p_type_list[count] = p_type_list[count] + P_SUM 
                actionGroupList1 = item.split('+')
                actionGroupList2 = []
                for actionGroup1 in actionGroupList1:
                    actionList1 = actionGroup1.split('.')
                    actionList2 = []
                    # handle WRITE(<) op and READ(>) op
                    for action in actionList1:  
                        c1 = action.count('<')
                        c2 = action.count('>')
                        if (c1 + c2) > 1:
                            raise InvalidPiCalculusSyntax 
                            
                        actionList2.append(action)
                        
                    actionGroupList2.append(actionList2)                               
            else:#no '+' op    
                actionGroup1 = item
                actionList1 = actionGroup1.split('.')
                actionList2 = []
                actionGroupList2 = []
                # handle WRITE(<) op and READ(>) op
                for action in actionList1:  
                    c1 = action.count('<')
                    c2 = action.count('>')
                    if (c1 + c2) > 1:
                        raise InvalidPiCalculusSyntax  
                    actionList2.append(action)
                actionGroupList2.append(actionList2)    
            p_list2.append(actionGroupList2)    
        return  p_list2, p_type_list 
    
    def run(self):   
        text0 = self.text # it is a string 
        text0 = text0.replace(" ","")

        # handle BOUND(@) op
        text1 = self.boundPreprocess(text0)  

        # handle PARALL(|) op  
        p_list = [text1] # it is a list now
        if text1.count('|') > 0:
            p_list = text1.split('|')  

        # handle REPEAT(!) op       
        p_list1, p_type_list = self.handleRepeat(p_list)

        # handle SUM(+) op
        p_list2, p_type_list = self.handleSum(p_list1, p_type_list)
           
        return p_type_list, p_list2


                    
