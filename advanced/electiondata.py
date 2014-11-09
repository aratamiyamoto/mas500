import sys
import re
from collections import OrderedDict
from bs4 import BeautifulSoup

class ElectionParser:
    def __init__(self):
        self.election_result = ElectionResult()

    def load_html(self, filename):
        html_file = open(filename, 'r')
        lines = html_file.readlines()
        soup = BeautifulSoup("".join(lines))
        html_file.close()

        table = soup.find('table', cellspacing="2")
        trs = table.findAll('tr')

        self.election_result = ElectionResult()

        parties = []
        for tr in trs:
            th = tr.find('th')

            state = re.compile('\W').sub('', th.contents[0])
            state_entry = StateEntry(state)

            if state == 'State':
                ths = tr.findAll('th')
                for th_party in ths[1:-1]:
                    party = re.compile('[^\w\s]').sub('', th_party.contents[0])
                    party = re.compile('\w+').search(party).group(0)
                    parties.append(party)
            elif re.compile('^[A-Z]{2}$').match(state):
                tds = tr.findAll('td')
                td_vals = []
                for td in tds[0:-1]:
                    val = re.compile('\*').sub('', td.string)
                    if val == '-':
                        val = -1
                    td_vals.append(int(val))
                for vote in zip(parties, td_vals):
                    state_entry.add_party(vote[0], vote[1])
            
                self.election_result.add_state(state_entry)

    def get_election_result(self):
        return self.election_result

    def save_to_csv(self, filename):
        parties = self.election_result.party_list()

        csv_file = open(filename, 'w')
        print >> csv_file, ','.join(['State'] + parties + ['Total Votes'])

        for state in self.election_result.state_list():
            state_entry = self.election_result.state_entry(state)
            votes = state_entry.parties.values()
            total_votes = sum(filter(lambda x: x >= 0, votes))
            line = [state] + [str(vote) if vote >= 0 else '-' for vote in votes] + [str(total_votes)]
            
            print >> csv_file, ','.join(line)

        totals = [self.election_result.total_vote_for_party(party) for party in parties]
        total_total_votes = sum(totals)
        line = ['Totals'] + [str(total) for total in totals] + [str(total_total_votes)]
        print >> csv_file, ','.join(line)

        csv_file.close()
        

    def save_to_json(self, filename):
        a = 1

class StateEntry:
    def __init__(self, state):
        self.state = state
        self.parties = OrderedDict()

    def add_party(self, party, votes):
        self.parties[party] = votes

    def party_count(self):
        return len(self.parties)

    def party_list(self):
        return self.parties.keys()

    def total_votes(self):
        return sum(self.parties.values())

    def winning_party(self):
        return reduce(lambda p, q:
                p if self.parties[p] > self.parties[q] else q, self.parties)

    def vote_rate(self, party):
        total_votes = self.total_votes()
        vote_for_party = self.parties[party]
        return float(vote_for_party) / total_votes

    def __repr__(self):
        return 'state=' + self.state + ' ' + self.parties.__repr__()

class ElectionResult:
    def __init__(self):
        self.states = []

    def add_state(self, state_entry):
        self.states.append(state_entry)

    def state_count(self):
        return len(self.states)

    def state_list(self):
        return map(lambda s: s.state, self.states)

    def state_entry(self, state):
        return filter(lambda s: s.state == state, self.states)[0]

    def party_count(self):
        return self.states[0].party_count()

    def party_list(self):
        return self.states[0].party_list()

    def total_vote_for_party(self, party):
        state_votes = [state.parties[party] for state in self.states]
        return sum(state_votes)

    def winning_party(self):
        parties = self.party_list()
        votes = [self.total_vote_for_party(party) for party in parties]
        winner = reduce(lambda p, q: p if p[1] > q[1] else q,
                zip(parties, votes))
        return winner[0]

    def num_winning_states(self, party):
        states = self.state_list()
        winning_states = [state.winning_party() for state in self.states]
        return winning_states.count(party)

    def most_popular_state(self, party):
        states = self.state_list()
        vote_rates = [state.vote_rate(party) for state in self.states]
        state_vote_pairs = filter(lambda p: p[1] >= 0, zip(states, vote_rates))
        state_with_highest_rate = reduce(lambda s, t: s if s[1] > t[1] else t,
                state_vote_pairs, ('', -sys.maxint - 1))
        return state_with_highest_rate[0]

    def least_popular_state(self, party):
        states = self.state_list()
        vote_rates = [state.vote_rate(party) for state in self.states]
        state_vote_pairs = filter(lambda p: p[1] >= 0, zip(states, vote_rates))
        state_with_highest_rate = reduce(lambda s, t: s if s[1] < t[1] else t,
                state_vote_pairs, ('', sys.maxint))
        return state_with_highest_rate[0]