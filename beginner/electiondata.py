class ElectionResults:
  
    def __init__(self, filename):
        self.filename = filename

    def load(self):
        self.file = open(self.filename, 'r')
        self.all_lines = self.file.readlines()

    def states(self):
        all_names = []
        for line in self.all_lines:
            columns = line.split(',')
            all_names.append(columns[1])
        return all_names[1:]

    def state_count(self):
        return len(self.states())
	
    def count_votes(self, person):
        person = person.lower()

        if person == "obama":
            field_index = 3
        elif person == "romney":
            field_index = 5
        else:
            raise Exception("Unknown name - " + person)

        votes = map(lambda line: line.split(',')[field_index], self.all_lines)
        votes = map(int, votes[1:])

        return sum(votes) 
