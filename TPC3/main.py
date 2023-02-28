import re


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



def main():
    # print(count_processes_by_year("processos.txt"))
    first_names, last_surnames = count_names_by_century("processos.txt")
    # print(first_names)
    print(last_surnames)
    return


if __name__ == "__main__":
    main()
