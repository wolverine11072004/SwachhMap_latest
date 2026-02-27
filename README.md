SwachhMap — reorganized project
Files:
- app.py         : Streamlit entrypoint
- ui.py          : UI components and main app logic (keeps original UI & features)
- auth.py        : authentication and token helpers
- data_store.py  : json helpers and default paths
- users.json, reports.json, user_tokens.json : existing data (copied from uploads)
- uploads/       : image uploads directory
How to run:
1. Install requirements: pip install streamlit geopy streamlit_folium
2. Run: streamlit run app.py
