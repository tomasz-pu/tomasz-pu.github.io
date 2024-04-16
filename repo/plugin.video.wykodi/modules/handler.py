import requests
import hashlib
import json
import re
import html
from modules.processor import get_video_url
from modules.automex import get_shared
from modules.config import _VIDEO_PROVIDERS, _SHARED_LIMIT, get_shared_emails
from modules.api_wrapper import get_JWT_token, call_wykop


def calc_pagination(page, pages_limit):
    pagination = {}
    pagination['last_page'] = int(page) * int(pages_limit)
    pagination['first_page'] = pagination['last_page'] - int(pages_limit) + 1
    return pagination


def convert_txt(text):
    sign_dict = {
        '&quot;': '"',
        '&amp;': '&',
        '<br />': '',
        '&lt;': '<',
        '&gt;': '>'
    }
    tag_re = re.compile(r'(<!--.*?-->|<[^>]*>)')

    text = tag_re.sub('', text)
    text = html.escape(text)

    for sign, correct_sign in sign_dict.items():
        text = text.replace(sign, correct_sign)

    return text


def cut_txt(text, char_c) -> str:
    if len(text) > char_c:
        text = text[0:char_c - 1]
    return text


def prepare_description(descr) -> str:
    descr = convert_txt(descr)
    descr = cut_txt(descr, 60)
    return descr


def get_video(url: str) -> str:
    source_lbl = False
    video_url = False
    for keyword, v_provider in _VIDEO_PROVIDERS.items():
        if keyword in url:
            video_url = get_video_url(v_provider, url)
            source_lbl = v_provider
            break
    return video_url, source_lbl


def parse_links(link: dict) -> dict:
    rec_dict = False
    video_url = False
    if 'source' in link.keys() and 'url' in link['source'].keys():
        # get the link
        video_url, source_lbl = get_video(link['source']['url'])

        if video_url:
            # get the name
            rec_dict = {}
            rec_dict['id'] = link['id']
            rec_dict['name'] = (
                f"[B][COLOR orange][{link['votes']['count']}][/COLOR][/B] "
                f"[COLOR gray][{source_lbl}]"
                f"[/COLOR] {prepare_description(link['title'])}..."
            )
            rec_dict['thumb'] = ''
            if link['media']['embed'] is not None:
                rec_dict['thumb'] = link['media']['embed']['thumbnail']
            rec_dict['video'] = video_url
            rec_dict['plot'] = link['description']
            rec_dict['original_url'] = link['source']['url']
            rec_dict['descr'] = link['description']

    return rec_dict


def parse_entries(entry: dict) -> dict:
    rec_dict = False
    video_url = False
    if entry['media']['embed'] is not None:
        # get the link
        video_url, source_lbl = get_video(entry['media']['embed']['url'])

        if video_url:
            # get the name
            rec_dict = {}
            rec_dict['id'] = entry['id']
            rec_dict['name'] = (
                f"[B][COLOR orange][{entry['votes']['up']}][/COLOR][/B] "
                f"[COLOR gray][{source_lbl}]"
                f"[/COLOR]){prepare_description(entry['content'])}..."
            )
            rec_dict['thumb'] = ''
            if entry['media']['embed'] is not None:
                rec_dict['thumb'] = entry['media']['embed']['thumbnail']
            rec_dict['video'] = video_url
            rec_dict['plot'] = entry['content']
            rec_dict['original_url'] = entry['media']['embed']['url']
            rec_dict['descr'] = entry['content']
    return rec_dict


def parse_shared(shared: dict) -> dict:
    rec_dict = False
    video_url = False

    video_url, source_lbl = get_video(shared['url'])

    if video_url:
        rec_dict = {}
        rec_dict['id'] = shared['id']
        rec_dict['name'] = (
                f"[B][COLOR orange][{shared['id']}][/COLOR][/B] "
                f"[COLOR gray][{source_lbl}][/COLOR] "
                f"{shared['description']}... "
            )
        rec_dict['thumb'] = shared['img']
        rec_dict['video'] = video_url
        rec_dict['plot'] = f"[COLOR orange]#{shared['created_at']}[/COLOR][CR]"
        rec_dict['original_url'] = shared['url']
        rec_dict['descr'] = shared['description']

    return rec_dict


def get_videos(mode: str, params: dict, api_key: str, api_secret: str) -> dict:
    vid_dictionary = {
        'links': []
    }
    # check if the request needs to go to Wykop
    if 'wykop' in mode:
        # get the token
        _jwt = get_JWT_token(api_key, api_secret)
        # check if token is generated
        if _jwt:
            # pagination 5 pages
            _lp = int(params['page']) * 5
            _fp = _lp - 5 + 1
            for x in range(_fp, _lp + 1):
                # set page no
                params['page'] = x
                api_req = call_wykop(_jwt, params)
                if api_req['data']:
                    for link in api_req['data']:
                        if mode == 'wykop01':
                            v_line = parse_links(link)
                        elif mode == 'wykop02':
                            v_line = parse_entries(link)

                        if v_line:
                            vid_dictionary['links'].append(v_line)
    if 'shared' in mode:
        response = json.loads(get_shared(params['page'], _SHARED_LIMIT))
        for shared_link in response['links']:
            # print(shared_link['url'])
            v_line = parse_shared(shared_link)

            if v_line:
                vid_dictionary['links'].append(v_line)

    return vid_dictionary

def build_shared_emails_list() -> list:
    shar_l = get_shared_emails()
    return shar_l
