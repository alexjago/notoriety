### Configuration file... ###

cfg_datafolder = "/media/alexjago/Narnia/Psephology/Results/AUS_2016/"
cfg_candidates = "SenateCandidatesBallotNumbers.csv"

cfg_popular = 6
# You're in the top 1...6? People like you

cfg_known = 0.5
# More than 50% of ballots list you? People know who you are.

cfg_notorious = 0.5
# You were listed in the bottom half of preferences? Notorious!
# 'bottom half' is of the full ballot, and further is overridden by cfg_popular
# So e.g. on a 34 ticket ballot, notoriety would begin at preference #18
# but on an 8 ticket ballot with cfg_popular=6; notoriety would only begin at
# preference #7, rather than at #4.

cfg_include_blanks = False
# Treat blank preferences as notorious.
# (If they were each assigned an average 'equal last' preference, that would
# put them over the notoriety threshold, at least for cfg_notorious=0.5)

cfg_state = "QLD"
cfg_ballots = "aec-senate-formalpreferences-20499-QLD.csv"

cfg_output = "output"
# output directory. Results CSVs will be placed in ./output/$cfg_state/
