# Print out all the state names from the csv
# Coded in the "object-oriented" style
from electiondata import ElectionResults

filename = '2012_US_election_state.csv'
results = ElectionResults(filename)
results.load()
print "Opened file:"

for name in ["Obama", "Romney"]:
    num_votes = results.count_votes(name)
    print str(num_votes) + " votes for " + name
