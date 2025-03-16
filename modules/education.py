import streamlit as st

def show_content():
    st.markdown("""
    <h1 style='text-align: center; color: #333; font-size: 2rem; margin-bottom: 2rem;'>
        📚 Training Hub
    </h1>
    """, unsafe_allow_html=True)

    # Initialize session state for progress tracking
    if 'completed_modules' not in st.session_state:
        st.session_state.completed_modules = set()

    modules = {
        "basics": {
            "title": "Basics of Poultry Farming",
            "icon": "🐣",
            "sections": [
                "Types of Poultry Birds",
                "Housing Requirements",
                "Basic Health Management",
                "Growth Stages"
            ],
            "content": {
                "Types of Poultry Birds": """
                - Layer Birds (Egg Production)
                - Broiler Birds (Meat Production)
                - Dual Purpose Breeds
                - Indigenous Breeds
                """,
                "Housing Requirements": """
                - Space Requirements
                - Ventilation Systems
                - Lighting Management
                - Temperature Control
                """,
                "Basic Health Management": """
                - Daily Health Checks
                - Common Signs of Illness
                - Basic First Aid
                - When to Call a Vet
                """,
                "Growth Stages": """
                - Day-Old Chicks (0-2 weeks)
                - Growers (2-8 weeks)
                - Finishers (8-12 weeks)
                - Layer Development
                """
            }
        },
        "disease": {
            "title": "Disease Management",
            "icon": "💉",
            "sections": [
                "Common Diseases",
                "Prevention Measures",
                "Vaccination Schedule",
                "Bio-security"
            ],
            "content": {
                "Common Diseases": """
                - Respiratory Infections
                - Digestive Issues
                - Parasitic Infections
                - Viral Diseases
                """,
                "Prevention Measures": """
                - Regular Cleaning
                - Proper Ventilation
                - Feed Management
                - Water Sanitation
                """,
                "Vaccination Schedule": """
                - Day 1: Marek's Disease
                - Day 7: Newcastle Disease
                - Day 14: Infectious Bursal Disease
                - Regular Boosters
                """,
                "Bio-security": """
                - Farm Entry Protocols
                - Visitor Management
                - Equipment Sanitation
                - Waste Management
                """
            }
        },
        "feed": {
            "title": "Feed Management",
            "icon": "🌾",
            "sections": [
                "Feed Types",
                "Feeding Schedule",
                "Water Management",
                "Storage"
            ],
            "content": {
                "Feed Types": """
                - Starter Feed (0-3 weeks)
                - Grower Feed (3-8 weeks)
                - Finisher Feed (8+ weeks)
                - Layer Feed
                """,
                "Feeding Schedule": """
                - Morning Feed
                - Afternoon Supplements
                - Evening Feed
                - Night Requirements
                """,
                "Water Management": """
                - Quality Standards
                - Consumption Rates
                - Cleaning Schedule
                - Additives Management
                """,
                "Storage": """
                - Storage Conditions
                - Pest Control
                - Stock Rotation
                - Quality Checks
                """
            }
        }
    }

    # Modern card layout for modules
    st.markdown("""
    <style>
    .module-card {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 2px 12px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
    }
    .module-header {
        display: flex;
        align-items: center;
        margin-bottom: 1rem;
    }
    .module-icon {
        font-size: 2rem;
        margin-right: 1rem;
    }
    .module-title {
        font-size: 1.2rem;
        color: #333;
        margin: 0;
    }
    .section-content {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        margin-top: 0.5rem;
    }
    .progress-bar {
        height: 4px;
        background: #eee;
        border-radius: 2px;
        margin-top: 0.5rem;
    }
    .progress-value {
        height: 100%;
        background: #ff4b4b;
        border-radius: 2px;
        transition: width 0.3s ease;
    }
    </style>
    """, unsafe_allow_html=True)

    # Display modules
    for module_id, module in modules.items():
        st.markdown(f"""
        <div class="module-card">
            <div class="module-header">
                <div class="module-icon">{module['icon']}</div>
                <h3 class="module-title">{module['title']}</h3>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Calculate progress
        completed_sections = len([
            section for section in module['sections']
            if f"{module_id}_{section}" in st.session_state.completed_modules
        ])
        progress = completed_sections / len(module['sections']) * 100

        # Show progress bar
        st.markdown(f"""
        <div class="progress-bar">
            <div class="progress-value" style="width: {progress}%;"></div>
        </div>
        """, unsafe_allow_html=True)

        # Section content
        for section in module['sections']:
            with st.expander(f"{section}"):
                st.markdown(module['content'][section])

                # Mark as complete button
                key = f"{module_id}_{section}"
                if key in st.session_state.completed_modules:
                    st.success("✅ Completed")
                else:
                    if st.button("Mark as Complete", key=key):
                        st.session_state.completed_modules.add(key)
                        st.rerun()