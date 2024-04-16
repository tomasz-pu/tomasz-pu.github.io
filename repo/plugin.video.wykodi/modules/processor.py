import requests
import json
from urllib import parse

def get_video_url(channel, url):
    if channel == "GFY":
        x_start='"video":'
        x_end = '</script><style data-react-helmet="true">'
        y_end = '"creator"'

        try:
            request = requests.get(url).text
            start_index = request.find(x_start) + len(x_start)
            end_index = request.find(x_end)
            request = request[start_index:end_index]
            new_url = json.loads(request[0:request.find(y_end) - 1] + str('}'))
            return new_url['contentUrl']
        except:
            return False
    
    if channel == "ST":
        try:
            request = requests.get(url).text
            og_start='"og:video:secure_url" content="'
            og_end = '"/><meta property="og:video:type"'

            start_index = request.find(og_start) + len(og_start)
            end_index = request.find(og_end)

            new_url = request[start_index:end_index].replace('">','')
            new_url = new_url.replace(' ','')
            new_url = new_url.replace('&amp;','&')
            new_url = new_url.rstrip()
            #print("debug:: ",new_url)
            return new_url
        except:
            return False

    if channel == "YT":
        rem_youtube = "https://youtu.be/"
        yt_suff = "?t="
        plugin = "plugin://plugin.video.youtube/play/?video_id="
        try:
            if 'https://consent.youtube.com/m?continue=' in url:
                # remove the consent message
                url = url.replace('https://consent.youtube.com/m?continue=','')
                # encode 
                url = parse.unquote(url)

            if 'youtube.com' in url:
                if '/shorts/' not in url:
                    params = parse.parse_qs(parse.urlsplit(url.replace('/v/','?v=')).query)
                    print(url, params)
                    return plugin + params['v'][0]
                else:
                    if '?' in url:
                        url = url[0:url.index('?')]
                    url = url.replace('https://youtube.com/shorts/','')
                    return plugin + url
            else:
                if 'youtu.be' in url:
                    if yt_suff in url:
                        # remove parameters
                        url = url[0:url.index(yt_suff)]
                    return plugin + url.replace(rem_youtube,'')  
                else:
                    return False
        except:
            return False