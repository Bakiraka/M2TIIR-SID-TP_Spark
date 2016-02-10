from pyspark import SparkContext
#Module for reducebykey function
from operator import add

#Context definition
sc = SparkContext(appName="truckcount")

# File reading
text_file = sc.textFile("/home/debian/data/data/generalvehicle.txt")

#filter out header
file_header = text_file.first()
data = text_file.filter(lambda x: x != file_header)

counted_tuples = data.map(lambda line: line.split("\t")) \
                     .filter(lambda x: x[5] >= '60' and x[5] <= '70' or x[5]==70 or x[5]==74 or x[5]==78 ) \
                     .filter(lambda x: x[60] > 0) \
                     .map(lambda x: x[5]) \
                     .map(lambda x: (x,1)) \
                     .reduceByKey(add) \
                     .collect()

print sum(pair[1] for pair in counted_tuples)


