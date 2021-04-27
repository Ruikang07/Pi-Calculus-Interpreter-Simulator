# CISC 465 project
# produced by Ruikang Luo
# 2021/04/19
from PicAntiCompiler import *
import random
from copy import deepcopy
from PicCompiler import P_NORMAL, P_REPEAT, P_SUM, P_MIX 
CH_REQ = 'waiting ch'
 

class PicRuntime():   
    def __init__(self, p_name_list, p_typeList, processList):
        self.process_list = deepcopy(processList)
        self.p_type_list = deepcopy(p_typeList)
        self.p_name_list = deepcopy(p_name_list)
        self.process = [] 
        self.p_type = None
        self.ch_req_list = []                      
        self.match_msg_list = []
        self.MU2_r_msg = ''
        self.MU1_r_msg = ''  
            
        for self.process in self.process_list:
            self.match_msg_list.append([])
            for actionGroup in self.process:
                actionGroup.reverse()             
                
                
    def run(self): 
        output = []
        expr_last = ''
        stopCount1 = 0
        while not self.checkEmptyProcess():
            if stopCount1 > 2:
                exp1 = output.pop()         
                if exp1 == '': exp1 = output.pop()
                exp2 = output.pop()
                if exp2 == '': exp2 = output.pop()         
                while exp1 == exp2 and output != []:
                    exp2 = output.pop()
                    if exp2 == '': exp2 = output.pop()
                    
                output.append(exp2)
                output.append(exp1)  
                output.append('END')
                return self.MU1_r_msg, self.MU2_r_msg, output
            
            len_P = len(self.process_list) # number of parraell processes
            pIndex = [i for i in range(len_P)]

            #randomly change the running order of processes to simulate concurrent environment
            random.shuffle(pIndex) 
        
            for i1 in range(len_P):
                i2 = pIndex[i1] #i2 is used as user_id/process_id              
                p_type = self.p_type_list[i2]  
                if p_type == P_NORMAL:                
                    self.normalProcessHandler(i2)
                elif p_type == P_REPEAT:
                    self.repeatProcessHandler(i2)   
                elif p_type == P_SUM:
                    self.sumProcessHandler(i2)  
                elif p_type == P_MIX:
                    self.mixProcessHandler(i2) 
            
            expr_new = antiCompiler(self.p_type_list, self.process_list)

            if expr_new == expr_last:
                stopCount1 += 1 
            else:
                if stopCount1 > 0: stopCount1 -= 1 
    
            expr_last = expr_new 
            output.append(expr_new)
                  
            ch_match = self.msgProcessing()
            output.append(ch_match)
            
        output.append('END') 
        return  self.MU1_r_msg, self.MU2_r_msg, output
                         
    def normalProcessHandler(self,i2):  
        process = self.process_list[i2]
        match_msg_1 = self.match_msg_list[i2]
        if process[0] == []:#check empty process
            return      
        if match_msg_1 == []:
            actionList = deepcopy(process[0])
            if len(actionList)>0:
                action = actionList.pop()
                actionList.append(action)
                ch_req = []
                ch_req.append(i2) 
                ch_req.append(deepcopy(action))            
                self.ch_req_list.append(ch_req)   
                match_msg_1 = ['waiting ch']  
        else:
            if match_msg_1[0] != 'waiting ch':
                actionList = deepcopy(process[0])
                action = actionList.pop()
                action0 = match_msg_1[0]
                action1 = match_msg_1[1]
                if action != action0:
                    print("\n\nsomething wrong in self.match_msg_list")
                    return
                if action.find('>') != -1:#read from channel
                    if actionList != []:
                        ch_r, name_r = action.split('>')
                        ch_s, name_s = action1.split('<')
                        len_a = len(actionList)
                        for ka in range(len_a):
                            str1 = actionList[ka].replace(name_r, name_s)
                            actionList[ka] = str1          
                match_msg_1 = []
                process[0] = actionList   
                self.process_list[i2] = process
        self.match_msg_list[i2] = match_msg_1         
        return             


    def repeatProcessHandler(self,i2):
        process = self.process_list[i2]
        match_msg_1 = self.match_msg_list[i2]
        if match_msg_1 == []: 
            actionList = process[0]
            action = actionList.pop()
            actionList.append(action)
            ch_req = []
            ch_req.append(i2) 
            ch_req.append(deepcopy(action))            
            self.ch_req_list.append(ch_req)   
            match_msg_1 = ['waiting ch']           
        elif match_msg_1[0] != 'waiting ch':
            process2 = deepcopy(process)
            self.p_type_list[i2] = P_NORMAL            
            self.process_list.append(process2)
            self.p_type_list.append(P_REPEAT)
            self.p_name_list.append(self.p_name_list[i2])
            self.p_name_list[i2] = self.p_name_list[i2].replace("!","")
            self.match_msg_list.append([])
        self.match_msg_list[i2] = match_msg_1    
        return  
        

    def sumProcessHandler(self,i2):  
        process = deepcopy(self.process_list[i2])
        match_msg_1 = self.match_msg_list[i2]
        if match_msg_1 == []:
            ch_req = []
            ch_req.append(i2)  
            for actionList in process:    
                action = actionList.pop()
                actionList.append(action) 
                ch_req.append(deepcopy(action))                 
            self.ch_req_list.append(ch_req)   
            match_msg_1 = ['waiting ch']            
        elif match_msg_1[0] != 'waiting ch': 
            action0 = match_msg_1[0]  
            for actionList in process:
                action =  actionList.pop()
                actionList.append(action) 
                if(action == action0):
                    process = [deepcopy(actionList)] 
                    self.process_list[i2] = process
                    self.p_type_list[i2] = P_NORMAL
                 
        self.match_msg_list[i2] = match_msg_1          
        return  
        
        
    def mixProcessHandler(self,i2):    
        process = self.process_list[i2]
        match_msg_1 = self.match_msg_list[i2]
        if match_msg_1 == []: 
            ch_req = []
            ch_req.append(i2)  
            for actionList in process:    
                action = actionList.pop()
                actionList.append(action) 
                ch_req.append(deepcopy(action))                 
            self.ch_req_list.append(ch_req)   
            match_msg_1 = ['waiting ch']          
        elif match_msg_1[0] != 'waiting ch':
            process2 = deepcopy(process) 
            action0 = match_msg_1[0]             
            for actionList in process:
                action =  actionList.pop()
                actionList.append(action) 
                if(action == action0):
                    process = [deepcopy(actionList)] 
                    self.process_list[i2] = process
                    self.p_type_list[i2] = P_NORMAL

            self.process_list.append(process2)
            self.p_type_list.append(P_MIX)
            self.p_name_list.append(self.p_name_list[i2])
            self.p_name_list[i2] = self.p_name_list[i2].replace("!","")
            self.match_msg_list.append([])
        self.match_msg_list[i2] = match_msg_1          
        return  
        

 
    def checkEmptyProcess(self): 
        emptyFlag = True
        for process in self.process_list:
            if process[0] != []:
                emptyFlag = False
        return  emptyFlag

    def getActionListExp(self, actionList):
        actionL2 = deepcopy(actionList)
        actionL2.reverse()
        count = 0
        exp = ''
        for action in actionL2:
            if count == 0:
                exp = action
            else:
                exp = exp + '.' + action
            count += 1
        if actionL2 == []: 
            exp = '0'  
        return exp    
    

    def msgProcessing(self):   
        ch_req_list1 = deepcopy(self.ch_req_list)
        ch_match = ''
        if( len(ch_req_list1 ) < 2 ):
            return ch_match
        ch_req_list1.reverse()   
        no_match_list1 = []   
        len_1 = len(ch_req_list1)
        if len_1 < 2: 
            return
        for i in range(len_1):#loop for ch_req_list1 to find matching 
            match_flag = False
            ch_req1 = ch_req_list1[i]  
            if ch_req1 == []:continue
            p_id1 = ch_req1[0]        
            actionList1 = ch_req1[1:]
            for action1 in actionList1:#loop for the actions in ch_req1
                a1_tmp = action1.replace('<', ' < ')
                a1_tmp = a1_tmp.replace('>', ' > ')
                ch1, rw1, name1 = a1_tmp.split(' ')
                for j in range(len_1):#loop for ch_req_list1 to find matching 
                    if i == j: continue
                    ch_req2 = ch_req_list1[j]
                    if ch_req2 == []:continue
                    p_id2 = ch_req2[0]  
                    actionList2 = ch_req2[1:]
                    for action2 in actionList2:#loop for the actions in ch_req2
                        a2_tmp = action2.replace('<', ' < ')
                        a2_tmp = a2_tmp.replace('>', ' > ')
                        ch2, rw2, name2 = a2_tmp.split(' ')
                        if ch1 == ch2 and rw1 != rw2:
                            match_flag = True
                            self.match_msg_list[p_id1] = [ch1+rw1+name1,ch2+rw2+name2]
                            self.match_msg_list[p_id2] = [ch2+rw2+name2,ch1+rw1+name1]
                            if( name1 == 'msgMU1'):
                                self.MU1_r_msg = name2
                            if( name2 == 'msgMU1'):
                                self.MU1_r_msg = name1  
                                
                            if( name1 == 'msgMU2'):
                                self.MU2_r_msg = name2
                            if( name2 == 'msgMU2'):
                                self.MU2_r_msg = name1   
                                
                            if p_id1 < p_id2:
                                ch_match = ch_match+'ch_matched for P_ids:'+str(p_id1)+'<-->'+str(p_id2)+',     '
                                ch_match = ch_match+ch1+rw1+name1+"<--->"+ch2+rw2+name2+"\n"
                            else:
                                ch_match = ch_match+'ch_matched for P_ids:'+str(p_id2)+'<-->'+str(p_id1)+',     '
                                ch_match = ch_match+ch2+rw2+name2+"<--->"+ch1+rw1+name1+"\n"                                    

                            ch_req_list1[i] = []
                            ch_req_list1[j] = []
                            ch1 = ""
                            rw1 = ""
                            name1 = ""
                            break               
                if match_flag == True:  
                    break                
        ch_req_list2 = []                    
        for ch_req in ch_req_list1: 
            if ch_req != []: 
                ch_req_list2.append(ch_req)

        self.ch_req_list = ch_req_list2
        return ch_match
        
