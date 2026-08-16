"""Streamlit Deployment App for Farmigo - Pan-India Agricultural Rental System
Deploy on Streamlit Cloud (share.streamlit.io) with:
streamlit run streamlit_app.py
"""
import os
import streamlit as st
import pandas as pd

# 1. Page Configuration
st.set_page_config(
    page_title="Farmigo · Agricultural Machinery Marketplace",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling
st.markdown("""
<style>
  .main-header {
    font-family: 'Plus Jakarta Sans', sans-serif;
    color: #0f172a;
    font-weight: 800;
  }
  .sub-text {
    color: #047857;
    font-weight: 700;
    font-size: 1.05rem;
  }
  .card-box {
    background-color: #ffffff;
    border-radius: 16px;
    padding: 20px;
    border: 1px solid #e2e8f0;
    box-shadow: 0 4px 12px rgba(0,0,0,0.05);
    margin-bottom: 20px;
  }
  .price-tag {
    color: #047857;
    font-weight: 800;
    font-size: 1.3rem;
  }
  .loc-tag {
    color: #64748b;
    font-weight: 600;
    font-size: 0.88rem;
  }
</style>
""", unsafe_allow_html=True)

# 2. Database / Dataset Loader
@st.cache_data
def load_equipment_data():
    items = [
        {"id": 1, "name": "Mahindra 575 DI Tractor", "category": "tractor", "brand": "Mahindra", "price_per_day": 1200, "location": "Pollachi, Tamil Nadu", "lat": 10.6609, "lng": 77.0048, "image": "tractor_mahindra.png"},
        {"id": 2, "name": "John Deere Combine Harvester", "category": "harvester", "brand": "John Deere", "price_per_day": 3500, "location": "Ludhiana, Punjab", "lat": 30.9010, "lng": 75.8573, "image": "combine_harvester.png"},
        {"id": 3, "name": "Sonalika Heavy Duty 750 DI", "category": "tractor", "brand": "Sonalika", "price_per_day": 1400, "location": "Karnal, Haryana", "lat": 29.6857, "lng": 76.9905, "image": "tractor_mahindra.png"},
        {"id": 4, "name": "Kubota Vineyard Mini Tractor", "category": "tractor", "brand": "Kubota", "price_per_day": 1100, "location": "Nashik, Maharashtra", "lat": 19.9975, "lng": 73.7898, "image": "power_tiller.png"},
        {"id": 5, "name": "Power Tiller 7HP", "category": "tiller", "brand": "VST Shakti", "price_per_day": 600, "location": "Mandya, Karnataka", "lat": 12.5218, "lng": 76.8951, "image": "power_tiller.png"},
        {"id": 6, "name": "Reversible MB Plough", "category": "plough", "brand": "Lemken", "price_per_day": 400, "location": "Bareilly, Uttar Pradesh", "lat": 28.3670, "lng": 79.4304, "image": "reversible_plough.png"},
        {"id": 7, "name": "Boom Sprayer 400L", "category": "sprayer", "brand": "Aspee", "price_per_day": 800, "location": "Anand, Gujarat", "lat": 22.5645, "lng": 72.9289, "image": "boom_sprayer.png"},
        {"id": 8, "name": "Agri Drone Sprayer", "category": "drone", "brand": "Garuda", "price_per_day": 2500, "location": "Guntur, Andhra Pradesh", "lat": 16.3067, "lng": 80.4365, "image": "agri_drone.png"},
        {"id": 9, "name": "Preet Heavy Duty 9049 Tractor", "category": "tractor", "brand": "Preet", "price_per_day": 1600, "location": "Indore, Madhya Pradesh", "lat": 22.7196, "lng": 75.8577, "image": "tractor_mahindra.png"},
        {"id": 10, "name": "Kubota Automatic Paddy Transplanter", "category": "harvester", "brand": "Kubota", "price_per_day": 1800, "location": "Bhubaneswar, Odisha", "lat": 20.2961, "lng": 85.8245, "image": "combine_harvester.png"},
        {"id": 11, "name": "Heavy Duty Rotary Tiller", "category": "tiller", "brand": "Shrachi", "price_per_day": 750, "location": "Bikaner, Rajasthan", "lat": 28.0229, "lng": 73.3119, "image": "power_tiller.png"},
        {"id": 12, "name": "Multicrop High-Speed Thresher", "category": "harvester", "brand": "Kirloskar", "price_per_day": 1300, "location": "Patna, Bihar", "lat": 25.5941, "lng": 85.1376, "image": "combine_harvester.png"},
        {"id": 13, "name": "Solar Crop Harvester Unit", "category": "harvester", "brand": "FieldKing", "price_per_day": 2200, "location": "Bardhaman, West Bengal", "lat": 23.2324, "lng": 87.8615, "image": "combine_harvester.png"},
    ]
    return pd.DataFrame(items)

df_all = load_equipment_data()

# 3. Sidebar Navigation & Filters
st.sidebar.image("app/static/img/login_hero.png", caption="Farmigo Agricultural Network", use_container_width=True)
st.sidebar.title("🌾 Navigation")
view_mode = st.sidebar.radio(
    "Select View Mode",
    ["🛒 Equipment Marketplace", "🗺️ Pan-India Location Radar", "📊 Analytics Dashboard", "🌐 Full Web App View"]
)

st.sidebar.markdown("---")
st.sidebar.subheader("🔍 Filter Machinery")

categories = ["All Categories"] + sorted(list(df_all["category"].str.title().unique()))
selected_cat = st.sidebar.selectbox("Category", categories)

locations = ["All States / Locations"] + sorted(list(df_all["location"].unique()))
selected_loc = st.sidebar.selectbox("State / Location", locations)

max_price = int(df_all["price_per_day"].max())
selected_price = st.sidebar.slider("Max Daily Price (₹)", 400, max_price, max_price, step=100)

# Apply Filters
df_filtered = df_all.copy()
if selected_cat != "All Categories":
    df_filtered = df_filtered[df_filtered["category"].str.lower() == selected_cat.lower()]
if selected_loc != "All States / Locations":
    df_filtered = df_filtered[df_filtered["location"] == selected_loc]
df_filtered = df_filtered[df_filtered["price_per_day"] <= selected_price]

# 4. View Rendering

# MODE 1: MARKETPLACE
if view_mode == "🛒 Equipment Marketplace":
    st.markdown("<h1 class='main-header'>🌾 Farmigo · Agricultural Machinery Marketplace</h1>", unsafe_allow_html=True)
    st.markdown("<p class='sub-text'>Rent high-performance tractors, harvesters, tillers, and sprayers directly from verified owners across India.</p>", unsafe_allow_html=True)
    st.markdown("---")

    # Metrics Summary
    col_m1, col_m2, col_m3, col_m4 = st.columns(4)
    col_m1.metric("Available Fleet", f"{len(df_filtered)} Units")
    col_m2.metric("Pan-India Hubs", "13 States")
    col_m3.metric("Daily Rental Range", f"₹{df_filtered['price_per_day'].min() or 400} - ₹{df_filtered['price_per_day'].max() or 3500}")
    col_m4.metric("Estimated Savings", "~85% vs buying")

    st.markdown("<h3 style='color:#0f172a; margin-top:20px;'>Available Equipment Fleet</h3>", unsafe_allow_html=True)

    if len(df_filtered) == 0:
        st.info("No equipment matches your selected filter criteria. Try adjusting the sidebar filters.")
    else:
        cols = st.columns(3)
        for idx, row in df_filtered.reset_index().iterrows():
            col_idx = idx % 3
            with cols[col_idx]:
                st.markdown("<div class='card-box'>", unsafe_allow_html=True)
                img_path = os.path.join("app", "static", "img", "equipment", row["image"])
                if os.path.exists(img_path):
                    st.image(img_path, use_container_width=True)
                else:
                    st.image("app/static/img/login_hero.png", use_container_width=True)
                
                st.markdown(f"**Tag**: `{row['category'].upper()}` | Brand: **{row['brand']}**")
                st.markdown(f"### {row['name']}")
                st.markdown(f"<span class='loc-tag'>📍 {row['location']}</span>", unsafe_allow_html=True)
                st.markdown(f"<span class='price-tag'>₹{row['price_per_day']:.0f}</span> / day", unsafe_allow_html=True)
                
                with st.expander("📅 Book Equipment"):
                    start_d = st.date_input("Start Date", key=f"start_{row['id']}")
                    end_d = st.date_input("End Date", key=f"end_{row['id']}")
                    days = (end_d - start_d).days + 1
                    if days > 0:
                        st.success(f"Total: ₹{days * row['price_per_day']:.0f} for {days} day(s)")
                        if st.button("Confirm Rental Request", key=f"btn_{row['id']}"):
                            st.balloons()
                            st.success("✅ Rental Booking Request Dispatched to Equipment Owner!")
                    else:
                        st.error("End date must be on or after start date.")
                st.markdown("</div>", unsafe_allow_html=True)

# MODE 2: PAN-INDIA LOCATION RADAR MAP
elif view_mode == "🗺️ Pan-India Location Radar":
    st.markdown("<h1 class='main-header'>🗺️ Pan-India Field Machinery Location Radar</h1>", unsafe_allow_html=True)
    st.markdown("<p class='sub-text'>Interactive map of verified farm machinery across 13 major agricultural states of India.</p>", unsafe_allow_html=True)
    st.markdown("---")

    # Map Dataframe
    map_df = df_filtered[["lat", "lng", "name", "price_per_day", "location"]].rename(columns={"lat": "latitude", "lng": "longitude"})
    st.map(map_df, zoom=4, use_container_width=True)

    st.markdown("### Equipment Hub Locations Summary")
    st.dataframe(
        df_filtered[["name", "category", "brand", "location", "price_per_day"]].rename(columns={
            "name": "Equipment Title", "category": "Category", "brand": "Manufacturer",
            "location": "Regional Hub", "price_per_day": "Daily Rate (₹)"
        }),
        use_container_width=True
    )

# MODE 3: ANALYTICS DASHBOARD
elif view_mode == "📊 Analytics Dashboard":
    st.markdown("<h1 class='main-header'>📊 Executive Rental Analytics Dashboard</h1>", unsafe_allow_html=True)
    st.markdown("<p class='sub-text'>Financial analytics, rental revenue growth, and fleet category distribution.</p>", unsafe_allow_html=True)
    st.markdown("---")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Active Listings", "13 Machinery Units", "+18%")
    c2.metric("Monthly Rental Earnings", "₹1,42,800", "↑ 24% vs last month")
    c3.metric("Total Rental Days", "184 Days", "+32 days")
    c4.metric("Avg Renter Rating", "4.9 ★", "Top Verified Portal")

    col_left, col_right = st.columns(2)
    with col_left:
        st.markdown("### 📈 Monthly Revenue Growth (₹)")
        rev_data = pd.DataFrame({
            "Month": ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug"],
            "Revenue (₹)": [42000, 58000, 74000, 91000, 112000, 128000, 135000, 142800]
        }).set_index("Month")
        st.line_chart(rev_data)

    with col_right:
        st.markdown("### 🍩 Fleet Category Distribution")
        cat_counts = df_all["category"].value_counts().reset_index()
        cat_counts.columns = ["Category", "Count"]
        st.bar_chart(cat_counts.set_index("Category"))

# MODE 4: EMBEDDED WEB APP VIEW
elif view_mode == "🌐 Full Web App View":
    st.markdown("<h1 class='main-header'>🌐 Full Web Application Interface</h1>", unsafe_allow_html=True)
    st.markdown("<p class='sub-text'>Live embedded web view of the Farmigo Flask Application.</p>", unsafe_allow_html=True)
    st.components.v1.iframe("http://127.0.0.1:5000", height=820, scrolling=True)
