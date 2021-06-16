

### INPPUT AND PREPROCESSING ###

k = int(input("Enter number of groups: "))

# number of tasks per group
n = [0] * k
for i in range(k):
    n[i] = int(input("Enter number of tasks in group " + str(i) + ": "))
# total number of tasks
N = sum(n)
    
# duration of tasks in each group
d = [0] * k
for i in range(k):
    d[i] = int(input("Enter duration of tasks in group " + str(i) + ": "))
# total completion time
C = 0
for i in range(k):
    C += n[i] * d[i]
    


### SOCIAL WELFARE ###
    
# fully random
sRandom = (N + 1) * C / 2

''' #long formula
s = 0
for i in range(k):
    s += n[i] * (C + d[i]) /2'''

    
# random within groups
sGroups = 0
for i in range(k):
    ci = n[i] * d[i]
    sGroups += n[i] * (ci + d[i]) / 2
    # externalities imposed on future groups
    sGroups += ci * sum(n[i+1:])
    
print("Social welfare:", sRandom, sGroups)
print("Ratio:", sRandom / sGroups)


# different types of random within groups when k > 2
sw = {}

# compute social welfare of groups last to pres combined
def computeSW(last, pres):
    cGroup = 0
    for i in range(last, pres + 1):
        cGroup += n[i] * d[i]
    
    intern = 0
    for i in range(last, pres + 1):
        intern += n[i] * (cGroup + d[i]) / 2

    extern = sum(n[pres+1:]) * cGroup
    return intern + extern
    
def generate(sep, last, pres, s):
    if pres == k-1:
        # compute last group
        sw[sep] = s + computeSW(last, pres)
        return
    generate(sep + '1', pres + 1, pres + 1, s + computeSW(last, pres))
    generate(sep + '0', last, pres + 1, s)

generate("", 0, 0, 0)



### INDIVIDUAL FAIRNESS ###
fRandom = 1

fGroups = 1
t = 0
for i in range(k):
    ci = n[i] * d[i]
    expected = t + (ci + d[i]) / 2
    random = (C + d[i]) / 2
    fi = expected / random
    fGroups = max(fi, fGroups)
    t += ci

print("Fairness:", fRandom, fGroups)

# different types of random within groups when k > 2
fd = {} # fairness dictionary

def computeF(last):
    # expected completion time in random assignment
    random = (C + d[last]) /2

    cGroup = 0
    for i in range(last, k):
        cGroup += n[i] * d[i]
    expected = (C - cGroup) + (cGroup + d[last]) / 2
    return expected / random
    
def generate2(sep, last, pres):
    if pres == k-1:
        fd[sep] = computeF(last)
        return
    generate2(sep + '1', pres + 1, pres + 1)
    generate2(sep + '0', last, pres + 1)

generate2("", 0, 0)



### DATA VISUALIZATION ###
import matplotlib.pyplot as plt

dataSW = []
dataF = []

for key, value in sw.items():
    dataSW.append(value)
    dataF.append(fd[key])

plt.scatter(dataSW, dataF)
plt.xlabel("social welfare")
plt.ylabel("fairness")
plt.show()



