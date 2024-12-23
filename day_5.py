import re

data = """47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47

"""

with open("input_5", "r") as file:
    data = file.read()

rule_pattern = re.compile(r"\d+\|\d+")
update_pattern = re.compile(r"(\d+,)+\d")

rules = []
updates = []

for line in data.splitlines():
    if rule_pattern.match(line):
        rules.append(line)
    elif update_pattern.match(line):
        updates.append(line)

# Build a map page : set of pages which it has to be in front of

# Build map
relations = dict()
for rule in rules:
    numbers = rule.split("|")
    before = int(numbers[0])
    after = int(numbers[1])
    if relations.get(before) is None:
        relations[before] = set()
    relations[before].add(after)

updates = [[int(number) for number in line.split(",")] for line in updates]

def is_correct_update(update, relations):
    seen = set() 
    for page in update:
        if seen.intersection(relations.get(page, set())):
            return False
        seen.add(page)
    return True

def get_middle_page(update):
    assert len(update) % 2 == 1
    return update[len(update) // 2]

# Solution to part one:
# correct_updates = [update for update in updates if is_correct_update(update, relations)]
# print(sum(get_middle_page(update) for update in correct_updates))

# Solution to part two:
incorrect_updates = [update for update in updates if not is_correct_update(update, relations)]

def correct_update(update):
    correct = []
    seen = set()
    for page in update:
        if seen.intersection(relations.get(page, set())):
            # Insert the page in the correct place.
            # Just go left until you have all that you have to be in front of.
            pages_i_need_to_be_before = relations.get(page)
            seen_copy = seen.copy()
            i = len(correct) 
            while seen_copy.intersection(pages_i_need_to_be_before):
                i -= 1
                seen_copy.remove(correct[i])
            correct.insert(i, page)
        else:
            correct.append(page)
        seen.add(page)
    return correct

corrected_updates = [correct_update(update) for update in incorrect_updates]

print(sum(get_middle_page(update) for update in corrected_updates))
