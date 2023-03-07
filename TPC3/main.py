import re
import json
from math import floor


def count_lines_by_year(filename):
    # Create an empty dictionary to store the counts for each year
    year_counts = {}

    # Open the file for reading
    with open(filename, 'r') as f:
        # Loop over each line in the file
        for line in f:
            # Split the line into its components
            parts = line.strip().split('::')
            num_of_process, date_str, *names = parts

            # Extract the year from the date
            year = date_str.split('-')[0]

            # Increment the count for this year in the dictionary
            year_counts[year] = year_counts.get(year, 0) + 1

    # Return the dictionary of year counts
    return year_counts


def count_processes_by_year(filename):
    # Create an empty dictionary to store the counts for each year
    year_counts = {}

    # Open the file for reading
    with open(filename, 'r') as f:
        # Define a regex pattern to match the date string
        date_pattern = r'\d{4}-\d{2}-\d{2}'

        # Loop over each line in the file
        for line in f:
            # Extract the date string using regex
            match = re.search(date_pattern, line)
            if not match:
                continue
            date_str = match.group(0)

            # Extract the year from the date
            year = date_str[:4]

            # Increment the count for this year in the dictionary
            year_counts[year] = year_counts.get(year, 0) + 1

    # Return the dictionary of year counts
    return dict(sorted(year_counts.items()))


def group_by_year():
    file = open("processos.txt", "r")
    years = dict()
    er_date = re.compile(r"(?P<year>\d+)-(?P<month>\d+)-(?P<day>\d+)")
    for line in file.readlines():
        process = er_date.search(line)
        if process is not None:
            year = process.groupdict().get("year")
            if year not in years:
                years[year] = 1
            else:
                years[year] = years[year] + 1
    file.close()
    return dict(sorted(years.items()))


def count_names_by_century(filename):
    # Create empty dictionaries to store the counts for first names and last surnames
    first_name_counts = {}
    last_name_counts = {}

    # Open the file for reading
    with open(filename, 'r') as f:
        # Define regex patterns to match first and last names
        """name_pattern = r"(?P<first_name>\w+)[^\d:-]+ (?P<last_name>\w+)"
        first_name_pattern = rf'{name_pattern}(?={name_pattern}*$)'
        last_name_pattern = rf'{name_pattern}$'"""

        first_name_pattern = r"(?P<first_name>\w+)[^\d:-]+"
        last_name_pattern = r"(?P<last_name>\w+)"

        # Loop over each line in the file
        for line in f:
            # Extract the date string using regex
            date_pattern = r'\d{4}-\d{2}-\d{2}'
            match = re.search(date_pattern, line)
            if not match:
                continue
            date_str = match.group(0)

            # Extract the year from the date
            year = int(date_str[:4])

            # Compute the century for this year
            century = (year - 1) // 100 + 1

            # Extract the first and last names using regex
            """first_name_match = re.search(first_name_pattern, line)
            print(first_name_match)
            last_name_match = re.search(last_name_pattern, line)
            print(last_name_match)"""
            name_match = re.search(first_name_pattern, line)
            # if first_name_match and last_name_match:
            if name_match:
                name = name_match.group()
                # print(name)

                first_name = name.split(" ")[0]
                # print(first_name)
                last_name = name.split(" ")[2]

                # Increment the count for this first name in this century
                if century not in first_name_counts:
                    first_name_counts[century] = {}
                first_name_counts[century][first_name] = first_name_counts[century].get(first_name, 0) + 1

                # Increment the count for this last name in this century
                if century not in last_name_counts:
                    last_name_counts[century] = {}
                last_name_counts[century][last_name] = last_name_counts[century].get(last_name, 0) + 1

    # Return the dictionaries of name counts by century
    return dict(sorted(first_name_counts.items())), dict(sorted(last_name_counts.items()))


def freq_names(filename):
    file = open(filename, "r")
    er_names = re.compile(r"(?P<first_name>\w+)[^\d:-]+ (?P<last_name>\w+)")
    er_date = re.compile(r"(?P<year>\d+)-(?P<month>\d+)-(?P<day>\d+)")
    all_first_names = dict()
    all_last_names = dict()
    for line in file.readlines():
        process = er_date.search(line)
        if process is not None:
            year = int(process.groupdict().get("year"))
            century = floor(year / 100) + 1

            first_last_name = er_names.findall(line)
            for f_l_name in first_last_name:
                first_name = f_l_name[0]
                # print(first_name)
                # add first name to dict
                if century not in all_first_names:
                    all_first_names[century] = {}
                all_first_names[century][first_name] = all_first_names[century].get(first_name, 0) + 1
                last_name = f_l_name[1]
                # add last name to dict
                if century not in all_last_names:
                    all_last_names[century] = {}
                all_last_names[century][last_name] = all_last_names[century].get(last_name, 0) + 1
    file.close()
    return dict(sorted(all_first_names.items())), dict(sorted(all_last_names.items()))


def freq_relation(filename):
    file = open(filename, "r")
    relation = {}
    pattern = r',[^\s*\d+][\w\s]*\.[\s]+Proc\.'
    match = re.compile(pattern)
    for line in file.readlines():
        rel = match.findall(line)
        if rel:
            for r in rel:
                r = str(r).lower()
                r = r[1:-7]
                if r not in relation:
                    relation[r] = 1
                else:
                    relation[r] = relation.get(r) + 1
    file.close()

    return dict(sorted(relation.items()))


def to_json(filepath: str):
    if re.match(r".json", filepath) is None:
        filepath = filepath + ".json"
    out_file = open(filepath, "w")
    file = open("processos.txt", "r")
    pattern = re.compile(
        r"(?P<id>\d+)::(?P<year>\d+)-(?P<month>\d+)-(?P<day>\d+)::(?P<nome>[\w\s]+)::(?P<nomePai>[\w\s]+)?::(?P<nomeMae>[\w\s]+)?::(?P<observacoes>.+[^:])?::")
    dict1 = {}
    for i in range(0, 20):
        sno = 'Linha ' + str(i + 1)
        line = file.readline()
        if pattern.search(line) is not None:
            data = pattern.search(line).groupdict()
            dict1[sno] = data
    json.dump(dict1, out_file, indent=8, sort_keys=False)
    out_file.close()
    file.close()


def split_first_last_name(name):
    return re.match(r"\w+\b", name).group(), re.search(r"\b\w+$", name).group()


def top5_names(filename):
    file = open(filename, "r")
    pattern = re.compile(
        r"(?P<id>\d+)::(?P<year>\d+)-(?P<month>\d+)-(?P<day>\d+)::(?P<nome>[\w\s]+)::(?P<nomePai>[\w\s]+)?::(?P<nomeMae>[\w\s]+)?")
    first_name, last_name = split_first_last_name()


def parse(path):
    file = open(path)
    regex_str = r"(?P<dir>\d+)::(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})::(?P<name>[\w\s]+)::(?P<father>[" \
                r"\w\s]+)::(?P<mother>[\w\s]+)::(?P<obs>[^:]*):: "
    res = []
    regex = re.compile(regex_str)
    for line in file.readlines():
        if match := regex.finditer(line):
            res = res + [m.groupdict() for m in match]

    return res


def top5_names_freq(data, century, idx):
    names = {}

    for entry in data:
        if (int(entry["year"]) - 1) // 100 + 1 == century:

            name = split_first_last_name(entry["name"])
            # print(name)
            if name[idx] not in names:
                names[name[idx]] = 0

            names[name[idx]] += 1

            father = split_first_last_name(entry["father"])
            if father[idx] not in names:
                names[father[idx]] = 0

            names[father[idx]] += 1

            mother = split_first_last_name(entry["mother"])
            if mother[idx] not in names:
                names[mother[idx]] = 0

            names[mother[idx]] += 1
    res = sorted(names.items(), key=lambda x: x[1], reverse=True)[:5]
    return res


def top5_names_freq_century(data):
    first_name = {}
    last_name = {}
    for i in range(0, 22):
        first_name[i] = top5_names_freq(data, i, 0)
        last_name[i] = top5_names_freq(data, i, 1)

    return first_name, last_name


def top5_names_freq_all(data):
    first_name, last_name = top5_names_freq_century(data)
    sum_first_name = {}
    sum_last_name = {}

    for names in first_name.values():
        for k, v in names:
            if k not in sum_first_name:
                sum_first_name[k] = v
            else:
                sum_first_name[k] += v

    for names in last_name.values():
        for k, v in names:
            if k not in sum_last_name:
                sum_last_name[k] = v
            else:
                sum_last_name[k] += v

    f_names = sorted(sum_first_name.items(), key=lambda x: x[1], reverse=True)[:5]
    l_names = sorted(sum_last_name.items(), key=lambda x: x[1], reverse=True)[:5]
    return f_names, l_names


def main():
    filename = "processos.txt"
    # print(count_processes_by_year("processos.txt"))
    # first_names, last_surnames = count_names_by_century("processos.txt")
    # print(first_names)
    # print(last_surnames)
    # print(freq_names(filename))
    # print(freq_relation(filename))
    data = parse(filename)
    print(top5_names_freq_century(data))
    print(top5_names_freq_all(data))
    to_json("teste")
    return


if __name__ == "__main__":
    main()
