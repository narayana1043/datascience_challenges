import csv

def make_data(data):
    print(data)


if __name__ == "__main__":
    with open('./loan_timing.csv') as file:
        data = csv.reader(file)
    for i in data:
        print(i)
    # make_data(data)
