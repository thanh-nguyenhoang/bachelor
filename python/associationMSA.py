"""
reads a log and extracts all process sequences
"""

import csv

# ASCII range (A:65 Z:90)
# number = 97.
# ascii = chr(number)
# print(ascii)


def getNextAscii():
    num = 65
    while True:
        yield num
        num += 1
        if num > 90:
            raise ValueError(
                "Data set contains more than 24 unique events, either increase the range from A:Z to a bigger range or make less unique events")


class Row:
    def __init__(self, episodeId, activityEvent):
        self.episodeId = episodeId
        self.activityEvent = [activityEvent]
        self.pseudoActivityEvent = [activityEvent]
        self.fasta = []

    def addActivity(self, activity):
        self.activityEvent.append(activity)
        self.pseudoActivityEvent.append(activity)

    def compare(self, other):
        return self.activityEvent == other.activityEvent

    def fillNulls(self, amount):
        for _ in range(amount):
            self.activityEvent.append("NULL")

    def pseudoToString(self):
        return ''.join(self.pseudoActivityEvent)

rows = []
rowIndex = -1


with open('data/AllSeverityCodes.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=';')
    line_count = 0
    # Read the file into rows object
    for row in csv_reader:
        if line_count == 0:
            # Skip header
            print("reading Header")
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

    # Replacing all the characters
    gen = getNextAscii()
    translateDictionary = {}
    rows: Row
    for row in rows:
        row: Row
        for index, event in enumerate(row.activityEvent):
            if event in translateDictionary:
                pass
            else:
                translateDictionary[event] = chr(next(gen))
            replaceChar = translateDictionary[event]
            row.pseudoActivityEvent[index] = replaceChar
    print("replaced all characters")
    # longest_length = 0
    invTranslateDictionary = {v: k for k, v in translateDictionary.items()}
    ofile = open("results/step1/transponiertFasta.fasta", "w")
    for i in range(len(rows)):
        ofile.write(">" + rows[i].episodeId + "\n" +
                    rows[i].pseudoToString() + "\n")
    ofile.close()
    print("written fasta file")
    sequences = []
    for i in range(len(rows)):
        sequences.append(rows[i].pseudoToString())
    
    import subprocess
    msa = subprocess.run(["clustalo", "-i", "results/step1/transponiertFasta.fasta", "-o", "results/step1/msa.fasta", "--force", "-v"])
    print(msa)

from Bio import SeqIO
for index, record in enumerate(SeqIO.parse("results/step1/msa.fasta", "fasta")):
    fasta = []
    for activity in str(record.seq):
        if activity == '-':
            fasta.append('NULL')
            continue
        fasta.append(invTranslateDictionary[activity])
    rows[index].fasta = fasta
# find out the length of the new rows array
headerLength = len(rows[0].fasta)
headerString = []
for index in range(headerLength):
    headerString.append("Activity "+str(index))

# writing the fiel
with open('results/step1/associationMSA.csv', mode='w', newline='') as activityCsv:
    activityWriter = csv.writer(
        activityCsv, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    activityWriter.writerow(headerString)
    for row in rows:
        activityWriter.writerow(row.fasta)
print('finished')
