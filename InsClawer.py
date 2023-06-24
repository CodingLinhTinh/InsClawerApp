from instagrapi import Client
import pandas as pd
from langdetect import detect
from geopy.geocoders import Nominatim
import time 
import re

class InsClawer:
    def __init__(self):
        self.client = Client()
        
        self.data = None 
        self.output = []
        self.username = ""
        self.error = None
        
    def get_country_name(self, location):
        geolocator = Nominatim(user_agent="my_app")
        location_data = geolocator.geocode(location, exactly_one=True)
        if location_data:
            is_germany = location_data.raw['display_name'].split(",")[-1].strip()
            if is_germany == "Deutschland":
                return True
        return False
        
    def classify_language(self, bio):
        try:
            lang = detect(bio)
            if lang == "de":
                return True
        except:
            return False
    
    def clientLogin(self ,username, password):
        try:        
            self.client.load_settings("session.json")
            self.client.login(username, password)
            self.client.get_timeline_feed()
            
        except Exception as e:
            self.error = e
            wait_time_minutes = 60
            time.sleep(wait_time_minutes * 60)

    def getUserName(self):
        self.client.delay_range = [1,3]
        self.username = self.client.account_info().dict()["username"]
    
    def clientLogout(self):
        self.client.logout()
        
    # lấy dữ liệu từ amount người dùng đầu tiên
    def getMediasTopData(self, user_input, amount):
        self.client.delay_range = [1,3]
        self.data = self.client.hashtag_medias_top(user_input, amount=amount)
        time.sleep(5)
    
    def getFollowers(self, username):
        self.client.delay_range = [1,3]
        follower_count = self.client.user_info_by_username(username).dict()
        return follower_count["follower_count"]
    
    def getUserData(self):
        for d in self.data:
            data            = d.dict()
            pk              = int( data["user"]["pk"] )
            username        = data['user']['username']
            full_name       = data['user']['full_name']
            biography       = data['caption_text']
            hashtags        = [tag for tag in biography.split() if tag.startswith('#')]
            location        = data['location'] 
            follower_count  = self.getFollowers(username)
            
            
            location_name   = None
            language = ""
            email           = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b', biography)
            phone           = re.findall(r'\b\d{10,11}\b', biography)
            
            
            if location is not None:
                location_name   = location['name']
                if self.get_country_name(location_name):
                    language = "German"
                else:
                    language = "Others"
            else: 
                location_name = ""
                if self.classify_language(biography):
                    language = "German"
                else:
                    language = "Others"
            
            
            if username not in self.output:
                self.output.append({
                    "Username":     username,
                    "Full name":    full_name,
                    "Email":        email,
                    "Phone":        phone,
                    "Biography":    biography,
                    "City":         location_name,
                    "Followers":    follower_count,
                    "Hashtags":     hashtags,
                    "Language":     language
                })
            
    def createCSV(self, file_path):
        # Đọc dữ liệu từ file CSV đã tồn tại (nếu có)
        existing_data = pd.DataFrame()
        try:
            existing_data = pd.read_csv(file_path)
        except FileNotFoundError:
            pass

        # Tạo DataFrame từ dữ liệu mới
        new_data = pd.DataFrame(self.output)

        # Kết hợp dữ liệu cũ và dữ liệu mới
        combined_data = pd.concat([existing_data, new_data], ignore_index=True)

        # Ghi dữ liệu vào file CSV
        combined_data.to_csv(file_path, index=False, encoding='utf-8')
    
    def remove_duplicates_csv(self, file_path, columns_to_check):
        # Đọc dữ liệu từ file CSV
        data = pd.read_csv(file_path)
        
        # Kiểm tra và loại bỏ các dữ liệu trùng lặp dựa trên các cột được chỉ định
        if all(col in data.columns for col in columns_to_check):
            data = data.drop_duplicates(subset=columns_to_check)
        
        # Ghi dữ liệu đã loại bỏ trùng lặp vào file CSV mới
        data.to_csv(file_path, index=False)
    
    
    
    
    
    
    
    
    
        
        
        
        
    
    