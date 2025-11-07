
class Statz:
    '''
    A class to track a specific statistic over time and the total.
    Attributes:
        name (str): The name of the statistic.
        total (int): The total value of the statistic.
        over_time (list): A list of values representing the statistic over time.
    '''
    def __init__(self, name, value, category):
        self.name = name
        self.total = value
        self.over_time = []
        self.category = category

    def average(self):
        if self.over_time:
            return sum(self.over_time) / len(self.over_time)
        else:
            return 0

    def most_common(self):
        if self.over_time:
            #filter out "" 
            tmp = [list(filter(lambda x: x != "", self.over_time))]
            #make tmp hashable
            tmp = [item for sublist in tmp for item in sublist]
            return max(set(tmp), key=tmp.count)
        else:
            return None

    def append(self, value):
        self.over_time.append(value)
        #check if type can be added to total
        if isinstance(value, (int, float)):
            self.total += value

