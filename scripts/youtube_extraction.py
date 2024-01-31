from googleapiclient.discovery import build
import yaml

with open("src/config.yaml", "r") as config:
    config_data = yaml.safe_load(config)

# API key obtained from the google cloud 
api= config_data['config']['Google_API_Key']

# Api service for youtube to access data of the channel
api_service_name = "youtube"
api_version = "v3"

class Youtube:
    def __init__(self):
        self.youtube = build(api_service_name, api_version, 
                             developerKey=api)

    #function to extract the channel details
    def channel_info(self, chid):

        request = self.youtube.channels().list(part="snippet,contentDetails,statistics", id=chid)
        response = request.execute()
        if 'items'in response and len(response['items']) > 0:
            channel_data =  {'channel_name': response['items'][0]['snippet']['title'],
                             'channel_id': response['items'][0]['id'],
                             'subscription_count': response['items'][0]['statistics']['subscriberCount'],
                             'channel_views': response['items'][0]['statistics']['viewCount'],
                             'channel_description': response['items'][0]['snippet']['description'],
                             'upload_id': response['items'][0]['contentDetails']['relatedPlaylists']['uploads'],
                             'country': response['items'][0]['snippet'].get('country', 'Not Available') }
            return (channel_data)
        
        else:
            return (False)
        
    def playlist_info(self, chid):

        playlist_data = []
        next_page_token = None
        while True:

            request = self.youtube.playlists().list(part="snippet,contentDetails",channelId=chid, 
                                                    maxResults=50, pageToken=next_page_token)
            response = request.execute()

            for item in response['items']: 
                data = {'PlaylistId':item['id'],
                        'Title':item['snippet']['title'],
                        'ChannelId':item['snippet']['channelId'],
                        'ChannelName':item['snippet']['channelTitle'],
                        'PublishedAt':item['snippet']['publishedAt'],
                        'VideoCount':item['contentDetails']['itemCount']}
                playlist_data.append(data)
            next_page_token = response.get('nextPageToken')
            if next_page_token is None:
                break
        return(playlist_data)


    def video_list(self,chid):
        video_ids = []
        request = self.youtube.channels().list(id=chid, part='contentDetails')
        reponse = request.execute()
        playlist_id = reponse['items'][0]['contentDetails']['relatedPlaylists']['uploads']
        next_page_token = None
        
        while True:
            request = self.youtube.playlistItems().list( part = 'snippet', playlistId = playlist_id,  
                                                    maxResults = 50, pageToken = next_page_token)
            response = request.execute()
            
            for i in range(len(response['items'])):
                video_ids.append(response['items'][i]['snippet']['resourceId']['videoId'])
            next_page_token = response.get('nextPageToken')
            
            if next_page_token is None:
                break
        return(video_ids)
    
    def video_info(self, video):

        request = self.youtube.videos().list(part="snippet,contentDetails,statistics", id= video)
        response = request.execute()

        for item in response["items"]:
            data = {'Channel_Name': item['snippet']['channelTitle'],
                    'Channel_Id': item['snippet']['channelId'],
                    'Video_Id': item['id'],
                    'Title' : item['snippet']['title'],
                    'Tags' : item['snippet'].get('tags'),
                    'Thumbnail' : item['snippet']['thumbnails']['default']['url'],
                    'Description' : item['snippet']['description'],
                    'Published_Date' : item['snippet']['publishedAt'],
                    'Duration' : item['contentDetails']['duration'],
                    'Views' : item['statistics']['viewCount'],
                    'Likes' : item['statistics'].get('likeCount'),
                    'Comments' : item['statistics'].get('commentCount'),
                    'Favorite_Count' : item['statistics']['favoriteCount'],
                    'Definition' : item['contentDetails']['definition'],
                    'Caption_Status' : item['contentDetails']['caption']}
        return(data)
    
    def comment_info(self, video):
        
        comments = []
        try:
            request = self.youtube.commentThreads().list(part = "snippet",videoId = video, 
                                                        maxResults = 50 )
            response = request.execute()
            
            
            for item in response["items"]:
                    data = {'Comment_Id' : item["snippet"]["topLevelComment"]["id"],
                            'Video_Id' : item["snippet"]["videoId"],
                            'Comment_Text' : item["snippet"]["topLevelComment"]["snippet"]["textOriginal"],
                            'Comment_Author' : item["snippet"]["topLevelComment"]["snippet"]["authorDisplayName"],
                            'Comment_Published_time' : item["snippet"]["topLevelComment"]["snippet"]["publishedAt"]}
                    comments.append(data)
        except:
            pass

        return(comments)

