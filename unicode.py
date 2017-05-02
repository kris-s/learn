import hashlib
from unicodedata import normalize

yes1 = "\u0079\u0065\u0301\u0073"  # yés
yes2 = "\u0079\u00E9\u0073"        # yés

print()
print("Not normalized:", yes1, yes2, yes1 == yes2)
# >>> yés yés False

yes1_normal = normalize('NFC', yes1)
yes2_normal = normalize('NFC', yes2)

print("    Normalized:", yes1_normal, yes2_normal, yes1_normal == yes2_normal)
# >>> yés yés True

print("\nUsing NFC normalization, both strings now contain the same codepoints.")
for i, c in enumerate(yes1_normal):
    print('yes1: U+%04X' % ord(c), 'yes2: U+%04X' % ord(yes2_normal[i]))


yes1_hash = hashlib.sha1()
yes1_hash.update(yes1.encode())

yes2_hash = hashlib.sha1()
yes2_hash.update(yes2.encode())

print("\nNot normalized:")
print(yes1_hash.digest().hex())
print(yes2_hash.digest().hex())

yes1_hash = hashlib.sha1()
yes2_hash = hashlib.sha1()
yes1_hash.update(yes1_normal.encode())
yes2_hash.update(yes2_normal.encode())

print("\nNormalized:")
print(yes1_hash.digest().hex())
print(yes2_hash.digest().hex())
