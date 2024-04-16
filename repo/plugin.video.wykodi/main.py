# Module: main
# Author: Tom3kP
# Created on: 08/03/2021

import sys
from urllib.parse import urlencode, parse_qsl
import xbmcgui
import xbmcplugin
import xbmc
import xbmcaddon
from modules.automex import ping, share
from modules.config import _TRACK_PLAYS, API_KEY, API_SECRET, _MENU
from modules.handler import get_videos, build_shared_emails_list

# Get the plugin url in plugin:// notation.
_URL = sys.argv[0]
# Get the plugin handle as an integer number.
_HANDLE = int(sys.argv[1])


def get_url(**kwargs):
    return '{}?{}'.format(_URL, urlencode(kwargs))


def play_video(path):
    play_item = xbmcgui.ListItem(path=path)
    if 'streamable' in path:
        play_item.setMimeType('video/mp4')
        play_item.setContentLookup(False)
    xbmcplugin.setResolvedUrl(_HANDLE, True, listitem=play_item)


def get_cat_details(cat_id: str) -> dict:
    _details = {}
    _details['params'] = {}
    _details['mode'] = {}
    for inx, level in enumerate([int(x) for x in cat_id.split('-')]):
        if inx > 0:
            _level = _details['category']['subcategories'][level]
        else:
            _level = _MENU[level]
        _details['category'] = _level
        if 'params' in _details['category'].keys():
            for par_name, par_val in _details['category']['params'].items():
                _details['params'][par_name] = par_val
        if 'mode' in _details['category'].keys():
            _details['mode'] = _details['category']['mode']
    return _details


def get_content(cat_id=10, page=1) -> None:
    # get the exact tree
    sel_cat = get_cat_details(str(cat_id))
    xbmcplugin.setPluginCategory(_HANDLE, sel_cat['category']['name'])
    xbmcplugin.setContent(_HANDLE, 'videos')
    # check if it is a folder or content needs to be listed
    if 'subcategories' in sel_cat['category'].keys():
        for idx, subcategory in sel_cat['category']['subcategories'].items():
            list_item = xbmcgui.ListItem(label=subcategory['name'])
            list_item.setInfo(
                'video', {
                    'title': subcategory['name'],
                    'plot': subcategory['descr'],
                    'mediatype': 'video'
                }
            )
            # generate url
            url = get_url(action='folder', category=f'{cat_id}-{idx}', page=1)
            xbmcplugin.addDirectoryItem(_HANDLE, url, list_item, True)
    else:
        # add page number to params
        sel_cat['params']['page'] = page
        _videos = get_videos(
            sel_cat['mode'],
            sel_cat['params'],
            API_KEY, API_SECRET
        )
        # Iterate through videos.
        for video in _videos['links']:
            list_item = xbmcgui.ListItem(label=video['name'])
            videoInfoTag = list_item.getVideoInfoTag()
            videoInfoTag.setPlot(video['plot'])
            list_item.setArt(
                {
                    'thumb': video['thumb'],
                    'icon': video['thumb'],
                    'fanart': video['thumb']
                }
            )
            list_item.setProperty('IsPlayable', 'true')
            _nurl = get_url(
                action='share',
                link=video['original_url'],
                descr=video['descr'],
                img=video['thumb']
                )
            
            list_item.addContextMenuItems(
                [
                    ('Share with...', 'RunPlugin(%s)' % (_nurl)),
                ],
                replaceItems=False
            )
            url = get_url(action='play', video=video['video'])
            xbmcplugin.addDirectoryItem(_HANDLE, url, list_item, False)
        # next page
        url = get_url(action='folder', category=cat_id, page=int(page) + 1)
        list_item = xbmcgui.ListItem(
            label="Next (" + str(int(page) + 1) + ")..."
            )
        videoInfoTag = list_item.getVideoInfoTag()
        videoInfoTag.setPlot(
            'See the next page: [B]' + str(int(page) + 1) + '[/B]'
        )
        list_item.setProperty('IsPlayable', 'false')
        xbmcplugin.addDirectoryItem(_HANDLE, url, list_item, True)

    xbmcplugin.endOfDirectory(_HANDLE)


def router(paramstring) -> None:
    params = dict(parse_qsl(paramstring))
    if params:
        if params['action'] == 'folder':
            get_content(params['category'], params['page'])
        elif params['action'] == 'play':
            if _TRACK_PLAYS:
                ping({
                    "video": params['video']
                })
            # Play a video from a provided URL.
            play_video(params['video'])

        elif params['action'] == 'share':

            dialog = xbmcgui.Dialog()

            emails_list = build_shared_emails_list()
            if len(emails_list) > 0:
                pass
                #ret = dialog.contextmenu(emails_list)
                ret = dialog.select('Share with..', emails_list)
                if ret != -1:
                    share(params['link'], params['descr'], params['img'], emails_list[ret])
                    not_txt = f'Shared with {emails_list[ret]}'
                else:
                    not_txt = 'Sharing cancelled'
            else:
                not_txt = 'Please add email address(es) to share with'

            __addon__ = xbmcaddon.Addon()

            notification = (
                __addon__.getAddonInfo('name'),  # addonname
                not_txt,  # text to display
                5000,  # time in miliseconds
                __addon__.getAddonInfo('icon')  # icon
            )

            xbmc.executebuiltin(
                'Notification(%s, %s, %d, %s)' % notification
            )
    else:
        get_content()

if __name__ == '__main__':
    router(sys.argv[2][1:])
