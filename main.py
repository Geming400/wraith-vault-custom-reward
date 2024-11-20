import base64
import logging
import random
from mitmproxy import http
import hashlib

logging.basicConfig(level=logging.DEBUG)

def gen_random_chars():
    return ''.join(random.choice('1234567890qwertyuiopaqsdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM') for i in range(5))

def add_reward_hash(raw_reward_string: str, ):
    SALT = "pC26fpYaQCtg"
    
    reward_hash = hashlib.sha1((raw_reward_string[5:] + SALT).encode())
    return reward_hash.hexdigest()

def cyclic_xor(plaintext: str, key: str):
    def text2ascii(text):
        return [ord(c) for c in text]

    key = text2ascii(key)
    plaintext = text2ascii(plaintext)

    keysize = len(key)
    input_size = len(plaintext)

    cipher = []

    for i in range(input_size):
        cipher.append(plaintext[i] ^ key[i % keysize])

    return ''.join(chr(c) for c in cipher)

def decode_chk(chk: str, random_limit = 5, xor_key = "59182") -> int:
    """Returns the original chosen random value

    Args:
        chk (str): The chk.
        random_limit (int, optional): What's the lenght of the random letters. Defaults to 5.
        xor_key (str, optional): The xor key used to decode the random value. Defaults to "59182".
    """
    
    chk_2 = chk[random_limit:]
    """The second part of the CHK
    """
    
    return int(cyclic_xor(base64.b64decode(chk_2.encode()).decode(), xor_key))

def decode_secret_reward(raw_string: str):
    return cyclic_xor(
        base64.urlsafe_b64decode(raw_string.split("|")[0][5:].encode()).decode(),
        '59182')

def encrypt_secret_reward(reward_string: str, add_hash = True, random_chars = gen_random_chars(), log=False, appended_front_chars = gen_random_chars()) -> str:
    xor_result = cyclic_xor(random_chars + ":" + reward_string, '59182')

    
    encoded_string = base64.urlsafe_b64encode(xor_result.encode()).decode()
    
    if log:
        logging.info("New response (decoded): " + random_chars + ":" + reward_string)
        
    if add_hash:
        return appended_front_chars + encoded_string + "|" + add_reward_hash(encrypt_secret_reward(reward_string, False, random_chars=random_chars, appended_front_chars=appended_front_chars))
    else:
        return appended_front_chars + encoded_string

class Items:  
    class Shards:
        fire = 1
        ice = 2
        poison = 3
        shadow = 4
        lava = 5
        earth = 10
        blood = 11
        metal = 12
        light = 13
        soul = 14
    
    class Obtainables:
        orb = 7
        diamond = 8
    
    class Keys:
        demon_key = 6
        golden_key = 15

class GjRewards:
    def __init__(self) -> None:
        self.chk = ""
        self.original_random_string = ""
    
    def get_random_value_from_chk(self) -> int:
        if self.chk:
            logging.info("Original CHK random value is " + str(decode_chk(self.chk)))
            return decode_chk(self.chk)
        else:
            logging.error("No CHK value found??")
    
    def response(self, flow: http.HTTPFlow) -> None:
        if "reward" in flow.request.path.lower():
            appended_front_chars = flow.response.text[:5] # the random string appended to the front
            logging.info("original_random_string = " + appended_front_chars)
            random_chars = decode_secret_reward(flow.response.text).split(":")[0]
            logging.info("random chars = " + random_chars)
            
            
            REWARD_ID = None
            ITEM_ID = None
            NUM_OF_ITEMS = None
            
            #REWARD_ID = decode_secret_reward(flow.response.text).split(":")[2]
            #ITEM_ID = decode_secret_reward(flow.response.text).split(":")[4].split(",")[0]
            #NUM_OF_ITEMS = decode_secret_reward(flow.response.text).split(":")[4].split(",")[1]
            
            #CHK = f"{''.join(random.choice('1234567890qwertyuiopaqsdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM') for i in range(5))}{base64.b64encode(cyclic_xor(str(random.randint(10000, 1000000)), '59182').encode()).decode()}"
            
            secret_reward = f"{self.get_random_value_from_chk()}:{REWARD_ID}:1:{ITEM_ID},{NUM_OF_ITEMS}"
            encrypted_reward = encrypt_secret_reward(secret_reward, random_chars=random_chars, log=True, appended_front_chars=appended_front_chars)
            
            logging.info("Original response: " + flow.response.text)
            old_response = decode_secret_reward(flow.response.text)
            logging.info("Original response (decoded): " + decode_secret_reward(flow.response.text))

            flow.response.text = encrypted_reward
            
            logging.info("New response: " + flow.response.text)
            
            chars = []
            
            for char in old_response:
                chars.append(ord(char))
            logging.info(chars)
            
            chars = []
            for char in decode_secret_reward(encrypted_reward):
                chars.append(ord(char))
            logging.info(chars)
    
    def request(self, flow: http.HTTPFlow):
        def replace_last_char(text: str, to_replace: str):
            text = text[:len(text) - 1]
            text = text + to_replace
            return text
            
        def url_form_to_dict(url_encoded_form: str):
            dict_url_form = {}
            for item in url_encoded_form.split("&"):
                try:
                    key, value = item.split("=")
                except:
                    key, value = replace_last_char(item, "{EQUAL_SIGN}").split("=")
                    
                dict_url_form[key] = value.replace("{EQUAL_SIGN}", "=")
            return dict_url_form
        
        def dict_to_url_form(dict: dict):
            url_encoded_form = ""
            for key, value in dict.items():
                url_encoded_form = url_encoded_form + f"{key}={value}&"
            return url_encoded_form.removesuffix("&")
            
            
        if "reward" in flow.request.path.lower():
            logging.info(flow.request.text)
            chk = url_form_to_dict(flow.request.text).get("chk")
            if chk:
                logging.info("CHK found! " + chk)
            else:
                logging.error("CHK not found!")
            self.chk = url_form_to_dict(flow.request.text)["chk"]
            
            new_request_body = url_form_to_dict(flow.request.text)
            new_request_body["rewardKey"] = "skibidi"
            
            flow.request.text = dict_to_url_form(new_request_body)
            

addons = [
    GjRewards()
]
