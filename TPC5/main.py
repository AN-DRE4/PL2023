import re


def tratarNumero(numero_matches):
    if len(numero_matches) != 9:
        if numero_matches[0:2] == "00":
            return 2  # Número Internacional
    if numero_matches[0:3] == "601" or numero_matches[0:3] == "641":
        return 1  # Número Bloqueado
    if numero_matches[0] == "2":
        return 3  # Número Nacional
    if numero_matches[0:4] == "800":
        return 4  # Número Verde
    if numero_matches[0:4] == "808":
        return 5  # Número Azul
    return -1  # Número Inválido


def cabine_telefonica():
    str_ip = input("maq: Bem vindo(a), levante o auscultador para iniciar uma chamada (escreva LEVANTAR): \n")
    if str_ip != "LEVANTAR":
        print("maq: Ação inválida, tente novamente.\n")
        cabine_telefonica()
    else:
        while True:
            print("maq: Insira agora as moedas na máquina, para iniciar a chamada.\n")
            moedas_str = input(
                "maq: Escreva MOEDA seguido das moedas que quer inserir (Exemplo MOEDA 10c, 30c, 50c, 2e.)\n")
            if moedas_str == "ABORTAR":
                print("maq: Interrompendo atividade\n")
                break
            matches = re.findall(r"MOEDA\s([\dce,.\s]+)", moedas_str)
            if len(matches) == 0:
                print("maq: Ação inválida, tente novamente.\n")
                continue
            coins = []
            for match in matches:
                coins = match.split(', ')
            saldo = 0
            str_saldo = ""
            for coin in coins:
                if coin == "1c":
                    saldo += 0.01
                elif coin == "2c":
                    saldo += 0.02
                elif coin == "5c":
                    saldo += 0.05
                elif coin == "10c":
                    saldo += 0.1
                elif coin == "20c":
                    saldo += 0.2
                elif coin == "50c":
                    saldo += 0.5
                elif coin == "1e":
                    saldo += 1
                elif coin == "2e":
                    saldo += 2
                else:
                    str_saldo += coin + " - moeda inválida;"
            if str_saldo != "":
                print("maq: " + str_saldo + " saldo = " + str(saldo) + "€\n")
            else:
                print("maq: saldo = " + str(saldo) + "€\n")
            while True:
                print("maq: Insira o número que pretende ligar.\n")
                numero_str = input("maq: Escreva T= seguido do número que pretende ligar (Exemplo T=912345678)\n")
                if numero_str == "ABORTAR":
                    print("maq: Interrompendo atividade e devolvendo moedas\n")
                    print("maq: troco = " + str(saldo) + "€; Volte Sempre!\n")
                    break
                numero_matches = re.findall(r"T=(\d+)", numero_str)
                if len(numero_matches) == 0:
                    print("maq: Ação inválida, tente novamente.\n")
                    continue
                choice = tratarNumero(numero_matches[0])
                # TODO: Tratar o número consoante o tipo


def main():
    cabine_telefonica()
    return


if __name__ == "__main__":
    main()
