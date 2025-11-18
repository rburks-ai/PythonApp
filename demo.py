import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Page config
st.set_page_config(page_title="Nearby Sporting Events", page_icon="🏟️", layout="wide")

# Generate fake sporting events data
@st.cache_data
def generate_events():
    sports = ["Basketball", "Soccer", "Baseball", "Hockey", "Football", "Tennis", "Volleyball"]
    venues = ["Downtown Arena", "City Stadium", "Olympic Park", "Central Sports Complex", 
              "Riverside Field", "Metro Dome", "Championship Court"]
    teams_prefix = ["Tigers", "Eagles", "Warriors", "Knights", "Dragons", "Sharks", "Phoenix"]
    
    events = []
    base_lat, base_lon = 33.7490, -84.3880  # Atlanta coordinates
    
    for i in range(20):
        date = datetime.now() + timedelta(days=random.randint(0, 30))
        sport = random.choice(sports)
        venue = random.choice(venues)
        team1 = random.choice(teams_prefix)
        team2 = random.choice([t for t in teams_prefix if t != team1])
        
        events.append({
            "id": i + 1,
            "sport": sport,
            "title": f"{team1} vs {team2}",
            "venue": venue,
            "date": date.strftime("%Y-%m-%d"),
            "time": f"{random.randint(10, 20)}:{random.choice(['00', '30'])}",
            "price": f"${random.randint(15, 150)}",
            "distance": round(random.uniform(0.5, 15), 1),
            "lat": base_lat + random.uniform(-0.1, 0.1),
            "lon": base_lon + random.uniform(-0.1, 0.1),
            "available_seats": random.randint(50, 5000)
        })
    
    return pd.DataFrame(events)

# Title
st.title("🏟️ Nearby Sporting Events")
st.markdown("Discover exciting sporting events happening near you!")

# Sidebar filters
st.sidebar.header("Filters")
df = generate_events()

sports_filter = st.sidebar.multiselect(
    "Select Sports",
    options=sorted(df['sport'].unique()),
    default=sorted(df['sport'].unique())
)

max_distance = st.sidebar.slider("Maximum Distance (miles)", 0.5, 15.0, 10.0, 0.5)

price_range = st.sidebar.slider(
    "Price Range ($)",
    int(df['price'].str.replace('$', '').astype(int).min()),
    int(df['price'].str.replace('$', '').astype(int).max()),
    (15, 150)
)

# Filter data
filtered_df = df[
    (df['sport'].isin(sports_filter)) &
    (df['distance'] <= max_distance) &
    (df['price'].str.replace('$', '').astype(int) >= price_range[0]) &
    (df['price'].str.replace('$', '').astype(int) <= price_range[1])
].sort_values('distance')

# Display metrics
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Events", len(filtered_df))
col2.metric("Closest Event", f"{filtered_df['distance'].min():.1f} mi" if len(filtered_df) > 0 else "N/A")
col3.metric("Sports Available", filtered_df['sport'].nunique())
col4.metric("Avg Price", f"${int(filtered_df['price'].str.replace('$', '').astype(int).mean())}" if len(filtered_df) > 0 else "N/A")

st.markdown("---")

# Map
if len(filtered_df) > 0:
    st.subheader("📍 Event Locations")
    st.map(filtered_df[['lat', 'lon']], zoom=11)
    
    st.markdown("---")
    
    # Events list
    st.subheader("🎫 Upcoming Events")
    
    for _, event in filtered_df.iterrows():
        with st.container():
            col1, col2, col3 = st.columns([3, 2, 1])
            
            with col1:
                st.markdown(f"### {event['sport']}: {event['title']}")
                st.write(f"📍 {event['venue']}")
                st.write(f"📅 {event['date']} at {event['time']}")
            
            with col2:
                st.write(f"**Distance:** {event['distance']} miles")
                st.write(f"**Price:** {event['price']}")
                st.write(f"**Seats Available:** {event['available_seats']:,}")
            
            with col3:
                st.write("")
                st.write("")
                if st.button("View Details", key=f"btn_{event['id']}"):
                    st.info(f"Opening details for {event['title']}...")
            
            st.markdown("---")
else:
    st.warning("No events found matching your criteria. Try adjusting the filters!")

# Footer
st.sidebar.markdown("---")
st.sidebar.info("💡 **Tip:** Adjust filters to find events that match your preferences!")
