import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import logging
from .api_config import api_client

logger = logging.getLogger(__name__)

def get_health_data():
    """Get health monitoring data with fallback to dummy data."""
    try:
        # Dummy health data for demonstration
        return {
            'mortality_rate': 2.5,
            'feed_consumption': 85.3,
            'water_consumption': 92.1,
            'temperature': 25.6,
            'humidity': 65.2,
            'ammonia_levels': 15.4,
            'last_vaccination': '2024-03-10',
            'next_vaccination': '2024-04-10'
        }
    except Exception as e:
        logger.error(f"Error getting health data: {e}")
        return None

def display_health_summary():
    """Display key health metrics in the dashboard."""
    try:
        health_data = get_health_data()
        if not health_data:
            st.warning("Health data temporarily unavailable")
            return

        # Create metrics display
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                "Mortality Rate",
                f"{health_data['mortality_rate']}%",
                "-0.5%"
            )
        
        with col2:
            st.metric(
                "Feed Consumption",
                f"{health_data['feed_consumption']}%",
                "2.1%"
            )
        
        with col3:
            st.metric(
                "Water Consumption",
                f"{health_data['water_consumption']}%",
                "1.8%"
            )
    except Exception as e:
        logger.error(f"Error displaying health summary: {e}")
        st.warning("Unable to display health summary")

def show_health_module():
    """Display the health monitoring module."""
    try:
        st.markdown("## Health Monitoring")
        
        # Create tabs for different health aspects
        tab1, tab2, tab3 = st.tabs([
            "Environmental Conditions",
            "Health Metrics",
            "Vaccination Schedule"
        ])
        
        with tab1:
            show_environmental_conditions()
        
        with tab2:
            show_health_metrics()
        
        with tab3:
            show_vaccination_schedule()
            
    except Exception as e:
        logger.error(f"Error in health module: {e}")
        st.error("An error occurred while loading the health module")
        st.markdown("### Basic Health Information")
        display_health_summary()

def show_environmental_conditions():
    """Display environmental conditions monitoring."""
    try:
        health_data = get_health_data()
        if not health_data:
            st.warning("Environmental data temporarily unavailable")
            return
            
        st.markdown("### Environmental Conditions")
        
        # Create metrics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                "Temperature",
                f"{health_data['temperature']}°C",
                "0.8°C"
            )
        
        with col2:
            st.metric(
                "Humidity",
                f"{health_data['humidity']}%",
                "-2.3%"
            )
        
        with col3:
            st.metric(
                "Ammonia Levels",
                f"{health_data['ammonia_levels']} ppm",
                "-1.2 ppm"
            )
            
        # Add a line chart for temperature trends
        dates = pd.date_range(start='2024-03-01', end='2024-03-17', freq='D')
        temp_data = pd.DataFrame({
            'Date': dates,
            'Temperature': [25 + i * 0.1 for i in range(len(dates))]
        })
        
        fig = px.line(temp_data, x='Date', y='Temperature',
                     title='Temperature Trend')
        st.plotly_chart(fig, use_container_width=True)
        
    except Exception as e:
        logger.error(f"Error showing environmental conditions: {e}")
        st.warning("Unable to display environmental conditions")

def show_health_metrics():
    """Display health metrics and statistics."""
    try:
        health_data = get_health_data()
        if not health_data:
            st.warning("Health metrics temporarily unavailable")
            return
            
        st.markdown("### Health Metrics")
        
        # Create a sample dataset for demonstration
        dates = pd.date_range(start='2024-03-01', end='2024-03-17', freq='D')
        metrics_data = pd.DataFrame({
            'Date': dates,
            'Mortality Rate': [2.5 - i * 0.1 for i in range(len(dates))],
            'Feed Consumption': [85 + i * 0.2 for i in range(len(dates))],
            'Water Consumption': [90 + i * 0.15 for i in range(len(dates))]
        })
        
        # Create multi-line chart
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=metrics_data['Date'],
            y=metrics_data['Mortality Rate'],
            name='Mortality Rate',
            line=dict(color='#ef4444')
        ))
        
        fig.add_trace(go.Scatter(
            x=metrics_data['Date'],
            y=metrics_data['Feed Consumption'],
            name='Feed Consumption',
            line=dict(color='#3b82f6')
        ))
        
        fig.add_trace(go.Scatter(
            x=metrics_data['Date'],
            y=metrics_data['Water Consumption'],
            name='Water Consumption',
            line=dict(color='#10b981')
        ))
        
        fig.update_layout(
            title='Health Metrics Trends',
            xaxis_title='Date',
            yaxis_title='Value',
            hovermode='x unified'
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
    except Exception as e:
        logger.error(f"Error showing health metrics: {e}")
        st.warning("Unable to display health metrics")

def show_vaccination_schedule():
    """Display vaccination schedule and records."""
    try:
        health_data = get_health_data()
        if not health_data:
            st.warning("Vaccination data temporarily unavailable")
            return
            
        st.markdown("### Vaccination Schedule")
        
        # Display vaccination information
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Last Vaccination")
            st.markdown(f"**Date:** {health_data['last_vaccination']}")
            st.markdown("**Type:** Regular Health Check")
            st.markdown("**Status:** Completed ✅")
        
        with col2:
            st.markdown("#### Next Vaccination")
            st.markdown(f"**Date:** {health_data['next_vaccination']}")
            st.markdown("**Type:** Preventive Care")
            st.markdown("**Status:** Scheduled 📅")
        
        # Add a timeline or calendar view
        st.markdown("#### Vaccination Timeline")
        
        # Sample vaccination schedule
        schedule = pd.DataFrame({
            'Date': ['2024-03-10', '2024-04-10', '2024-05-10', '2024-06-10'],
            'Type': ['Health Check', 'Preventive', 'Booster', 'Regular'],
            'Status': ['Completed', 'Scheduled', 'Planned', 'Planned']
        })
        
        st.dataframe(
            schedule,
            column_config={
                "Date": "Date",
                "Type": "Vaccination Type",
                "Status": "Status"
            },
            hide_index=True
        )
        
    except Exception as e:
        logger.error(f"Error showing vaccination schedule: {e}")
        st.warning("Unable to display vaccination schedule")

def get_disease_data(region='all'):
    """Get disease tracking data for poultry"""
    response = api_client.get_disease_alerts(region)
    
    if response.get('error'):
        st.warning(f"Error fetching disease data: {response['message']}")
        return get_mock_disease_data()
        
    return response

def get_mock_disease_data():
    """Provide sample disease tracking data for demonstration"""
    today = datetime.now()
    dates = [(today - timedelta(days=x)).strftime('%Y-%m-%d') for x in range(30)]
    
    diseases = [
        "Avian Influenza",
        "Newcastle Disease",
        "Infectious Bronchitis",
        "Coccidiosis",
        "Salmonella"
    ]
    
    regions = ["North", "South", "East", "West", "Central"]
    
    alerts = []
    for date in dates:
        for disease in diseases:
            for region in regions:
                if (hash(f"{date}{disease}{region}") % 10) < 3:  # Random occurrence
                    alerts.append({
                        'date': date,
                        'disease': disease,
                        'region': region,
                        'risk_level': ['Low', 'Medium', 'High'][hash(f"{date}{disease}") % 3],
                        'affected_farms': hash(f"{date}{disease}{region}") % 50,
                        'status': ['Active', 'Contained', 'Monitoring'][hash(f"{date}{disease}{region}") % 3]
                    })
    
    return {
        'alerts': alerts,
        'summary': {
            'total_alerts': len(alerts),
            'high_risk': sum(1 for a in alerts if a['risk_level'] == 'High'),
            'active_cases': sum(1 for a in alerts if a['status'] == 'Active')
        }
    }

def create_disease_heatmap(data):
    """Create a heatmap of disease occurrences by region"""
    df = pd.DataFrame(data)
    pivot = pd.pivot_table(
        df,
        values='affected_farms',
        index='region',
        columns='disease',
        aggfunc='sum',
        fill_value=0
    )
    
    fig = px.imshow(
        pivot,
        aspect="auto",
        color_continuous_scale="RdYlBu_r",
        title="Disease Occurrence Heatmap by Region"
    )
    
    fig.update_layout(height=400)
    return fig

def show_health_monitoring():
    st.header("🏥 Health Monitoring & Disease Tracking")
    
    # Region selection
    region = st.selectbox(
        "Select Region",
        ["All Regions", "North", "South", "East", "West", "Central"],
        help="Choose a region to view specific health alerts"
    )
    
    # Get disease data
    disease_data = get_disease_data(region.lower() if region != "All Regions" else "all")
    
    if disease_data:
        # Summary metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(
                "Total Alerts",
                disease_data['summary']['total_alerts'],
                help="Total number of disease alerts in the selected region"
            )
        with col2:
            st.metric(
                "High Risk Cases",
                disease_data['summary']['high_risk'],
                help="Number of high-risk disease cases"
            )
        with col3:
            st.metric(
                "Active Cases",
                disease_data['summary']['active_cases'],
                help="Number of currently active disease cases"
            )
        
        # Disease tracking tabs
        tabs = st.tabs(["Current Alerts", "Disease Map", "Prevention Guide"])
        
        with tabs[0]:
            # Filter alerts
            alerts_df = pd.DataFrame(disease_data['alerts'])
            if region != "All Regions":
                alerts_df = alerts_df[alerts_df['region'] == region]
            
            # Sort by date and risk level
            alerts_df = alerts_df.sort_values(['date', 'risk_level'], ascending=[False, False])
            
            # Display alerts with color coding
            for _, alert in alerts_df.iterrows():
                color = {
                    'High': 'red',
                    'Medium': 'orange',
                    'Low': 'green'
                }[alert['risk_level']]
                
                with st.container():
                    st.markdown(f"""
                    <div style='border-left: 5px solid {color}; padding-left: 10px;'>
                        <h4>{alert['disease']}</h4>
                        <p>Region: {alert['region']} | Risk Level: {alert['risk_level']} | Status: {alert['status']}</p>
                        <p>Date: {alert['date']} | Affected Farms: {alert['affected_farms']}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    st.divider()
        
        with tabs[1]:
            # Disease heatmap
            st.plotly_chart(create_disease_heatmap(disease_data['alerts']), use_container_width=True)
            
            # Additional insights
            st.subheader("Regional Insights")
            alerts_df = pd.DataFrame(disease_data['alerts'])
            for region in alerts_df['region'].unique():
                region_data = alerts_df[alerts_df['region'] == region]
                with st.expander(f"{region} Region Analysis"):
                    st.write(f"Total Alerts: {len(region_data)}")
                    st.write(f"Most Common Disease: {region_data['disease'].mode().iloc[0]}")
                    st.write(f"Average Affected Farms: {region_data['affected_farms'].mean():.1f}")
        
        with tabs[2]:
            st.subheader("Disease Prevention Guidelines")
            
            prevention_tips = {
                "Biosecurity Measures": [
                    "Implement strict visitor protocols",
                    "Use footbaths at entry points",
                    "Regular cleaning and disinfection",
                    "Proper disposal of dead birds"
                ],
                "Vaccination Program": [
                    "Follow recommended vaccination schedule",
                    "Store vaccines at proper temperature",
                    "Maintain vaccination records",
                    "Monitor post-vaccination reactions"
                ],
                "Farm Management": [
                    "Control rodents and wild birds",
                    "Maintain proper ventilation",
                    "Regular health monitoring",
                    "Isolate sick birds promptly"
                ]
            }
            
            for category, tips in prevention_tips.items():
                with st.expander(category):
                    for tip in tips:
                        st.markdown(f"- {tip}")
    
    else:
        st.error("Unable to fetch health monitoring data. Please try again later.") 