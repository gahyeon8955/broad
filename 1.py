word = input()
word = word.upper()
if len(word) > 1000000:
    raise("다시해")
alphabet_dictionary = dict()

for alphabet in word:
    if alphabet in alphabet_dictionary:
        alphabet_dictionary[alphabet] += 1
    else:
        alphabet_dictionary[alphabet] = 1

sorted_dict = sorted(alphabet_dictionary.items(),key= lambda x: x[1],reverse=True)


big = 0
big_word = ''
count = 0
for x,y in sorted_dict:
    if len(sorted_dict)==1:
        print(x)
        break
    elif y>big:
        big = y
        big_word = x
        count += 1
    elif y==big:
        print("?")
        break
    elif y<big:
        print(big_word)
        break


    