
from typing import List
import csv

from fastapi import requests


def get_random_numbers() -> List[int]:
    url="https://www.random.org/integers/?num=8000&min=0&max=36&col=10&base=10&format=plain&rnd=new"
    resp = requests.get(url)
    text = resp.text   
    numbers = []
    for line in text.strip().split('\n'):
        numbers.extend([int(num) for num in line.split()])

    import time
    time.sleep(2)  # To avoid hitting the API rate limit
    return numbers


def save_random_numbers_to_csv(filename: str = "random_numbers.csv", iterations: int = 10) -> None:
    """
    Calls get_random_numbers 10 times and saves all results to a CSV file.
    
    Args:
        filename: The name of the CSV file to save to
        iterations: Number of times to call get_random_numbers (default 10)
    """
    all_numbers = []
    
    for i in range(iterations):
        print(f"Fetching batch {i + 1}/{iterations}...")
        numbers = get_random_numbers()
        all_numbers.extend(numbers)
    
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['random_number'])  # Header
        for num in all_numbers:
            writer.writerow([num])
    
    print(f"Saved {len(all_numbers)} random numbers to {filename}")


if __name__ == "__main__":
    save_random_numbers_to_csv()