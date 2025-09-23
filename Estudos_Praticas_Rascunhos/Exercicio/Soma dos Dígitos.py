valor = int(input("Digite um número: "))
no = 0

for i in range(len(str(valor))):
    no += int(str(valor)[i])

print(f"Soma dos dígitos: {no}")


####################################################################
valor = int(input("Digite um número: ")) # Solicita um número ao usuário
soma = sum(int(d) for d in str(valor))  # transforma o número em string, o "d" passa indice por indece e converte de volta para inteiro e soma
print(f"Soma dos dígitos: {soma}")