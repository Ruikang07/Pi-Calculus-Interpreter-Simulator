# Pi-Calculus-Interpreter-Simulator
A python implementation of Pi-Calculus Interpreter and Simulator


π-Calculus Syntax Used in The Interpreter and Simulator

syntax            syntax	Description
x<y.P	            write y to channel x
x>y.P	            read from channel x to y
x@P	              bound x to P
(x,y,z)@P	        bound x,y,z to P
P|Q	              run concurrently
P+Q	              run P or Q
!P 	              repeat P
0	                nil process, all actions finished
x>a.y<v	          Actions x>a and y<b run sequentially
P := x>a.y<v	    P is a terminal expression 
picExpr ::= P|Q	  picExpr is a non-terminal expression
             
All π-Calculus expressions in our Interpreter and Simulator have picExpr as the name of its final expression.
