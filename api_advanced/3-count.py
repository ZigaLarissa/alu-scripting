#!/usr/bin/python3

"""
A recursive function that querries the reddit api, parses title
of all hot posts, and prints a sorted count of given keywords.
"""


import re
import requests


def count_words(subreddit, word_list, after=None, counts=None):
    if counts is None:
        counts = {}
    headers = {'User-Agent': 'Mozilla/5.0'}
    url = f'https://www.reddit.com/r/{subreddit}/hot.json'
    params = {'limit': 100}
    if after:
        params['after'] = after
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        data = response.json()
        after = data['data']['after']
        posts = data['data']['children']
        for post in posts:
            title = post['data']['title'].lower()
            for word in word_list:
                word = word.lower()
                if re.search(rf'\b{word}\b', title):
                    if word in counts:
                        counts[word] += 1
                    else:
                        counts[word] = 1
        if after:
            count_words(subreddit, word_list, after=after, counts=counts)
        else:
            sorted_counts = sorted(counts.items(), key=lambda x: (-x[1], x[0]))
            for count in sorted_counts:
                print(f'{count[0]}: {count[1]}')
    else:
        return {}
