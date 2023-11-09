from instagrapi import Client
import pandas as pd
from datetime import datetime, timezone
from geopy.geocoders import Nominatim

import time 

class Automation:
    def __init__(self) -> None:
        self.client = Client()
        self.media_pk = None
        
    
    def clientLogin(self ,username, password):
        try:         
            self.client.load_settings("session.json")
            self.client.login(username, password)
            self.client.get_timeline_feed()
            return True
            
        except Exception as e:
            print(e)
            pass
    
    def clientLogout(self):
        self.client.logout()
    
    def getMediaPkfromUrl(self, media_url):
        return self.client.media_pk_from_url(media_url)
      
    def getMediaId(self, media_pk):
        return self.client.media_id(media_pk)  
    
    def likeAMedia(self, media_pk):
        media_id = self.getMediaId(media_pk)
        self.client.media_like(media_id)
        
    def unlikeAMedia(self,media_pk):
        media_id = self.getMediaId(media_pk)
        self.client.media_unlike(media_id)
    
    def archiveMedia(self, media_pk):
        media_id = self.getMediaId(media_pk)
        self.client.media_archive(media_id)
        
    def unarchiveMedia(self, media_pk):
        media_id = self.getMediaId(media_pk)
        self.client.media_unarchive(media_id)
    
    def viewAMedia(self, media_pk):
        media_id = self.getMediaId(media_pk)
        self.client.media_seen( [media_id] )
       
    def infoAMedia(self, media_pk):
        data = self.client.media_info(media_pk).dict()
        
        time = data["taken_at"]
        lng =  None
        lat =  None
        location = ""
        try:
            lng = data["location"]["lng"]
            lat = data["location"]["lat"]
            # Khởi tạo đối tượng geocoder (Nominatim)
            geolocator = Nominatim(user_agent="my_geocoder")

            # Tìm địa điểm từ tọa độ
            location = str(geolocator.reverse((lat, lng), language="en").address)
        except Exception as e:
            print(e)
            pass
        
        username = data["user"]["username"]
        full_name = data["user"]["full_name"]
        comment_count = data["comment_count"]
        like_count =  data["like_count"]
        caption_text =  data["caption_text"]
        view_count =  data["view_count"]
        video_duration = data["video_duration"]
        title =  data["title"]
        
        formatted_datetime = time.strftime("%Y-%m-%d %H:%M:%S %Z")
        
        return {
            "title": title,
            "caption_text": caption_text,
            "video_duration": video_duration,
            "view_count": view_count,
            "like_count": like_count,
            "comment_count": comment_count,
            "username": username,
            "full_name": full_name,
            "location": location,
            "time": formatted_datetime
        }
        
    def getUserInfoByUsername(self, username):
        return self.client.user_id_from_username(username)
    
    def getUserMedias(self, user_id, amount):
        result = []
        data = self.client.user_medias(user_id, amount=amount)
        for d in data:
            media_id = self.getMediaId(d["pk"])
            result.append(media_id)
            
        self.client.media_seen(result)
        
    def FollowUser(self, user_id):
        return self.client.user_follow(user_id)
    
    def UnFollowUser(self, user_id):
        return self.client.user_unfollow(user_id)
    
# photo_upload(path: Path, caption: str, upload_id: str, usertags: List[Usertag], location: Location, extra_data: Dict = {})
    def PhotoUpload(self,path,caption,extra_data):
        self.client.photo_upload(
            path=path, 
            caption=caption,
            extra_data = extra_data
        )
        
        
        
    
    