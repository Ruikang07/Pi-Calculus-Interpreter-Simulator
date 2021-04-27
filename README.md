# Pi-Calculus-Interpreter-Simulator
A python implementation of Pi-Calculus Interpreter and Simulator  

A project of course CISC 465

| Syntax  | Description  |  
| :-------------- |:---------------| 
| x<y.P      | write y to channel x | 
| x>y.P      | read from channel x to y       |   
| (x,y,z)@P | bound x,y,z to P        |   
| P &#124; Q      | run P and Q concurrently | 
| P+Q      | run P or Q       |   
| !P | repeat P        |    
| 0      | nil process, all actions finished | 
| x>a.y<v      | Actions x>a and y<b run sequentially       |   
| P:=x>a.y<v | P is a terminal expression        |   
| picExpr::=P &#124; Q| picExpr is a non-terminal expression | 
 
All π-Calculus expressions in our Interpreter and Simulator have picExpr as the name of its final expression.  
  
  
GUI of Interpreter
<img width="964" alt="GUI of Pi-Calculus Interpreter" src="https://github.com/Ruikang07/Pi-Calculus-Interpreter-Simulator/blob/b595949a5fa6817ae066c1e8ad3ea6b246ac9bf7/figures/picInterpreterGUI.PNG">
Inspired by Ruslan Spivak's work[1],  the abstract syntax tree (AST) module was added to our π-Calculus Interpreter.
  
  
GUI of Simulator
<img width="964" alt="GUI of Pi-Calculus Simulator" src="https://github.com/Ruikang07/Pi-Calculus-Interpreter-Simulator/blob/b565d8884cb29c95dca2c0e3f57caeab43d9d0a0/figures/picSimulatorGUI.PNG">  

Reference:  

[1]Ruslan Spivak,  "Let's Build A Simple Interpreter," https://github.com/rspivak/lsbasi
