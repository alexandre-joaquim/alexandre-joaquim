valor = int(input("Digite um número inicial: "))
valorf = int(input("Digite um número final: "))

#se o valor inicial for menor que o valor final então para cada numero no intervalo de valor inicial até o valor final-1 será contado de 2 em 2 negativo e irá imprimindo
#caso contrário, irá imprimir que o início deve ser maior que o fim
if valor > valorf:
    for i in range(valor , valorf-1, -2):
        print(i)
else:
    print("Início deve ser maior que o fim.")