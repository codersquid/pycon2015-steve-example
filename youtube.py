#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
# if you don't import apiclient first, oath2 can't import urllib
from apiclient.discovery import build
from steve.util import (
    get_from_config,
    get_project_config,
    save_json_files
)
import argparse

from pyconscrape import (
    parse_title,
    parse_speakers,
    parse_speakers_and_description,
)


DRAFT = 2


class YouTubeScraper(object):
    def __init__(self, cfg, max_results=50):
        self.max_results = max_results
        self.cfg = cfg
        self.svc = build(
            get_from_config(cfg, 'api_service_name', 'youtube'),
            get_from_config(cfg, 'api_version', 'youtube'),
            developerKey=get_from_config(cfg, 'api_key', 'youtube'),
        )

    def scrape_channel(self, channel_id):
        video_ids = self.list_channel(channel_id)
        videos = self.list_videos(video_ids)
        data = self.video_results_to_steve_data(videos)
        return data

    def scrape_playlist(self, playlist_id):
        video_ids = self.list_playlist(playlist_id)
        videos = self.list_videos(video_ids)
        data = self.video_results_to_steve_data(videos)
        return data

    def list_playlist(self, playlist_id):
        options = {
            'part': 'id,snippet',
            'maxResults': self.max_results,
            'playlistId': playlist_id,
        }
        response = self.svc.playlistItems().list(**options).execute()
        pages = [[item['snippet']['resourceId']['videoId'] for item in response.get('items', [])]]
        while 'nextPageToken' in response:
            options['pageToken'] = response['nextPageToken']
            print 'fetching next page {}'.format(options['pageToken'])
            response = self.svc.playlistItems().list(**options).execute()
            pages.append([item['snippet']['resourceId']['videoId'] for item in response.get('items', [])])
        return pages

    def list_channel(self, channel_id):
        options = {
            'channelId': channel_id,
            'maxResults': self.max_results,
            'part': 'id',
            'type': 'video',
        }
        search_response = self.svc.search().list(**options).execute()
        pages = [[item['id']['videoId'] for item in search_response.get('items', [])]]

        while 'nextPageToken' in search_response:
            options['pageToken'] = search_response['nextPageToken']
            print 'fetching next page {}'.format(options['pageToken'])
            search_response = self.svc.search().list(**options).execute()
            pages.append([item['id']['videoId'] for item in search_response.get('items', [])])
        return pages

    def list_videos(self, video_pages):
        videos = []
        for page in video_pages:
            videostr = ','.join(page)
            video_response = self.svc.videos().list(
                id=videostr,
                part='snippet,player,status'
            ).execute()
            videos.extend([v for v in video_response.get('items', [])])
        return videos

    def video_results_to_steve_data(self, video_results):
        data = []
        for v in video_results:
            d = self.video_to_dict(v)
            if 'id' not in v:
                # should never happen
                continue
            fn = 'json/{}.json'.format(v['id'])
            data.append((fn, d))
        return data

    def video_to_dict(self, video):
        """Converts youtube#video to a python dict
        """

        snippet = video.get('snippet', {})
        status = video.get('status', {})
        player = video.get('player', {})
        thumbnails = snippet.get('thumbnails', {})
        thumbnail = thumbnails.get('high', {})
        video_id = video['id']

        """
        if self.cfg.has_option('project', 'language'):
            language = get_from_config(self.cfg, 'language'),
        else:
            language = 'English'
        """

        raw_title = snippet.get('title', '')
        title = parse_title(raw_title)
        raw_description = snippet.get('description', '')
        d = parse_speakers_and_description(raw_description)
        raw_speakers = d['speakers']
        speakers = parse_speakers(raw_speakers)

        item = {
            'category': get_from_config(self.cfg, 'category'),
            'title': title,
            'description': d['description'],
            'copyright_text': status.get('license', ''),
            'recorded': snippet.get('publishedAt', '')[0:10],
            'thumbnail_url': thumbnail.get('url', ''),
            'embed': player.get('embedHtml', ''),
            'summary': '',
            'language': 'English',
            'state': DRAFT,
            'whiteboard': 'needs editing',
            'quality_notes': '',
            'slug': '',
            'speakers': speakers,
            'source_url': 'https://www.youtube.com/watch?v={}'.format(video_id)
        }
        return item



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--maxresults", help="Max results", default=50)
    parser.add_argument("-c", "--channel", action='store_true', help="YouTube channel id")
    parser.add_argument("-p", "--playlist", action='store_true',  help="YouTube playlist id")
    args = parser.parse_args()

    cfg = get_project_config()

    scraper = YouTubeScraper(cfg, max_results=args.maxresults)

    if args.channel:
        channel_id = get_from_config(cfg, 'channel_id', 'youtube')
        print("scraping channel {}".format(channel_id))
        data = scraper.scrape_channel(channel_id)
        save_json_files(cfg, data)

    elif args.playlist:
        playlist_id = get_from_config(cfg, 'playlist_id', 'youtube')
        print("scraping playlist {}".format(playlist_id))
        data = scraper.scrape_playlist(playlist_id)
        save_json_files(cfg, data)

    else:
        print("nothing to do. no channel or playlist requested")
