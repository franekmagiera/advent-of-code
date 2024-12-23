data = """
1
2
3
2024
""".strip()

with open("input_22", "r") as file:
    data = file.read().strip()

numbers = [int(number) for number in data.splitlines()]

def next_secret(secret):
    secret = ((secret * 64) ^ secret) % 16777216
    secret = ((secret // 32) ^ secret) % 16777216
    secret = (secret * 2048 ^ secret) % 16777216
    return secret

def get_nth_secret(secret, n):
    for _ in range(n):
        secret = next_secret(secret)
    return secret

# result = sum(get_nth_secret(number, 2000) for number in numbers)
# print(result)

# Part 2
def generate_secrets(secret, n):
    i = 0
    while i < n:
        yield secret
        secret = next_secret(secret)
        i += 1
    
prices = [
    [secret % 10 for secret in generate_secrets(number, 2000)]
    for number in numbers
]

# Preinitialize with 0s.
diffs = [
    [0 for price in seller]
    for seller in prices
]

for i, seller in enumerate(prices):
    for j, price in enumerate(seller):
        if j == 0:
            continue
        diffs[i][j] = prices[i][j] - prices[i][j-1]

# How to find the best combination of 4 price changes to get the maximum amount?
# Let's try complete search.

# For every seller, get the combination: price mapping.
seller_offers = []
for n, seller_prices in enumerate(prices):
    i = 1
    offers = {}
    while i + 3 < len(diffs[n]):
        combination = (diffs[n][i], diffs[n][i+1], diffs[n][i+2], diffs[n][i+3])
        price = seller_prices[i+3]
        if combination not in offers:
            offers[combination] = price
        i += 1
    seller_offers.append(offers)

# Get all possible combinations.
combinations = set(combination for offers in seller_offers for combination in offers)

best_profit = 0
best_combination = None
for combination in combinations: # (-2, 1, -1, 3):
    total_profit = 0
    for seller in seller_offers:
        price = seller.get(combination, 0)
        total_profit += price

    if total_profit > best_profit:
        best_profit = total_profit
        best_combination = combination

print(best_profit)
print(best_combination)
