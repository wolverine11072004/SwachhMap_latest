
import streamlit as st
import time
from datetime import datetime
from data_store import get_default_files, load_json_file, save_json_file
from auth import (authenticate_user, save_user, add_tokens, get_user_tokens)
import os
from functools import lru_cache
from geopy.geocoders import Nominatim

BASE_DIR = os.path.dirname(__file__)
PATHS = get_default_files(BASE_DIR)
UPLOAD_DIR = PATHS['UPLOAD_DIR']
os.makedirs(UPLOAD_DIR, exist_ok=True)

# --- Styles and UI ---
def apply_custom_styles():
    st.markdown("""<style>
    /* simplified CSS from original to keep exact look */
    [data-testid="stAppViewContainer"] {
        border: 5px solid #1e3c72;
        border-radius: 18px;
        box-shadow: 0 0 24px 0 rgba(30,60,114,0.10);
        margin: 18px;
        padding: 0 !important;
        background-clip: padding-box;
    }
    .main, body, [data-testid="stAppViewContainer"] {
        background-color: #e6f9ec !important;
        color: #333;
        font-family: 'Inter', sans-serif;
    }
    .hero { background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%); color:white; padding:2rem; border-radius:12px; margin-bottom:1rem; }
    .auth-form { background:white; padding:1rem; border-radius:12px; border:2px solid #1e3c72; }
    </style>""", unsafe_allow_html=True)

def show_footer():
    st.markdown("""<div style='background-color:#1e3c72;color:white;padding:1rem;border-radius:12px;'>
        <div style='display:flex;justify-content:space-between;flex-wrap:wrap;'>
            <div><h3 style='color:#2E86AB;'>SwacchMap</h3><p>Empowering communities...</p></div>
            <div><h4 style='color:#2E86AB;'>Quick Links</h4><p>Home</p><p>Features</p></div>
            <div><h4 style='color:#2E86AB;'>Support</h4><p>Help Center</p></div>
        </div>
        <div style='text-align:center;margin-top:1rem;border-top:1px solid #6c757d;padding-top:0.5rem;'>
            <p>© 2025 SwachhMap. All rights reserved.</p>
        </div>
    </div>""", unsafe_allow_html=True)

# Home, Login, Signup, and main app functions closely mirror original file's UI and behaviour.
def show_home_page():
    apply_custom_styles()

    # --- Header ---
    st.markdown(
        """<h1 style='text-align:center;color:#1e3c72;margin-top:0;'>
        SwachhMap <span style='font-size:1rem;color:#2a5298;'>Nexagen</span></h1>""",
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns([8, 1, 1])
    with col2:
        if st.button("Log in", key="top_login_btn"):
            st.session_state.page = "login"
            st.rerun()
    with col3:
        if st.button("Sign Up", key="top_signup_btn"):
            st.session_state.page = "signup"
            st.rerun()

    # --- Hero Section ---
    st.markdown(
        """
        <div style='width:100%;background:linear-gradient(135deg,#1e3c72 0%,#2a5298 100%);
                    color:white;padding:3rem 1rem;border-radius:12px;
                    margin:2rem 0;text-align:center;'>
            <h1 style='margin-bottom:1rem;'>Clean Cities, Smarter Cities</h1>
            <p style='font-size:1.1rem;max-width:800px;margin:auto;'>
                Empowering communities with AI-powered waste detection, 
                citizen reporting, and municipal management for a cleaner India.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # --- Watch Demo Button (shows video inline) ---
    if st.button("▶ Watch Demo"):
        st.video(r"D:\Nexagen\WhatsApp Video 2025-09-10 at 20.03.21_c1113534.mp4")

    # --- Stats Section ---
    st.markdown(
        """
        <div style='width:100%;margin:2rem 0;text-align:center;'>
            <div style='display:flex;justify-content:space-around;flex-wrap:wrap;'>
                <div style='margin:1rem;'>
                    <h2 style='color:#1e3c72;'>87%</h2>
                    <p>Reports Resolved<br><small>67,421 of 77,051 reports</small></p>
                </div>
                <div style='margin:1rem;'>
                    <h2 style='color:#1e3c72;'>92%</h2>
                    <p>Response Rate<br><small>Within 24 hours</small></p>
                </div>
                <div style='margin:1rem;'>
                    <h2 style='color:#1e3c72;'>76%</h2>
                    <p>User Satisfaction<br><small>Based on feedback</small></p>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # --- Footer Section ---
    st.markdown(
        """
        <div style='width:100%;background:#1e3c72;color:white;padding:2rem;
                    border-radius:12px;margin-top:2rem;'>
            <div style='display:flex;justify-content:space-between;flex-wrap:wrap;'>
                <div style='margin:1rem;'>
                    <h3 style='color:#fff;'>SwachhMap</h3>
                    <p>Empowering communities with AI-powered waste detection 
                    and reporting for cleaner, smarter cities across India.</p>
                </div>
                <div style='margin:1rem;'>
                    <h4 style='color:#fff;'>Quick Links</h4>
                    <p>Home</p>
                    <p>Features</p>
                    <p>Dashboard</p>
                    <p>About Us</p>
                </div>
                <div style='margin:1rem;'>
                    <h4 style='color:#fff;'>Support</h4>
                    <p>Help Center</p>
                    <p>Contact Us</p>
                    <p>Privacy Policy</p>
                    <p>Terms of Service</p>
                </div>
            </div>
            <div style='text-align:center;margin-top:1rem;border-top:1px solid #6c757d;padding-top:0.5rem;'>
                <p>© 2025 SwachhMap. All rights reserved. Building cleaner cities through technology.</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )





def show_login_page():
    apply_custom_styles()
    import random
    if "login_captcha" not in st.session_state:
        a, b = random.randint(1,9), random.randint(1,9)
        st.session_state.login_captcha = (a,b,a+b)

    tab1, tab2 = st.tabs(["👮 Admin Panel","👤 Citizen Login"])
    with tab1:
        st.markdown("""<div class='auth-form'>""", unsafe_allow_html=True)
        st.subheader("🔐 Admin Login")
        admin_username = st.text_input("Admin Username", key="admin_username")
        admin_password = st.text_input("Admin Password", type="password", key="admin_password")
        captcha_answer = st.text_input(f"Human Verification: What is {st.session_state.login_captcha[0]} + {st.session_state.login_captcha[1]}?", key="admin_captcha")
        if st.button("Login as Admin", key="admin_login_btn"):
            if captcha_answer.strip() != str(st.session_state.login_captcha[2]):
                st.error("Human verification failed.")
            elif admin_username == "admin" and admin_password == "admin":
                st.session_state.logged_in = True
                st.session_state.username = "admin"
                st.session_state.page = "app"
                st.success("Welcome, Admin!")
                time.sleep(0.5)
                st.rerun()
            else:
                st.error("Invalid admin credentials.")
        st.markdown("</div>", unsafe_allow_html=True)
        if st.button("Back to Home", key="admin_login_back_btn"):
            st.session_state.page = "home"
            st.rerun()

    with tab2:
        st.markdown("<div class='auth-form'>", unsafe_allow_html=True)
        st.subheader("🔐 Citizen Login")
        username = st.text_input("Username", key="login_username")
        password = st.text_input("Password", type="password", key="login_password")
        captcha_answer2 = st.text_input(f"Human Verification: What is {st.session_state.login_captcha[0]} + {st.session_state.login_captcha[1]}?", key="citizen_captcha")
        if st.button("Login", key="login_btn"):
            if captcha_answer2.strip() != str(st.session_state.login_captcha[2]):
                st.error("Human verification failed.")
            elif authenticate_user(username, password, BASE_DIR):
                st.session_state.logged_in = True
                st.session_state.username = username
                st.session_state.tokens = get_user_tokens(username, BASE_DIR)
                st.session_state.page = "app"
                st.success(f"Welcome back, {username}!")
                time.sleep(0.5)
                st.rerun()
            else:
                st.error("Invalid username or password.")
        st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("""<div class='auth-switch'><p>Don't have an account? <a href='#' onclick="window.location.href='?page=signup'">Sign up</a></p></div>""", unsafe_allow_html=True)
        if st.button("Back to Home", key="login_back_btn"):
            st.session_state.page = "home"
            st.rerun()

def show_signup_page():
    apply_custom_styles()
    st.markdown("""<div class='auth-header'><h1>SwacchMap</h1><p>Citizen Registration</p></div>""", unsafe_allow_html=True)
    st.markdown("<div class='auth-form'>", unsafe_allow_html=True)
    st.subheader("📝 Citizen Sign Up")
    username = st.text_input("Choose a username", key="signup_username")
    password = st.text_input("Choose a password", type="password", key="signup_password")
    confirm = st.text_input("Confirm password", type="password", key="signup_confirm")
    if st.button("Sign Up", key="signup_btn"):
        if not username or not password:
            st.error("All fields are required.")
        elif username == "admin":
            st.error("Username 'admin' is reserved.")
        elif password != confirm:
            st.error("Passwords do not match.")
        elif save_user(username, password, BASE_DIR):
            add_tokens(username, 0, BASE_DIR)
            st.success("Account created — please login.")
            time.sleep(1)
            st.session_state.page = "login"
            st.rerun()
        else:
            st.error("Username already exists.")
    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("""<div class='auth-switch'><p>Already have an account? <a href='#' onclick="window.location.href='?page=login'">Login</a></p></div>""", unsafe_allow_html=True)
    if st.button("Back to Home", key="signup_back_btn"):
        st.session_state.page = "home"
        st.rerun()

# Reports, Map, and View Reports
def load_reports():
    return load_json_file(PATHS['REPORT_FILE'], [])

def save_report(report):
    reports = load_reports()
    reports.append(report)
    save_json_file(PATHS['REPORT_FILE'], reports)

def show_report_issue():
    st.subheader("📤 Report a Cleanliness Issue")
    import requests
    detected_location = ""
    if st.button("📍 Detect My Location (via IP)"):
        try:
            ip_req = requests.get("https://ipinfo.io/json")
            if ip_req.status_code == 200:
                data = ip_req.json()
                city = data.get("city", "")
                region = data.get("region", "")
                country = data.get("country", "")
                loc = data.get("loc", "")
                detected_location = ", ".join([city, region, country]).strip(", ")
                if loc:
                    detected_location += f" ({loc})"
                st.success(f"Detected location: {detected_location}")
            else:
                st.warning("Could not detect location automatically.")
        except Exception:
            st.warning("Could not detect location automatically.")

    location = st.text_input("Location", value=detected_location, key="report_location_input")
    description = st.text_area("Issue Description", key="report_description_input")
    image = st.file_uploader("Upload an image (optional)", type=['jpg','jpeg','png'], key="report_image_input")
    if st.button("Submit Report"):
        if not location or not description:
            st.error("Please provide both location and description.")
        else:
            filename = None
            if image:
                filename = f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{image.name}"
                with open(os.path.join(UPLOAD_DIR, filename), "wb") as f:
                    f.write(image.read())
            report = {
                "username": st.session_state.username or "Unknown User",
                "location": location,
                "description": description,
                "image": filename,
                "timestamp": datetime.now().isoformat(),
                "status": "Pending"
            }
            with st.spinner("Submitting report..."):
                save_report(report)
                add_tokens(st.session_state.username, 10, BASE_DIR)
                if image:
                    add_tokens(st.session_state.username, 5, BASE_DIR)
                st.session_state.tokens = get_user_tokens(st.session_state.username, BASE_DIR)
                time.sleep(0.3)
            st.success("✅ Report submitted successfully!")
            st.balloons()
            time.sleep(0.2)
            st.rerun()

def show_view_reports():
    st.subheader("📋 Submitted Reports")
    reports = load_reports()
    status_filter = st.selectbox("Filter by status", ["All","Pending","In Progress","Resolved"], key="filter_status")
    location_search = st.text_input("Search by location or user", key="search_box")
    filtered = reports
    if status_filter != "All":
        filtered = [r for r in filtered if r.get("status","Pending")==status_filter]
    if location_search:
        q = location_search.lower()
        filtered = [r for r in filtered if q in r.get("location","").lower() or q in r.get("username","").lower()]
    if not filtered:
        st.info("No reports match your filters.")
        return
    updated = False
    for idx, report in enumerate(reversed(filtered)):
        all_reports = load_reports()
        key = (report.get("username"), report.get("timestamp"), report.get("location"))
        report_index = None
        for i, ar in enumerate(all_reports):
            if (ar.get("username"), ar.get("timestamp"), ar.get("location")) == key:
                report_index = i
                break
        st.markdown("---")
        st.markdown(f"*User:* {report.get('username','Unknown')}")
        st.markdown(f"*Location:* {report.get('location','N/A')}")
        st.markdown(f"*Description:* {report.get('description','N/A')}")
        status = report.get('status','Pending')
        color = {'Pending':'orange','In Progress':'blue','Resolved':'green'}.get(status,'gray')
        st.markdown(f"*Status:* <span style='color:{color}; font-weight:bold'>{status}</span>", unsafe_allow_html=True)
        st.markdown(f"*Timestamp:* {report.get('timestamp','N/A')}")
        if report.get('image'):
            img_path = os.path.join(UPLOAD_DIR, report['image'])
            if os.path.exists(img_path):
                st.image(img_path, width=300)
        if st.session_state.username and st.session_state.username.lower() == 'admin' and report_index is not None:
            status_options = ['Pending','In Progress','Resolved']
            current = all_reports[report_index].get('status','Pending')
            try:
                default_idx = status_options.index(current)
            except ValueError:
                default_idx = 0
            new_status = st.selectbox('Update status', status_options, index=default_idx, key=f'status_{report_index}')
            if st.button('Save status', key=f'save_{report_index}'):
                all_reports[report_index]['status'] = new_status
                save_json_file(PATHS['REPORT_FILE'], all_reports)
                if new_status == 'Resolved':
                    resolved_user = all_reports[report_index].get('username')
                    add_tokens(resolved_user, 20, BASE_DIR)
                st.success('Status updated.')
                updated = True
    if updated:
        time.sleep(0.2)
        st.rerun()

@lru_cache(maxsize=256)
def geocode_lru(location_name):
    try:
        geolocator = Nominatim(user_agent='swacchmap')
        return geolocator.geocode(location_name, timeout=10)
    except Exception:
        return None

def geocode_location(location_name):
    try:
        geolocator = Nominatim(user_agent='swacchmap_app')
        location = geolocator.geocode(location_name)
        if location:
            return {'lat': location.latitude, 'lon': location.longitude}
    except:
        return None

def show_map_view():
    st.subheader("🗺 Map View of Reports")
    reports = load_reports()
    if not reports:
        st.info("No reports to display.")
        return
    map_data = []
    for report in reports:
        if report.get('location'):
            loc = geocode_location(report['location'])
            if loc:
                map_data.append({'lat': loc['lat'], 'lon': loc['lon']})
    if map_data:
        st.map(map_data)
    else:
        st.warning("No valid location coordinates found.")

def show_user_stats_sidebar():
    reports = load_reports()
    user_reports = [r for r in reports if isinstance(r, dict) and r.get('username') == st.session_state.username]
    total = len(user_reports)
    dates = sorted({r.get('timestamp','')[:10] for r in user_reports if r.get('timestamp')}, reverse=True)
    streak = 0
    today = datetime.now().date()
    for i, d in enumerate(dates):
        try:
            dt = datetime.strptime(d, "%Y-%m-%d").date()
            if (today - dt).days == i:
                streak += 1
            else:
                break
        except Exception:
            continue
    st.sidebar.markdown(f"📊 *Total Reports:* {total}")
    st.sidebar.markdown(f"🔥 *Current Streak:* {streak} days")
    tokens = get_user_tokens(st.session_state.username, BASE_DIR)
    st.sidebar.markdown(f"💰 *Tokens:* {tokens}")
    max_tokens = 50
    st.sidebar.write("🎯 *Progress towards goal*")
    st.sidebar.progress(min(tokens / max_tokens, 1.0))

def show_leaderboard_sidebar():
    reports = load_reports()
    counts = {}
    for r in reports:
        if not isinstance(r, dict):
            continue
        user = r.get('username','Unknown')
        counts[user] = counts.get(user,0) + 1
    if not counts:
        return
    st.sidebar.markdown("## 🏆 Top Contributors")
    sorted_users = sorted(counts.items(), key=lambda x: x[1], reverse=True)[:5]
    medals = ['🥇','🥈','🥉']
    for idx, (user, cnt) in enumerate(sorted_users, start=1):
        medal = medals[idx-1] if idx <= 3 else '•'
        st.sidebar.write(f"{medal} *{user}* — {cnt} reports")

def main_app():
    apply_custom_styles()
    st.sidebar.success(f"Logged in as: {st.session_state.username}")
    show_user_stats_sidebar()
    show_leaderboard_sidebar()
    if st.sidebar.button("🚪 Logout"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.session_state.page = "home"
        time.sleep(0.2)
        st.rerun()
    if "main_tab" not in st.session_state:
        st.session_state.main_tab = "report"
    tab_map = {"report":"📝 Report Issue","view":"📂 View Reports","map":"🗺 Map View"}
    cols = st.columns(3, gap='large')
    tab_keys = list(tab_map.keys())
    for i, key in enumerate(tab_keys):
        selected = "selected" if st.session_state.main_tab == key else ""
        btn_html = f'<button style="width:100%;padding:0.75rem;border-radius:12px;background:#1e3c72;color:white;font-weight:700;">{tab_map[key]}</button>'
        cols[i].markdown(btn_html, unsafe_allow_html=True)
        if cols[i].button(' ', key=f'tab_{key}'):
            st.session_state.main_tab = key
    if st.session_state.main_tab == 'report':
        show_report_issue()
    elif st.session_state.main_tab == 'view':
        show_view_reports()
    elif st.session_state.main_tab == 'map':
        show_map_view()
