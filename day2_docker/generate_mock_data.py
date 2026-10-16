import random
from datetime import datetime, timedelta

import numpy as np
import pandas as pd
# Configuration
NUM_RUNS = 500
TEAMS = ['Frontend', 'Backend', 'Data', 'Security']
WORKFLOWS = ['Build & Test', 'Deploy to Staging', 'Security Scan', 'Deploy to Prod']
STATUSES = ['success', 'success', 'success', 'failure', 'cancelled'] # Weighted for more successes

# Generate timestamps over the last 30 days
end_date = datetime.now()
start_date = end_date - timedelta(days=30)
timestamps = [start_date + timedelta(seconds=random.randint(0, int((end_date - start_date).total_seconds()))) for _ in range(NUM_RUNS)]
timestamps.sort()

data = {
    'run_id': range(1000, 1000 + NUM_RUNS),
    'timestamp': timestamps,
    'team': [random.choice(TEAMS) for _ in range(NUM_RUNS)],
    'workflow_name': [random.choice(WORKFLOWS) for _ in range(NUM_RUNS)],
    'status': [random.choice(STATUSES) for _ in range(NUM_RUNS)],
    'duration_seconds': np.random.normal(loc=120, scale=40, size=NUM_RUNS).astype(int), # Avg 2 mins, varying
}

df = pd.DataFrame(data)

# Add some realism: Failures take longer to timeout, Security scans take longer overall
df.loc[df['status'] == 'failure', 'duration_seconds'] += np.random.randint(50, 150)
df.loc[df['workflow_name'] == 'Security Scan', 'duration_seconds'] += np.random.randint(60, 200)

# Ensure no negative durations
df['duration_seconds'] = df['duration_seconds'].clip(lower=10)

df.to_csv('workflow_logs.csv', index=False)
print(f"Generated {NUM_RUNS} mock GitHub Actions logs in 'workflow_logs.csv'")