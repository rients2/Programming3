import matplotlib.pyplot as plt
nr = []
time_int = []

with open('output/timings.txt') as file:
    next(file)
    for row in file:
        row = row.replace('\n','')
        row = row.replace(' ','\t')
        row2 = row.split('\t',1)
        nr.append(int(row2[0]))
        time_int.append(float(row2[1]))

plt.plot(nr, time_int, color='green', label='Process time')
plt.xlabel('Nr of threads')
plt.ylabel('Time')
plt.title('Blast time per thread')
plt.legend()
plt.savefig('output/timings.png')
plt.close()