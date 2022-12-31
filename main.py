import dotenv
import os
import re
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import json

results = []
users = []

def main():
    dotenv.load_dotenv()
    slack_token = os.environ['SLACK_BOT_TOKEN']
    channel_name = os.environ.get('CHANNEL_NAME','wordle')

    client = WebClient(token=slack_token)

    try:
        convos_resp = client.conversations_list(limit=1000)
        wordles = [channel for channel in convos_resp['channels'] if channel['name']==channel_name]
        channel_id = wordles[0]['id']
        client.conversations_join(channel=channel_id)

        for msg in iter(yield_messages(client,channel_id)):
            result = parse_msg(msg)
            if result:
                results.append(result)

        user_ids = set(res['user'] for res in results)
        for user_id in user_ids:
            resp = client.users_info(user=user_id)
            profile = resp['user']['profile']
            users.append({'user':user_id, 'real_name':profile['real_name'], 'display_name':profile['display_name']})

        # output = {'results':results, 'users':users}
        # with open('out.json','w') as f:
        #     json.dump(output,f)
        with open('results.json','w') as f:
            json.dump(results,f)
        with open('users.json','w') as f:
            json.dump(users,f)

    except SlackApiError as e:
        # You will get a SlackApiError if "ok" is False
        print(e.response["error"])    # str like 'invalid_auth', 'channel_not_found'

def parse_msg(message):
    result = dict()
    result['user'] = message['user']
    [sec,microsec] = message['ts'].split('.')
    millisec = int(sec+microsec[:3])
    result['ts'] = millisec

    pattern = re.compile(r'(Woo?rdle6?) (\d*) (X|\d*)/')
    m = pattern.search(message['text'])
    if m:
        result['game'] = m.group(1)
        result['index'] = int(m.group(2))
        result['score'] = m.group(3)
        return result
    else:
        print(f'Could not parse: {message}')

def yield_messages(client,channel_id):
    cursor = None
    while True:
        resp = client.conversations_history(channel=channel_id, cursor=cursor)
        for msg in resp['messages']:
            yield msg
        try:
            cursor = resp['response_metadata']['next_cursor']
        except TypeError:
            return


if __name__=='__main__':
    main()