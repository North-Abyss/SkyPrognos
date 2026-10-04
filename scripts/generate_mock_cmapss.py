"""Generates mock C-MAPSS dataset matching the exact schema for testing when public mirrors are down."""
import pandas as pd
import numpy as np
import os

def generate_mock_cmapss():
    os.makedirs('data/raw', exist_ok=True)
    
    # Schema: unit, cycle, op1, op2, op3, sensor1 to sensor21
    np.random.seed(42)
    
    # Train
    train_data = []
    for unit in range(1, 101):
        max_cycle = np.random.randint(150, 300)
        for cycle in range(1, max_cycle + 1):
            rul = max_cycle - cycle
            # As RUL decreases, sensor readings drift
            sensor_drift = (max_cycle - cycle) / max_cycle
            row = [unit, cycle, 0.0, 0.0, 100.0] + [np.random.normal(500, 10) + (50 * (1 - sensor_drift)) for _ in range(21)]
            train_data.append(row)
            
    pd.DataFrame(train_data).to_csv('data/raw/train_FD001.txt', sep=' ', header=False, index=False)
    
    # Test
    test_data = []
    rul_data = []
    for unit in range(1, 101):
        max_cycle = np.random.randint(150, 300)
        # Randomly cut off before max_cycle
        cutoff = np.random.randint(50, max_cycle - 20)
        for cycle in range(1, cutoff + 1):
            sensor_drift = (max_cycle - cycle) / max_cycle
            row = [unit, cycle, 0.0, 0.0, 100.0] + [np.random.normal(500, 10) + (50 * (1 - sensor_drift)) for _ in range(21)]
            test_data.append(row)
        rul_data.append([max_cycle - cutoff])
        
    pd.DataFrame(test_data).to_csv('data/raw/test_FD001.txt', sep=' ', header=False, index=False)
    pd.DataFrame(rul_data).to_csv('data/raw/RUL_FD001.txt', sep=' ', header=False, index=False)
    print("Synthetic C-MAPSS data generated in data/raw/")

if __name__ == "__main__":
    generate_mock_cmapss()
