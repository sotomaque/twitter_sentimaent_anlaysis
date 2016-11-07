
# twitter sentiment analysis
import tweepy
from textblob import TextBlob
from textblob_fr import PatternTagger, PatternAnalyzer

import numpy as np
import operator

# Step 1 - authenticate
consumer_key = 'Z1zdsNd2toTUFoMQIuJkzoRHv'
consumer_secret = 'Qfi5rKQ7Fiu2QcKo5lJ2wYCJy5Lvp2SCBqf2lvzEERQ0qtky6P'

access_token = '2480130140-fiFfmgRPRMRYmxCf38oDAipkJqNP2qJdWNB1ver'
access_token_secret = 'bKGk52wUFF6YSIzre4yQbPfxBthwLtxkx8TLn6sqaolYR'
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)



#Step 2b - Function of labelisation of analysis
def get_label(analysis, threshold = 0):
	if analysis.sentiment[0]>threshold:
		return 'Positive'
	else:
		return 'Negative'

def get_polarity(topic):
	#Step 2 - Prepare query features
	#List of candidates to French Republicans Primary Elections
	candidates_names = ['Clinton', 'Trump']
	#Hashtag related to the debate
	name_of_debate = str(topic) 
	#Date of the debate : October 13th
	since_date = "2016-10-01"
	until_date = "2016-11-06"

	#Step 3 - Retrieve Tweets and Save Them
	all_polarities = dict()
	for candidate in candidates_names:
		this_candidate_polarities = []
		#Get the tweets about the debate and the candidate between the dates
		this_candidate_tweets = api.search(q=[name_of_debate, candidate], count=100, since = since_date, until=until_date)
		#Save the tweets in csv
		with open('%s_tweets.csv' % candidate, 'wb') as this_candidate_file:
			this_candidate_file.write('tweet,sentiment_label\n')
			for tweet in this_candidate_tweets:
				analysis = TextBlob(tweet.text, pos_tagger=PatternTagger(), analyzer=PatternAnalyzer())
				#Get the label corresponding to the sentiment analysis
				this_candidate_polarities.append(analysis.sentiment[0])
				this_candidate_file.write('%s,%s\n' % (tweet.text.encode('utf8'), get_label(analysis)))
		#Save the mean for final results
		all_polarities[candidate] = np.mean(this_candidate_polarities)
	 
	#Step bonus - Print a Result
	sorted_analysis = sorted(all_polarities.items(), key=operator.itemgetter(1), reverse=True)
	print 'Mean Sentiment Polarity in descending order :'
	for candidate, polarity in sorted_analysis:
		print '%s : %0.3f' % (candidate, polarity)

topics = ['Russia', '2A', 'Heathcare', 'Congress', 'Immigration', 'economy', 'wallstreet', 'taxes']

for i in topics:
	print 'polarity of %s' % i
	print '\n'
	get_polarity(i)
	print '\n'