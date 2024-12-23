data = "125 17"

with open("input_11", "r") as file:
    data = file.read()

stones = list()
for number in data.split():
    stones.append(int(number))

def count_digits(number):
    return len(str(number))

def split_even_number(number):
    number = str(number)
    return int(number[:len(number)//2]), int(number[len(number)//2:])

def blink(stone, times) -> int:  
    stones = dict()  # number: count
    stones[stone] = 1
    for _ in range(times):
        new_stones = dict()
        for stone in stones:
            if stone == 0:
                new_stones[1] = new_stones.get(1, 0) + stones[stone]
            elif count_digits(stone) % 2 == 0:
                left, right = split_even_number(stone)
                new_stones[left] = new_stones.get(left, 0) + stones[stone]
                new_stones[right] = new_stones.get(right, 0) + stones[stone]
            else:
                new_stones[stone * 2024] = new_stones.get(stone * 2024, 0) + stones[stone]
        stones = new_stones
    return sum(stones[stone] for stone in stones) 

print(sum(blink(stone, 75) for stone in stones))
