# + - * / %


digito = input('Faça o seu caluculo: ').replace('+',' + ').replace('-',' - ').replace('*',' * ').replace('*',' * ').replace('%',' % ').strip().split()

resultado = 0

for ind in range(len(digito)):
    if digito[ind] == '+':
        break
        
