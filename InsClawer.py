from instagrapi import Client
import pandas as pd
from instagrapi.exceptions import RateLimitError
import time 

class InsClawer:
    def __init__(self):
        self.client = Client()
        self.data = None 
        self.output = []
        self.username = ""
    
    def clientLogin(self ,username, password):
        try:        
            self.client.load_settings("session.json")
            self.client.login(username, password)
            self.client.get_timeline_feed()
               
        except RateLimitError:
            # Wait for a few minutes before retrying
            wait_time_minutes = 5
            print(f"Rate limit exceeded. Waiting for {wait_time_minutes} minutes...")
            time.sleep(wait_time_minutes * 60) # Convert minutes to seconds

    def getUserName(self):
        self.username = self.client.account_info().dict()["username"]
    
    def clientLogout(self):
        self.client.logout()
        
    # lấy dữ liệu từ amount người dùng đầu tiên
    def getMediasTopData(self, user_input, amount):
        self.data = self.client.hashtag_medias_top(user_input, amount=amount)
    
    def getUserData(self):
        for d in self.data:
            data            = d.dict()
            pk              = data['user']['pk']
            username        = data['user']['username']
            full_name       = data['user']['full_name']
            profile_pic_url = data['user']['profile_pic_url']

            caption         = data['caption_text']
            hashtags        = [tag for tag in caption.split() if tag.startswith('#')]
        
            location        = data['location'] 
            location_name   = None 

            if location is not None:
                location_name   = location['name']
                
            self.output.append({
                "pk":               pk,
                "username":         username,
                "full_name":        full_name,
                "profile_pic_url":  profile_pic_url,
                "caption":          caption,
                "hashtags":         hashtags,
                "location_name":    location_name,
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
    
    
    
    
    
    
    
        
        
        
        
    
    