# A test suite for the classed defined in election_analyzer.py

import sys
import os
script_path = os.path.dirname(os.path.realpath(sys.argv[0]))
sys.path.append(script_path + '/../')

from election_analyzer import *
import unittest
import filecmp

sample_html = 'sample-vote.html'
sample_csv = 'sample-vote.csv'
sample_json = 'sample-vote.json'
reference_csv = 'reference.csv'
reference_json = 'reference.json'

test_state = "State1"
test_parties = [ "Party1", "Party2", "Party3" ]
test_votes = [ 100, 30, 50 ]
test_total_tag = 'Total'
test_total_votes = 180

# Test cases for ElectionParser
class ElectionParserTest(unittest.TestCase):
    def setUp(self):
        self.parser = ElectionParser()
        self.parser.loadHtml(sample_html)

    def testLoadHtml(self):
        # it should work even if loadHtml() called multiple times
        self.parser.loadHtml(sample_html)

        assert self.parser.election_result.partyCount() == 3
        assert self.parser.election_result.stateCount() == 3

    def testLoadHtml(self):
        assert self.parser.election_result.partyCount() == 3
        assert self.parser.election_result.stateCount() == 3

    def testGetElectionResult(self):
        returned_election_result = self.parser.getElectionResult()
        assert returned_election_result is self.parser.election_result

    def testSaveToCsv(self):
        self.parser.loadHtml(sample_html)
        self.parser.saveToCsv(sample_csv)
        assert filecmp.cmp(sample_csv, reference_csv)

    def testSaveToJson(self):
        self.parser.loadHtml(sample_html)
        self.parser.saveToJson(sample_json)
        assert filecmp.cmp(sample_json, reference_json)

# Test cases for StateEntry
class StateEntryTest(unittest.TestCase):

    def setUp(self):
        self.entry = StateEntry(test_state)

        self.filled_entry = StateEntry(test_state)
        for party in zip(test_parties, test_votes):
            self.filled_entry.addParty(party[0], party[1])
        self.filled_entry.setTotal(test_total_tag, test_total_votes)

    def testConstructor(self):
        assert self.entry.state == test_state
        assert self.entry.parties == OrderedDict()
        assert len(self.entry.parties) == 0

    def testAddParty(self):
        self.entry.addParty(test_parties[0], test_votes[0])
        assert self.entry.parties == \
            OrderedDict({test_parties[0]: test_votes[0]})

    def testSetTotal(self):
        self.entry.setTotal(test_total_tag, test_total_votes)
        assert self.entry.total == \
            OrderedDict({test_total_tag: test_total_votes})

    def testPartyCount(self):
        assert self.filled_entry.partyCount() == len(test_parties)

    def testPartyList(self):
        assert self.filled_entry.partyList() == test_parties

    def testTotalVotes(self):
        assert self.filled_entry.totalVotes() == test_total_votes

    def testWinningParty(self):
        assert self.filled_entry.winningParty() == test_parties[0]

    def testVoteRate(self):
        assert self.filled_entry.voteRate(test_parties[0]) == \
            float(test_votes[0]) / test_total_votes
        assert self.filled_entry.voteRate(test_parties[1]) == \
            float(test_votes[1]) / test_total_votes
        assert self.filled_entry.voteRate(test_parties[2]) == \
            float(test_votes[2]) / test_total_votes

    def testEntry(self):
        assert self.filled_entry.entry() == OrderedDict((
            ('State', test_state), \
            ('Votes', OrderedDict(( \
                (test_parties[0], test_votes[0]), \
                (test_parties[1], test_votes[1]), \
                (test_parties[2], test_votes[2])))), \
            (test_total_tag, test_total_votes)))

# Test cases for ElectionResult
class ElectionResultTest(unittest.TestCase):

    def setUp(self):
        parser = ElectionParser()
        parser.loadHtml(sample_html)
        self.result = parser.getElectionResult()

        self.empty_result = ElectionResult()

        self.test_entry = StateEntry(test_state)
        for party in zip(test_parties, test_votes):
            self.test_entry.addParty(party[0], party[1])
        self.test_entry.setTotal(test_total_tag, test_total_votes)

    def testConstructor(self):
        assert self.empty_result.states == []

    def testAddState(self):
        self.empty_result.addState(self.test_entry)
        assert self.empty_result.states == [self.test_entry]

    def testSetTotalState(self):
        self.empty_result.setTotalState(self.test_entry)
        assert self.empty_result.total_state == self.test_entry

    def testStateCount(self):
        assert self.result.stateCount() == 3

    def testStateList(self):
        assert self.result.stateList() == ['State 1', 'State 2', 'State 3']

    def testStateEntry(self):
        assert self.result.stateEntry('State 1').state == 'State 1'
        assert self.result.stateEntry('State 1').parties == \
            OrderedDict((('Party A', 80), ('Party B', 50), ('Party C', 20)))

    def testPartyCount(self):
        assert self.result.partyCount() == 3

    def testPartyList(self):
        assert self.result.partyList() == ['Party A', 'Party B', 'Party C']

    def testTotalVoteForParty(self):
        assert self.result.totalVoteForParty('Party A') == 170
        assert self.result.totalVoteForParty('Party B') == 110
        assert self.result.totalVoteForParty('Party C') == 60

    def testWinningParty(self):
        assert self.result.winningParty() == 'Party A'

    def testNumWinningStates(self):
        assert self.result.numWinningStates('Party A') == 2
        assert self.result.numWinningStates('Party B') == 1
        assert self.result.numWinningStates('Party C') == 0

    def testMostPopularState(self):
        assert self.result.mostPopularState('Party A') == 'State 3'
        assert self.result.mostPopularState('Party B') == 'State 2'
        assert self.result.mostPopularState('Party C') == 'State 3'

    def testLeastPopularState(self):
        assert self.result.leastPopularState('Party A') == 'State 2'
        assert self.result.leastPopularState('Party B') == 'State 3'
        assert self.result.leastPopularState('Party C') == 'State 2'

if __name__ == "__main__":
    unittest.main()
