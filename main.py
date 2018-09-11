#! /usr/bin/python3

from config import *
import csv
import os.path
import sys

# First we need to analyse the candidates
#  to figure out what the highest ticket is
#  I have manually done up a spreadsheet identifying such
#  including TICKET, Vote as pseudocandidates

max_ATLs = 0
tickets = {}

popularity = {} # n-list by divbooth
prefcount = {} # also an n-list by divbooth
notoriety = {} # ditto

def ticketToNum(ticketStr):
    # A == 1; Z == 26; AA == 27; AZ == 52
    # It's base 26 but offset by 1
    # Can we recurse? Better not

    total = 0
    # countdown
    for i in range(len(ticketStr)):
        total += ( (26**(len(ticketStr)-(i+1))) * (1 + ord(ticketStr[i].upper()) - ord('A')) )
    
    return total

with open(os.path.join(cfg_datafolder, cfg_candidates), newline='') as candscsv:
    # Need to filter through this by state and then find the highest ticket
    # that isn't UG
    candsrdr = csv.DictReader(candscsv)

    for candsrow in candsrdr:
        if candsrow['State'] != cfg_state:
            continue
             
        if candsrow['Ticket'] == 'UG':
            continue
        elif candsrow['LastName'] == 'TICKET' and candsrow['FirstNames'] == 'Vote':
            tn = ticketToNum(candsrow['Ticket'])
            if tn > max_ATLs:
                max_ATLs = tn
                
            if candsrow['Party']:
                tickets[tn] = candsrow['Party']
            else:
                tickets[tn] = "Group " + candsrow['Ticket']

    # print(*(["Number\tTicket Name"]+[str(k)+'\t'+tickets[k] for k in tickets.keys()]), sep='\n', file=sys.stderr)

print("*** Tallying ***", file=sys.stderr)

with open(os.path.join(cfg_datafolder, cfg_ballots), newline='') as prefscsv:

    prefsreader = csv.DictReader(prefscsv)
    # since we didn't define fieldnames, the first row is taken implicitly


    progress = 0

    # Iterate over all the rows of the main thing
    for prefrow in prefsreader:

        progress += 1

        if (progress % 100000 == 0):
            print("Progress:\t", progress, file=sys.stderr)
##            break

        divnm = str(prefrow['ElectorateNm'])
        boothnm = str(prefrow['VoteCollectionPointNm'])

        if divnm[0] == '-':
            continue
            # just skip over that '-----' line (and any others)

        seq = str(prefrow['Preferences']).split(',')[0:max_ATLs]
        # Now we have our ATL preference sequence
        #print(prefrow)
        #print(seq)

        divbooth = divnm+boothnm

        for i in range(max_ATLs):
            if seq[i].isnumeric():
                if int(seq[i]) <= cfg_popular:        
                    try:
                        popularity[divbooth][i+3] += 1
                    except KeyError:
                        popularity[divbooth] = [divnm, boothnm, 0] + [0]*max_ATLs
                        popularity[divbooth][i+3] += 1

                elif int(seq[i]) >= int(max_ATLs * cfg_notorious):
                    try:
                        notoriety[divbooth][i+3] += 1
                    except KeyError:
                        notoriety[divbooth] = [divnm, boothnm, 0] + [0]*max_ATLs
                        notoriety[divbooth][i+3] += 1

            if(seq[i]):    
                try: # if they are pref'd at all...
                    prefcount[divbooth][i+3] += 1
                except KeyError:
                    prefcount[divbooth] = [divnm, boothnm, 0] + [0]*max_ATLs
                    prefcount[divbooth][i+3] += 1
            else:
                if cfg_include_blanks: #
                    try:
                        notoriety[divbooth][i+3] += 1
                    except KeyError:
                        notoriety[divbooth] = [divnm, boothnm, 0] + [0]*max_ATLs
                        notoriety[divbooth][i+3] += 1
                        
        try:
            popularity[divbooth][2] += 1 # update total for popularity
        except KeyError:
            popularity[divbooth] = [divnm, boothnm, 1] + [0]*max_ATLs
        try:
            prefcount[divbooth][2] += 1 # update total for prefcount
        except KeyError:
            prefcount[divbooth] = [divnm, boothnm, 1] + [0]*max_ATLs
        try:
            notoriety[divbooth][2] += 1 # update total for notoriety
        except KeyError:
            notoriety[divbooth] = [divnm, boothnm, 1] + [0]*max_ATLs
                    
# output

print("*** Writing Files ***", file=sys.stderr)

popularity_fn = os.path.join(cfg_output, cfg_state, "popularity.csv")
prefcount_fn = os.path.join(cfg_output, cfg_state, "prefcount.csv")
notoriety_fn = os.path.join(cfg_output, cfg_state, "notoriety.csv")

try:
    os.makedirs(os.path.join(cfg_output, cfg_state))
except FileExistsError:
    pass # sweet, nothing to do

with open(popularity_fn, 'w') as fp:
    wr = csv.writer(fp, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

    wr.writerow(["Division", "Booth", "Total"] + [tickets[i] for i in tickets.keys()])

    for ids in popularity.keys():
        wr.writerow(popularity[ids])

with open(prefcount_fn, 'w') as fp:
    wr = csv.writer(fp, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

    wr.writerow(["Division", "Booth", "Total"] + [tickets[i] for i in tickets.keys()])

    for ids in prefcount.keys():
        wr.writerow(prefcount[ids])

with open(notoriety_fn, 'w') as fp:
    wr = csv.writer(fp, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

    wr.writerow(["Division", "Booth", "Total"] + [tickets[i] for i in tickets.keys()])

    for ids in notoriety.keys():
        wr.writerow(notoriety[ids])

        
        
