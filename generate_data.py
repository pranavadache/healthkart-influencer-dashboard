import pandas as pd
import numpy as np
from faker import Faker
import random
from datetime import datetime, timedelta

# Initialize Faker for generating fake data
fake = Faker('en_IN') # Using Indian locale for names

# --- Configuration ---
NUM_INFLUENCERS = 50
NUM_POSTS_PER_INFLUENCER_RANGE = (3, 8)
START_DATE = datetime.now() - timedelta(days=180)
END_DATE = datetime.now()

# --- 1. Generate 'influencers' table ---
print("Generating 'influencers' data...")
influencers = []
categories = ["Fitness", "Wellness", "Beauty", "Lifestyle", "Parenting"]
platforms = ["Instagram", "YouTube", "Twitter"]

for i in range(1, NUM_INFLUENCERS + 1):
    influencer_id = f"INF{i:03d}"
    gender = random.choice(["Male", "Female", "Non-Binary"])
    if gender == "Male":
        name = fake.name_male()
    else:
        name = fake.name_female()

    influencers.append({
        "influencer_id": influencer_id,
        "name": name,
        "category": random.choice(categories),
        "gender": gender,
        "follower_count": random.randint(5000, 500000),
        "platform": random.choice(platforms)
    })

influencers_df = pd.DataFrame(influencers)
influencers_df.to_csv("data/influencers.csv", index=False)
print(f"Successfully generated {len(influencers_df)} records for influencers.")

# --- 2. Generate 'posts' table ---
print("\nGenerating 'posts' data...")
posts = []
post_id_counter = 1
for _, influencer in influencers_df.iterrows():
    num_posts = random.randint(*NUM_POSTS_PER_INFLUENCER_RANGE)
    for _ in range(num_posts):
        post_date = fake.date_time_between(start_date=START_DATE, end_date=END_DATE)
        reach = int(influencer['follower_count'] * random.uniform(0.1, 0.6))
        likes = int(reach * random.uniform(0.02, 0.15))
        comments = int(likes * random.uniform(0.01, 0.1))

        posts.append({
            "post_id": f"POST{post_id_counter:04d}",
            "influencer_id": influencer['influencer_id'],
            "platform": influencer['platform'],
            "date": post_date.strftime("%Y-%m-%d %H:%M:%S"),
            "url": f"https://{influencer['platform'].lower()}.com/{influencer['name'].replace(' ', '').lower()}/post/{post_id_counter}",
            "caption": fake.sentence(nb_words=20),
            "reach": reach,
            "likes": likes,
            "comments": comments
        })
        post_id_counter += 1

posts_df = pd.DataFrame(posts)
posts_df.to_csv("data/posts.csv", index=False)
print(f"Successfully generated {len(posts_df)} records for posts.")


# --- 3. Generate 'tracking_data' table ---
print("\nGenerating 'tracking_data'...")
tracking_data = []
tracking_id_counter = 1

brands_products = {
    "MuscleBlaze": ["Whey Protein", "BCAA", "Creatine", "Mass Gainer"],
    "HKVitals": ["Biotin", "Multivitamin", "Omega 3", "Collagen"],
    "Gritzo": ["SuperMilk for Kids", "Protein Oats for Teens", "Gummy Stars"]
}

campaigns = [
    "MB_SummerFit", "HKV_GlowUp", "Gritzo_KidsHealth", "MB_NewYearBulk", "HKV_DailyWellness"
]

for _, post in posts_df.iterrows():
    # Simulate conversions based on reach
    conversions = int(post['reach'] * random.uniform(0.0001, 0.002))
    
    for _ in range(conversions):
        brand = random.choice(list(brands_products.keys()))
        product = random.choice(brands_products[brand])
        order_date = datetime.strptime(post['date'], "%Y-%m-%d %H:%M:%S") + timedelta(days=random.randint(0, 5))
        
        # Simulate revenue based on brand
        if brand == "MuscleBlaze":
            revenue = random.uniform(1500, 5000)
        elif brand == "HKVitals":
            revenue = random.uniform(400, 2000)
        else: # Gritzo
            revenue = random.uniform(300, 1000)

        tracking_data.append({
            "tracking_id": f"TRK{tracking_id_counter:05d}",
            "source": "influencer_marketing",
            "campaign": random.choice(campaigns),
            "influencer_id": post['influencer_id'],
            "user_id": fake.uuid4(),
            "product": product,
            "date": order_date.strftime("%Y-%m-%d %H:%M:%S"),
            "orders": 1,
            "revenue": round(revenue, 2)
        })
        tracking_id_counter += 1

tracking_data_df = pd.DataFrame(tracking_data)
tracking_data_df.to_csv("data/tracking_data.csv", index=False)
print(f"Successfully generated {len(tracking_data_df)} records for tracking_data.")


# --- 4. Generate 'payouts' table ---
print("\nGenerating 'payouts' data...")
payouts = []
for _, influencer in influencers_df.iterrows():
    basis = random.choice(['per_post', 'per_order'])
    
    # Get all tracking data for this influencer
    influencer_revenue = tracking_data_df[tracking_data_df['influencer_id'] == influencer['influencer_id']]['revenue'].sum()
    influencer_orders = tracking_data_df[tracking_data_df['influencer_id'] == influencer['influencer_id']]['orders'].sum()
    
    if basis == 'per_post':
        rate = random.choice([5000, 10000, 25000, 50000]) # Fixed rate per post
        num_posts = len(posts_df[posts_df['influencer_id'] == influencer['influencer_id']])
        total_payout = rate * num_posts
    else: # per_order
        rate = round(random.uniform(0.10, 0.25), 2) # Commission rate
        total_payout = influencer_revenue * rate

     # --- This is the NEW, corrected code ---
payouts.append({
    "influencer_id": influencer['influencer_id'],
    "basis": basis,
    "rate": rate,
    "total_orders_by_influencer": influencer_orders, # <-- RENAMED this key
    "total_payout": round(total_payout, 2)
})

payouts_df = pd.DataFrame(payouts)
payouts_df.to_csv("data/payouts.csv", index=False)
print(f"Successfully generated {len(payouts_df)} records for payouts.")

print("\nAll data generation complete. Files are in the 'data' directory.")