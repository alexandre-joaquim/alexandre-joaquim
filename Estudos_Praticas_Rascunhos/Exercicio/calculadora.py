from numpy.ma.core import indices

# 1+1
digitos = input("Calculo: ")
digitos.replace(" ","")
for i in range(0,len(digitos)):
    if digitos[i].isnumeric():
        print("sim")
    else:
        print("no")