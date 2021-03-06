# takes generalizedData and counts them
import csv
import sys
from collections import Counter
from string import Template

class Sequence:
  def __init__(self, activities, count) -> None:
      self.activities = activities
      self.count = count
      self.finalActivities = []
  def setAbsoluteFrequency(self):
    self.finalActivities= [self.count] + list(self.activities)

with open('results/step2/generalizedData.csv') as csv_file:
  csv_reader = csv.reader(csv_file, delimiter=';')
  line_count = 0
  sequences = []
  activityLength = 0

  headerString = []

  currentSequence: Sequence
  for currentSequence in csv_reader:
    if line_count == 0:
      currentSequence.insert(0, "frequency")
      headerString = currentSequence
      line_count += 1
    else:
      replaceTimesSign = ["NULL" if x=="*" else x for x in currentSequence]
      sequences.append(tuple(replaceTimesSign))
  countOccurances = list(Counter(sequences).items())
  
  countedSequences = []
  for sequence in countOccurances:
    tmpSequence: Sequence
    tmpSequence = Sequence(sequence[0], sequence[1])
    tmpSequence.setAbsoluteFrequency()
    countedSequences.append(tmpSequence)
  outputFileName = Template('results/step3/finalData$number.csv')
  with open(outputFileName.substitute(number=sys.argv[1]), mode='w', newline='') as activityCsv:
        activityWriter = csv.writer(activityCsv, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        activityWriter.writerow(headerString)
        for row in countedSequences:
            activityWriter.writerow(row.finalActivities)
  print('finished %s' % sys.argv[1])