# Written by John Burton
import csv

# get the home team from the user
home_team = input("Enter the home team name: ")

# get the away team from the user
away_team = input("Enter the away team name: ")


def getData(team_name):
    # read in data from cbb_advanced_stats.csv
    with open('cbb_advanced_stats.csv', 'r') as f:
        reader = csv.reader(f)
        data = list(reader)

    # read in data from cbb_opponent_stats.csv
    with open('cbb_opponent_stats.csv', 'r') as f:
        reader = csv.reader(f)
        opp_data = list(reader)

    # loop through the data
    for row in data:
        # if row is empty, skip it
        if row == []:
            continue
        # search for the team name
        if team_name.lower() in row[0].lower():
            # print(row)

            # save the team's data
            team_data = row
            break

    # if the team is not found, ask the user to enter the team name again
    if team_data == []:
        print("Team not found. Try again.")
        team_name = input("Enter the team name: ")
        team_data = getData(team_name)

    # loop through the data
    for row in opp_data:
        # if row is empty, skip it
        if row == []:
            continue
        # search for the team name
        if team_name.lower() in row[0].lower():
            # only print columns 16-end
            # print(row[16:])

            # save the team's opponent data
            team_opp_data = row[16:]
            break
    
    # if the team is not found, ask the user to enter the team name again
    if team_opp_data == []:
        print("Team not found. Try again.")
        team_name = input("Enter the team name: ")
        team_opp_data = getData(team_name)

    # return the team's data and opponent data
    return team_data, team_opp_data


# function to predict the score of a game
def predictScore(home_team, home_team_or, home_team_dr, home_team_pace, away_team, away_team_or, 
                away_team_dr, away_team_pace, home_team_trb, home_team_top, away_team_trb, 
                away_team_top, home_team_win, away_team_win, home_team_srs, away_team_srs):

    # average the pace of the home team and away team
    avg_pace = (home_team_pace + away_team_pace) / 2

    # adjust the offensive/defensive ratings to the average pace
    home_team_or = (home_team_or / 100) * avg_pace
    home_team_dr = (home_team_dr / 100) * avg_pace
    away_team_or = (away_team_or / 100) * avg_pace
    away_team_dr = (away_team_dr / 100) * avg_pace

    # calculate the home and away team's scores
    home_team_score = (home_team_or + away_team_dr) / 2
    away_team_score = (away_team_or + home_team_dr) / 2

    # using rebounding and turnover percentages, calculate the home and away team's scores
    home_trb_top = home_team_trb - home_team_top
    away_trb_top = away_team_trb - away_team_top

    difference = home_trb_top - away_trb_top
    if difference > 0:
        difference = difference * 0.5
        home_team_score = home_team_score + difference
        away_team_score = away_team_score - difference
    elif difference < 0:
        difference = difference * 0.5
        home_team_score = home_team_score - difference
        away_team_score = away_team_score + difference

    # add the home team's win percentage is greater than .7, multiply it by 2 and add it to the home team's score
    if home_team_win > .7:
        home_team_score = home_team_score + (home_team_win * 2)
    # if the home team's win percentage is greater than .5, add it to the home team's score
    elif home_team_win > .5:
        home_team_score = home_team_score + home_team_win

    # if the away team's win percentage is greater than .5, add it to the away team's score
    if away_team_win > .5:
        away_team_score = away_team_score + away_team_win
    else:
        away_team_score = away_team_score - away_team_win

    # get the difference between the home team's SRS and the away team's SRS
    srs_difference = home_team_srs - away_team_srs

    # if the home team's SRS is greater than the away team's SRS by 10 or more, add the difference/1.2 to the home team's score
    if srs_difference >= 10:
        home_team_score = home_team_score + (srs_difference / 1.2)
    # if the home team's SRS is greater than the away team's SRS by 5 or more, add the difference/4 to the home team's score
    elif srs_difference >= 5:
        home_team_score = home_team_score + (srs_difference / 4)

    # adjust the away team's score based on the away team's SRS compared to the home team's SRS
    # get the difference between the away team's SRS and the home team's SRS
    srs_difference = away_team_srs - home_team_srs
    # if the away team's SRS is greater than the home team's SRS by 10 or more, add the difference/1.2 to the away team's score
    if srs_difference >= 10:
        away_team_score = away_team_score + (srs_difference / 1.2)
    # if the away team's SRS is greater than the home team's SRS by 5 or more, add the difference/4 to the away team's score
    elif srs_difference >= 5:
        away_team_score = away_team_score + (srs_difference / 4)


    # round the scores to whole numbers
    home_team_score = round(home_team_score)
    away_team_score = round(away_team_score)

    # print the predicted score
    print(home_team + " vs. " + away_team)
    if home_team_score > away_team_score:
        print(home_team + " wins " + str(home_team_score) + "-" + str(away_team_score))
    elif home_team_score < away_team_score:
        print(away_team + " wins " + str(away_team_score) + "-" + str(home_team_score))





# call the getData function for the home team and away team
home_team_data, home_team_opp_data = getData(home_team)
away_team_data, away_team_opp_data = getData(away_team)

# change the data types of the home team's data and opponent data, except for time name
home_team = home_team_data[0]
home_team_data = [float(x) for x in home_team_data[1:]]
home_team_opp_data = [float(x) for x in home_team_opp_data]

# change the data types of the away team's data and opponent data, except for time name
away_team = away_team_data[0]
away_team_data = [float(x) for x in away_team_data[1:]]
away_team_opp_data = [float(x) for x in away_team_opp_data]

### get home team's stats ###
home_team_or = home_team_data[15]
home_team_pace = home_team_data[14]
home_team_dr = home_team_opp_data[0]
# total rebounding percentage and turnover percentage
home_team_trb = home_team_data[19]
home_team_top = home_team_data[24]
# home win percentage w/l
home_team_win = (home_team_data[8] / (home_team_data[8] + home_team_data[9]))
# Simple Rating System (SRS)
home_team_srs = home_team_data[4]


### get away team's stats ##
away_team_or = away_team_data[15]
away_team_pace = away_team_data[14]
away_team_dr = away_team_opp_data[0]
# total rebounding percentage and turnover percentage
away_team_trb = away_team_data[19]
away_team_top = away_team_data[24]
# away win percentage w/l
away_team_win = (away_team_data[10] / (away_team_data[10] + away_team_data[11]))
# Simple Rating System (SRS)
away_team_srs = away_team_data[4]


# call the predictScore function
predictScore(home_team, home_team_or, home_team_dr, home_team_pace, away_team, away_team_or, 
            away_team_dr, away_team_pace, home_team_trb, home_team_top, away_team_trb, 
            away_team_top, home_team_win, away_team_win, home_team_srs, away_team_srs)