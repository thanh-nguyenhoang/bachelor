import matplotlib.pyplot as plt
import numpy as np
naivFile = r"logNaiv"
msaFile = r"logMSA"


def roundSixColon(line) -> float:
    return round(float(line[line.index(":")+2:len(line)]), 6)


def roundSixEq(line) -> float:
    return round(float(line[line.index("=")+2: len(line)]), 6)


class Log:
    def __init__(self, path, name) -> None:
        self.name = name
        self.initTime = 0
        self.kStep = []
        self.supressionStep = []
        self.readInput = True  # flag to differentiate between input and output values
        self.prosecInput = []
        self.prosecOutput = []
        self.marketInput = []
        self.marketOutput = []
        self.precisionInput = []
        self.precisionOutput = []
        self.nUEntropyInput = []
        self.nUEntropyOutput = []
        self.equivalenceClasses = []
        self.supressedRecords = []
        self.supressionSteps = 0
        self.kSteps = 0
        self.userTime = []
        with open(path) as f:
            line_count = 0
            for line in f:
                if line_count == 1:
                    self.setInitTime(line)
                    line_count += 1
                    continue
                if "limit" in line:
                    self.insertLimit(line)
                if "Input:" in line:
                    self.readInput = True
                if "Output:" in line:
                    self.readInput = False
                if "Prosecutor re-identification risk" in line:
                    self.appendProsecutor(line)
                if "Marketer re-identification risk" in line:
                    self.appendMarketer(line)
                if "Non-Uniform Entropy" in line:
                    self.appendNUEntropy(line)
                if "Precision" in line:
                    self.appendPrecision(line)
                if "equivalence classes" in line:
                    self.appendEquivalenceClasses(line)
                if "suppressed records" in line:
                    self.appendSuppressedRecords(line)
                if "real " in line:
                    self.appendRealTime(line)
                line_count += 1
        self.supressionSteps = self.kStep.count(self.kStep[0])
        self.kSteps = int(len(self.kStep) / self.supressionSteps)
        self.xAxisKSteps = self.kStep[0:self.kSteps]
        self.createAllGraphs()

    def insertLimit(self, line) -> None:
        self.kStep.append(line[line.index("k=")+2:line.index("supression")-1])
        self.supressionStep.append(
            round(float(line[line.index("n=")+2:len(line)]), 3))

    def setInitTime(self, line) -> None:
        self.initTime = float(line.replace("real ", ""))

    def appendProsecutor(self, line) -> None:
        if self.readInput:
            self.prosecInput.append(roundSixColon(line))
        else:
            self.prosecOutput.append(roundSixColon(line))

    def appendMarketer(self, line) -> None:
        if self.readInput:
            self.marketInput.append(roundSixColon(line))
        else:
            self.marketOutput.append(roundSixColon(line))

    def appendNUEntropy(self, line) -> None:
        if self.readInput:
            self.nUEntropyInput.append(roundSixColon(line))
        else:
            self.nUEntropyOutput.append(roundSixColon(line))

    def appendPrecision(self, line) -> None:
        if self.readInput:
            self.precisionInput.append(roundSixColon(line))
        else:
            self.precisionOutput.append(roundSixColon(line))

    def appendEquivalenceClasses(self, line) -> None:
        self.equivalenceClasses.append(roundSixEq(line))

    def appendSuppressedRecords(self, line) -> None:
        self.supressedRecords.append(roundSixEq(line))

    def appendRealTime(self, line) -> None:
        self.userTime.append(float(line.replace("real ", "")))

    def getYValues(self, selfParam):
        graphs = []
        for i in range(0, self.supressionSteps):
            graph = []
            for k in range(0, self.kSteps):
                graph.append(selfParam[k+i*self.kSteps])
            graphs.append(graph)
        return graphs

    def createPrecisionGraph(self) -> None:
        graphs = self.getYValues(self.precisionOutput)
        for graphIndex in range(0, len(graphs)):
            labelName = self.supressionStep[graphIndex *
                                            (int(len(self.supressionStep)/self.supressionSteps))]
            plt.plot(self.xAxisKSteps, graphs[graphIndex],
                     label='%.1f %% supression rate' % (labelName * 100))
        plt.legend(loc='lower left')
        plt.xlabel('k Parameter')
        plt.ylabel('Präzision in % (höher ist besser)')
        plt.grid()
        plt.savefig('img/results/precision%s.png' % self.name)

    def createNUEntropyGraph(self) -> None:
        graphs = self.getYValues(self.nUEntropyOutput)
        for graphIndex in range(0, len(graphs)):
            labelName = self.supressionStep[graphIndex *
                                            (int(len(self.supressionStep)/self.supressionSteps))]
            plt.plot(self.xAxisKSteps, graphs[graphIndex],
                     label='%.1f %% supression rate' % (labelName * 100))
        plt.legend(loc='upper left')
        plt.xlabel('k Parameter')
        plt.ylabel('Non-UNiform Entropy in % (niedriger ist besser)')
        plt.grid()
        plt.savefig('img/results/nUEntropy%s.png' % self.name)

    def createMarketGraph(self) -> None:
        graphsInput = self.getYValues(self.marketInput)
        graphsOutput = self.getYValues(self.marketOutput)
        for graphIndex in range(0, len(graphsInput)):
            labelName = self.supressionStep[graphIndex *
                                            (int(len(self.supressionStep)/self.supressionSteps))]
            plt.plot(self.xAxisKSteps, graphsInput[graphIndex],
                     label='%.1f %% supression rate input' % (labelName * 100))
        for graphIndex in range(0, len(graphsOutput)):
            labelName = self.supressionStep[graphIndex *
                                            (int(len(self.supressionStep)/self.supressionSteps))]
            plt.plot(self.xAxisKSteps, graphsOutput[graphIndex],
                     label='%.1f %% supression rate output' % (labelName * 100))
        plt.legend(loc='center left')
        plt.xlabel('k Parameter')
        plt.ylabel('marketer angriffs erfolgschance % (niedriger ist besser)')
        plt.grid()
        plt.savefig('img/results/marketer%s.png' % self.name)

    def createprosecGraph(self) -> None:
        graphsInput = self.getYValues(self.prosecInput)
        graphsOutput = self.getYValues(self.prosecOutput)
        for graphIndex in range(0, len(graphsInput)):
            labelName = self.supressionStep[graphIndex *
                                            (int(len(self.supressionStep)/self.supressionSteps))]
            plt.plot(self.xAxisKSteps, graphsInput[graphIndex],
                     label='%.1f %% supression rate input' % (labelName * 100))
        for graphIndex in range(0, len(graphsOutput)):
            labelName = self.supressionStep[graphIndex *
                                            (int(len(self.supressionStep)/self.supressionSteps))]
            plt.plot(self.xAxisKSteps, graphsOutput[graphIndex],
                     label='%.1f %% supression rate output' % (labelName * 100))
        plt.legend(loc='center right')
        plt.xlabel('k Parameter')
        plt.ylabel('prosecutor angriffs erfolgschance % (niedriger ist besser)')
        plt.grid()
        plt.savefig('img/results/prosec%s.png' % self.name)

    def createStatisticsGraph(self) -> None:
        # userTime, supressedRecords, equivalenceClasses
        width = 0.35
        graphsUserTime = self.getYValues(self.userTime)
        graphsSupressedRecords = self.getYValues(self.supressedRecords)
        graphsEquivalenceClasses = self.getYValues(self.equivalenceClasses)
        for graphIndex in range(0, len(graphsUserTime)):
            addedTime = [x + self.initTime for x in graphsUserTime[graphIndex]]
            labelName = self.supressionStep[graphIndex *
                                            (int(len(self.supressionStep)/self.supressionSteps))]
            plt.plot(self.xAxisKSteps, graphsUserTime[graphIndex],
                     label='%.1f %% suppression rate' % (labelName * 100))
            plt.plot(self.xAxisKSteps, addedTime,
                     label='%.1f %% suppression rate total time' % (labelName * 100))
        plt.legend(loc='best')
        plt.xlabel('k Parameter')
        plt.ylabel('zeit in s (niedriger ist besser)')
        plt.grid()
        plt.savefig('img/results/time%s.png' % self.name)
        plt.cla()
        for graphIndex in range(0, len(graphsSupressedRecords)):
            labelName = self.supressionStep[graphIndex *
                                            (int(len(self.supressionStep)/self.supressionSteps))]
            plt.plot(self.xAxisKSteps, graphsSupressedRecords[graphIndex],
                     label='%.1f %% suppression rate' % (labelName * 100))
        plt.legend(loc='best')
        plt.xlabel('k Parameter')
        plt.ylabel('# Anzahl der unterdrückten Werte')
        plt.grid()
        plt.savefig('img/results/supressed%s.png' % self.name)
        plt.cla()
        for graphIndex in range(0, len(graphsEquivalenceClasses)):
            labelName = self.supressionStep[graphIndex *
                                            (int(len(self.supressionStep)/self.supressionSteps))]
            plt.plot(self.xAxisKSteps, graphsEquivalenceClasses[graphIndex],
                     label='%.1f %% suppression rate' % (labelName * 100))
        plt.legend(loc='best')
        plt.xlabel('k Parameter')
        plt.ylabel('# Anzahl der Equivalenzklassen')
        plt.grid()
        plt.savefig('img/results/equivalenceClasses%s.png' % self.name)

    def createAllGraphs(self) -> None:
        self.createPrecisionGraph()
        self.createMarketGraph()
        self.createNUEntropyGraph()
        self.createprosecGraph()
        self.createStatisticsGraph()


naivLog = Log(naivFile, 'Naiv')
msaLog = Log(msaFile, 'MSA')

print("done reading logs")
