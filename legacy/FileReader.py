import pandas as pd
with open("livedata.txt") as df:
    data =[]
    ColumnNames=[]
    for line in df:
        if len(line)> 100 and not line.startswith(" ID"):  # removes all unnecessary lines from the data
            for word in line.split():
                data.append(word)
        elif line.startswith(" ID"):
            for word in line.split():
                ColumnNames.append(word)


    #  The following line coverts the list to a nested list with each sublist having 26 elements
    data = [data[i:i + 25] for i in range(0, len(data), 25)]
    ColumnNames=ColumnNames[0:26]
    #  The following 3 lines remove a repeat column header and combine it into one
    ColumnNames.pop(17)
    ColumnNames.pop(17)
    ColumnNames.insert(17,"Sig-Strength")

df = pd.DataFrame(data,columns=ColumnNames)

print(df)

