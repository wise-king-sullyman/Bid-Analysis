#convert csv into list of rows
def rowList(file):
    import csv
    f = open(file)
    csv_f = csv.reader(f)
    rowList = []
    
    #create list from rows in csv
    for row in csv_f:
        rowList.append(row)
        
    return rowList
   
#remove all budget pricing rounds from dataset
def removeBudgets(file):
   table = rowList(file)
    
   for row in table:
        if 'Budget' in row[1]:
           table.remove(row)
        elif row[9] == ' ':
           table.remove(row)
   return table

#sort bids into wins and losses
def bidResult(file, result):

    rows = removeBudgets(file)
    wonBids = []
    lostBids = []
    
    for row in rows:
        if row[12] == 'W':
            wonBids.append(row)
        else:
            lostBids.append(row)
            
    if result == 'W':
        return wonBids
    elif result == 'L':
        return lostBids
    else:
        return rows
   
   
#convert rowList into a list of columns
def columnList(file):
    rows = removeBudgets(file)
    
    #hacky as fuck way to create column names
    Date = []
    Name = []
    Takeoff = []
    Pricing = []
    Win = []

    #hacky as fuck way to fill columns
    for row in rows:
        Date.append(row[0])
        Name.append(row[1])
        Takeoff.append(row[9])
        Pricing.append(row[10])
        Win.append(row[12])

    columnList = [Date, Name, Takeoff, Pricing, Win]

    return columnList
   
#search desired data set
def dataSearch(data, searchWord):
    searchResults = []
    
    for entry in data:
        if searchWord in entry:
            searchResults.append(entry)
            
    return searchResults

#return set of all estimators who have performed takeoff
def takeoffers(file):
   columns = columnList(file)
   estimators = []
   searchResults = dataSearch(columns[2], '')

   for result in searchResults:
      if result != '':
         estimators.append(result)
   
   return set(estimators)

#return won bids % of any specific estimator
def winRatio(file, estimator):

    winning_bids = bidResult(file, 'W')
    winning_bids_estimator = dataSearch(winning_bids, estimator)
    total_bids = bidResult(file, '')
    total_bids_estimator = dataSearch(total_bids, estimator)

    return len(winning_bids_estimator)/len(total_bids_estimator)

for estimator in takeoffers('Bids.csv'):
   print( estimator + ': ' + str(round((winRatio('Bids.csv', estimator)* 100), 2)))
