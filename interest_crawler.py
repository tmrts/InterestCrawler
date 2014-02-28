# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
import re
import urllib
import urllib3
import optparse
import toolbelt
import anonymous_browser

from random import choice
from collections import defaultdict


def get_tweets(handle):
    query = urllib.quote_plus('from:' +
                              handle +
                              ' since:2009-01-01 include:retweets')
    tweets = []
    browser = anonymous_browser()
    browser.anonymize()

    response = browser.open('http://search.twitter.com/'
                            'search.json?q=' + query
                            )

    json_objects = json.load(response)
    for result in json_objects['results']:
        new_result = {}
        new_result['from_user'] = result['from_user_name']
        new_result['geo'] = result['geo']
        new_result['tweet'] = result['text']
        tweets.append(new_result)
    return tweets


def find_interests(tweets):
    interests = defaultdict(list)

    for tweet in tweets:
        text = tweet['tweet']
        # Regexp to grab URLs might miss certain types of URL since it's hard
        # to match all possible URLs with a regexp. But, it is sufficient for
        # this program.
        links = re.compile('(http.*?)\Z|(http.*?) ').findall(text)

        for link in links:
            if link[0]:
                link = link[0]
            elif link[1]:
                link = link[1]
            else:
                continue

            with suppress(Exception):
                response = urllib3.urlopen(link)
                full_link = response.url
                interests['links'].append(full_link)

        interests['users'] += re.compile('(@\w+)').findall(text)
        interests['hashtags'] += re.compile('(#\w+)').findall(text)

    interests['users'].sort()
    interests['hashtags'].sort()
    interests['links'].sort()

    return interests


def main():
    parser = optparse.OptionParser('usage %prog ' + '-u <twitter handle>')

    parser.add_option('-u',
                      dest='handle',
                      type='string',
                      help='specify twitter handle'
                      )

    (options, args) = parser.parse_args()
    handle = options.handle
    if handle is None:
        print(parser.usage)
        exit(0)

    tweets = get_tweets(handle)
    interests = find_interests(tweets)
    print('\n[+] Links.')
    for link in set(interests['links']):
        print(' [+] ' + str(link))

    print('\n[+] Users.')
    for user in set(interests['users']):
        print(' [+] ' + str(user))

    print('\n[+] HashTags.')
    for hashtag in set(interests['hashtags']):
        print(' [+] ' + str(hashtag))


if __name__ == '__main__':
    main()
