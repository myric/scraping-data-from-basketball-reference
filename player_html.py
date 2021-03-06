#!/usr/bin/env python

import requests
import pickle
import sys
from player_index import get_all_players

def get_player_html(url):
    '''
    Retrieves the HTML for a given URL
    PARAMS  url: string URL suffix
    RETURN  html: bytes of the HTML for the requested page
    '''
    html=None
    try:
        html=requests.get('https://www.basketball-reference.com'+url).content
    # sometimes the request is refused if we are sending too many at a time
    except requests.exceptions.ConnectionError:
        print('Connection refused for: '+url)
    return html

def get_all_html(all_players):
    '''
    Stores the HTML of every player on Basketball-Reference into a dictionary
    PARAMS  all_players: pandas DataFrame of basic information about players
    RETURN  all_html: dictionary of all players with URL as keys and HTML as values
    '''
    n_players=all_players.shape[0]

    # save the HTML of each player page to a dictionary
    # this could be parallelized but that increases the chances of a ConnectionError
    all_html={}
    for i in range(n_players):
        url=all_players['url'].iloc[i]
        all_html[url]=get_player_html(url)
        sys.stdout.write('\rprocessed player '+str(i+1)+' of '+str(n_players))
        sys.stdout.flush()
    return all_html

def main():
    # get a DataFrame of all players
    all_players=get_all_players()

    all_html=get_all_html(all_players)
    print('')

    pickle.dump(all_html,open('data/all_html.pkl','wb'))
    print('saved to data/all_html.pkl')

if __name__=='__main__':
    main()
