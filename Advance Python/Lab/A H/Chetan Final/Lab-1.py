import re
from datetime import datetime
import os

def process(row: str, products: dict[str, int], ratings: dict[str, int]) -> None:
    pattern = re.compile("\"[^\"]*\"")
    row = re.sub(pattern, "", row).strip().split()
    if len(row) > 4:
        raise ValueError("Extra Values")
    if len(row[0]) == 6 or row[0].isalnum():
        if len(row[1]) == 10 or row[1].isalnum():
            if datetime.strptime(row[2], "%Y-%m-%d"):
                if 1 <= int(row[3]) <= 5:
                    products[row[1]] = products.get(row[1], 0) + 1
                    ratings[row[1]] = ratings.get(row[1], 0) + int(row[3])
                    return
    raise ValueError("Some Error")

def read(file: str, products: dict[str, int], ratings: dict[str, int]) -> tuple[int, int]:
    valid, invalid = 0, 0
    try:
        with open(file.replace("\\", "/"), "r") as f:
            for row in f.readlines():
                try:
                    process(row, products, ratings)
                    valid += 1
                except:
                    invalid += 1
    except Exception as e:
        print(f"Cannot open file {file}\nError: {e}")
    return valid, invalid

def start(dir: str, products: dict[str, int], ratings: dict[str, int]) -> tuple[int, int]:
    valid, invalid = 0, 0
    for name in os.listdir(dir):
        file = os.path.join(dir, name)
        if os.path.isfile(file):
            v, i = read(file, products, ratings)
            valid, invalid = valid + v, invalid + i
        elif os.path.isdir(file):
            v, i = start(file, products, ratings)
            valid, invalid = valid + v, invalid + i
    return valid, invalid

def main():
    dir = r"files"
    products, ratings = {}, {}
    valid, invalid = start(dir, products, ratings)
    average = {p: ratings[p] / products[p] for p in products}
    top_keys = sorted(average, reverse=True, key=lambda x: average[x])[:3]
    with open("summary.txt", "w+") as f:
        f.write(f"1) The total number of reviews processed -> {valid + invalid}\n")
        f.write(f"2) The total number of valid reviews -> {valid}\n")
        f.write(f"3) The total number of invalid reviews -> {invalid}\n")
        f.write("4) Top 3 products with the highest average ratings\n")
        for i, key in enumerate(top_keys):
            f.write(f"\t{i+1}) {key} -> {average[key]}\n")

if __name__ == "__main__":
    main()
