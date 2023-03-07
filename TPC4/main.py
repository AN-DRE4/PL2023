import re


def parse_csv(filename):
    res = []
    with open(filename, "r") as f:
        lines = f.readlines()
        for line in lines:
            regex = re.split(r",", line)
            # remove \n
            regex[-1] = regex[-1].replace("\n", "")
            print(regex)
            res.append(regex)
    return res


def to_json(lista):
    with open("alunos1.json", "w") as f:
        f.write("[\n")
        for i in range(len(lista)):
            f.write("{\n")
            f.write(f"\"nome\": \"{list[i][0]}\",\n")
            f.write(f"\"numero\": \"{list[i][1]}\",\n")
            f.write(f"\"email\": \"{list[i][2]}\",\n")
            f.write(f"\"nota\": \"{list[i][3]}\"\n")
            if i != len(list) - 1:
                f.write("},\n")
            else:
                f.write("}\n")
        f.write("]\n")
    return


def main():
    lista = parse_csv("alunos1.csv")
    to_json(lista)
    return


if __name__ == "__main__":
    main()
