import re


def formatoSaldo(amount):
    euros = int(amount)
    cents = int(round((amount - euros) * 100)) if amount != euros else None
    if cents is not None:
        return f"{euros}e{cents:02d}c"
    else:
        return f"{euros}e"


def tratarNumero(numero_matches):
    if len(numero_matches) != 9:
        if numero_matches[0:2] == "00":
            return 2  # Número Internacional
    elif numero_matches[0:3] == "601" or numero_matches[0:3] == "641":
        return 1  # Número Bloqueado
    elif numero_matches[0] == "2":
        return 3  # Número Nacional
    elif numero_matches[0:3] == "800":
        return 4  # Número Verde
    elif numero_matches[0:3] == "808":
        return 5  # Número Azul
    return -1  # Número Inválido


def calculate_change(change):
    coins = {
        "2e": 200,
        "1e": 100,
        "50c": 50,
        "20c": 20,
        "10c": 10,
        "5c": 5,
        "2c": 2,
        "1c": 1,
    }

    change_in_cents = int(round(change * 100))
    coin_counts = {}

    for coin, value in coins.items():
        count = change_in_cents // value
        if count > 0:
            coin_counts[coin] = count
            change_in_cents -= count * value

    coin_list = []
    for coin, count in coin_counts.items():
        coin_str = f"{count}x{coin}"
        coin_list.append(coin_str)

    return ", ".join(coin_list)


def cabine_telefonica():
    str_ip = input("maq: Bem vindo(a), levante o auscultador para iniciar uma chamada (escreva LEVANTAR): \n")
    saldo = 0
    pousar = False
    if str_ip != "LEVANTAR":
        print("maq: Ação inválida, tente novamente.\n")
        cabine_telefonica()
    else:
        while not pousar:
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
                print("maq: saldo = " + formatoSaldo(saldo) + "\n")
            while True:
                print("maq: Insira o número que pretende ligar.\n")
                numero_str = input("maq: Escreva T= seguido do número que pretende ligar (Exemplo T=912345678)\n")
                if numero_str == "ABORTAR":
                    print("maq: Interrompendo atividade e devolvendo moedas\n")
                    print("maq: troco = " + str(calculate_change(saldo)) + "; Volte Sempre!\n")
                    break
                if numero_str == "POUSAR":
                    pousar = True
                    break
                numero_matches = re.findall(r"T=(\d+)", numero_str)
                if len(numero_matches) == 0:
                    print("maq: Ação inválida, tente novamente.\n")
                    continue
                choice = tratarNumero(numero_matches[0])
                match choice:
                    case 1:
                        print("maq: Esse número não é permitido neste telefone. Queira discar novo número!\n")
                        continue
                    case 2:
                        if saldo >= 1.5:
                            saldo -= 1.5
                            print("maq: saldo = " + formatoSaldo(saldo) + "\n")
                        else:
                            print("maq: Saldo insuficiente para ligação internacional. Insira mais dinheiro!\n")
                            break
                    case 3:
                        if saldo >= 0.25:
                            saldo -= 0.25
                            print("maq: saldo = " + formatoSaldo(saldo) + "\n")
                        else:
                            print("maq: Saldo insuficiente para ligação internacional. Insira mais dinheiro!\n")
                            pass
                    case 4:
                        print("maq: Chamada nacional não cobra tarifa.\n")
                        print("maq: saldo = " + formatoSaldo(saldo) + "\n")
                    case 5:
                        if saldo >= 0.1:
                            saldo -= 0.1
                            print("maq: saldo = " + formatoSaldo(saldo) + "\n")
                        else:
                            print("maq: Saldo insuficiente para ligação internacional. Insira mais dinheiro!\n")
                            pass
                    case _:
                        print("maq: O número que inseriu não é válido, insira um novo.\n")
                        continue
        print("maq: troco = " + str(calculate_change(saldo)) + "; Volte Sempre!\n")
        return


def main():
    cabine_telefonica()
    return


if __name__ == "__main__":
    main()
