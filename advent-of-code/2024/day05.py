from pathlib import Path


def load(path):
    path = Path(path)
    return path.read_text()

# content = load('example.txt')
content = load('input.txt')

def parse():
    rules = []
    pages = []

    for line in content.splitlines():
        if '|' in line:
            rules.append(line.split('|'))
        elif ',' in line:
            pages.append(line.split(','))

    return rules, pages

rules, pages = parse()
print(rules)


def check(page_group):
    for i, page in enumerate(page_group):
        matching_rules = [r for r in rules if r[0]==page]

        for _, after in matching_rules:
            if after in page_group:
                if page_group.index(after) < i:
                    return False
        
    return True

def fix(page_group):
    page_group = list(page_group)

    while not check(page_group):
        for i, page in enumerate(page_group):
            matching_rules = [r for r in rules if r[0]==page]

            print(matching_rules)
            for _, after in matching_rules:
                if after in page_group:
                    if page_group.index(after) < i:
                        j = page_group.index(after)

                        page_group[i], page_group[j] = page_group[j], page_group[i]
    
    return [int(p) for p in page_group]

def p1():
    print(rules)

    total = 0
    total2 = 0

    for page_group in pages:
        if check(page_group):
            values = [int(p) for p in page_group]
            total += values[len(values)//2]
        else:
            fixed_values = fix(page_group)
            total2 += fixed_values[len(fixed_values)//2]

    return total, total2

print(p1())
