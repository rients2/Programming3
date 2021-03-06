import pandas as pd
import shutil

df = pd.read_csv('output/kmars.csv',header=None)
df = df.drop_duplicates(subset=1, keep="last")
df = df[df[1] == df[1].max()]

kmar_len = int(df[0])
print(kmar_len)

og = f'/students/2021-2022/master/Rients_DSLS/output/{kmar_len}/contigs.fa'

target = '/homes/rdalstra/Documents/Programming3/Assignment4/output/contigs.fa'

shutil.move(og, target)

print('Done')