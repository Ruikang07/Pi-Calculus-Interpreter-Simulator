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
  


<img
src=“.//figures/picInterpreterGUI.jpg”
>
