# CISC 465 project
# produced by Ruikang Luo
# 2021/04/19

from PicCompiler import PicCompiler
from PicRuntime import PicRuntime
from PicException import *
from PicExpressionFilter import *
from PicGenAST import picGenAST
from copy import deepcopy
from tkinter import * 
import tkinter as tk
from tkinter import scrolledtext 
from tkinter import filedialog as fd
import threading
import random
import time


def main():
    win = tk.Tk() 
    win.title('Pi Calculus Interpreter')
    win.geometry("800x400") 
    
        
    def openInputExpFile():   
        types = (
            ('pic files', '*.txt'),
            ('All files', '*.*')
        )
        file1 = fd.askopenfile(initialdir = './examples4Interpreter',filetypes = types)
            
        inputExp = ''
        inputWin.delete(1.0,"end")
        inputWin.insert(1.0, inputExp)
        
        lines = file1.readlines()
        for line in lines:
            inputWin.insert(END, line)
        
    def handdlePicError(msg):
        outputExp = msg
        outputWin.configure(state='normal')
        outputWin.delete(1.0,"end")
        outputWin.insert(1.0, outputExp)      
        outputWin.configure(state='disabled')
        return       
    
    
    def runInputExp():
        clearOutputWin()
        text=inputWin.get("1.0","end")
        lines = text.splitlines() 
        
        try:    
            picExpr, p_name_list = computePicExpr(lines)
            picCompiler = PicCompiler(picExpr)
            p_type_list, processList  = picCompiler.run()
            picRuntime1 = PicRuntime(p_name_list, p_type_list, processList)
            man_r_msg, car_r_msg, output = picRuntime1.run()  
            p_type_list = deepcopy(picRuntime1.p_type_list)
            p_name_list = deepcopy(picRuntime1.p_name_list)
        except NameError:
            msg = "Invalid Pi Calculus Syntax"
            handdlePicError(msg)
            return
        except InvalidPiCalculusSyntax:
            msg = "Invalid Pi Calculus Syntax"
            handdlePicError(msg)
            return    
         

        updateOutputWin(output, p_name_list)
        
        return
   
    def initInputWin():
        inputWin.delete("1.0",END)
        file1 = open("./examples4Interpreter/example1.txt","r")
        lines = file1.readlines()
        for line in lines:
            inputWin.insert(END, line)        
        
    def clearInputWin():
        inputWin.delete("1.0","end")
 

    def clearOutputWin():
        outputWin.configure(state='normal')
        outputWin.delete("1.0","end")
        outputWin.configure(state='disabled') 
        
    def updateOutputWin1(text):
        outputWin.configure(state='normal')
        outputWin.delete(1.0,"end")
        outputWin.insert(1.0, text)
        outputWin.configure(state='disabled')        
        
    def genAST():
        text=inputWin.get("1.0","end")
        lines = text.splitlines() 
        try:    
            picExpr, p_name_list = computePicExpr(lines)
        except NameError:
            msg = "Invalid Pi Calculus Syntax"
            handdlePicError(msg)
            return
        except InvalidPiCalculusSyntax:
            msg = "Invalid Pi Calculus Syntax"
            handdlePicError(msg)
            return  
    
        picGenAST(picExpr)
        outStr = 'AST was written into picAST.dot\n'
        outStr = outStr + 'Use Graphviz utility as following to create png file\n'
        outStr = outStr + '>dot -Tpng -o picAST.png picAST.dot\n'
        outStr = outStr + 'You need install Graphviz package before using it'
        outputWin.configure(state='normal')
        outputWin.delete(1.0,"end")
        outputWin.insert(1.0, outStr)      
        outputWin.configure(state='disabled')         
        return 
    ######################################################################################   
    def updateOutputWin(output, p_name_list):
        #print("updateOutputWin(output, p_name_list):\np_name_list = ", p_name_list)
        clearOutputWin()
        line_new = ''
        line_old = ''
        result = ''
        for line in output:
            if not line: continue
            if line == 'END': break
            line_new = "picExpr:= " + line
            num_match = line.count('ch_matched for P_ids:')
            if num_match == 1:
                text_output = line_old+'\n\n'+ line
                result = result + text_output           
                ch_matched_list = line.split('ch_matched for P_ids:')
                ch_matched_list = ch_matched_list[1:]
                ch_matched = ch_matched_list[0]
                ch_matched = ch_matched.strip()     
                item1, item2 = ch_matched.split(',')
                item1 = item1.strip()
                item2 = item2.strip()
                pid_1, pid_2 = item1.split('<-->')  
                pid_1 = int(pid_1)
                pid_2 = int(pid_2)
                action1, action2 = item2.split('<--->')
                if '>' in action1:
                    sender1 = p_name_list[pid_2]
                    receiver1 = p_name_list[pid_1]
                else: 
                    sender1 = p_name_list[pid_1]
                    receiver1 = p_name_list[pid_2]
                sender1 = sender1.strip() 
                receiver1 = receiver1.strip() 
            elif num_match > 1:
                text_output = line_old+'\n\n'+ line
                result = result + text_output
                ch_matched_list = line.split('ch_matched for P_ids:')
                ch_matched_list =ch_matched_list[1:]
                for ch_matched in ch_matched_list:
                    if ch_matched == '':continue
                    ch_matched = ch_matched.strip()         
                    item1, item2 = ch_matched.split(',')
                    item1 = item1.strip()
                    item2 = item2.strip()
                    pid_1, pid_2 = item1.split('<-->')
                    pid_1 = int(pid_1)
                    pid_2 = int(pid_2)
                    action1, action2 = item2.split('<--->') 
                    if '>' in action1:
                        sender2 = p_name_list[pid_2]
                        receiver2 = p_name_list[pid_1]
                    else:
                        sender2 = p_name_list[pid_1]
                        receiver2 = p_name_list[pid_2]
                    sender2 = sender2.strip() 
                    receiver2 = receiver2.strip()  
            line_old = line_new 
        result = result + line_old
        outputWin.configure(state='normal')
        outputWin.delete(1.0,"end")
        outputWin.insert(1.0, result)
        outputWin.configure(state='disabled')          
      

    #level paned window for vertical layout
    pwL1 = PanedWindow(orient ='vertical')  

    #pwL1 row1
    label_a = Label(pwL1, text="Input π-Calculus expression below or read from a file:", font=("Times New Roman", 12)) 
    pwL1.add(label_a) 

    #pwL1 row2
    inputWin = scrolledtext.ScrolledText(height = 6, width = 50, bg='light gray', bd=5)    
    initInputWin()
    pwL1.add(inputWin) 

    #pwL1 row3
    #level 2 paned window in pwL1
    pwL2 = PanedWindow(pwL1,sashrelief=tk.SUNKEN,sashpad=1)   
    pwL1.add(pwL2) 

    #creating Button 
    
    label_b = Label(pwL2, text="", font=("Times New Roman", 12)) 
    label_b.grid(row=1,column=0)
    runPiExp = tk.Button(pwL2, text="Open Input Exp File ", font=("Times New Roman", 12), command=openInputExpFile) 
    runPiExp.grid(row=1,column=1)
    
    
    label_b = Label(pwL2, text="", font=("Times New Roman", 12)) 
    label_b.grid(row=1,column=2)
    runPiExp = tk.Button(pwL2, text="Run Input Exp", font=("Times New Roman", 12), command=runInputExp) 
    runPiExp.grid(row=1,column=3)


    label_d = Label(pwL2, text="", font=("Times New Roman", 12)) 
    label_d.grid(row=1,column=4)
    clearInput = tk.Button(pwL2, text="Clear Input", font=("Times New Roman", 12), command=clearInputWin) 
    clearInput.grid(row=1,column=5)

    label_d = Label(pwL2, text="", font=("Times New Roman", 12)) 
    label_d.grid(row=1,column=6)
    clearOutput = tk.Button(pwL2, text="Clear Output", font=("Times New Roman", 12), command=clearOutputWin) 
    clearOutput.grid(row=1,column=7)

    label_d = Label(pwL2, text="", font=("Times New Roman", 12)) 
    label_d.grid(row=1,column=8)
    genAST = tk.Button(pwL2, text="generate AST", font=("Times New Roman", 12), command=genAST) 
    genAST.grid(row=1,column=9)
    
    #pwL1 row4
    #Readonly Text for output
    outputWin = scrolledtext.ScrolledText(height = 6, width = 50, bg='light gray', bd=5)  
    outputWin.configure(state='disabled')
    pwL1.add(outputWin)   

    pwL1.pack(fill = BOTH, expand = True) 
    pwL1.configure(sashrelief = RAISED) 
    win.mainloop() 
    
    
if __name__ == '__main__':
    main() 