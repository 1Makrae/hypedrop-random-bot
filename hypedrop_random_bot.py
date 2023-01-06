import pandas as pd
import numpy as np


class Bot:

    def __init__(self):
        self.name = "Bot Makrae"
        self.cases = pd.read_csv("hypedrop_cases.csv")
        regionValid = False
        while not regionValid:
            region = input(self.name + ": What region are you from?\n 1. NA\n 2. EU\n")
            try:
                if region == "1" or region == "NA":
                    regionValid = True
                    self.region = "PriceNA"
                elif region == "2" or region == "EU":
                    regionValid = True
                    self.region = "PriceEU"
                else:
                    print(self.name + ": Please enter a valid region")
            except Exception:
                pass

    def generate_battle(self):
        decideMode = False
        decideNumCases = False
        decideFormat = False
        decideOpponent = False
        total = 0
        budget = self.decide_budget()
        remainingBudget = budget
        optionValid = False
        while not optionValid:
            option = input(self.name + ": Would you like me to decide Crazy vs Regular Mode?\n 1. Y\n 2. N\n")
            try:
                if option == "1" or option == "Y":
                    optionValid = True
                    decideMode = True
                elif option == "2" or option == "N":
                    optionValid = True
                    decideMode = False
                else:
                    print(self.name + ": Please enter a valid option")
            except Exception:
                pass

        optionValid = False
        while not optionValid:
            option = input(self.name + ": Would you like to choose the number of cases in the battle?\n 1. Y\n 2. N\n")
            try:
                if option == "1" or option == "Y":
                    optionValid = True
                    decideNumCases = True
                elif option == "2" or option == "N":
                    optionValid = True
                    decideNumCases = False
                else:
                    print(self.name + ": Please enter a valid option")
            except Exception:
                pass
        numCases = False
        if decideNumCases:
            numCases = self.decide_num_cases(budget)

        cases = []
        if numCases:
            while len(cases) < numCases:
                avgBudget = (remainingBudget / numCases) * 1.2
                if avgBudget > remainingBudget:
                    avgBudget = remainingBudget
                avgMinBudget = (remainingBudget/numCases) * 0.4
                case = self.generate_case(avgBudget,avgMinBudget)
                cases.append(self.cases.at[case,"Case"])
                remainingBudget -= self.cases.at[case,self.region]
        else:
            while remainingBudget > budget * 0.1:
                minBudget = budget * 0.2
                case = self.generate_case(budget, minBudget)
                cases.append(self.cases.at[case, "Case"])
                remainingBudget -= self.cases.at[case, self.region]
        optionValid = False
        while not optionValid:
            option = input(self.name + ": Would you like me to choose your opponent for the battle?\n 1. Y\n 2. N\n")
            try:
                if option == "1" or option == "Y":
                    optionValid = True
                    decideOpponent = True
                elif option == "2" or option == "N":
                    optionValid = True
                    decideOpponent = False
                else:
                    print(self.name + ": Please enter a valid option")
            except Exception:
                pass
        optionValid = False
        while not optionValid:
            option = input(self.name + ": Would you like me to choose the format of the battle?\n 1. Y\n 2. N\n")
            try:
                if option == "1" or option == "Y":
                    optionValid = True
                    decideFormat = True
                elif option == "2" or option == "N":
                    optionValid = True
                    decideFormat = False
                else:
                    print(self.name + ": Please enter a valid option")
            except Exception:
                pass
        mode = False
        if decideMode:
            mode = self.decide_mode()
        gameFormat = False
        if decideFormat:
            gameFormat = self.decide_format()
        opponent = False
        if decideOpponent:
            opponent = self.decide_opponent()
        self.output_decision(cases, mode, gameFormat, opponent)

    def generate_case(self, budget=100,minBudget = 0):
        df = self.cases
        index = df[self.region] <= budget
        fitsBudget = df[index]
        index = fitsBudget[self.region] > minBudget
        fitsBudget = fitsBudget[index]
        randomCase = fitsBudget.sample()
        caseIndex = randomCase.index[0]
        return caseIndex

    def change_settings(self):
        pass

    def action(self):
        stop = False
        while not stop:
            action = input(self.name + ": What would you like to do?\n1. Random Battle\n2. Random Solo Open\n3. "
                                       "Surprise Me\n4. Adjust Settings (Not Completed)\n5. Exit\n")
            try:
                if action == "1" or action.lower() == "random battle":
                    self.generate_battle()
                elif action == "2" or action.lower() == "random solo open":
                    budget = self.decide_budget()
                    case = self.generate_case(budget)
                    caseName = self.cases.at[case, 'Case']
                    print(self.name + ": I think you should do the " + caseName + " case")
                    print(self.name + ": Good Luck!")
                    input(self.name + ": If you don't make profit I will do better next time!\n")
                elif action == "3" or action.lower() == "surprise me":
                    self.generate_battle()
                elif action == "4" or action.lower() == "adjust settings":
                    self.change_settings()
                elif action == "5" or action.lower() == "exit":
                    stop = True
                else:
                    print(self.name + ": Please enter a valid action")
            except Exception:
                pass

    def decide_mode(self):
        rand = np.random.randint(2)
        if rand == 0:
            return "Regular Mode"
        else:
            return "Crazy Mode"

    def decide_num_cases(self, budget):
        optionValid = False
        while not optionValid:
            num = input(self.name + ": How many cases would you like in your battle?\n")
            try:
                if int(num) <= 100 and budget / int(num) > 0.5:
                    optionValid = True
                else:
                    print(self.name + ": Please enter a valid number of cases")
            except Exception:
                pass
        return int(num)

    def decide_format(self):
        rand = np.random.randint(4)
        if rand == 0:
            return "1v1"
        elif rand == 1:
            return "1v1v1"
        elif rand == 1:
            return "1v1v1v1"
        else:
            return "2v2"

    def decide_opponent(self):
        rand = np.random.randint(2)
        if rand == 0:
            return "Bot"
        else:
            return "Person"

    def output_decision(self, cases, mode, versusMode, opponent):
        print(self.name + ": I think you should do this battle")
        print(self.name + ": " + str(cases))
        if mode:
            print(self.name + ": You should do " + mode)
        if versusMode:
            print(self.name + ": The battle should be " + versusMode)
        if opponent:
            print(self.name + ": Your opponent should be a " + opponent)
        print(self.name + ": Good Luck!")
        input(self.name + ": If you don't make profit I will do better next time!\n")

    def decide_budget(self):
        optionValid = False
        while not optionValid:
            num = input(self.name + ": What is your budget?\n")
            try:
                num = int(num)
                if type(num) == int and num >= 1:
                    optionValid = True
                    int(num)
                else:
                    print(self.name + ": Please enter a valid number of cases")
            except Exception:
                pass
        return num


def main():
    bot = Bot()
    bot.action()


main()
