import pyspark
from pyspark import SparkContext
from pyspark.sql import Row
from pyspark.sql import SQLContext
from pyspark import SparkFiles
from pyspark.sql.functions import mean
import pyspark.sql.functions as f
from pyspark.ml.stat import Correlation
import csv
import pandas as pd


sc = SparkContext('local[16]')
spark = SQLContext(sc)

df = spark.read.csv('/data/dataprocessing/interproscan/all_bacilli.tsv', sep=r'\t', header=False)

df = df.toDF('Protein_accession','Sequence_MD5_digest','Sequence_length','Analysis','Signature_accession',
             'Signature_description','Start_location','Stop_location','Score','Status','Date','INT_accession',
             'INT_description','GO_annotations','Pathways_annotations')

#1
quest1 = df.select('INT_accession').distinct().count()

#2. 
quest2 = df.select('Protein_accession').count() / df.select('Protein_accession').distinct().count()
#3
quest3df = df[df.GO_annotations.contains('GO')]
quest3 = quest3df.groupby('GO_annotations').count().orderBy("count", ascending=False).first()[0]

#4
# Its either this:
quest4df = df.withColumn('lenght', ( df['Stop_location'] - df['Start_location'] ))
quest4 = quest4df.select(mean('lenght')).collect()[0][0]
# Or this:
# quest4 = df.select(mean ('Sequence_length')).collect()[0][0]

#5
quest5df = df[df.INT_accession.contains('IPR0')]
quest5_list = quest5df.groupby('INT_accession').count().orderBy("count", ascending=False).take(10)
quest5 = []
for nr in range(0,len(quest5_list)):
    quest5.append(quest5_list[nr][0])

#6
quest6df = quest5df.withColumn('lenght', ( df['Stop_location'] - df['Start_location'] ) / df['Sequence_length'])
quest6df2 = quest6df[quest6df['lenght'] > 0.9]
quest6_list = quest6df2.groupby('INT_accession').count().orderBy("count", ascending=False).take(10)
quest6 = []
for nr in range(0,len(quest6_list)):
    quest6.append(quest6_list[nr][0])

#7
# Thank you stackoverflow https://stackoverflow.com/questions/48927271/count-number-of-words-in-a-spark-dataframe 
quest7df = df[df.INT_accession.isin('-') == False]
quest7_list = quest7df.withColumn('word', f.explode(f.split(f.col('INT_description'), ' ')))\
    .groupBy('word')\
    .count()\
    .sort('count', ascending=False)\
    .take(10)
quest7 = []
for nr in range(0,len(quest7_list)):
    quest7.append(quest7_list[nr][0])

#8
quest8_list = quest7df.withColumn('word', f.explode(f.split(f.col('INT_description'), ' ')))\
    .groupBy('word')\
    .count()\
    .sort('count', ascending=True)\
    .take(10)
quest8 = []
for nr in range(0,len(quest8_list)):
    quest8.append(quest8_list[nr][0])

#9
quest9_list = quest6df2.withColumn('word', f.explode(f.split(f.col('INT_description'), ' ')))\
    .groupBy('word')\
    .count()\
    .sort('count', ascending=False)\
    .take(10)
quest9 = []
for nr in range(0,len(quest9_list)):
    quest9.append(quest9_list[nr][0])

#10
quest10df = quest6df
quest10df2 = quest7df.groupby('INT_accession').count()
quest10df = quest10df.join(quest10df2,'INT_accession')
quest10 = quest10df.corr('lenght', 'count')

# Making the csv
output = {'question_nr' : range(1,11),
 'answers' : [quest1, quest2, quest3, quest4, quest5, quest6, quest7, quest8, quest9, quest10],
 'explain' : [quest1, quest2, quest3, quest4, quest5, quest6, quest7, quest8, quest9, quest10],
}
output = pd.DataFrame(output)
output.to_csv('/homes/rdalstra/Documents/Programming3/Assignment5/output/answers.csv', sep=',', index=False)