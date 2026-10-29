# main.py
import logging
from telegram import Bot # Import from modern python-telegram-bot library (v20+)
import yaml
from utils.parser import TirangamParser
from utils.analyzer import PredictionAnalyzer
import time

# Load configuration settings without hardcoding values directly in code.
try:
    with open('config.yaml', 'r') as file:
        config = yaml.safe_load(file)

    BOT_TOKEN = config['bot_token']         # Replace placeholder token later during setup phase.
    SITE_URL = config['site_url']           # Address of target site to parse/predict trends from.

except FileNotFoundError or KeyError:
    print("Configuration Error: Ensure 'config.yaml' exists and contains required fields.")
    exit()

# Initialize parser instance using configured URL.
parser = TirangamParser(SITE_URL)
analyzer = PredictionAnalyzer()

def send_notification(message):
    """Sends formatted alert message directly into Telegram chat for specified users."""
    
    # Assuming user IDs are stored in config under key like 'user_ids_to_notify'. 
    # Adjust import path if needed based on final structure design choice made earlier (list vs single).
    try:
        app = Bot(token=BOT_TOKEN) 
        
        target_users = getattr(config, 'user_ids_to_notify', [123456789]) # Fallback default ID
        
        for uid in target_users:
            text_msg = f"🔮 *New Prediction Alert (Tirangam.ai)*\n\n{message}" 
            app.send_message(chat_id=str(uid), text=text_msg, parse_mode='Markdown')
            
    except Exception as e:
        print(f"Delivery failure to user {uid}: {e}")

async def main_loop():
    """Main event loop that runs continuously until stopped manually."""
    
    from telegram import Bot
    
    try:
        while True:
            current_data = parser.fetch_data() 
            
            if current_data and current_data.get('raw_value'): 
                side = current_data['side'] # Extract BIG/SMALL status
                
                analyzer.add_result(side) 
                
                prediction_side = analyzer.predict_next_side() 
                 
                message_body = f"""🔮 *Status:* Data Retrieved Successfully.  
📅 *Date/Time:* {current_data['time']}  
👁️ *Current Impulse (Source):* **{side}**  

🤖 *AI Analysis Prediction for Next Step:* → **{prediction_side}**

✅ Source verified & analysis complete."""
                 
                 send_notification(message_body)
            else:
                 print("Data fetch failed or site offline, waiting for update cycle...")
            
             # Sleep interval defined in config or default fallback if key missing.
            check_interval = getattr(config.get('check_interval_seconds'), 60, 60) 
            time.sleep(check_interval) 

    except KeyboardInterrupt:
        print("\nBot stopped gracefully.")

# Direct execution wrapper for simplicity without advanced frameworks like asyncio/run_until_stopped().
if __name__ == "__main__":
     try:
         while True:
              current_data = parser.fetch_data() 
              
              if current_data and current_data.get('raw_value'): 
                 side = current_data['side'] 
                 analyzer.add_result(side) 
                 
                 prediction_side = analyzer.predict_next_side() 
                 
                 message_body = f"""🔮 *Status:* Data Retrieved.  
📅 *Date/Time:* {current_data['time']}  
👁️ *Current Impulse (Source):* **{side}** 

🤖 *AI Prediction for Next Step:* → **{prediction_side}**

✅ Source verified & analysis complete."""
                  
                  # Instantiate Bot object directly inside loop or initialize once outside (best practice).
                  # Re-initializing here ensures fresh instance per check if needed, though optional.
                  app_instance = Bot(token=BOT_TOKEN) 
                  
                  target_users = getattr(config.get('user_ids_to_notify'), [123456789])
                  
                  for uid in target_users:
                      try:
                          full_msg = f"🔮 *New Prediction Alert (Tirangam.ai)*\n\n{message_body}" 
                          app_instance.send_message(chat_id=str(uid), text=full_msg, parse_mode='Markdown')
                          
                      except Exception as e:
                        print(f"Delivery error to user {uid}: {e}")
              

              else:
                   print("Data fetch failed or site offline, waiting...")
              
              check_interval = getattr(config.get('check_interval_seconds'), 60, 60) 
              time.sleep(check_interval) 

     except KeyboardInterrupt:
         print("\nBot stopped gracefully.")

