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
                print(name)

                first_name = name.split(" ")[0]
                print(first_name)
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
    pattern = r',[^\s*\d+][\w\s]*\.[ ]Proc\.'
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
    pattern = re.compile(r"(?P<id>\d+)[::]+(?P<year>\d+)-(?P<month>\d+)-(?P<day>\d+)[::]+(?P<name>[\w\s]+)")
    # pattern to get the id, year, month, day and name from a line in the format id::year-month-day::name

    for i in range(0, 20):
        line = file.readline(i)
        print(line)
        if pattern.search(line) != None:
            data = pattern.search(line).groupdict()
            print(data)
            out_file.write("{")
            for k, v in data.items():
                if k == "id":
                    out_file.write(f"\n    {str(k)}: {str(v)}")
                else:
                    out_file.write(f",\n    {str(k)}: {str(v)}")
            out_file.write("\n}\n")

    out_file.close()
    file.close()


def main():
    filename = "processos.txt"
    # print(count_processes_by_year("processos.txt"))
    # first_names, last_surnames = count_names_by_century("processos.txt")
    # print(first_names)
    # print(last_surnames)
    #print(freq_names(filename))
    #print(freq_relation(filename))
    to_json("teste")
    return


if __name__ == "__main__":
    main()
