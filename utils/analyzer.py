# utils/analyzer.py
from typing import Optional, Dict, List

class PredictionAnalyzer:
    
    def __init__(self):
        self.history = [] # Store results like {"time": None, "side": "BIG"} or similar
        
    def add_result(self, side: str):
        """Records a result into memory."""
        from datetime import datetime
        self.history.append({"time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "side": side})
        
        # Keep only last 10 entries to avoid memory bloat during long runs.
        if len(self.history) > 10: 
            del self.history[0]

    def predict_next_side(self) -> Optional[str]:
        """Simple logic: If recent majority follows one trend, continue it; else reverse (optional)."""
        
        if len(self.history) < 2:
            return None

        last_results = [item['side'] for item in reversed(self.history)][:5] # Review the latest 5 results
        
        big_count = last_results.count('BIG')
        small_count = last_results.count('SMALL')
        
        total = big_count + small_count
        
        if total == 0: return None

        ratio_big = big_count / total * 100
        
        # Strategy Example A: Follow Strong Trend (>70% dominance) OR Immediate Impulse.
        # Adjust thresholds based on your preferred risk profile.
        
        if ratio_big >= 70 and 'BIG' in last_results[-1]: 
            return "BIG" 
        elif (total - big_count)/total * 100 >= 70 and 'SMALL' in last_results[-1]:
            return "SMALL"
        else:
             # If balanced or low sample size, follow the most recent result as an impulse signal.
             return last_results[-1]

# Integration example with parser/analyzer workflow:
if __name__ == "__main__":
    analyzer = PredictionAnalyzer()
    
    # Simulation of loading history (or real-time via parser integration).
    for s in ['BIG', 'BIG', 'SMALL', 'BIG', 'BIG']: 
        analyzer.add_result(s)

    prediction = analyzer.predict_next_side()
    print(f"Analysis concluded choice side: {prediction}")
