"""
reads a log and extracts all process sequences
"""

import csv

class Row:
    def __init__(self, episodeId, activityEvent):
        self.episodeId = episodeId
        self.activityEvent = [activityEvent]
    def addActivity(self, activity):
        self.activityEvent.append(activity)
    def compare(self, other):
        return self.activityEvent == other.activityEvent
    def fillNulls(self, amount):
        for _ in range(amount):
            self.activityEvent.append("NULL")

rows = []
rowIndex = -1

with open('data/AllSeverityCodes.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=';')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            line_count += 1
        else:
            if(rowIndex == -1):
                tmpRow = Row(row[0], row[4])
                rows.append(tmpRow)
                rowIndex += 1
            else:
                currentRow = rows[rowIndex]
                # check if next row is same episode
                if(row[0] == currentRow.episodeId):
                    currentRow.addActivity(row[4])
                else: 
                    rows.append(Row(row[0], row[4]))
                    rowIndex += 1
            line_count += 1

    maxActivityLength = 0
    for row in rows:
        maxActivityLength = max(maxActivityLength, len(row.activityEvent) - 1)

    # filling everything with Nulls
    for row in rows:
        row.fillNulls(maxActivityLength - len(row.activityEvent))
    # creating the Headerstring
    # headerString = ["absoluteFreq"]
    headerString = []
    for x in range(maxActivityLength):
        headerString.append(f'Activity {x+1}')

    with open('results/step1/associationNaiv.csv', mode='w', newline='') as activityCsv:
        activityWriter = csv.writer(activityCsv, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        activityWriter.writerow(headerString)
        for row in rows:
            activityWriter.writerow(row.activityEvent)
print('associationNaiv done')
