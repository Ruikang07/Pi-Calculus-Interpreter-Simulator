# CISC 465 project
# Inspired by Ruslan Spivak's work 
# produced by Ruikang Luo
# 2021/04/19

from PicCompiler import PicCompiler, P_NORMAL, P_REPEAT, P_SUM, P_MIX 

def picGenAST(expr):
    picCompiler = PicCompiler(expr)
    p_type_list, processList  = picCompiler.run()
    
    s1 = '  '
    s2 = ' [label="'
    s3 = '"]'
    s4 = ' -> '
    
    lines = []
    lines.append('digraph astgraph {')
    lines.append('  node [shape=circle, fontsize=12, fontname="Courier", height=.1];')
    lines.append('  ranksep=.3;')
    lines.append('  edge [arrowsize=.5]')
    
    
    name0 = 'root'
    op0 = '|'
    node = s1+name0+s2+op0+s3
    lines.append(node)

    len_P = len(processList)
    for i1 in range(len_P):
        process = processList[i1]
        name0 = 'root'
        name1 ='process'+str(i1)
        if p_type_list[i1] == P_NORMAL:
            op1 = ''
            node = s1+name1+s2+op1+s3
            conn = s1+name0+s4+name1
            lines.append(node)                
            lines.append(conn)
            
            i2 = 0
            actionList = process[i2]
            name2 = name1+'group'+str(i2)
            op2 = '.'
            if len(actionList ) == 1:op2 = ''
            node = s1+name2+s2+op2+s3
            conn = s1+name1+s4+name2
            lines.append(node)
            lines.append(conn)
            i3 = 0
            for action in actionList:  
                name3 = name1+'_action'+str(i3)
                i3 += 1
                a1_tmp = action.replace('<', ' < ')
                a1_tmp = a1_tmp.replace('>', ' > ')
                name4_1, op3, name4_2 = a1_tmp.split(' ')
                node = s1+name3+s2+op3+s3
                conn = s1+name2+s4+name3
                lines.append(node)
                lines.append(conn)
                
                name4 = name3+name4_1
                op4 = name4_1
                node = s1+name4+s2+op4+s3
                conn = s1+name3+s4+name4
                lines.append(node)
                lines.append(conn)

                name4 = name3+name4_2
                op4 = name4_2
                node = s1+name4+s2+op4+s3
                conn = s1+name3+s4+name4
                lines.append(node)
                lines.append(conn)

        if p_type_list[i1] == P_REPEAT:
            op1 = '!()'
            node = s1+name1+s2+op1+s3
            conn = s1+name0+s4+name1
            lines.append(node)                
            lines.append(conn)
            
            i2 = 0
            actionList = process[i2]
            name2 = name1+'group'+str(i2)
            op2 = '.'
            if len(actionList ) == 1:op2 = ''
            node = s1+name2+s2+op2+s3
            conn = s1+name1+s4+name2
            lines.append(node)
            lines.append(conn)
            i3 = 0
            for action in actionList:  
                name3 = name1+'_action'+str(i3)
                i3 += 1
                a1_tmp = action.replace('<', ' < ')
                a1_tmp = a1_tmp.replace('>', ' > ')
                name4_1, op3, name4_2 = a1_tmp.split(' ')
                node = s1+name3+s2+op3+s3
                conn = s1+name2+s4+name3
                lines.append(node)
                lines.append(conn)
                
                name4 = name3+name4_1
                op4 = name4_1
                node = s1+name4+s2+op4+s3
                conn = s1+name3+s4+name4
                lines.append(node)
                lines.append(conn)

                name4 = name3+name4_2
                op4 = name4_2
                node = s1+name4+s2+op4+s3
                conn = s1+name3+s4+name4
                lines.append(node)
                lines.append(conn)
                
        if p_type_list[i1] == P_SUM:
            op1 = '(+)'
            node = s1+name1+s2+op1+s3
            conn = s1+name0+s4+name1
            lines.append(node)                
            lines.append(conn)
            i2 = 0
            for actionList in process:
                name2 = name1+'group'+str(i2)
                i2 += 1
                op2 = '.'
                if len(actionList ) == 1:op2 = ''
                node = s1+name2+s2+op2+s3
                conn = s1+name1+s4+name2
                lines.append(node)
                lines.append(conn)
                i3 = 0
                for action in actionList:  
                    name3 = name2+'_action'+str(i3)
                    i3 += 1
                    a1_tmp = action.replace('<', ' < ')
                    a1_tmp = a1_tmp.replace('>', ' > ')
                    name4_1, op3, name4_2 = a1_tmp.split(' ')
                    node = s1+name3+s2+op3+s3
                    conn = s1+name2+s4+name3
                    lines.append(node)
                    lines.append(conn)
                    
                    name4 = name3+name4_1
                    op4 = name4_1
                    node = s1+name4+s2+op4+s3
                    conn = s1+name3+s4+name4
                    lines.append(node)
                    lines.append(conn)

                    name4 = name3+name4_2
                    op4 = name4_2
                    node = s1+name4+s2+op4+s3
                    conn = s1+name3+s4+name4
                    lines.append(node)
                    lines.append(conn)
                    
        if p_type_list[i1] == P_MIX:
            op1 = '!(+)'
            node = s1+name1+s2+op1+s3
            conn = s1+name0+s4+name1
            lines.append(node)                
            lines.append(conn)
            i2 = 0
            for actionList in process:
                name2 = name1+'group'+str(i2)
                i2 += 1
                op2 = '.'
                if len(actionList ) == 1:op2 = ''
                node = s1+name2+s2+op2+s3
                conn = s1+name1+s4+name2
                lines.append(node)
                lines.append(conn)
                i3 = 0
                for action in actionList:  
                    name3 = name2+'_action'+str(i3)
                    i3 += 1
                    a1_tmp = action.replace('<', ' < ')
                    a1_tmp = a1_tmp.replace('>', ' > ')
                    name4_1, op3, name4_2 = a1_tmp.split(' ')
                    node = s1+name3+s2+op3+s3
                    conn = s1+name2+s4+name3
                    lines.append(node)
                    lines.append(conn)
                    
                    name4 = name3+name4_1
                    op4 = name4_1
                    node = s1+name4+s2+op4+s3
                    conn = s1+name3+s4+name4
                    lines.append(node)
                    lines.append(conn)

                    name4 = name3+name4_2
                    op4 = name4_2
                    node = s1+name4+s2+op4+s3
                    conn = s1+name3+s4+name4
                    lines.append(node)
                    lines.append(conn)  

  
    lines.append('}')
    
    file1 = open("picAST.dot","w+")
    for line in lines:
        file1.write(line+'\n')
    file1.close()
    
    return


