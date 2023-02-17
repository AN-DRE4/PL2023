import csv


def read_data_file(filename):
    # Define a list to store the data
    data = []

    # Open the CSV file and read the rows
    with open(filename, 'r') as file:
        reader = csv.reader(file, delimiter=',')

        # Skip the header row
        next(reader)

        # Iterate over the remaining rows and create a dictionary for each row
        for row in reader:
            data.append({
                'idade': int(row[0]),
                'sexo': row[1],
                'tensao': int(row[2]),
                'colesterol': int(row[3]),
                'batimento': int(row[4]),
                'temDoenca': int(row[5])
            })

    # Return the list of dictionaries
    return data


def read_data(filename):
    data = []
    with open(filename, 'r') as f:
        for line in f:
            row = line.strip().split(',')
            if len(row) != 6:
                continue
            idade, sexo, tensao, colesterol, batimento, temDoenca = row
            if int(colesterol) == 0:
                continue
            data.append({
                'idade': int(idade),
                'sexo': sexo,
                'tensao': int(tensao),
                'colesterol': int(colesterol),
                'batimento': int(batimento),
                'temDoenca': int(temDoenca),
            })
    return data


def disease_distribution_by_gender(data):
    # Define dictionaries to store the count of disease by gender
    disease_by_gender = {'M': 0, 'F': 0}
    count_by_gender = {'M': 0, 'F': 0}

    # Iterate over the data and update the counts
    for row in data:
        sexo = row['sexo']
        temDoenca = row['temDoenca']

        if sexo in ['M', 'F']:
            count_by_gender[sexo] += 1

            if temDoenca:
                disease_by_gender[sexo] += 1

    # Calculate the percentage of disease by gender
    distribution = {
        'M': disease_by_gender['M'] / count_by_gender['M'] * 100,
        'F': disease_by_gender['F'] / count_by_gender['F'] * 100
    }

    # Return the distribution dictionary
    return distribution


def get_oldest_age(data):
    oldest_age = 0
    for row in data:
        idade = row['idade']
        if idade > oldest_age:
            oldest_age = idade

    return oldest_age


def disease_distribution_by_age_group(data):
    # Get the oldest age in the data
    oldest_age = get_oldest_age(data)

    # Define a dictionary to store the counts for each age group
    count_by_age_group = {f'{i}-{i + 4}': 0 for i in range(0, oldest_age + 1, 5)}

    # Define a dictionary to store the count of disease for each age group
    disease_by_age_group = {f'{i}-{i + 4}': 0 for i in range(0, oldest_age + 1, 5)}

    # Iterate over the data and update the counts for each age group
    for row in data:
        idade = row['idade']
        temDoenca = row['temDoenca']

        # Determine the age group for the current row
        age_group = f'{(idade // 5) * 5}-{((idade // 5) * 5) + 4}'

        count_by_age_group[age_group] += 1

        if temDoenca:
            disease_by_age_group[age_group] += 1

    # Calculate the percentage of disease for each age group
    distribution = {}
    for age_group in count_by_age_group:
        if count_by_age_group[age_group] > 0:
            distribution[age_group] = (
                    disease_by_age_group[age_group] / count_by_age_group[age_group] * 100
            )

    # Return the distribution dictionary
    return distribution


def find_highest_cholesterol(data):
    highest_cholesterol = 0

    for row in data:
        if row['colesterol'] > highest_cholesterol:
            highest_cholesterol = row['colesterol']

    return highest_cholesterol


def disease_distribution_by_colesterol(data):
    # Get the highest cholesterol in the data
    highest_cholesterol = find_highest_cholesterol(data)

    # Define a dictionary to store the counts for each cholesterol group
    count_by_cholesterol_group = {f'{i}-{i + 9}': 0 for i in range(0, highest_cholesterol + 1, 10)}

    # Define a dictionary to store the count of disease for each cholesterol group
    disease_by_cholesterol_group = {f'{i}-{i + 9}': 0 for i in range(0, highest_cholesterol + 1, 10)}

    # Iterate over the data and update the counts for each cholesterol group
    for row in data:
        colesterol = row['colesterol']
        temDoenca = row['temDoenca']

        # Determine the cholesterol group for the current row
        cholesterol_group = f'{(colesterol // 10) * 10}-{((colesterol // 10) * 10) + 9}'

        count_by_cholesterol_group[cholesterol_group] += 1

        if temDoenca:
            disease_by_cholesterol_group[cholesterol_group] += 1

    # Calculate the percentage of disease for each colesterol group
    distribution = {}
    for cholesterol_group in count_by_cholesterol_group:
        if count_by_cholesterol_group[cholesterol_group] > 0:
            distribution[cholesterol_group] = (
                    disease_by_cholesterol_group[cholesterol_group] / count_by_cholesterol_group[
                cholesterol_group] * 100
            )

    # Return the distribution dictionary
    return distribution


def distribution_to_table(distribution: dict):
    print("----|----------")
    for k in distribution.keys():
        print(f"{str(k)} | {str(distribution[k])}")


def main():
    data = read_data_file("myheart.csv")
    distrib = disease_distribution_by_gender(data)
    # print(distrib)
    distribution_to_table(distrib)
    distrib2 = disease_distribution_by_age_group(data)
    # print(distrib2)
    distribution_to_table(distrib2)
    distrib3 = disease_distribution_by_colesterol(data)
    # print(distrib3)
    distribution_to_table(distrib3)


if __name__ == "__main__":
    main()
