import xbmcaddon

_PLUGIN_NAME = 'plugin.video.wykodi'

    #'Hits': {'descr':'Displays videos(hits) from the [B][COLOR blue]Wykop[/COLOR][/B]','has_sub': 1},
    #'Shared': {'descr':'Displays shared videos from the [B][COLOR blue]Wykop[/COLOR][/B]','has_sub': 0}

_VIDEO_PROVIDERS = {
    "youtube": "YT",
    "youtu.be": "YT",
    "streamable.com": "ST",
    "gfycat.com": "GFY"
}

_TRACK_PLAYS = eval(xbmcaddon.Addon(id = _PLUGIN_NAME).getSetting('track.play').capitalize())

# wykop credentials
API_KEY = xbmcaddon.Addon(id = _PLUGIN_NAME).getSetting('wykop.key')
API_SECRET = xbmcaddon.Addon(id = _PLUGIN_NAME).getSetting('wykop.secret')

# wykop paths
_API_URL = 'https://wykop.pl/api/v3'

# automex
_SHARED_LIMIT = xbmcaddon.Addon(id = _PLUGIN_NAME).getSetting('wykop.shared')

def get_shared_emails() -> list:
    shared_em = []
    for i in range(3):
        she = xbmcaddon.Addon(id = _PLUGIN_NAME).getSetting(f'wykop.sh.e{i + 1}')
        if "@" in she:
            shared_em.append(she)

    return shared_em



_MENU = {
    10: {
        'name': 'Main Menu',
        'descr': '',
        'subcategories': {
            10: {
                'name': 'Wykop',
                'descr': 'Displays videos from the [B][COLOR blue]Wykop[/COLOR][/B]',
                'params': {
                    'endpoint': 'links',
                    'type': 'homepage'
                },
                'mode': 'wykop01',
                'subcategories': {
                    10: {
                        'name': 'Najnowsze',
                        'descr': 'Wykop - Najnowsze wykopy',
                        'params': {'sort': 'newest'}
                    },
                    11: {
                        'name': 'Aktywne',
                        'descr': 'Wykop - Aktywne wykopy',
                        'params': {'sort': 'active'}
                    },
                    12: {
                        'name': 'Komentowane',
                        'descr': 'Wykop - Komentowane wykopy',
                        'params': {'sort': 'commented'}
                    },
                    13: {
                        'name': 'Wykopane',
                        'descr': 'Wykop - Wykopane wykopy',
                        'params': {'sort': 'digged'}
                    }
                }
            },
            11: {
                'name': 'Wykopalisko',
                'descr': 'Displays videos from the [B][COLOR blue]Wykopalisko[/COLOR][/B]',
                'params': {
                    'endpoint': 'links',
                    'type': 'upcoming'
                },
                'mode': 'wykop01',
                'subcategories': {
                    10: {
                        'name': 'Najnowsze',
                        'descr': 'Wykopalisko - Najnowsze wykopy',
                        'params': {'sort': 'newest'}
                    },
                    11: {
                        'name': 'Aktywne',
                        'descr': 'Wykopalisko - Aktywne wykopy',
                        'params': {'sort': 'active'}
                    },
                    12: {
                        'name': 'Komentowane',
                        'descr': 'Wykopalisko - Komentowane wykopy',
                        'params': {'sort': 'commented'}
                    },
                    13: {
                        'name': 'Wykopane',
                        'descr': 'Wykopalisko - Wykopane wykopy',
                        'params': {'sort': 'digged'}
                    }
                }
            },
            12: {
                'name': 'Mikroblog',
                'descr': 'Displays videos from the [B][COLOR blue]Mikroblog[/COLOR][/B]',
                'params': {
                    'endpoint': 'entries',
                },
                'mode': 'wykop02',
                'subcategories': {
                    10: {
                        'name': 'Najnowsze',
                        'descr': 'Mikroblog - Najnowsze wpisy',
                        'params': {'sort': 'newest'}
                    },
                    11: {
                        'name': 'Aktywne',
                        'descr': 'Mikroblog - Aktywne wpisy',
                        'params': {'sort': 'active'}
                    },
                    12: {
                        'name': 'Hot',
                        'descr': 'Mikroblog - Hot wpisy',
                        'params': {'sort': 'hot'},
                        'subcategories': {
                            10 : {
                                'name': 'Ostatnie 24 godziny',
                                'descr': 'Mikroblog - Hot wpisy z ostatnich 24h',
                                'params': {'last_update': 24}
                            },
                            11 : {
                                'name': 'Ostatnie 12 godzin',
                                'descr': 'Mikroblog - Hot wpisy z ostatnich 12h',
                                'params': {'last_update': 12}
                            },
                            12 : {
                                'name': 'Ostatnie 6 godzin',
                                'descr': 'Mikroblog - Hot wpisy z ostatnich 6h',
                                'params': {'last_update': 6}
                            },
                            13 : {
                                'name': 'Ostatnie 3 godziny',
                                'descr': 'Mikroblog - Hot wpisy z ostatnich 3h',
                                'params': {'last_update': 3}
                            },
                            14 : {
                                'name': 'Ostatnie 2 godzin',
                                'descr': 'Mikroblog - Hot wpisy z ostatnich 2h',
                                'params': {'last_update': 1}
                            },
                            15 : {
                                'name': 'Ostatnia godzina',
                                'descr': 'Mikroblog - Hot wpisy z ostatniej godziny',
                                'params': {'last_update': 6}
                            }
                        }
                    },
                }
            },
            13: {
                'name': 'Hity - Wykop',
                'descr': 'Displays hits from the [B][COLOR blue]Wykop[/COLOR][/B]',
                'params': {
                    'endpoint': 'hits/links',
                },
                'mode': 'wykop01',
                'subcategories': {
                    10: {
                        'name': '2024',
                        'descr': 'Rok 2024',
                        'params': {'year': 2024}
                    },
                    20: {
                        'name': '2023',
                        'descr': 'Rok 2023',
                        'params': {'year': 2023}
                    },
                    30: {
                        'name': '2022',
                        'descr': 'Rok 2022',
                        'params': {'year': 2022}
                    },
                    40: {
                        'name': '2021',
                        'descr': 'Rok 2021',
                        'params': {'year': 2021}
                    },
                    50: {
                        'name': '2020',
                        'descr': 'Rok 2020',
                        'params': {'year': 2020}
                    },
                    60: {
                        'name': '2019',
                        'descr': 'Rok 2019',
                        'params': {'year': 2019}
                    },
                    70: {
                        'name': '2018',
                        'descr': 'Rok 2018',
                        'params': {'year': 2018}
                    },
                    80: {
                        'name': '2017',
                        'descr': 'Rok 2017',
                        'params': {'year': 2017}
                    },
                    90: {
                        'name': '2016',
                        'descr': 'Rok 2016',
                        'params': {'year': 2016}
                    },
                    100: {
                        'name': '2015',
                        'descr': 'Rok 2015',
                        'params': {'year': 2015}
                    },
                    110: {
                        'name': '2014',
                        'descr': 'Rok 2014',
                        'params': {'year': 2014}
                    }
                }
            },
            14: {
                'name': 'Hity - Mirko',
                'descr': 'Displays hits from the [B][COLOR blue]Mikroblog[/COLOR][/B]',
                'params': {
                    'endpoint': 'hits/entries',
                },
                'mode': 'wykop02',
                'subcategories': {
                    10: {
                        'name': '2024',
                        'descr': 'Rok 2024',
                        'params': {'year': 2024}
                    },
                    20: {
                        'name': '2023',
                        'descr': 'Rok 2023',
                        'params': {'year': 2023}
                    },
                    30: {
                        'name': '2022',
                        'descr': 'Rok 2022',
                        'params': {'year': 2022}
                    },
                    40: {
                        'name': '2021',
                        'descr': 'Rok 2021',
                        'params': {'year': 2021}
                    },
                    50: {
                        'name': '2020',
                        'descr': 'Rok 2020',
                        'params': {'year': 2020}
                    },
                    60: {
                        'name': '2019',
                        'descr': 'Rok 2019',
                        'params': {'year': 2019}
                    },
                    70: {
                        'name': '2018',
                        'descr': 'Rok 2018',
                        'params': {'year': 2018}
                    },
                    80: {
                        'name': '2017',
                        'descr': 'Rok 2017',
                        'params': {'year': 2017}
                    },
                    90: {
                        'name': '2016',
                        'descr': 'Rok 2016',
                        'params': {'year': 2016}
                    },
                    100: {
                        'name': '2015',
                        'descr': 'Rok 2015',
                        'params': {'year': 2015}
                    },
                    110: {
                        'name': '2014',
                        'descr': 'Rok 2014',
                        'params': {'year': 2014}
                    }
                }
            }, 15: {
                'name': 'Shared',
                'descr': 'Shared videos from [B][COLOR blue]Wykodi[/COLOR][/B]',
                'params': {},
                'mode': 'shared'
            }
        }
    }
}