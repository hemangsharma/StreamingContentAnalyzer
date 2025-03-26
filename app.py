import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from streamlit.components.v1 import html

# Configure page
st.set_page_config(
    page_title="Streaming Content Analyzer",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
        .main {background-color: #f8f9fa;}
        .st-bw {background-color: black !important;}
        .css-18e3th9 {padding: 2rem 5rem;}
        h1 {color: #2b2d42;}
        .st-bb {background-color: black;}
        .st-at {background-color: #e9ecef;}
    </style>
""", unsafe_allow_html=True)

# Load the data
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("data.csv")
        df['Year'] = df['Year'].astype(int)
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame()

df = load_data()

# Sidebar filters
with st.sidebar:
    st.header("🎛️ Control Panel")
    st.markdown("Filter data to analyze specific content")
    
    type_filter = st.multiselect(
        "Content Type",
        options=df["Type"].unique(),
        default=df["Type"].unique(),
        help="Select movie and/or TV show types"
    )
    
    genre_options = df['Genre(s)'].str.split(', ', expand=True).stack().unique()
    genre_filter = st.multiselect(
        "Genres",
        options=genre_options,
        default=[],
        help="Select genres to analyze"
    )
    
    year_range = st.slider(
        "Release Year Range",
        min_value=int(df["Year"].min()),
        max_value=int(df["Year"].max()),
        value=(int(df["Year"].min()), int(df["Year"].max())),
        help="Select range of release years"
    )

# Apply filters
def apply_filters(df):
    filtered = df[df["Type"].isin(type_filter)]
    filtered = filtered[filtered["Year"].between(year_range[0], year_range[1])]
    
    if genre_filter:
        genre_mask = filtered['Genre(s)'].apply(
            lambda x: any(genre in x for genre in genre_filter)
        )
        filtered = filtered[genre_mask]
    
    return filtered

filtered_df = apply_filters(df)

# Main content
st.title("🎥 Streaming Content Analyzer")
st.markdown("Explore movie and TV show ratings across different dimensions")

# Key Metrics
st.header("📊 Key Metrics")
if not filtered_df.empty:
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Content", filtered_df.shape[0])
    with col2:
        st.metric("Average Rating", f"{filtered_df['Rating (Out of 5)'].mean():.1f}/5")
    with col3:
        st.metric("Movies", filtered_df[filtered_df['Type'] == 'Movie'].shape[0])
    with col4:
        st.metric("TV Shows", filtered_df[filtered_df['Type'] == 'TV Show'].shape[0])
else:
    st.warning("No data available with current filters")

# Visualizations
st.header("📈 Content Analysis")
tab1, tab2, tab3 = st.tabs(["Distribution Analysis", "Temporal Trends", "Genre Breakdown"])

with tab1:
    col1, col2 = st.columns(2)
    with col1:
        # Rating Distribution
        fig = px.histogram(
            filtered_df,
            x="Rating (Out of 5)",
            nbins=10,
            color_discrete_sequence=['#4361ee'],
            title="Rating Distribution",
            template="plotly_white"
        )
        fig.update_layout(bargap=0.1)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Type Comparison
        fig = px.box(
            filtered_df,
            x="Type",
            y="Rating (Out of 5)",
            color="Type",
            color_discrete_sequence=['#4361ee', '#4cc9f0'],
            title="Rating Distribution by Type",
            template="plotly_white"
        )
        st.plotly_chart(fig, use_container_width=True)

with tab2:
    # Temporal Trends
    yearly_data = filtered_df.groupby('Year').agg(
        Average_Rating=('Rating (Out of 5)', 'mean'),
        Count=('Rating (Out of 5)', 'count')
    ).reset_index()
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=yearly_data['Year'],
        y=yearly_data['Average_Rating'],
        name="Average Rating",
        line=dict(color='#4361ee', width=3)
    ))
    fig.add_trace(go.Bar(
        x=yearly_data['Year'],
        y=yearly_data['Count'],
        name="Content Count",
        marker_color='#4cc9f0',
        opacity=0.4
    ))
    fig.update_layout(
        title="Content Trends Over Time",
        template="plotly_white",
        hovermode="x unified",
        yaxis2=dict(title="Content Count", overlaying='y', side='right')
    )
    st.plotly_chart(fig, use_container_width=True)

with tab3:
    # Genre Analysis
    if not filtered_df.empty:
        genre_df = filtered_df['Genre(s)'].str.split(', ', expand=True).stack().reset_index(level=1, drop=True).reset_index(name='Genre')
        genre_counts = genre_df['Genre'].value_counts().reset_index()
        genre_counts.columns = ['Genre', 'Count']
        
        col1, col2 = st.columns(2)
        with col1:
            fig = px.bar(
                genre_counts.head(10),
                x='Count',
                y='Genre',
                orientation='h',
                color='Count',
                color_continuous_scale='Blues',
                title="Top Genres by Content Count",
                template="plotly_white"
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            fig = px.treemap(
                genre_counts,
                path=['Genre'],
                values='Count',
                color='Count',
                color_continuous_scale='Blues',
                title="Genre Distribution",
                template="plotly_white"
            )
            st.plotly_chart(fig, use_container_width=True)

# Data Explorer
st.header("🔍 Data Explorer")
with st.expander("View Raw Data"):
    st.dataframe(filtered_df.sort_values('Rating (Out of 5)', ascending=False), height=300)

# Download button
@st.cache_data
def convert_df(df):
    return df.to_csv(index=False).encode('utf-8')

if not filtered_df.empty:
    csv = convert_df(filtered_df)
    st.download_button(
        label="📥 Download Filtered Data",
        data=csv,
        file_name='filtered_content.csv',
        mime='text/csv'
    )

# Data source and info
st.markdown("---")
st.caption("Data Source: Your Dataset Name Here | Made with Streamlit 🎈")