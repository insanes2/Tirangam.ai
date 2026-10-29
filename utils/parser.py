# utils/parser.py
import requests
from bs4 import BeautifulSoup
from datetime import datetime

class TirangamParser:
    def __init__(self, base_url):
        self.base_url = base_url
    
    def fetch_data(self):
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36' # Modern UA for compatibility
            }
            response = requests.get(self.base_url, headers=headers, timeout=10)

            if response.status_code != 200:
                raise Exception(f"HTTP Error: {response.status_code}")

            soup = BeautifulSoup(response.text, 'lxml')

            results_container = soup.find('div', class_='results-container') # Adjust selector based on actual HTML
            
            current_prediction = None

            if results_container:
                latest_item = results_container.find(class_='latest-result-item') 

                if latest_item:
                    text_span = latest_item.find(class_='result-text')
                    color_class_list = latest_item.get('class', [])

                    result_text = text_span.text.strip() if text_span else ""

                    # Determine side (BIG/SMALL) by checking CSS classes or visual cues like green/red text.
                    is_big = ('text-success' in str(color_class_list).lower() 
                              or 'green' in [c.lower() for c in color_class_list])

                    current_prediction = {
                        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "side": "BIG" if is_big else ("SMALL" if not is_big and len(result_text) > 0 else "UNKNOWN"),
                        "raw_value": result_text,
                        "source_url": self.base_url
                    }

            return current_prediction
            
        except Exception as e:
            print(f"Parsing Error: {e}")
            # Return None or cached data if implemented. Here returning None on fail.
            return None

# Example usage of the parser:
if __name__ == "__main__":
    parser = TirangamParser("https://Tirangam.ai")
    data = parser.fetch_data()
    if data:
        print(f"Predicted Side: {data['side']}")
    else:
        print("Data not received (site might be down).")
