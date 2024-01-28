from scripts.mysql import *
import pandas as pd

class Sql(Mysql):
    def __init__(self):
        super().__init__(0)

    def q1(self):
        query = """SELECT video_name, channel_name FROM Video"""
        self.cursor.execute(query)
        data = self.cursor.fetchall()
        self.cursor.close()
        df = pd.DataFrame(data , columns=["Video Name" , "Channel Name"]).reset_index(drop= True)
        df.index += 1
        return(df)
    
    def q2(self):
        query = """SELECT channel_name, COUNT(video_id) AS number_of_videos
                    FROM Video
                    GROUP BY channel_name;
                    """
        self.cursor.execute(query)
        data = self.cursor.fetchall()
        self.cursor.close()
        df = pd.DataFrame(data,columns=["Channel Name" , "Video Count"] ).reset_index(drop = True)
        df.index += 1
        return(df)
    
    def q3(self):
        query = """ SELECT channel_name, video_name, view_count
                FROM Video
                ORDER BY view_count DESC
                LIMIT 10;
                """
        self.cursor.execute(query)
        data = self.cursor.fetchall()
        self.cursor.close()
        df = pd.DataFrame(data,columns=["Channel Name" , "Video Name", "Views"] ).reset_index(drop = True)
        df.index += 1
        return(df)
        
    def q4(self):
        query = """SELECT Video_name, comment_count from video ORDER BY comment_count DESC;"""
        self.cursor.execute(query)
        data = self.cursor.fetchall()
        self.cursor.close()
        df = pd.DataFrame(data,columns=[ "Video Name", "Comment Count"] ).reset_index(drop = True)
        df.index += 1
        return(df)
    
    def q5(self):
        query = """ SELECT v.video_name, v.channel_name, v.like_count AS highest_likes
                FROM Video v
                JOIN (
                    SELECT channel_name, MAX(like_count) AS max_likes
                    FROM Video
                    GROUP BY channel_name
                ) max_likes_per_channel ON v.channel_name = max_likes_per_channel.channel_name
                                        AND v.like_count = max_likes_per_channel.max_likes
                ORDER BY highest_likes DESC, v.video_name, v.channel_name;
                """
        self.cursor.execute(query)
        data = self.cursor.fetchall()
        self.cursor.close()
        df = pd.DataFrame(data,columns=[ "Video Name", "Channel Name", "Like Count"] ).reset_index(drop = True)
        df.index += 1
        return(df)
    
    def q6(self):
        query = """SELECT video_name, like_count FROM video ORDER BY like_count DESC;"""
        self.cursor.execute(query)
        data = self.cursor.fetchall()
        self.cursor.close()
        df = pd.DataFrame(data,columns=[ "Video Name", "Like Count"] ).reset_index(drop = True)
        df.index += 1
        return(df)
    
    def q7(self):
        query = """SELECT channel_name, channel_views FROM channel ORDER BY channel_views DESC;"""
        self.cursor.execute(query)
        data = self.cursor.fetchall()
        self.cursor.close()
        df = pd.DataFrame(data,columns=[ "Channel Name", "Views Count"] ).reset_index(drop = True)
        df.index += 1
        return(df)
    
    def q8(self):
        query = """ SELECT channel_name, video_name, published_date
                FROM Video
                WHERE EXTRACT(YEAR FROM published_date) = 2022;
                """
        self.cursor.execute(query)
        data = self.cursor.fetchall()
        self.cursor.close()
        df = pd.DataFrame(data,columns=[ "Channel Name", "Video Name", "Published Date"] ).reset_index(drop = True)
        df.index += 1
        return(df)

    def q9(self):
        query = """ SELECT channel_name, AVG(duration) AS avg_duration_seconds
                FROM Video
                GROUP BY channel_name;
                """
        self.cursor.execute(query)
        data = self.cursor.fetchall()
        self.cursor.close()
        df = pd.DataFrame(data,columns=[ "Channel Name", "Avg.Duration"] ).reset_index(drop = True)
        df.index += 1
        return(df)

    def q10(self):
        query = """ SELECT v.video_name, v.channel_name, v.comment_count AS highest_comments
                FROM Video v
                JOIN (
                    SELECT channel_name, MAX(comment_count) AS max_comments
                    FROM Video
                    GROUP BY channel_name
                ) max_comments_per_channel ON v.channel_name = max_comments_per_channel.channel_name
                                        AND v.comment_count = max_comments_per_channel.max_comments
                ORDER BY highest_comments DESC, v.video_name, v.channel_name;
                """
        self.cursor.execute(query)
        data = self.cursor.fetchall()
        self.cursor.close()
        df = pd.DataFrame(data,columns=[ "Video Name", "Channel Name", "Comment Count"] ).reset_index(drop = True)
        df.index += 1
        return(df)