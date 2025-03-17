import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
from .api_config import api_client

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