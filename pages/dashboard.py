import streamlit as st
import plotly.graph_objects as go


st.set_page_config(
    page_title="V.I.S.I.O.N — Dashboard",
    page_icon="🐦‍🔥",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ---------------------------------------------------------------------------
# LOAD DATA FROM LANDING PAGE
# ---------------------------------------------------------------------------
# landing.py should have set: st.session_state['variables'] = variables
# where `variables` is whatever gather_data(url) returns (dict / object).
# Adjust the key lookups below (variables["..."] or variables.attr) to match
# the real shape of what gather_data() returns.

if "variables" not in st.session_state:
    st.warning(
        "No video data found. Go back to the home page and enter a YouTube URL first.")
    st.stop()

variables = st.session_state["variables"]
print("dfadlfja;dfja;fdljad;fadkf")
print(type(variables))
# ---------------------------------------------------------------------------
# THEME — kept deliberately calm/neutral since the charts themselves will
# carry the color. Only a thin red accent line ties it back to the landing
# page; no big red fills, glows, or gradients here.
# ---------------------------------------------------------------------------
st.markdown(
    """
    <style>
        #MainMenu, footer, header {visibility: hidden;}

        .stApp {
            background-color: #fafafa;
        }

        .block-container {
            padding-top: 2rem;
            padding-bottom: 3rem;
            max-width: 1200px;
        }

        /* section headers */
        .section-title {
            font-size: 1.05rem;
            font-weight: 700;
            color: #262626;
            margin: 0.4rem 0 0.8rem 0;
            padding-left: 0.6rem;
            border-left: 4px solid #c0392b;
        }

        /* card-style containers (KPI cards, chart frames, text frames) */
        div[data-testid="stVerticalBlockBorderWrapper"] {
            background: #ffffff;
            border-radius: 12px;
            border: 1px solid #e8e8e8;
            box-shadow: 0 1px 3px rgba(0,0,0,0.04);
        }

        .kpi-label {
            font-size: 0.78rem;
            font-weight: 600;
            letter-spacing: 0.04em;
            color: #8a8a8a;
            text-transform: uppercase;
            margin-bottom: 0.15rem;
        }

        .kpi-value {
            font-size: 1.5rem;
            font-weight: 700;
            color: #1a1a1a;
        }

        .video-meta-label {
            font-size: 0.75rem;
            color: #9a9a9a;
            text-transform: uppercase;
            letter-spacing: 0.03em;
        }

        .video-meta-value {
            font-size: 1.15rem;
            font-weight: 700;
            color: #1a1a1a;
        }

        .video-title {
            font-size: 1.3rem;
            font-weight: 700;
            color: #1a1a1a;
            margin-bottom: 0.3rem;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# 1) VIDEO HEADER ROW — title + views / likes / comments / language
# ---------------------------------------------------------------------------
with st.container(border=True):
    # TODO: swap these for the real fields coming out of `variables`
    st.markdown(
        f'<div class="video-title">{variables.get("title", "Video Title")}</div>', unsafe_allow_html=True)

    meta_cols = st.columns(4)
    meta_items = [
        ("Views", variables['video_info'][0].get("view_count", "—")),
        ("Likes", variables['video_info'][0].get("like_count", "—")),
        ("Comments", variables['video_info'][0].get("comment_count", "—")),
        ("Language", variables['video_info'][0].get("default_language", "—")),
    ]
    for col, (label, value) in zip(meta_cols, meta_items):
        with col:
            st.markdown(
                f'<div class="video-meta-label">{label}</div>', unsafe_allow_html=True)
            st.markdown(
                f'<div class="video-meta-value">{value}</div>', unsafe_allow_html=True)

st.write("")  # spacing

# ---------------------------------------------------------------------------
# 2) KPI CARD ROW — Topics | Love | Hate | Requests | Suggestions
# ---------------------------------------------------------------------------

# Count of topics by category
love_topics = [t for t in variables['topics']
               if 'love' in t['category'].lower()]
hate_topics = [t for t in variables['topics']
               if 'hate' in t['category'].lower()]
request_topics = [t for t in variables['topics']
                  if 'request' in t['category'].lower()]
suggestion_topics = [t for t in variables['topics']
                     if 'suggestion' in t['category'].lower()]

total_topics = len(variables['topics'])


# Total comments (size) for each category
n_love_comments = sum(t['total_comments'] for t in love_topics)
n_hate_comments = sum(t['total_comments'] for t in hate_topics)
n_request_comments = sum(t['total_comments'] for t in request_topics)
n_suggestion_comments = sum(t['total_comments'] for t in suggestion_topics)

n_total_comments = sum(t['total_comments'] for t in variables['topics'])
# ----------------------------------------------------------------------------------

# ---------------------------------------------------------------------------------------
fig_topics = go.Figure()

fig_topics.add_trace(
    go.Indicator(
        mode="number",
        value=total_topics,
        number={
            "font": {"size": 60}     # Percentage size
        },
        title={
            "text": (
                "<span style='font-size:34px'><b>Topics 📝</b></span>"
            )
        }
    )
)

fig_topics.update_layout(
    height=250,
    width=400,
    margin=dict(l=20, r=20, t=40, b=20),
    paper_bgcolor="white",
)

# ------------------------------------------------------------------------------------------
percentage = (n_love_comments / n_total_comments) * 100

fig_love = go.Figure()

fig_love.add_trace(
    go.Indicator(
        mode="number",
        value=percentage,
        number={
            "suffix": " %",
            "font": {"size": 60}     # Percentage size
        },
        title={
            "text": (
                "<span style='font-size:34px'><b>Love 💕</b></span><br><br>"
                f"<span style='font-size:18px ; text-align:left'>{len(love_topics)} topics</span>  "
                f"<span style='font-size:18px'>{n_love_comments} comments</span>"
            )
        }
    )
)

fig_love.update_layout(
    height=250,
    width=400,
    margin=dict(l=20, r=20, t=40, b=20),
    paper_bgcolor="white",
)
# -------------------------------------------------------------------------------------------------------------------

percentage = (n_hate_comments / n_total_comments) * 100

fig_hate = go.Figure()

fig_hate.add_trace(
    go.Indicator(
        mode="number",
        value=percentage,
        number={
            "suffix": " %",
            "font": {"size": 60}
        },
        title={
            "text": (
                "<span style='font-size:34px'><b>Hate 😡</b></span><br><br>"
                f"<span style='font-size:18px'>{len(hate_topics)} topics</span>&nbsp;&nbsp;&nbsp;"
                f"<span style='font-size:18px'>{n_hate_comments} comments</span>"
            )
        }
    )
)

fig_hate.update_layout(
    height=250,
    width=400,
    margin=dict(l=20, r=20, t=40, b=20),
    paper_bgcolor="white",
)

# ----------------------------------------------------------------------------------------------------------------------
percentage = (n_request_comments / n_total_comments) * 100

fig_requests = go.Figure()

fig_requests.add_trace(
    go.Indicator(
        mode="number",
        value=percentage,
        number={
            "suffix": " %",
            "font": {"size": 60}
        },
        title={
            "text": (
                "<span style='font-size:34px'><b>Requests 🙋</b></span><br><br>"
                f"<span style='font-size:18px'>{len(request_topics)} topics</span>&nbsp;&nbsp;&nbsp;"
                f"<span style='font-size:18px'>{n_request_comments} comments</span>"
            )
        }
    )
)

fig_requests.update_layout(
    height=250,
    width=400,
    margin=dict(l=20, r=20, t=40, b=20),
    paper_bgcolor="white",
)

# -------------------------------------------------------------------------------------------------------------------------------
percentage = (n_suggestion_comments / n_total_comments) * 100

fig_suggestions = go.Figure()

fig_suggestions.add_trace(
    go.Indicator(
        mode="number",
        value=percentage,
        number={
            "suffix": " %",
            "font": {"size": 60}
        },
        title={
            "text": (
                "<span style='font-size:34px'><b>Suggestions 💡</b></span><br><br>"
                f"<span style='font-size:18px'>{len(suggestion_topics)} topics</span>&nbsp;&nbsp;&nbsp;"
                f"<span style='font-size:18px'>{n_suggestion_comments} comments</span>"
            )
        }
    )
)

fig_suggestions.update_layout(
    height=250,
    width=400,
    margin=dict(l=20, r=20, t=40, b=20),
    paper_bgcolor="white",
)

figures = [
    fig_topics,
    fig_love,
    fig_hate,
    fig_requests,
    fig_suggestions,
]

cols = st.columns(5)

for col, fig in zip(cols, figures):
    with col:
        with st.container(border=True):
            st.plotly_chart(fig, use_container_width=True)
# ---------------------------------------------------------------------------
# 3) ROW — Share of Categories (Pie chart)  |  Tags Word Cloud (matplotlib)
# ---------------------------------------------------------------------------
row2_col1, row2_col2 = st.columns(2)

with row2_col1:
    st.markdown('<div class="section-title">Share of Categories in Comments</div>',
                unsafe_allow_html=True)
    pie_chart_frame = st.container(border=True, height=420)
    with pie_chart_frame:
        # PLUG IN HERE: your Plotly pie chart figure, e.g.
        #   st.plotly_chart(pie_fig, use_container_width=True)
        st.caption(
            "🔧 Insert Plotly pie chart here → st.plotly_chart(pie_fig, use_container_width=True)")

with row2_col2:
    st.markdown('<div class="section-title">Tags of the Video</div>',
                unsafe_allow_html=True)
    wordcloud_frame = st.container(border=True, height=420)
    with wordcloud_frame:
        # PLUG IN HERE: this one is matplotlib (plt), not plotly, so use
        # st.pyplot() instead of st.plotly_chart(), e.g.
        #   st.pyplot(wordcloud_fig, use_container_width=True)
        st.caption(
            "🔧 Insert matplotlib word cloud here → st.pyplot(wordcloud_fig)")

st.write("")  # spacing

# ---------------------------------------------------------------------------
# 4) ROW — Topic Distribution (by likes/comments/replies) | Topics over time
# ---------------------------------------------------------------------------
row3_col1, row3_col2 = st.columns(2)

with row3_col1:
    st.markdown('<div class="section-title">Topic Distribution (by Likes, Comments, Replies)</div>',
                unsafe_allow_html=True)
    topic_dist_frame = st.container(border=True, height=380)
    with topic_dist_frame:
        # PLUG IN HERE: your Plotly horizontal bar chart, e.g.
        #   st.plotly_chart(topic_distribution_fig, use_container_width=True)
        st.caption(
            "🔧 Insert Plotly bar chart here → st.plotly_chart(topic_distribution_fig, use_container_width=True)")

with row3_col2:
    st.markdown('<div class="section-title">Topics Discussed Over Time</div>',
                unsafe_allow_html=True)
    topic_time_frame = st.container(border=True, height=380)
    with topic_time_frame:
        # PLUG IN HERE: your Plotly line chart, e.g.
        #   st.plotly_chart(topics_over_time_fig, use_container_width=True)
        st.caption(
            "🔧 Insert Plotly line chart here → st.plotly_chart(topics_over_time_fig, use_container_width=True)")

st.write("")  # spacing

# ---------------------------------------------------------------------------
# 5) DETAILED TOPIC EXPLORER — one expander per topic
#    (▼ Editing / ▼ Music / ▼ Thumbnail ... each with Summary, Creator
#    Takeaway, Representative comment, Top comments)
# ---------------------------------------------------------------------------
st.markdown('<div class="section-title">Detailed Topic Explorer</div>',
            unsafe_allow_html=True)

# `topics` should be a list of dicts coming from `variables`, one per topic,
# each shaped roughly like:
# {
#     "name": "Editing",
#     "summary": "...",
#     "creator_takeaway": "...",
#     "representative_comment": "...",
#     "top_comments": ["...", "...", "..."],
# }
topics = variables.get("topics", [])

topic_explorer_expanders = []  # array container, one expander per topic
for topic in topics:
    exp = st.expander(f"▼ {topic.get('name', 'Topic')}")
    with exp:
        text_frame = st.container(border=True)
        with text_frame:
            st.markdown("**Summary**")
            st.write(topic.get("summary", "—"))

            st.markdown("**Creator Takeaway**")
            st.write(topic.get("creator_takeaway", "—"))

            st.markdown("**Representative Comment**")
            st.info(topic.get("representative_comment", "—"))

            st.markdown("**Top Comments**")
            for comment in topic.get("top_comments", []):
                st.write(f"— {comment}")
    topic_explorer_expanders.append(exp)

if not topics:
    st.caption(
        "No topics found in `variables['topics']` yet — this section will populate once gather_data() returns topic data.")
