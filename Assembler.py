regs = {'x0':'00000', 'x1':'00001', 'x2':'00010', 'x3':'00011', 'x4':'00100'
       , 'x5':'00101', 'x6':'00110', 'x7':'00111', 'x8':'01000', 'x9':'01001', 'x10':'01010'
       , 'x11':'01011', 'x12':'01100', 'x13':'01101', 'x14':'01110', 'x15':'01111'
       , 'x16':'10000', 'x17':'10001', 'x18':'10010', 'x19':'10011', 'x20':'10100'
       , 'x21':'10101', 'x22':'10110', 'x23':'10111', 'x24':'11000', 'x25':'11001'
       , 'x26':'11010', 'x27':'11011', 'x28':'11100', 'x29':'11101', 'x30':'11110', 'x31':'11111'}

opcodes = {'add':'0110011', 'sub':'0110011', 'or':'0110011', 'xor':'0110011', 'and':'0110011',
           'sll':'0110011', 'srl':'0110011', 'sra':'0110011', 'slt':'0110011', 'sltu':'0110011',

           'addi':'0010011', 'xori':'0010011', 'ori':'0010011', 'andi':'0010011', 'slli':'0010011',
           'srli':'0010011', 'srai':'0010011', 'slti':'0010011', 'sltiu':'0010011',

           'lb':'0000011', 'lh':'0000011', 'lw':'0000011', 'lbu':'0000011', 'lhu':'0000011', 'jalr':'1100111',
           'ecall':'1110011', 'ebreak':'1110011',

           'sb':'0100011', 'sh':'0100011', 'sw':'0100011',

           'beq':'1100011', 'bne':'1100011', 'blt':'1100011', 'bge':'1100011', 'bltu':'1100011', 'bgeu':'1100011',

           'jal':'1101111',

           'lui':'0110111',

           'auipc':'0010111'
           }

funct3 = {'add':'000', 'sub':'000', 'addi':'000', 'lb':'000', 'sb':'000',
          'beq':'000', 'jal':'000', 'jalr':'000', 'ecall':'000', 'ebreak':'000',

          'sll':'001', 'slli':'001', 'lh':'001', 'sh':'001', 'bne':'001',

          'slt':'010', 'slti':'010', 'lw':'010', 'sw':'010',

          'sltu':'011', 'sltiu':'011',

          'xor':'100', 'xori':'100', 'lbu':'100', 'blt':'100',

          'srl':'101', 'sra':'101', 'srli':'101', 'srai':'101', 'lhu':'101', 'bge':'101',

          'or':'110', 'ori':'110', 'bltu':'110',

          'and':'111', 'andi':'111', 'bgeu':'111'}

funct7 = {'slli':'0000000', 'srli':'0000000', 'add':'0000000', 'sll':'0000000', 'slt':'0000000', 'sltu':'0000000',
          'xor':'0000000', 'srl':'0000000', 'or':'0000000', 'and':'0000000', 'ecall':'000000000000', 'ebreak':'000000000001',

          'srai':'0100000', 'sub':'0100000', 'sra':'0100000'}

R_types = ['add', 'sub', 'or', 'xor', 'and', 'sll', 'srl', 'sra', 'slt', 'sltu']

I_types = ['addi', 'xori', 'ori', 'andi', 'slli', 'srli', 'srai', 'slti', 'sltiu',
           'lb', 'lh', 'lw', 'lbu', 'lhu', 'jalr', 'ecall', 'ebreak']

S_types = ['sb', 'sh', 'sw']

SB_types = ['beq', 'bne', 'blt', 'bge', 'bltu', 'bgeu']

UJ_types = ['jal']

U_types = ['lui', 'auipc']

address = {}
pc = -4
data = []
name_write = ''
file_path = ''

def Bin(n, len):
    n = int(n)
    if n < 0:
        return bin(2 ** len + n)[2:]
    return bin(n)[2:].zfill(len)

def HexToBin(hex, len):
    int_num = int(hex[2:].upper(), 16)
    bin = Bin(int_num, len)
    return bin

def R_type(ins):
    bin = ''

    bin += funct7[ins[0]]
    bin += Bin(ins[3][1:], 5)
    bin += Bin(ins[2][1:], 5)
    bin += funct3[ins[0]]
    bin += Bin(ins[1][1:], 5)
    bin += opcodes[ins[0]]

    return bin + '\n'

def I_type(ins):
    bin = ''
    index = -1

    if ins[0] == 'ecall':
        bin = '00000000000000000000000001110011'

    elif ins[0] == 'ebreak':
        bin = '00000000000100000000000001110011'

    else:
        for x in ins:

            if x.isnumeric() is True or x.find('-') != -1:
                bin += Bin(x, 12)
                index = ins.index(x)

            elif x.find('0x') != -1:
                bin += HexToBin(x, 12)
                index = ins.index(x)

        if index == 3:
            if ins[0] == 'srai' or ins[0] == 'slli' or ins[0] == 'srli':
                bin = funct7[ins[0]] + bin[7:]
            bin += Bin(ins[2][1:], 5)
            bin += funct3[ins[0]]
            bin += Bin(ins[1][1:], 5)
            bin += opcodes[ins[0]]

        elif index == 2:
            bin += Bin(ins[3][1:], 5)
            bin += funct3[ins[0]]
            bin += Bin(ins[1][1:], 5)
            bin += opcodes[ins[0]]

    return bin + '\n'

def S_type(ins):
    bin = ''
    imm = ''

    if ins[2].isnumeric() is True:
        imm = Bin(ins[2], 12)

    elif ins[2].find('0x') != -1:
        imm = HexToBin(ins[2], 12)

    bin += imm[:7]
    bin += Bin(ins[1][1:], 5)
    bin += Bin(ins[3][1:], 5)
    bin += funct3[ins[0]]
    bin += imm[7:]
    bin += opcodes[ins[0]]

    return bin + '\n'

def SB_type(ins):
    global pc
    bin = ''
    imm = ''
    imm_number = 0
    if address.get(ins[3] + ':') != None:
        imm_number = address.get(ins[3] + ':') - pc
        imm = Bin(imm_number, 13)

    elif ins[3].find('0x') != -1:
        imm = HexToBin(ins[3], 13)

    else:
        imm = Bin(ins[3], 13)

    bin += imm[0]
    bin += imm[2:8]
    bin += Bin(ins[2][1:], 5)
    bin += Bin(ins[1][1:], 5)
    bin += funct3[ins[0]]
    bin += imm[8:12]
    bin += imm[1]
    bin += opcodes[ins[0]]

    return bin + '\n'

def UJ_type(ins):
    global pc
    bin = ''
    imm = ''

    if address.get(ins[2] + ':') != None:
        imm_number = address.get(ins[2] + ':') - pc
        imm = Bin(imm_number, 21)

    elif ins[2].find('0x') != -1:
        imm = HexToBin(ins[2], 21)

    else:
        imm = Bin(ins[2], 21)

    bin += imm[0]
    bin += imm[10:20]
    bin += imm[9]
    bin += imm[1:9]
    bin += Bin(ins[1][1:], 5)
    bin += opcodes[ins[0]]

    return bin + '\n'

def U_type(ins):
    bin = ''
    imm = ''

    if ins[2].find('0x') != -1:
        imm = HexToBin(ins[2], 20)

    else:
        imm = Bin(ins[2], 20)

    bin += imm
    bin += Bin(ins[1][1:], 5)
    bin += opcodes[ins[0]]

    return bin + '\n'

# clean the input risc v code file and print cleaned code in 'cleaned_risc_v_instruction.txt'
def clean_raw_code(file):
    global name_write

    data = file.readlines()
    name_write = file.name[:len(file.name)-2] + '_Cleaned.txt'
    #print(name_write)
    file.close()

    file = open(name_write, 'w')

    for i in range(0, len(data)):

        string1 = data[i]

        if string1.find('.text') != -1:

            for j in range(i + 1, len(data)):
                string2 = data[j]

                # xoa comments
                if string2.find('#') != -1:
                    string2 = string2[:string2.index('#')]
                if string2.find('//') != -1:
                    string2 = string2[:string2.index('//')]

                # xoa dau cham phay, dau ngoac
                string2 = string2.replace(',', ' ')
                string2 = string2.replace('(', ' ')
                string2 = string2.replace(')', ' ')

                # xoa khoang trang dau cuoi va dau \n
                string2 = string2.strip()

                # kiem tra instruction co chung dong voi label, neu co tach
                if string2.find(':') != -1:
                    if string2.find(':') != len(string2) - 1:
                        label = string2[0:string2.find(':') + 1]
                        instruction = string2[string2.find(':') + 1:]

                        # xoa khoang trang dau cuoi va dau \n
                        label = label.strip()
                        instruction = instruction.strip()

                        # xoa khoang trang du trong label
                        label = label.replace(' ', '')
                        label = label.replace('\t', '')

                        file.write(label + '\n')
                        file.write(instruction + '\n')
                    else:
                        # xoa khoang trang du trong label
                        string2 = string2.replace(' ', '')
                        string2 = string2.replace('\t', '')
                        file.write(string2 + '\n')
                else:
                    if string2 != '':
                        file.write(string2 + '\n')
    file.close()

# calculate the address of the labels
def calculate_address(file):
    global name_write
    global pc
    global data
    global address

    file = open(name_write, 'r')
    data = file.readlines()
    file.close()

    pc = -4

    # calculate the address of the labels
    for ins in data:
        if ins.find(':') != -1:
            address.update({(ins[:ins.find(':') + 1]): (pc + 4)})
        else:
            pc += 4

# generate risc_v code to binary code
def Generate_Binary_code(file):

    global name_write
    global pc
    global data

    file = open(name_write, 'r')
    name_write = os.path.basename(file.name)
    name_write = name_write[:len(name_write)-12]
    data = file.readlines()
    file.close()

    name_write = name_write[:4] + 'Binary_code_' + name_write[4:] + '.txt'
    #print(name_write)
    result_path = "C:/Users/Asus/Desktop/RISC-V-Assembler/RISC-V-Assembler/result_bin"
    name_write = f"{result_path}/{name_write}"
    file = open(name_write, 'w')

    pc = -4
    binary = ''

    for ins in data:
        if ins.find(':') == -1:

            pc += 4

            ins = ins.split()
            # print(ins)
            if R_types.count(ins[0]) != 0:
                binary += R_type(ins)

            elif I_types.count(ins[0]) != 0:
                binary += I_type(ins)

            elif S_types.count(ins[0]) != 0:
                binary += S_type(ins)

            elif SB_types.count(ins[0]) != 0:
                binary += SB_type(ins)

            elif UJ_types.count(ins[0]) != 0:
                binary += UJ_type(ins)

            else:
                binary += U_type(ins)
    file.write(binary)
    file.close()

def Main(file):
    global data
    global address

    clean_raw_code(file)

    calculate_address(file)

    Generate_Binary_code(file)

    data.clear()
    address.clear()

# Read text File
def read_text_file(file_path):
    with open(file_path, 'r') as file:
        Main(file)

# iterate through all file
#C:/Users/Asus/Desktop/RISC-V-Assembler/RISC-V-Assembler/testcase
src = input('Enter your testcase dir path: ')

import glob
import os

obj_list=glob.glob(src+"/**",recursive=True)
#print(obj_list)
cnt_fi = 0
cnt_dir = 0
for fi in obj_list:
    if fi.endswith('.S'):
        read_text_file(fi)






