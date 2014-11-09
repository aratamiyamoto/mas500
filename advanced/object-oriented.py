from electiondata import *

def main():
    html_filename = 'popular-vote.html'
    csv_filename = 'popular-vote.csv'
    json_filename = 'popular-vote.json'

    parser = ElectionParser()
    parser.load_html(html_filename)
    result = parser.get_election_result()

    print 'state_count =', result.state_count()
    print 'state_list =', result.state_list()
    print 'party_list =', result.party_list()

    for party in result.party_list():
        most_popular_state = result.most_popular_state(party)
        least_popular_state = result.least_popular_state(party)
        vote_rate_in_most_popular_state = result.state_entry(most_popular_state).vote_rate(party)
        vote_rate_in_least_popular_state = result.state_entry(least_popular_state).vote_rate(party)

        print 'total_vote_for_party(' + party + ') = ', result.total_vote_for_party(party)
        print 'num_winning_states(' + party + ') = ', result.num_winning_states(party)
        print 'most_popular_state(%s) = %s(%.3f%%)' % (party, most_popular_state, vote_rate_in_most_popular_state * 100)
        print 'least_popular_state(%s) = %s(%.3f%%)' % (party, least_popular_state, vote_rate_in_least_popular_state * 100)

    print 'winning_party =', result.winning_party()
    for state in result.state_list():
        state_entry = result.state_entry(state)
        print 'winning_party(' + state + ') = ', state_entry.winning_party()

    parser.save_to_csv(csv_filename)
    parser.save_to_json(json_filename)

if __name__ == '__main__':
    main()
