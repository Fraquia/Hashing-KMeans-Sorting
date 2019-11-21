import numpy as np
import random
import math
import time
import pickle
with open("passwords1.txt","r") as f:
    text=f.read()
text=text.split("\n")
text = text[:-1]
random.seed(1024)
def hash_function_coeff(number,length):
    hash_coeff=np.array([[random.randint(0,length-1) for i in range(20)]], dtype=object)
    for i in range(number-1):
        hash_coeff=np.concatenate((hash_coeff,np.array([[random.randint(0,n-1) for i in range(20)]])))
    return hash_coeff
def hashing(coeffs,text):
    for idx,passw in enumerate(text):
        ord_of_words=[]
        for alph in passw:
            ord_of_words.append(ord(alph))
        ord_of_words=np.array(ord_of_words, dtype=object)
        for coeff in coeffs:
            try:
                result=np.remainder(np.sum(coeff*ord_of_words),479252981)
                bloom_filter[result]=1
            except Exception as e1:
                print(e1)
                print(idx)
        if idx % 1000000 == 0:
            print("{} of them handled and saved.Keep going".format(idx))
            if idx % 10000000 == 0:
                np.save("bloom_filter.npy", bloom_filter)

def control_hash(coeffs,pass2,bloom_filter):
    not_inside=[]
    question_possitive=[]
    for idx,passw in enumerate(pass2):
        if idx % 10000 == 0:
            print(len(not_inside))
        ord_of_words=[]
        for alph in passw:
            ord_of_words.append(ord(alph))
        ord_of_words = np.array(ord_of_words, dtype=object)
        flag=1
        for coeff in coeffs:
            result=np.remainder(np.sum(coeff*ord_of_words),479252981)
            if not bloom_filter[result]:
                not_inside.append(idx)
                flag = 0
                break
        if flag:
            question_possitive.append(idx)


    return(not_inside,question_possitive)

#number of element inserted
n=len(text)
print(n)
# p is the false possitive rate
p=0.1
# number of filter that bloom need
m=-(n*np.log(p))/np.square(np.log(2))
## k number of hash function
k=(479252981/n)*np.log(2)
print(m)
bloom_filter=np.zeros(479252981,dtype=np.int)
coeff=hash_function_coeff(math.ceil(k),479252981)

start=time.time()
hashing(coeff,text)
with open("passwords2.txt", "r") as f:
    text=f.read()
text=text.split("\n")
text = text[:-1]
print(len(text))

print("It starts controll other list wait")
results=control_hash(coeff,text,bloom_filter)
end=time.time()

print("Bloom filter length",479252981)
print("number of hash function",math.ceil(k))
print("Number of elemnts",n)
print("Probability of false positive",p)
print('Number of duplicates detected: ', len(results[1]))
print('Notinside ', len(results[0]))
print(end-start)
with open('parrot.pkl', 'wb') as f:
    pickle.dump(results, f)
