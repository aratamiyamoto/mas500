# excersises functions defined in election_analyzer

from election_analyzer import *

def main():
    html_filename = 'popular-vote.html'
    csv_filename = 'popular-vote.csv'
    json_filename = 'popular-vote.json'

    parser = ElectionParser()
    parser.loadHtml(html_filename)
    result = parser.getElectionResult()

    print 'stateCount =', result.stateCount()
    print 'stateList =', result.stateList()
    print 'partyList =', result.partyList()

    for party in result.partyList():
        most_popular_state = result.mostPopularState(party)
        least_popular_state = result.leastPopularState(party)
        vote_rate_in_most_popular_state = \
            result.stateEntry(most_popular_state).voteRate(party)
        vote_rate_in_least_popular_state = \
            result.stateEntry(least_popular_state).voteRate(party)

        print 'totalVoteForparty(' + party + ') =', \
            result.totalVoteForParty(party)
        print 'numWinningStates(' + party + ') =', \
            result.numWinningStates(party)
        print 'mostPopularState(%s) = %s(%.3f%%)' % \
            (party, most_popular_state, vote_rate_in_most_popular_state * 100)
        print 'leastPopularState(%s) = %s(%.3f%%)' % \
            (party, least_popular_state, vote_rate_in_least_popular_state * 100)

    print 'winningParty =', result.winningParty()
    for state in result.stateList():
        state_entry = result.stateEntry(state)
        print 'winningParty(' + state + ') =', state_entry.winningParty()

    parser.saveToCsv(csv_filename)
    parser.saveToJson(json_filename)

if __name__ == '__main__':
    main()
