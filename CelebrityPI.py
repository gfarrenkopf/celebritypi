import sys
import operator
import requests
import json
import twitter
from watson_developer_cloud import PersonalityInsightsV2 as PersonalityInsights

def analyze(handle):
  twitter_consumer_key = 'uQ4KRrLXJuAHtPiwaURf4cgSk'
  twitter_consumer_secret = 'ng1ZWQWZTyKBRfJAkU7teaBiX463F242xqP6GQC4ACzPTvMMRk'
  twitter_access_token = '2810898171-4lynaBEOrQuCgzjWAAcuVLiqlJ9vrFb6ERfKVpD'
  twitter_access_secret = 'lR7Q8pw5nc1ngKt6TQvWqMpZ4H3F4nfSxExi4F7FOcG7o'

  twitter_api = twitter.Api(consumer_key=twitter_consumer_key, consumer_secret=twitter_consumer_secret, access_token_key=twitter_access_token, access_token_secret=twitter_access_secret)

  statuses = twitter_api.GetUserTimeline(screen_name=handle, count=500, include_rts=False)

  text = b""

  for status in statuses:
    if (status.lang =='en'):
      text += status.text.encode('utf-8')

  pi_username = '52d9def9-6ae4-4ee5-bf84-b366c1bbd1fc'
  pi_password = 'b4LwQq5hbRGh'

  personality_insights = PersonalityInsights(username=pi_username, password=pi_password)

  pi_result = personality_insights.profile(text)

  return pi_result

def flatten(orig):
  data = {}
  for c in orig['tree']['children']:
    if 'children' in c:
      for c2 in c['children']:
        if 'children' in c2:
          for c3 in c2['children']:
            if 'children' in c3:
              for c4 in c3['children']:
                if(c4['category'] == 'personality'):
                  data[c4['id']] = c4['percentage']
                  if 'children' not in c3:
                    if(c3['category'] == 'personality'):
                      data[c3['id']] = c3['percentage']
  return data

def compare(dict1, dict2):
	compared_data = {}
	for keys in dict1:
		if dict1[keys] != dict2[keys]:
			compared_data[keys]=abs(dict1[keys] - dict2[keys])
	return compared_data

user_handle = "@HillaryClinton"
celebrity_handle = "@realDonaldTrump"

user_result = analyze(user_handle)
celebrity_result = analyze(celebrity_handle)

user = flatten(user_result)
celebrity = flatten(celebrity_result)

compared_results = compare(user,celebrity)

sorted_result = sorted(compared_results.items(), key=operator.itemgetter(1))

for keys, value in sorted_result[:5]:
	print(keys),
	print(user[keys]),
	print('->'),
	print(celebrity[keys]),
	print('->'),
	print(compared_results[keys])
