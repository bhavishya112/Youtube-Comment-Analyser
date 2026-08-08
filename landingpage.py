import streamlit as st
import time
import requests
import re
st.set_page_config(
    page_title="V.I.S.I.O.N",
    page_icon="🐦‍🔥",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ---------------------------------------------------------------------------
# STYLES
# ---------------------------------------------------------------------------
st.markdown(
    """
    <style>
        #MainMenu, footer, header {visibility: hidden;}

        .stApp {
            background:
                radial-gradient(ellipse 900px 500px at 50% 0%, rgba(139,0,20,0.55) 0%, rgba(60,0,10,0.35) 30%, rgba(10,0,2,0.0) 65%),
                linear-gradient(180deg, #030102 0%, #0c0203 22%, #1a0405 40%, #f5eeee 100%);
            background-attachment: fixed;
        }

        .block-container {
            padding-top: 8rem;
            max-width: 900px;
        }

        .eyebrow {
            text-align: center;
            letter-spacing: 0.35em;
            font-size: 0.85rem;
            color: rgba(255,180,180,0.55);
            font-weight: 500;
            margin-bottom: 0.6rem;
            font-family: 'Courier New', monospace;
        }

        .hero-title {
            text-align: center;
            font-size: 4.2rem;
            font-weight: 800;
            letter-spacing: 0.25em;
            color: #f3eaea;
            margin-bottom: 0.3rem;
            font-family: 'Georgia', serif;
            text-shadow: 0 0 40px rgba(255,60,60,0.35);
        }

        .hero-title .dot {
            color: #ff3b3b;
        }

        .hero-sub {
            text-align: center;
            font-size: 1.05rem;
            font-style: italic;
            color: rgba(240,220,220,0.7);
            margin-bottom: 2.6rem;
            font-family: 'Georgia', serif;
        }

        .hero-cta {
            text-align: center;
            font-size: 1rem;
            color: rgba(255,255,255,0.55);
            margin-bottom: 1.4rem;
            letter-spacing: 0.02em;
        }

        div[data-testid="stTextInput"] {
            max-width: 680px;
            margin: 0 auto;
        }

        div[data-testid="stTextInput"] input {
            background: rgba(20,10,10,0.55);
            border: 1px solid rgba(255,90,90,0.25);
            border-radius: 14px;
            padding: 1rem 1.3rem;
            color: #f5eaea;
            font-size: 0.95rem;
            box-shadow: 0 0 30px rgba(255,40,40,0.08);
        }

        div[data-testid="stTextInput"] input::placeholder {
            color: rgba(230,210,210,0.4);
        }

        div[data-testid="stTextInput"] input:focus {
            border: 1px solid rgba(255,90,90,0.55);
            box-shadow: 0 0 35px rgba(255,60,60,0.25);
        }

        .footnote {
            text-align: center;
            margin-top: 1.6rem;
            font-size: 0.8rem;
            color: rgba(220,200,200,0.4);
            letter-spacing: 0.02em;
        }

        .error-note {
            text-align: center;
            color: #ff8080;
            font-size: 0.85rem;
            margin-top: 0.6rem;
            background-color: #00004d;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# CONTENT
# ---------------------------------------------------------------------------
st.markdown('<div class="eyebrow">Y O U T U B E&nbsp;&nbsp;C O M M E N T&nbsp;&nbsp;I N T E L L I G E N C E</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="hero-title">V<span class="dot">.</span>I<span class="dot">.</span>S<span class="dot">.</span>I<span class="dot">.</span>O<span class="dot">.</span>N</div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="hero-sub">Viewer Insight &amp; Sentiment Intelligence Optimization Network</div>',
    unsafe_allow_html=True,
)
st.markdown('<div class="hero-cta">Enter a YouTube video URL to get started</div>',
            unsafe_allow_html=True)

video_url = st.text_input(
    "youtube_url",
    placeholder="https://www.youtube.com/watch?v=...",
    label_visibility="collapsed",
    key="video_url_input",
)

FASTAPI_URL = "http://127.0.0.1:8001"

is_youtube = bool(
    re.match(r'^(https?://)?(www\.)?(youtube\.com|youtu\.be)/.+$', video_url))
try:

    placeholder = st.empty()
    if not is_youtube and video_url:
        placeholder.markdown(
            "<span class='error-note'>❌ Invalid YouTube URL</span>",
            unsafe_allow_html=True,
            text_alignment="center"
        )
        time.sleep(3)  # Show for 3 seconds
        placeholder.empty()

    elif is_youtube:
        response = requests.post(
            f"{FASTAPI_URL}/analyse",
            json={"video_url": video_url},
        )
        response.raise_for_status()

        response = response.json()

        # st.session_state["variables"] = st.session
        job_id = response["job_id"]

        with st.status("Starting analysis...", expanded=True) as status:

            previous_stage = None

            while True:
                r = requests.get(f"{FASTAPI_URL}/status/{job_id}")
                r.raise_for_status()

                data = r.json()

                stage = data["stage"]
                state = data["state"]

                if stage != previous_stage:
                    st.write(stage)
                    previous_stage = stage

                status.update(
                    label=stage,
                    state="running",
                    expanded=True,
                )

                if state == "complete":
                    status.update(
                        label="Analysis complete!",
                        state="complete",
                        expanded=False,
                    )
                    result = requests.post(f"{FASTAPI_URL}/result/{job_id}")
                    result.raise_for_status()
                    result = result.json()
                    # print(result, flush=True)
                    st.session_state["variables"] = result
                    st.switch_page("pages/dashboard.py")
                    break

                elif state == "failed":
                    status.update(
                        label="Analysis failed, we'll try to fix it",
                        state="error",
                        expanded=True,
                    )
                    break

                time.sleep(5)

except requests.exceptions.HTTPError as E:
    placeholder = st.empty()
    placeholder.markdown(
        f"<span class='error-note'>{str(E)}</span>",
        unsafe_allow_html=True,
        text_alignment="center"
    )
    time.sleep(3)  # Show for 3 seconds
    placeholder.empty()


st.markdown(
    '<div class="footnote">This system uses advanced ML techniques to analyse comment sentiment, engagement patterns and viewer intent.</div>',
    unsafe_allow_html=True,
)
