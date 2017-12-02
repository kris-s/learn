#!/usr/local/bin/python3

def day_one(captcha):
    captcha = [int(c) for c in str(captcha)]
    total = 0
    for i, digit in enumerate(captcha):
        doubled = captcha[:]
        doubled.extend(captcha[:])
        if digit == doubled[i+1]:
            total += digit
    return total


def day_two(spreadsheet):
    checksum = 0
    for row in spreadsheet.split('\n'):
        row = [int(val) for val in row.split()]
        if row:
            checksum += max(row) - min(row)
    return checksum
