from googleapiclient.discovery import build
import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import requests
from datetime import datetime
import matplotlib
matplotlib.use('Agg')

class YouTubeAnalyzer:
    def __init__(self, api_key):
        self.api_key = api_key
        self.youtube = build('youtube', 'v3', developerKey=api_key)

    def get_channel_id(self, q):
        request = self.youtube.search().list(
            part='id,snippet',
            q=q,
            type='video',
            maxResults=50
        )

        response = request.execute()

        for item in response['items']:
            if q in item['snippet']['channelTitle']:
                return item['snippet']['channelId']

    def get_channel_stats(self, channel_id):
        request = self.youtube.channels().list(
            part="snippet,contentDetails,statistics",
            id=channel_id
        )
        response = request.execute()
        return response['items']

    def get_video_list(self, upload_id):
        video_list = []
        request = self.youtube.playlistItems().list(
            part="snippet,contentDetails",
            playlistId=upload_id,
            maxResults=50
        )
        next_page = True
        while next_page:
            response = request.execute()
            data = response['items']

            for video in data:
                video_id = video['contentDetails']['videoId']
                if video_id not in video_list:
                    video_list.append(video_id)

            if 'nextPageToken' in response.keys():
                next_page = True
                request = self.youtube.playlistItems().list(
                    part="snippet,contentDetails",
                    playlistId=upload_id,
                    pageToken=response['nextPageToken'],
                    maxResults=50
                )
            else:
                next_page = False

        return video_list

    def get_video_details(self, video_list):
        stats_list = []

        for i in range(0, len(video_list), 50):
            request = self.youtube.videos().list(
                part="snippet,contentDetails,statistics",
                id=video_list[i:i + 50]
            )

            data = request.execute()
            for video in data['items']:
                title = video['snippet']['title']
                published = video['snippet']['publishedAt']
                description = video['snippet']['description']
                tag_count = len(video['snippet'].get('tags', []))
                view_count = video['statistics'].get('viewCount', 0)
                like_count = video['statistics'].get('likeCount', 0)
                dislike_count = video['statistics'].get('dislikeCount', 0)
                comment_count = video['statistics'].get('commentCount', 0)
                stats_dict = dict(title=title, description=description, published=published,
                                  tag_count=tag_count, view_count=view_count, like_count=like_count,
                                  dislike_count=dislike_count, comment_count=comment_count)
                stats_list.append(stats_dict)

        return stats_list

    def analyze_channel(self, q):
        channel_id = self.get_channel_id(q)
        if channel_id:
            channel_stats = self.get_channel_stats(channel_id)
            upload_id = channel_stats[0]['contentDetails']['relatedPlaylists']['uploads']
            video_list = self.get_video_list(upload_id)
            video_data = self.get_video_details(video_list)

            df = pd.DataFrame(video_data)
            df['title_length'] = df['title'].str.len()
            df["view_count"] = pd.to_numeric(df["view_count"])
            df["like_count"] = pd.to_numeric(df["like_count"])
            df["dislike_count"] = pd.to_numeric(df["dislike_count"])
            df["comment_count"] = pd.to_numeric(df["comment_count"])

            df['published'] = pd.to_datetime(df['published']).dt.strftime('%m-%Y')

            data = df.copy()
            df_sorted = data[data['published'].str.contains('2022')].sort_values('published')
            df_sorted['published'] = pd.to_datetime(df_sorted['published']).dt.strftime('%m')
            df_sorted['view_count'] = (df_sorted['view_count'] / 10000000)

            self.plot_and_save(df_sorted)

    def plot_and_save(self, df_sorted):
        plot = sns.lineplot(x='published', y='view_count', data=df_sorted, errorbar=None)
        plot.set(title='Views per month in 2022', xlabel='Months in 2022',
                 ylabel='Number of Views(in 10 Millions)')

        # Save the plot as an image
        filename = "static/img/data_image.png"
        plt.savefig(filename, dpi=300, bbox_inches='tight')

if __name__ == "__main__":
    api_key = 'API_KEY'
    youtube_analyzer = YouTubeAnalyzer(api_key)
    youtube_analyzer.analyze_channel("Your Query")
