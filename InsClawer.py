from instagrapi import Client
from instagrapi.mixins.challenge import ChallengeChoice
import pandas as pd
from langdetect import detect
from geopy.geocoders import Nominatim
import time 
import re

class InsClawer:
    def __init__(self):
        self.client = Client()
        self.data = [] 
        self.output = []
        

        
    def get_country_name(self, location):
        geolocator = Nominatim(user_agent="my_app",timeout=5)
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
            
            print("Logged In.")
            
        except Exception as e:
            print(e)
            pass
    
    def clientLogout(self):
        self.client.logout()
        
    # lấy dữ liệu từ amount người dùng đầu tiên
    def getMediasTopData(self, user_input, amount):
        print("getMediasTopData")
        try:
            self.data = self.client.hashtag_medias_top(user_input, amount=amount)
        except Exception as e:
            print(e)
            pass
        
        
    # lấy dữ liệu từ những người đã follow top 5 ngưởi có lượng follow lớn nhất từ file csv
    def getUserFollowersData(self, user_id, amount):  
        print("getUserFollowersData")      
        ### amount là số lượng users
        ids                 = self.client.user_followers(user_id=user_id, amount= amount).keys()
        username            = None
        full_name           = None 
        biography           = None 
        location            = None
        follower_count      = None 
        following_count     = None
        location_name   = None
        language = ""
        
        email = None
        phone =  None
        
        for id in ids:
            try:
                data = self.client.user_info(id).dict() 
                try:
                    pk          = int( data["pk"] )
                except TypeError:
                    print("Value cannot be converted to an integer.")
                    pass
                username        = data['username']
                full_name       = data['full_name']
                biography       = data['biography']
                
                try:
                    location        = data['location']
                except Exception as e:
                    pass
                
                ## Lấy thông tin Is Private?", "Is Verified?": None, "Media Count", "Following Count"
                more_data           = self.client.user_info_by_username(username).dict()
                
                follower_count      = more_data['follower_count']
                following_count     = more_data["following_count"]
                
                

                email           = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b', biography)
                phone           = re.findall(r'\b\d{10,11}\b', biography)
                
                if location is not None:
                    location_name   = location['name']
                    if self.get_country_name(location_name):
                        language = "German"
                    else:
                        language = "Others"
                else: 
                    location_name = "No City"
                    if self.classify_language(biography):
                        language = "German"
                    else:
                        language = "Others"
                        
                
                if username not in self.output:
                    self.output.append({
                        "PK"                : pk,
                        "Username"          : username,
                        "Full name"         : full_name,
                        "Email"             : email,
                        "Phone"             : phone,
                        "Followers"         : follower_count,
                        "Following Count"   : following_count,
                        "City"              : location_name,
                        "Language"          : language
                    })
                    print(f"Added {username}")
                    time.sleep(3)
            except Exception as e:
                print(e)
                
                pass

    
    
    def getUserData(self):
        print("getUserData")
        
        username            = None
        full_name           = None 
        biography           = None 
        location            = None
        follower_count      = None 
        following_count     = None
        
        location_name       = None
        language            = ""
        
        email               = None
        phone               =  None
        
        for d in self.data:
            data            = d.dict()
            try:
                pk          = int( data["user"]["pk"] )
            except TypeError:
                print("Value cannot be converted to an integer.")
                pass
            username        = data['user']['username']
            full_name       = data['user']['full_name']
            biography       = data['caption_text']
            
            try:
                location        = data['location']
            except Exception as e:
                pass
            
            
            
            ## Lấy thông tin Is Private?", "Is Verified?": None, "Media Count", "Following Count"
            more_data           = self.client.user_info_by_username(username).dict()
            following_count     = more_data["following_count"]
            follower_count      = more_data["follower_count"]
            
            email           = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b', biography)
            phone           = re.findall(r'\b\d{10,11}\b', biography)
                
            if location is not None:
                location_name   = location['name']
                if self.get_country_name(location_name):
                    language = "German"
                else:
                    language = "Others"
            else: 
                location_name = "No City"
                if self.classify_language(biography):
                    language = "German"
                else:
                    language = "Others"
            
                
            if username not in self.output:
                if follower_count > 0:
                    # Lấy thông tin followers
                    self.getUserFollowersData(user_id=pk, amount=50)                    
                    
                
                self.output.append({
                    "PK":                   pk,
                    "Username":             username,
                    "Full name":            full_name,
                    "Email":                email,
                    "Phone":                phone,
                    "Followers":            follower_count,
                    "Following Count":      following_count,
                    "City":                 location_name,
                    "Language":             language,
                })
                print(f"Added {username}")
                time.sleep(3)
                
    
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
        
    def savingOnlyEmailorPhone(self, file_path):
        # Đọc dữ liệu từ tệp CSV gốc
        df = pd.read_csv(file_path)
        filtered_data = df.query('Email != "[]" or Phone != "[]"')
        filtered_data.to_csv(file_path, index=False)
        
    
    
      
