import math

pergunta = input("Qual unidade você deseja converter?\n[1] - Comprimento.\n[2] - Massa (Peso).\n[3] - Volume.\n[4] - Temperatura.\n[5] - Área.\n[6] - Velocidade.\n[7] - Pressão.\n[8] - Energia.\n[9] - Tempo.\n[10] - Fluxo de Carga Elétrica.\n")

if pergunta == "1":
    print("Você escolheu Comprimento. Adicione o valor que deseja converter e a unidade de origem no final do numero.")
    print("As unidades aceitas são: km, m, cm, mm, mi, yd, ft, in.")
    print("Exemplo: 1.5 km, 2.5 m, 3.0 cm, 4.0 mm, 5.0 mi, 6.0 yd, 7.0 ft, 8.0 in.")
    valor = input("Valor: ")
    
    if valor[-2].isnumeric():
        match valor[-1]:
            case "m":
                valor = float(valor[:-1]) # remove o 'm' do final
                print(f'\n{valor} m = {valor / 1000:,.2f} km (quilômetros)')
                print(f'{valor} m = {valor * 1:,.2f} m (metros)')
                print(f'{valor} m = {valor * 100:,.2f} cm (centímetros)')
                print(f'{valor} m = {valor * 1000:,.2f} mm (milímetros)')
                print(f'{valor} m = {valor * 0.000621371:,.2f} mi (milhas)')
                print(f'{valor} m = {valor * 1.09361:,.2f} yd (jardas)')
                print(f'{valor} m = {valor * 3.28084:,.2f} ft (pés)')
                print(f'{valor} m = {valor * 39.3701:,.2f} in (polegadas)')
                
       
            

