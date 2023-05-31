import sys
outpt=[]
def write(s):
    # while(s[-1]=='\n'):
    #     s=s[:-1]
    print(s)
    
    # print(s)


reg={
    "000":0,"001":0,"010":0,"011":0,"100":0,"101":0,"110":0,"111":0
}

addr_variables={}
addr_labels={}
mem_addr={}
# def checkl(lst,l):
#     # print(lst)
#     if(len(lst)!=l):
#         # print(s)
#         raise Exception("Syntax Error")
#     if(lst[1] not in registers or lst[2] not in registers):
#         raise Exception("Invalid reg name")
# # Type A:Harshit 

def A(s):#op-5 u-2 r1-3,r2-3,r3-3
    if(s[:2]!="00"):
        raise Exception("For Type A Unused Bits should be 00")
    r1=s[2:5]
    r2=s[5:8]
    r3=s[8:]
    if('111' in [r1,r2,r3]):
        raise Exception("Can not use Flag register ")
    if((r1 not in reg) or (r2 not in reg) or (r3 not in reg)):
        raise Exception("Invalide Register Address")
    return (r1,r2,r3)


def add(s):
    r1,r2,r3=A(s)
    reg[r1]=reg[r2]+reg[r3]    
def sub(s):
    r1,r2,r3=A(s)
    reg[r1]=reg[r2]-reg[r3]
def mul(s):
    # print("mul")
    r1,r2,r3=A(s)
    reg[r1]=reg[r2]*reg[r3]
def xor(s):
    # print(s[0])
    r1,r2,r3=A(s)
    reg[r1]=reg[r2]^reg[r3]
def Or(s):
    # print(s[0])
    r1,r2,r3=A(s)
    reg[r1]=reg[r2]|reg[r3]
def And(s):
    # print(s[0])
    r1,r2,r3=A(s)
    reg[r1]=reg[r2]&reg[r3]

#Type B
    
def B(s):
    if(s[0] != '0'):
        raise Exception("For type B Unused bit should be 0")
    r=s[1:4]
    if(r=='111'):
        raise Exception("Can not use FLAG REGISTER")
    if r not in reg:
        raise Exception("Invalid Register Address")
    Imm=s[4:]
    return r,Imm
def movB(s):
  r,Imm=B(s) 
  reg[r]=Imm 
    # printb(s)
def rs(s):
    r,Imm=B(s) 
    reg[r]=reg[r]>>Imm 
    
def ls(s):
   r,Imm=B(s) 
   reg[r]=reg[r]<<Imm 
#Type C
def C(s):
    if(s[:5]!="00000"):
        raise Exception("For Type C Unused Bits should be 00000")
    r1=s[5:8]
    r2=s[8:]
    
    if('111' in [r1,r2]):
        raise Exception("Can not use Flag register ")
    if((r1 not in reg) or (r2 not in reg) ):
        raise Exception("Invalide Register Address")
    return (r1,r2)
def div(s):
    r1,r2=C(s)
    r3=reg[r1]
    r4=reg[r2]
    if(r4==0):
        reg["111"]=1000
        reg["000"]=0
        reg["001"]=0 
        return   
    reg["000"]=r3/r4
    reg["001"]=r3%r4
    

def movC(s):
    r1,r2=C(s)
    reg[r1]=reg[r2]

def Not(s):
    r1,r2=C(s)
    reg[r1]=-1*reg[r2]

def cmp(s):
    r1,r2=C(s)
    r1=reg[r1]
    r2=reg[r2]
    # print(s[0])
    if(r1>r2):
        reg['111']=10
    if(r1==r2):
        reg['111']=1
    if(r1<r2):
        reg['111']=100
    
    
#type D:Dev Utkarsh
# def checkD(lst,l):
#     # print(lst)
#     if(len(lst)!=l):
#         # print(s)
#         raise Exception("Syntax Error")
#     if(lst[1] not in registers or lst[2] not in addr_variables):
#         raise Exception("Invalid reg name or variable name")
def D(s):
    if(s[0] != '0'):
        raise Exception("For type B Unused bit should be 0")
    r=s[1:4]
    if(r=='111'):
        raise Exception("Can not use FLAG REGISTER")
    if r not in reg:
        raise Exception("Invalid Register Address")
    addr=s[4:]
    return r,addr

def ld(s):
    r1,addr=D(s)
    reg[r1]=mem_addr[addr]
    
    

def st(s):
    r1,addr=D(s)
    mem_addr[addr]=reg[r1]
# def PC(start_idx):

# checker function for all jump function-E:-

def print_jump():
    print(opcodes[cmds][0]+"")

def check_jump(s):
    if(len(s)<2):
        # print(s)
        raise Exception("Syntax Error, less operands")
    elif(len(s)>2):
        # print(s)
        raise Exception("Syntax Error, more operands")
    flag=0
    for i in range(len(lines)):
        label_name=[]
        label_name=lines[i].split()
        if(label_name[0]==(s[1]+':')):
            flag=1
        if(flag==1):
            return
    if(flag==0):
        raise Exception("No such Label Found in the whole Assembly code")


#type E:Arpan
def jmp(s):
    check_jump(s)
    temp=0
    if (len(memory_for_labels[s[1]])<7):
        temp=7-len(memory_for_labels[s[1]])
    write("01111"+"0000"+"0"*temp + memory_for_labels[s[1]])
    for i in range(len(lines)):
        if(lines[i][0]==s[1]):
            # print(s[0])
            return i

def jlt(s):
    check_jump(s)
    #PRINTING
    temp=0
    if (len(memory_for_labels[s[1]])<7):
        temp=7-len(memory_for_labels[s[1]])
    write("11100"+"0000"+"0"*temp + memory_for_labels[s[1]])
    
    if(registers["FLAGS"][1]==100):
        for i in range(len(lines)):
            if(lines[i][0]==s[1]):
                print(s[0])
                return i
        # print(s[0])
    else:
        return cnt

def jgt(s):
    check_jump(s)
    temp=0
    if (len(memory_for_labels[s[1]])<7):
        temp=7-len(memory_for_labels[s[1]])
    write("11101"+"0000"+"0"*temp + memory_for_labels[s[1]])
    

    if(registers["FLAGS"][1]==10):
        for i in range(len(lines)):
            if(lines[i][0]==s[1]):
                # print(s[0])
                return i
        # print(s[0])
    else:
        return cnt

def je(s):
    check_jump(s)

    temp=0
    if (len(memory_for_labels[s[1]])<7):
        temp=7-len(memory_for_labels[s[1]])
    write("11111"+"0000"+"0"*temp + memory_for_labels[s[1]])


    if(registers["FLAGS"][1]==1):
        for i in range(len(lines)):
            if(lines[i][0]==s[1]):
                # print(s[0])
                return i
        # print(s[0])
    else:
        return cnt

# def check_halt():


#type-f Arpan:
def hlt(s):
    # printing
    write("11010"+"00000000000")
    sys.exit()
    # print()


#to check is it a valid syntax for declaring a var
def checkIsVar(s):
    if(len(s)!=2):
        raise Exception("Invalid Syntax")
    
opcodes = {
    "00000":add,"00001":sub,"00010":movB,"00011":movC,#move register
    "00100":ld,"00101":st,"00110":mul,"00111":div,"01000":rs,
    "01001":ls,"01010":xor,"01011":Or,"01100":And,"01101":Not,
    "01110":cmp,"01111":jmp,"11100":jlt,"11101":jgt,"11111":je,
    "11010":hlt,
}

file=open("SimpleSimulator/input.txt",'r')
lines=file.readlines()
# lines=sys.stdin.readlines()
cnt=0
final_code=[]
variables=[]
labels={}
f=0
instruction_address=[]
variable_idx=[]
return_address=0
# for line in sys.stdin:
#     line=line.rstrip()
#     lines.append(line)

for i in range(len(lines)):
    if(lines[i][-1]=='\n'):
        lines[i]=lines[i][:-1]
print(lines)
#Decode
def checkop(opc):
    if opc not in opcodes:
        raise Exception("Invalid Opcode")
pc=0
while(True):
    print(lines[pc])
    if(len(lines)!=7):
        raise Exception("Instruction should be 7 bit only")
    opcode=lines[pc][:5]
    checkop(opcode)
    opcodes[opcode](lines[pc][5:])
    pc+=1
    
# for line in lines:
#     cnt+=1
#     # print("line->",line)
#     # line=line.rstrip()
#     # lines.append(line)
#     if(line[-1]=='\n'):
#         line=line[:-1]
#     s=line.strip()
#     if(s=='' or s=='\n'):
#         continue
    
#     s=s.split()
#     if(s[0]=='var'):
#         variable_idx.append(cnt-1)
#         if(len(final_code)!=0):
#             raise Exception("var should be declare at top")
#         checkIsVar(s)
#         variables.append(s[1])
#         continue

#     # if (s[0]=='jmp'|'jgt'|'je'|'jlt'):
#     #     return_address=cnt # after completeing the label call if ret would be found then it would come back to the origina label
#     #     i=jmp(s)
#     #     if(i!=cnt):
#     #         line=lines[i]
    
#     elif(s[0] not in opcodes):
#         if(s[0][-1]==':' and len(s[0])>1):
#             if(s[0] in labels):
#                 raise Exception("label"+s[0]+"is already declared")
#             labels[s[0][:-1]]=len(final_code)
#         else:
#             raise Exception("Syntax Error")
        
#     final_code.append(s)
#     if(s[0]=='hlt'):
#         f=1
#         # break
#     if(len(s)==128):
#      break

# # if(f==0):
# #     raise Exception("hlt statement not used")
# # print(final_code)
# # print(variables)
# # print("printing labels!!!!!!!!")
# # print(labels)
# #assign address to variables using dictionary addr_variables declared at top
# # print(lines)
# memory_for_instructions=[]
# last="0000000"
# la=0
# for i in range(0,len(final_code)):

#     la=0000000+int(bin(i)[2:])
#     last=str(la)
#     memory_for_instructions.append(last)
# # print(memory_for_instructions)

# # memory_for_variables=[]
# for i in range(0,len(variables)):
#     addr_variables[variables[i]]=[str(bin(len(final_code)+i)[2:]),0]

# memory_for_labels={}
# for i in labels:
#     memory_for_labels[i]=memory_for_instructions[int(labels[i])]

# # print(memory_for_labels)


# # for i in range(len(lines)):
# #         label_name=[]
# #         label_name=lines[i].split()
# #         if(label_name[0]==(s[1]+':')):


# # memory_for_labels=[]
# # for i in range(0,len(labels)):
# #     addr_labels[labels[i]]=[str()]
# #     addr_labels[labels[i]]=[str()]

# # print("memory")
# # print(memory_for_instructions)

# # print("-----------------------------------------------------------------------------\n")
# # print(labels)
# # print("-----------------------------------------------------------------------------\n")
# # print(addr_variables)
# # for i in variables:
# #     printf("")

# # print(final_code)
# for i in range(len(final_code)):
    
#     inst=final_code[i][0]
#     # print(inst)
#     # print("->",inst)
#     # print(inst[0])
#     cmds=final_code[i]
#     # print(inst[:-1])
#     # print(lines)
#     # if(lines.index("hlt")<len(lines)-1):
#     #     raise Exception("No instructuins after halt")
#     if inst in opcodes:
#         opcodes[inst][0](cmds)
#     elif final_code[i][-1] == "hlt":
#         hlt(inst)
#     elif ':' in final_code[i][0]:
#         opcodes[final_code[i][1]][0](cmds[1:])
        
#     elif inst[:-1] in labels:
#         continue
#     else:
#         raise Exception("Invalid Syntax")
#   # if final_code[i]
# # printf("done")
# # f=open("out.txt",'a')
# # f.writelines(outpt)
# # f.close()
# if(f==0):
#     raise Exception("hlt statement not used")
# print(len(outpt))
# # for i in range(len(outpt)-1):
    
# #     print(outpt[i])
# # print(outpt[-1],end='')
# # sys.stdout.writelines(outpt)
# # providing addr to hlt and var

# # for i in range(128):
# #     s=input().strip()
# #     while s=='' or s=='\n':
# #         s=input().strip()
# #     s=s.split()