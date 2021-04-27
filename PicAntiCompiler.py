# CISC 465 project
# produced by Ruikang Luo
# 2021/04/19
P_NORMAL, P_REPEAT, P_SUM, P_MIX = (0, 1, 2, 3)
from copy import deepcopy

def getActionListExp(actionList):
    actionL2 = deepcopy(actionList)
    actionL2.reverse()
    count = 0
    exp = ''
    for action in actionL2:
        action = action.replace(' < ', '<')
        action = action.replace(' > ', '>')
        if count == 0:
            exp = action
        else:
            exp = exp + '.' + action
        count += 1
    if actionL2 == []: 
        exp = '0'  
    return exp  
        
def antiCompiler(p_typeList, processList):
    exp = ""   
    if(processList == []):return exp
    
    len_P = len(processList)
    for i in range(len_P):
        process = processList[i]
        if p_typeList[i] == P_MIX:
            exp1 = '!+('
            for actionList in process:
                exp2 = getActionListExp(actionList)
                exp1 = exp1 + '+' + exp2  
            exp1 = exp1 + ')'  
            exp1 = exp1.replace('+(+', '(')
        elif p_typeList[i] == P_SUM:
            exp1 = '+('
            for actionList in process:
                exp2 = getActionListExp(actionList)
                exp1 = exp1 + '+' + exp2
            exp1 = exp1 + ')' 
            exp1 = exp1.replace('+(+', '(')
        elif p_typeList[i] == P_REPEAT:
            actionList = process[0]
            exp1 = '!(' + getActionListExp(actionList) +')'               
        elif p_typeList[i] == P_NORMAL:
            actionList = process[0]
            exp1 = getActionListExp(actionList) 
        if( i == 0 ):
            exp = exp1
        else:
            exp = exp + '|' + exp1      
    return exp 
