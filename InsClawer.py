from instagrapi import Client
import pandas as pd
from langdetect import detect
import pycountry
import time 
import re

class InsClawer:
    def __init__(self):
        self.client = Client()
        
        self.data = None 
        self.output = []
        self.username = ""
        self.error = None
        
    def is_in_germany(self, location):
        try:
            country_code = pycountry.countries.search_fuzzy(location).alpha_2
            if country_code == 'DE':
                return True
            else:
                return False
        except LookupError:
            return False
        
    def classify_language(self, bio, location):
        try:
            lang = detect(bio)
            if lang == "de" or self.is_in_germany(location):
                return "German"
        except:
            return "Other"
    
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
            email           = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b', biography)
            phone           = re.findall(r'\b\d{10,11}\b', biography)
            
            
            if location is not None:
                location_name   = location['name']
            else: 
                location_name = ""
            
            
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
                    "Language":     self.classify_language(biography, location_name)
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

        # Kiểm tra và loại bỏ các dữ liệu trùng lặp
        if not existing_data.empty:
            columns_to_check = ['username', 'full_name']
            new_data = new_data.drop_duplicates(subset=columns_to_check)

        # Kết hợp dữ liệu cũ và dữ liệu mới
        combined_data = pd.concat([existing_data, new_data], ignore_index=True)

        # Ghi dữ liệu vào file CSV
        combined_data.to_csv(file_path, index=False, encoding='utf-8')
    
    
    
    
    
    
    
        
        
        
        
    
    