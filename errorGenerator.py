import os
import random
#import multiprocessing as mp

fileName = 'simulated_data_5000a.tsv'
os.chdir('/home/deney/Dropbox/doutorado/Bioinfo/projetos_paralelos/Simulated_data/') #Set local dos arquivos

#Exemplo de dataset:
#id	NOME	DTNASC	SEXO	NOMEMAE
#ID_3767986_l	SUZARA SALAZAR CALIXTO GOUVEIA	1968-07-28	F	AMANAIARA MELLO APARICIO CALIXTO
#ID_6080801_l	JOVANEA AMORIM FERNANDES ARAUJO	1999-06-14	F	OACIR ZAGANELLI SILVA FERNANDES

#Setup:
n = 5000
#------------------------------------#Porcentagem de erros:
sub_1 = int(0.35 * n)                #1. Uma substituição
del_1 = int(0.05 * n)                #2. Uma deleção
sub_2 = int(0.07 * n)                #3. Duas substituições
sub_3 = int(0.03 * n)                #4. Três substituições
del_nome_meio_mae = int(0.30 * n)    #5. Remove nome-meio mãe
del_nome_meio_pac = int(0.10 * n)    #6. Remove nome-meio paciente
nome_mae_casada = int(0.09 * n)      #7. Remove ultimo nome da mãe
mae_desconhecida = int(0.01 * n)     #8. Remove nome da mãe

def splited(fileName):
    with open(fileName, 'r') as file:
        seq = file.read()
        seq = seq[:-1].strip('\t').rsplit('\n')
    
    splited = []
    for i in seq[1:]:
        x1 = i.rsplit('\t')
        splited.append(x1)
    return (splited, seq)

splited, seq = splited(fileName)

def get_key(val):
    optionsDic = {'S':'Z', 'Z':'S',                 
                 'N':'M', 'M':'N',
                 'E':'I', 'I':'E',
                 'A':'O', 'O':'U',
                 'U':'O'}

    for key, value in optionsDic.items():
         if val == value:
             return key
    return val

def checkKey(options, var):
    key = random.choice(options)
    value = get_key(key)
    
    while (key == value):
        key = random.choice(options)
        value = get_key(key)
        
    while (key not in i[var]):
        key = random.choice(options)
        value = get_key(key)
        if key == value:
            key = '**'
    return (key, value)

options = ['S','Z','N','M','A','E','I','O','U']
optionsNum = ['0','1','2','3','4','5','6','7','8','9']
alphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 
            'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

sobrenomesMaes = [] #cria lista de sobrenomes para o proximo passo (8)

with open(fileName.rsplit('.',1)[0]+'_imputed_error.tsv', 'w') as f:
    f.write(seq[0] + '\n')
    count = 1
    sobreNome = 0
    for i in splited:
        #1. Gera um erro de grafia no nome do paciente[1]/mae[4]/data[2]:
        if count <= sub_1:
            options1 = [1,2,4]
            var = random.choice(options1)
            if var == 1:
                key, value = checkKey(options, var)
                f.write(i[0] +  '\t'+ i[1].replace(key, value, 1) + #paciente
                                '\t'+ i[2] +                        #data nascimento
                                '\t'+ i[3] + 
                                '\t'+ i[4] + '\n')                  #mae
            elif var == 2:
                key = random.choice(optionsNum)
                while (key not in i[var]):
                    key = random.choice(optionsNum)
                f.write(i[0] + '\t'+ i[1] +                         #paciente
                               '\t'+ i[2].replace(key, random.choice(optionsNum), 1) + #data nascimento
                               '\t'+ i[3] + 
                               '\t'+ i[4] +'\n')                    #mae
            elif var == 4:
                key, value = checkKey(options, var)
                f.write(i[0] + '\t'+ i[1] +                         #paciente
                               '\t'+ i[2] +                         #data nascimento
                               '\t'+ i[3] + 
                               '\t'+ i[4].replace(key, value, 1) + '\n') #mae
        
        elif (count <= (sub_1 + del_1)):
            #2. Deleta uma letra do nome do paciente[1]/mae[4]:
            options2 = [1, 4]
            var = random.choice(options2)
            if var == 1:
                key = random.choice(alphabet)
                while (key not in i[var]):
                    key = random.choice(alphabet)
                    if key == value:
                        key = '**'
                f.write(i[0] +  '\t'+ i[1].replace(key, '', 1) + #paciente
                                '\t'+ i[2] +                     #data nascimento
                                '\t'+ i[3] + 
                                '\t'+ i[4] +'\n')                #mae
            
            elif var == 4:
                key = random.choice(alphabet)
                while (key not in i[var]):
                    key = random.choice(alphabet)
                    if key == value:
                        key = '**'
                f.write(i[0] +  '\t'+ i[1] +                         #paciente
                                '\t'+ i[2] +                         #data nascimento
                                '\t'+ i[3] + 
                                '\t'+ i[4].replace(key, '', 1) +'\n') #mae
        
        elif (count <= (sub_1 + del_1 + sub_2)):
            #3. Gera dois erros de grafia no nome da mãe e do paciente:
            var1 = 1
            var4 = 4
            key1, value1 = checkKey(options, var1)
            key4, value4 = checkKey(options, var4)
            f.write(i[0] + '\t'+ i[1].replace(key1, value1, 1) +   #paciente
                           '\t'+ i[2] +                            #data nascimento                       
                           '\t'+ i[3] + 
                           '\t'+ i[4].replace(key4, value4, 1) +'\n') #mae
        
        elif (count <= (sub_1 + del_1 + sub_2 + sub_3)):
            #4. Gera três erros de grafia no nome da mãe (2) e do paciente (1):
            var1 = 1
            var2 = 2
            var4 = 4
            key1, value1 = checkKey(options, var1)
            
            key2 = random.choice(optionsNum)
            while (key2 not in i[var2]):
                key2 = random.choice(optionsNum)
            
            key4, value4 = checkKey(options, var4)
            f.write(i[0] + '\t'+ i[1].replace(key1, value1, 1) +   #paciente
                           '\t'+ i[2].replace(key2, random.choice(optionsNum), 1) + #data nascimento                       
                           '\t'+ i[3] + 
                           '\t'+ i[4].replace(key4, value4, 2) +'\n') #mae
               
        elif (count <= (sub_1 + del_1 + sub_2 + sub_3 + del_nome_meio_mae)):
            #5. Remove o nome do meio da mae:
            if len(i[4].split()) >= 4:
                f.write(i[0] +           
                            '\t'+ i[1] +                #paciente
                            '\t'+ i[2] +                #data nascimento
                            '\t'+ i[3] + 
                            '\t'+ i[4].split(' ')[0] +' '+ i[4].split(' ')[1] +' '+ i[4].split(' ')[-1]  +'\n')    #mae
                
                if len(sobrenomesMaes) < nome_mae_casada:
                    sobrenomesMaes.append(i[4].split(' ')[2])
            else:
                f.write(i[0] +           
                            '\t'+ i[1] +                #paciente
                            '\t'+ i[2] +                #data nascimento
                            '\t'+ i[3] + 
                            '\t'+ i[4].split(' ')[0] +' '+ i[4].split(' ')[-1]  +'\n')    #mae
            
                if len(sobrenomesMaes) < nome_mae_casada:
                    sobrenomesMaes.append(i[4].split(' ')[1])
   
        elif (count <= (sub_1 + del_1 + sub_2 + sub_3 + del_nome_meio_mae + del_nome_meio_pac)):
            #6. Remove o nome do meio do paciente:
            if len(i[1].split()) >= 4:
                f.write(i[0] +           
                            '\t'+ i[1].split(' ')[0] +' '+ i[1].split(' ')[1] +' '+ i[1].split(' ')[-1] +    #paciente
                            '\t'+ i[2] +                #data nascimento
                            '\t'+ i[3] + 
                            '\t'+ i[4] +'\n')           #mae
            else:    
                f.write(i[0] +           
                            '\t'+ i[1].split(' ')[0] +' '+ i[1].split(' ')[-1] +                #paciente
                            '\t'+ i[2] +                #data nascimento
                            '\t'+ i[3] + 
                            '\t'+ i[4] +'\n')    #mae
        
        elif (count <= (sub_1 + del_1 + sub_2 + sub_3 + del_nome_meio_mae + del_nome_meio_pac + mae_desconhecida)):
            #7. Mãe desconhecida:
            f.write(i[0] +  '\t'+ i[1] +                           #paciente
                            '\t'+ i[2] +                           #data nascimento
                            '\t'+ i[3] + 
                            '\t'+ '' +'\n')                        #mae
               
        elif (count <= (sub_1 + del_1 + sub_2 + sub_3 + del_nome_meio_mae + del_nome_meio_pac + mae_desconhecida + nome_mae_casada)):
            #8. Mãe nome casada:
            f.write(i[0] +  '\t'+ i[1] +                           #paciente
                            '\t'+ i[2] +                           #data nascimento
                            '\t'+ i[3] + 
                            '\t'+ i[4].split(' ')[0] +' '+ i[4].split(' ')[1] + ' ' + sobrenomesMaes[sobreNome] +'\n') #mae
            sobreNome += 1
        count += 1