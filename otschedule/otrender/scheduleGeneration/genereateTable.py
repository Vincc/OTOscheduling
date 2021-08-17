
dates = ["date1", "date2", "date3"]
times = ["10:40","2:40"]
students = ["1a,2a,3a,4a,5a", "1b,2b,3b,4b,5b", "1b,2b,3b,4b,5b"]

timesind = [[x%len(times) for x in range(len(i.split(",")))] for i in students]
datesind = [[x//round(len( i.split(","))/len(dates)) for x in range(len( i.split(",")))] for i in students]
print(timesind)
print(datesind)
