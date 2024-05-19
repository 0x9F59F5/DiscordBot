import re
from twikit import Client

USERNAME = 'twitter id'
EMAIL = 'email'
PASSWORD = 'password'
client = Client('en-US')
client.login(
	auth_info_1=USERNAME,
	auth_info_2=EMAIL,
	password=PASSWORD
)


def main():
	user_list = ['user']

	for users in user_list:

		user = client.get_user_by_screen_name(users)
		TWEET_IDS = user.get_tweets('Tweets')[0:5]

		for TWEET_ID in TWEET_IDS:  # 리스트의 각 요소에 대해 반복
			tweet = client.get_tweet_by_id(TWEET_ID.id)

			name, screen_name, profile_image_url = get_twitter_user_profile(user)

			tweet_data = get_twitter_user_tweet(tweet)
			if tweet_data is None:
				continue

			text, medias, videos, id, urls, created_at_datetime = tweet_data

			print(
				text,
				medias,
				videos,
				id,
				urls,
				created_at_datetime
			)


def get_twitter_user_profile(user):
	return [
		user.name,
		user.screen_name,
		user.profile_image_url.replace("_normal", "")
	]


def get_twitter_user_tweet(tweet):

	tweet_text = tweet.full_text
	urls = []
	medias = []
	videos = []

	# print(tweet_text)

	if tweet.media:

		for media in tweet.media:
			if 'video_info' in media:
				continue
			medias.append(media['media_url_https'])
	else:
		medias.append(None)

	if tweet.media and "video_info" in tweet.media[0]:
		last_variant_url = tweet.media[0]["video_info"]["variants"][-1].get("url", "")
		if last_variant_url:
			videos.append(last_variant_url)
		else:
			videos.append(None)

	if tweet.is_quote_status:
		urls.append(f'https://twitter.com/{tweet.quote.user.screen_name}/status/{tweet.quote.id}')

	# 트윗의 링크를 원본 링크로 변환
	if re.search(r'https?://\S+', tweet.text):

		for url in tweet.urls:
			shortened_url = url['url']
			expanded_url = url['expanded_url']

			urls.append(expanded_url)

			tweet_text = tweet_text.replace(shortened_url, expanded_url)

		text = re.sub(r'https://t.co/\S+', '', tweet_text)

		return [
			text,
			medias,
			videos,
			tweet.id,
			urls,
			tweet.created_at_datetime
		]
	else:
		return [
			tweet.text,
			medias,
			videos,
			tweet.id,
			urls,
			tweet.created_at_datetime
		]


main()
