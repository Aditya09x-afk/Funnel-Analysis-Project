# funnel_data_generator.py

import pandas as pd
import random
from faker import Faker
from datetime import timedelta

# Initialize Faker
fake = Faker()

# Store records
data = []

# Funnel stages
stages = ['Browse', 'Add to Cart', 'Checkout', 'Purchase']

# Probability of moving to the NEXT stage
stage_conversion = {
    'Browse': 0.7,
    'Add to Cart': 0.5,
    'Checkout': 0.6
}

# Supporting random data
devices = ['Mobile', 'Desktop', 'Tablet']
regions = ['North', 'South', 'East', 'West']
channels = ['Google Ads', 'Organic', 'Email', 'Social Media']
categories = ['Electronics', 'Fashion', 'Home', 'Beauty', 'Sports']

# Generate data for 10,000 users
for i in range(1, 10001):

    user_id = f"USR{i:05d}"
    session_id = f"SES{i:05d}"
    event_time = fake.date_time_between(start_date='-30d', end_date='now')

    device = random.choice(devices)
    region = random.choice(regions)
    channel = random.choice(channels)
    category = random.choice(categories)

    bounce_flag = "Yes"

    for idx, stage in enumerate(stages):

        # Revenue only for purchase
        revenue = round(random.uniform(200, 2000), 2) if stage == 'Purchase' else 0

        record = {
            'User_ID': user_id,
            'Session_ID': session_id,
            'Event': stage,
            'Timestamp': event_time.strftime('%Y-%m-%d %H:%M:%S'),
            'Device': device,
            'Region': region,
            'Channel': channel,
            'Product_Category': category,
            'Revenue': revenue,
            'Bounce_Flag': bounce_flag
        }

        data.append(record)

        # Add time gap between stages
        event_time += timedelta(minutes=random.randint(2, 5))

        # Stop if Purchase reached
        if stage == 'Purchase':
            bounce_flag = "No"
            break

        # Decide if user moves to next stage
        if random.random() > stage_conversion.get(stage, 0):
            break

# Convert to DataFrame
df = pd.DataFrame(data)

# Update bounce flag for users who purchased
purchased_users = df[df['Event'] == 'Purchase']['User_ID'].unique()
df.loc[df['User_ID'].isin(purchased_users), 'Bounce_Flag'] = 'No'

# Export dataset
df.to_csv("funnel_analysis_data.csv", index=False)

print("🍒 Funnel dataset generated successfully!")