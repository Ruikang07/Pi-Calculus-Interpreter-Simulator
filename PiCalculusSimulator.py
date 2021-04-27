# CISC 465 project
# produced by Ruikang Luo
# 2021/04/19

from PicCompiler import PicCompiler
from PicRuntime import PicRuntime
from PicException import *
from PicExpressionFilter import *

from tkinter import * 
import tkinter as tk
from tkinter import scrolledtext
from tkinter import filedialog
from tkinter.messagebox import askokcancel, showinfo, WARNING
import threading
from threading import Thread
import random
import time

import concurrent.futures
import threading

x_msc = 0
y_msc = 0
x_ms1 = 0
y_ms1 = 0
x_ms2 = 0
y_ms2 = 0    
x_off = 90
y_off = 64
cvWIDTH = 800
cvHEIGHT = 290
dict_pic = {}
simulator_expr_dir = './examples4Simulator/exd0/'



def sign(x): 
  return 1-(x<=0)

def main():
    win = Tk() 
    win.title('π Calculus Simulator')
    win.geometry("804x540") 
    TIME_DELAY = 40
    inputExp = StringVar() 
    msEdge = 400
    cvThreadList = []
    canvasStop = 0
    MU_List = []
    ch_List = []
    pic_ch = [0,0,100,100]
    x_mu1 = 0
    y_mu1 = 0
    x_mu2 = 0
    y_mu2 = 0

    
    
    # load the icons
    iconMSC = tk.PhotoImage(file='./icon/imgMSC.png')  
    iconBS = tk.PhotoImage(file='./icon/imgBS.png')
    iconMU1 = tk.PhotoImage(file='./icon/car1.png')
    iconMU2 = tk.PhotoImage(file='./icon/car2.png')   
    
    #executor1 = concurrent.futures.ThreadPoolExecutor(max_workers=8) 

    exit_event = threading.Event()
    stop_event = threading.Event()
    pause_event = threading.Event()
 
    def on_close():
        close = askokcancel("close", "Have you used exit button before close?")
        if close:
            pause_event.set()
            stop_event.set()
            exit_event.set()
            time.sleep(0.6)
            win.destroy()
        
    def move_MUs():
        positions = []
        for user in MU_List:
            position = updateCanvasMU(user) 
            positions.append(position)
        return positions 
        
    def show_Pic_Current_Channel(x1,y1,x2,y2):     
        global canvasStop, cvId_ch
        if( canvasStop == 0):          
            dx = (x2 - x1)/10.
            dy = (y2 - y1)/10.            

            for user in ch_List:     
                canvas2.coords(user['cvId'], [x1,y1,x1,y1])
                
            user2 = ch_List[9]
            for user in ch_List:
                x2 = x1 + dx
                y2 = y1 + dy    
                canvas2.coords(user['cvId'], [x1,y1,x2,y2])
                canvas2.coords(user2['cvId'], [x1,y1,x2,y2])
                time.sleep(0.1)
                x1 = x2
                y1 = y2
        return       
            
    def updateCanvasMU(user):
        global x_off, y_off, cvWIDTH, cvHEIGHT
        position = []
        global canvasStop
        if( canvasStop == 0):
            x1, y1 = canvas2.coords(user['cvId'])
            if x1 < 2*x_off and user['x_off'] < 0:
                user['x_off'] *= -1
            if x1 > cvWIDTH - 2*x_off and user['x_off'] > 0 :
                user['x_off'] *= -1    
            if y1 < 120 and user['y_off'] < 0:
                user['y_off'] *= -1  
            if y1 > cvHEIGHT - y_off -1 and user['y_off'] > 0 :
                user['y_off'] *= -1      
            canvas2.move(user['cvId'], user['x_off'], user['y_off'])  
            x1, y1 = canvas2.coords(user['cvId'])
            position = [x1,y1]  
        return position  


########################################################################################
    def getInputExp():
        inputExp=inputWin.get("1.0","end")
        return inputExp        
        
    def clearInputExp():
        inputWin.delete("1.0","end")
        
    def updateInputExpr(expr):
        inputWin.configure(state='normal')
        inputWin.delete(1.0,"end")
        inputWin.insert(1.0, expr)
        inputWin.configure(state='disabled') 

    def updateOutputWin(text):
        text1 = 'msg sent from MU1 to MU2: '+text
        outputWin.configure(state='normal')
        outputWin.delete(1.0,"end")
        outputWin.insert(1.0, text1)
        outputWin.configure(state='disabled')
              

    def picSimulationEngine():
        global simulator_expr_dir
        while True:
            if exit_event.is_set():
                break
            while True:
                if stop_event.is_set():
                    break  
                while True:
                    if pause_event.is_set():
                        break                   
                    ##########################################################################
                    [positionMU1, positionMU2] = move_MUs()
                    ##########################################################################
                    x_mu1, y_mu1 = positionMU1
                    x_mu2, y_mu2 = positionMU2   
                    dict_pic['mu1'] = [x_mu1, y_mu1]
                    dict_pic['mu2'] = [x_mu2, y_mu2]
                    
                    
                    #both MU1 and MU2 in MS1
                    if x_mu1 <= msEdge and x_mu2 <= msEdge:  
                        #canvas2.coords(cvId_MU1_msc, x_mu1+16, y_mu1+16, x_mu2+32, y_mu2+132)
                        MU1_s_msg = '"xMU1='+str(int(x_mu1))+'_yMU1='+str(int(y_mu1))+'"'
                        expr_file= simulator_expr_dir+'/expr_1_1.txt'
                        ms_flag = 11
                        runPicExpr(MU1_s_msg, expr_file, ms_flag)

                    #MU1 in MS1 and MU2 in MS2    
                    if x_mu1 <= msEdge and x_mu2 > msEdge:
                        MU1_s_msg = '"xMU1='+str(int(x_mu1))+'_yMU1='+str(int(y_mu1))+'"'
                        expr_file= simulator_expr_dir+'/expr_1_2.txt'
                        ms_flag = 12
                        runPicExpr(MU1_s_msg, expr_file, ms_flag)

                    #MU1 in MS2 and MU2 in MS1
                    if x_mu1 > msEdge and x_mu2 <= msEdge:
                        MU1_s_msg = '"xMU1='+str(int(x_mu1))+'_yMU1='+str(int(y_mu1))+'"'
                        expr_file= simulator_expr_dir+'/expr_2_1.txt'
                        ms_flag = 21
                        runPicExpr(MU1_s_msg, expr_file, ms_flag)

                    #both MU1 and MU2 in MS2
                    if x_mu1 > msEdge and x_mu2 > msEdge:     
                        MU1_s_msg = '"xMU1='+str(int(x_mu1))+'_yMU1='+str(int(y_mu1))+'"'
                        expr_file= simulator_expr_dir+'/expr_2_2.txt'
                        ms_flag = 22
                        runPicExpr(MU1_s_msg, expr_file, ms_flag)

                    time.sleep(0.5)
                time.sleep(0.1)  
            time.sleep(0.1)


    def handdlePicError(msg):
        expr2show = msg
        updateInputExpr(expr2show)
        selectInputFolder.configure(state='normal')
        restartSimulator.configure(state='disabled')
        pauseSimulator.configure(state='disabled')
        stopSimulator.configure(state='disabled')
        runSimulator.configure(state='disabled')
        pause_event.set()
        stop_event.set()
        return    
    
    def runPicExpr(MU1_s_msg, expr_file, ms_flag):
        try:    
            expr, p_name_list, expr2show = createSimulatorExpr(MU1_s_msg, expr_file)
            updateInputExpr(expr2show)
            time.sleep(1) 
            picCompiler = PicCompiler(expr)
            p_type_list, processList  = picCompiler.run()
            picRuntime1 = PicRuntime(p_name_list, p_type_list, processList) 
            MU1_r_msg, MU2_r_msg, output = picRuntime1.run() 
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

            
        updateChannelMatching(output, p_name_list, MU2_r_msg)

    ######################################################################################   
    def updateChannelMatching(output, p_name_list, MU2_r_msg):
        line_new = ''
        line_old = ''
        for line in output:
            if not line: continue
            if line == 'END': break
            line_new = "picExpr:= \n" + line
            num_match = line.count('ch_matched for P_ids:')
            if num_match == 1:
                text_output = line_old+'\n\n'+ line
                updateInputExpr(text_output)   
                
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
                sender1 = sender1[0:3] 
                receiver1 = receiver1[0:3]  

                ##########################################################################
                x1,y1 = dict_pic[sender1] 
                x2,y2 = dict_pic[receiver1] 
                
                x1 =  x1+16
                y1 =  y1+16
                x2 =  x2+16
                y2 =  y2+16
                
                if sender1 == receiver1:
                    x1 =  x1-32
                    x2 =  x2+32

                show_Pic_Current_Channel(x1,y1,x2,y2) 
                while True:
                    if not pause_event.is_set(): break
                ##########################################################################  
                
            elif num_match > 1:
                text_output = line_old+'\n\n'+ line
                updateInputExpr(text_output)                             
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
                    sender2 = sender2[0:3] 
                    receiver2 = receiver2[0:3]

                    ##########################################################################
                    x1,y1 = dict_pic[sender2] 
                    x2,y2 = dict_pic[receiver2] 
                    x1 =  x1+16
                    y1 =  y1+16
                    x2 =  x2+16
                    y2 =  y2+16
                    
                    if sender2 == receiver2:
                        x1 =  x1-32
                        x2 =  x2+32
                    
                    show_Pic_Current_Channel(x1,y1,x2,y2) 
                    while True:
                        if not pause_event.is_set(): break
                    ########################################################################## 
                
            line_old = line_new 

        #updateInputExpr(line_old)
        text_output = text_output + line_new
        updateInputExpr(text_output)  
        updateOutputWin(MU2_r_msg)
        show_Pic_Current_Channel(1000,1000,1200,1200)
        #time.sleep(0.5)



              
    ######################################################################################   
    def initPicSimulator(cvWIDTH,cvHEIGHT):
        global canvasStop, createCanvasObj
        global x_ms1, y_ms1, x_ms2, y_ms2
   
        canvasStop = 0

        createCanvasObj = False
        canvas2.create_rectangle(0, 0, msEdge, 300, fill='light blue')
        canvas2.create_rectangle(msEdge, 0, cvWIDTH, 300, fill='light green')          
        x_msc, y_msc = (msEdge-32,0)
        dict_pic['msc'] = [x_msc+16, y_msc+16]
        cvIdMSC = canvas2.create_image(x_msc, y_msc, image=iconMSC, anchor=NW) 
        x_ms1, y_ms1 = (0,20)
        dict_pic['ms1'] = [x_ms1+16, y_ms1+16]
        cvIdMS1 = canvas2.create_image(x_ms1, y_ms1, image=iconBS, anchor=NW) 
        x_ms2, y_ms2 = (cvWIDTH-64,20)
        dict_pic['ms2'] = [x_ms2+16, y_ms2+16]
        cvId_MS2 = canvas2.create_image(x_ms2, y_ms2, image=iconBS, anchor=NW)   
        
        #x_mu1, y_mu1 = (cvWIDTH-10*x_off-1,cvHEIGHT-5*y_off-1)
        x_mu1, y_mu1 = (10,119)
        dict_pic['mu1'] = [x_mu1, y_mu1]
        cvIdMU1 = canvas2.create_image(x_mu1, y_mu1, image=iconMU1, anchor=NW) 
        name = "MU1"             
        user = {"name":name, "cvId":cvIdMU1, "x_off":x_off, "y_off":y_off, "w":32, "h":32}
        MU_List.append(user) 
        
        #x_mu2, y_mu2 = (cvWIDTH-5*x_off-1,cvHEIGHT-2*y_off-1)
        x_mu2, y_mu2 = (3*x_off+10,119+y_off)
        dict_pic['mu2'] = [x_mu2, y_mu2]
        name = "MU2"
        cvIdMU2 = canvas2.create_image(x_mu2, y_mu2, image=iconMU2, anchor=NW)
        user = {"name":name, "cvId":cvIdMU2, "x_off":x_off, "y_off":y_off, "w":32, "h":32}
        MU_List.append(user)
        
        x1 = 1000
        y1 = 1000
        x2 = 1200
        y2 = 1200
        for i in range(10):
            ch_name = 'pic_ch'+str(i)
            if i < 9:
                cvId_ch = canvas2.create_line(x1, y1, x2, y2, width=3, fill="blue")
            else:    
                cvId_ch = canvas2.create_line(x1, y1, x2, y2, width=3, arrow=tk.LAST, fill="blue")
            ch_i = {"name":ch_name, "cvId":cvId_ch}
            ch_List.append(ch_i)


        ####################################################################
        pause_event.set()
        stop_event.set()
        thread = Thread(target=picSimulationEngine)
        thread.daemon = True
        thread.start()
        
        
    def selectInputFolder():
        global simulator_expr_dir
        simulator_expr_dir = filedialog.askdirectory(initialdir = "./examples4Simulator")
        expr_file= simulator_expr_dir+'/expr_1_1.txt'

        try:    
            expr, p_name_list, expr2show = createSimulatorExpr("Hi", expr_file)
        except NameError:
            msg = "Invalid Pi Calculus Syntax"
            handdlePicError(msg)
            return
        except InvalidPiCalculusSyntax:
            msg = "Invalid Pi Calculus Syntax"
            handdlePicError(msg)
            return         
        
        
        if expr == 'InvalidPiCalculusSyntax':
            expr2show = "Invalid Pi Calculus Syntax"
            updateInputExpr(expr2show)
            return        
        
        updateInputExpr(expr2show)
        runSimulator.configure(state='normal')
        return        

 
    def simulateInputExp():  
        global canvasStop
        canvasStop = 0
        selectInputFolder.configure(state='disabled')
        runSimulator.configure(state='disabled')
        restartSimulator.configure(state='disabled')
        pauseSimulator.configure(state='normal')
        stopSimulator.configure(state='normal')
        pause_event.clear()
        stop_event.clear()
            

        
        

    def simulateRestart():
        global canvasStop
        canvasStop = 0  
        restartSimulator.configure(state='disabled')
        pauseSimulator.configure(state='normal')
        stopSimulator.configure(state='normal')
        pause_event.clear()
               
    def simulatePause():
        global canvasStop
        canvasStop = 1
        restartSimulator.configure(state='normal')
        pauseSimulator.configure(state='disabled')
        pause_event.set()
        
    def simulateStop():
        global canvasStop
        canvasStop = 1
        updateInputExpr('Please select a π-Calculus expression input folder in examples4Simulator')
        selectInputFolder.configure(state='normal')
        restartSimulator.configure(state='disabled')
        pauseSimulator.configure(state='disabled')
        stopSimulator.configure(state='disabled')
        runSimulator.configure(state='disabled')
        pause_event.set()
        stop_event.set()
        
             
        
    def simulateExit():
        global canvasStop
        canvasStop = 1
        pause_event.set()
        stop_event.set()
        exit_event.set()
        time.sleep(0.6)
        exit(0)
 
#######################################################################################################################

    #level paned window for vertical layout
    pwL1 = PanedWindow(orient ='vertical')  

    #pwL1 row1
    label_a = Label(pwL1, text="π Calculus Expression for Simulation", font=("Times New Roman", 12)) 
    pwL1.add(label_a) 

    #pwL1 row2
    inputWin = scrolledtext.ScrolledText(height = 8, width = 50, bg='light gray', bd=5)  
    updateInputExpr('Please select a π-Calculus expression input folder in examples4Simulator')
    inputWin.configure(state='disabled')
    pwL1.add(inputWin) 

    #pwL1 row3
    #level 2 paned window in pwL1
    pwL2 = PanedWindow(pwL1,sashrelief=tk.SUNKEN,sashpad=1)   
    pwL1.add(pwL2) 

    #creating Button widget 
    #produce some space for button menu
    label_b = Label(pwL2, text="", font=("Times New Roman", 12)) 
    label_b.grid(row=1,column=0)
    #real button

    label_d = Label(pwL2, text="", font=("Times New Roman", 12)) 
    label_d.grid(row=1,column=1)
    selectInputFolder = tk.Button(pwL2, text="Select Input Folder", font=("Times New Roman", 12), command=selectInputFolder) 
    selectInputFolder.grid(row=1,column=2)
    
    label_d = Label(pwL2, text="", font=("Times New Roman", 12)) 
    label_d.grid(row=1,column=3)
    runSimulator = tk.Button(pwL2, text="Simulate Input", font=("Times New Roman", 12), command=simulateInputExp) 
    runSimulator.grid(row=1,column=4)
    runSimulator.configure(state='disabled')
    
    label_d = Label(pwL2, text="", font=("Times New Roman", 12)) 
    label_d.grid(row=1,column=5)
    restartSimulator = tk.Button(pwL2, text="Restart Simulating", font=("Times New Roman", 12), command=simulateRestart) 
    restartSimulator.grid(row=1,column=6)
    restartSimulator.configure(state='disabled')    
    
    label_d = Label(pwL2, text="", font=("Times New Roman", 12)) 
    label_d.grid(row=1,column=7)
    pauseSimulator = tk.Button(pwL2, text="Pause Simulating", font=("Times New Roman", 12), command=simulatePause) 
    pauseSimulator.grid(row=1,column=8)    
    pauseSimulator.configure(state='disabled')

    label_d = Label(pwL2, text="", font=("Times New Roman", 12)) 
    label_d.grid(row=1,column=9)
    stopSimulator = tk.Button(pwL2, text="Stop Simulating", font=("Times New Roman", 12), command=simulateStop) 
    stopSimulator.grid(row=1,column=10)    
    stopSimulator.configure(state='disabled')  
    
    label_d = Label(pwL2, text="", font=("Times New Roman", 12)) 
    label_d.grid(row=1,column=11)
    exitSimulator = tk.Button(pwL2, text="Exit Simulating", font=("Times New Roman", 12), command=simulateExit) 
    exitSimulator.grid(row=1,column=12)         
    
    #pwL1 row4
    canvas2 = tk.Canvas(win, bg='grey', width=cvWIDTH, height=cvHEIGHT)
    pwL1.add(canvas2) 
       
    #pwL1 row5
    outputWin = tk.Text(height = 1, width = 50, bg='light gray', bd=5)  
    outputWin.configure(state='disabled')
    pwL1.add(outputWin) 

    pwL1.pack(fill = BOTH, expand = True) 

    pwL1.configure(sashrelief = RAISED) 
    
    initPicSimulator(cvWIDTH,cvHEIGHT)   
    
    restartSimulator.configure(state='disabled')
    pauseSimulator.configure(state='disabled')
    stopSimulator.configure(state='disabled')
    runSimulator.configure(state='disabled')
        
    win.protocol("WM_DELETE_WINDOW",  on_close)
    
    win.mainloop() 
    
    
if __name__ == '__main__':
        main()
