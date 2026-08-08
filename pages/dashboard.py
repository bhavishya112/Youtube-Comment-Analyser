import streamlit as st
import plotly.graph_objects as go
import pickle
import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from logger import setup_logger


logger = setup_logger(__name__, "logs/dashboard.log")


try:

    with open("backend/variables_state.pkl", "rb") as fb:
        st.session_state['variables'] = pickle.load(fb)

    st.set_page_config(
        page_title="V.I.S.I.O.N — Dashboard",
        page_icon="🐦‍🔥",
        layout="wide",
        initial_sidebar_state="collapsed",
    )

    def human_readable(num: str):

        if (not num or not num.isnumeric()):
            return num
        num = int(num)
        if num >= 1_000_000_000:
            return f"{num/1_000_000_000:.1f}B"
        elif num >= 1_000_000:
            return f"{num/1_000_000:.1f}M"
        elif num >= 1_000:
            return f"{num/1_000:.1f}K"
        else:
            return str(num)

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
    # print("dfadlfja;dfja;fdljad;fadkf")
    # print(type(variables))
    # ---------------------------------------------------------------------------
    # THEME — same dark red / black glow family as the landing page (V.I.S.I.O.N)
    # so the two pages read as one product instead of two separate apps.
    # ---------------------------------------------------------------------------
    st.markdown(
        """
        <style>
            #MainMenu, footer, header {visibility: hidden;}

            .stApp {
                background:
                    radial-gradient(ellipse 1000px 380px at 50% 0%, rgba(139,0,20,0.35) 0%, rgba(60,0,10,0.20) 32%, rgba(10,0,2,0.0) 65%),
                    linear-gradient(180deg, #0b0203 0%, #150304 10%, #1c1414 22%, #232020 100%);
                background-attachment: fixed;
            }

            .block-container {
                padding-top: 2.2rem;
                padding-bottom: 3rem;
                max-width: 1280px;
            }

            h1, h2, h3, p, span, label, div {
                color: #f0e6e6;
            }

            /* thin glossy red dot used as a recurring accent, echoing the
            dots between the letters of V.I.S.I.O.N on the landing page */
            .glow-dot {
                display: inline-block;
                width: 9px;
                height: 9px;
                border-radius: 50%;
                background: radial-gradient(circle at 35% 30%, #ff8080, #ff2b2b 60%, #7a0000 100%);
                box-shadow: 0 0 10px rgba(255,45,45,0.75), 0 0 22px rgba(255,45,45,0.35);
                margin-right: 0.55rem;
                vertical-align: middle;
            }

            /* section headers */
            .section-title {
                font-size: 1.05rem;
                font-weight: 700;
                letter-spacing: 0.03em;
                color: #f3eaea;
                margin: 0.4rem 0 0.9rem 0;
            }

            /* card-style containers (KPI cards, chart frames, text frames) */
            div[data-testid="stVerticalBlockBorderWrapper"] {
                background: rgba(20,10,10,0.55);
                border-radius: 18px;
                border: 1px solid rgba(255,90,90,0.20);
                box-shadow: 0 0 24px rgba(255,30,30,0.06), 0 2px 10px rgba(0,0,0,0.35);
            }

            /* let bordered containers actually behave like flex boxes so
            embedded plotly / matplotlib figures scale to fit instead of
            spilling out of / getting clipped by the frame */
            div[data-testid="stVerticalBlockBorderWrapper"] > div {
                display: flex;
                flex-direction: column;
                height: 100%;
            }
            div[data-testid="stVerticalBlockBorderWrapper"] .element-container {
                width: 100%;
            }
            div[data-testid="stVerticalBlockBorderWrapper"] iframe,
            div[data-testid="stVerticalBlockBorderWrapper"] .stPlotlyChart,
            div[data-testid="stVerticalBlockBorderWrapper"] .stImage img {
                border-radius: 12px;
            }

            .kpi-label {
                font-size: 0.78rem;
                font-weight: 600;
                letter-spacing: 0.05em;
                color: rgba(240,220,220,0.55);
                text-transform: uppercase;
                margin-bottom: 0.15rem;
            }

            .kpi-value {
                font-size: 1.5rem;
                font-weight: 700;
                color: #fbf1f1;
            }

            .video-meta-label {
                font-size: 0.75rem;
                color: rgba(240,220,220,0.5);
                text-transform: uppercase;
                letter-spacing: 0.04em;
            }

            .video-meta-value {
                font-size: 1.15rem;
                font-weight: 700;
                color: #fbf1f1;
            }

            .video-title {
                font-size: 1.35rem;
                font-weight: 700;
                color: #fbf1f1;
                margin-bottom: 0.4rem;
                letter-spacing: 0.01em;
            }

            .kpi-card {
                background: transparent;
                border-radius: 16px;
                padding: 1rem;
                min-height: 220px;
                display: flex;
                flex-direction: column;
                justify-content: flex-start;
            }

            .kpi-card-title {
                font-size: 1.05rem;
                font-weight: 700;
                color: #fbf1f1;
                margin-bottom: 0.5rem;
                line-height: 1.15;
            }

            .kpi-card-value {
                font-size: 3.2rem;
                font-weight: 700;
                color: #ff6b6b;
                text-shadow: 0 0 22px rgba(255,60,60,0.35);
                margin-bottom: 0.5rem;
            }

            .kpi-card-meta {
                font-size: 0.94rem;
                color: rgba(235,215,215,0.65);
                line-height: 1.55;
            }

            .kpi-card-meta span {
                display: block;
            }

            /* expander (Detailed Topic Explorer) restyled to match the frame
            language used everywhere else on the page */
            div[data-testid="stExpander"] {
                background: rgba(20,10,10,0.55);
                border-radius: 16px;
                border: 1px solid rgba(255,90,90,0.20);
                box-shadow: 0 0 20px rgba(255,30,30,0.05);
                overflow: hidden;
            }
            div[data-testid="stExpander"] summary {
                color: #fbf1f1;
                font-weight: 600;
            }

            [data-testid="stInfo"] {
                background: rgba(255,60,60,0.10);
                border: 1px solid rgba(255,90,90,0.25);
                border-radius: 10px;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # ---------------------------------------------------------------------------
    # 1) VIDEO HEADER ROW — title + views / likes / comments / language
    # ---------------------------------------------------------------------------
    print(variables['video_info'][0].get("title", "Video Title"))
    with st.container(border=True):
        # TODO: swap these for the real fields coming out of `variables`
        st.markdown(
            f'<div class="video-title"><span class="glow-dot"></span>Title : {variables["video_info"][0].get("title", "Video Title")}</div>', unsafe_allow_html=True)

        meta_cols = st.columns(4)
        meta_items = [
            ("Views", human_readable(
                variables['video_info'][0].get("view_count", "—"))),
            ("Likes", human_readable(
                variables['video_info'][0].get("like_count", "—"))),
            ("Comments", human_readable(
                variables['video_info'][0].get("comment_count", "—"))),
            ("Language", human_readable(
                variables['video_info'][0].get("default_audio_language", "—"))),
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
    love_topics = [
        t for t in variables['topics']
        if t.get('category') and 'love' in t['category'].lower()
    ]

    hate_topics = [
        t for t in variables['topics']
        if t.get('category') and 'hate' in t['category'].lower()
    ]

    request_topics = [
        t for t in variables['topics']
        if t.get('category') and 'request' in t['category'].lower()
    ]

    suggestion_topics = [
        t for t in variables['topics']
        if t.get('category') and 'suggestion' in t['category'].lower()
    ]

    total_topics = len(variables['topics'])

    # Total comments (size) for each category
    n_love_comments = sum(t['total_comments'] for t in love_topics)
    n_hate_comments = sum(t['total_comments'] for t in hate_topics)
    n_request_comments = sum(t['total_comments'] for t in request_topics)
    n_suggestion_comments = sum(t['total_comments'] for t in suggestion_topics)

    n_total_comments = sum(t['total_comments'] for t in variables['topics'])
    # ----------------------------------------------------------------------------------

    # ---------------------------------------------------------------------------------------

    def render_kpi_card(column, title_html, value, meta_html):
        card_html = f"""
        <div class="kpi-card">
            <div class="kpi-card-title">{title_html}</div>
            <div class="kpi-card-value">{value}</div>
            <div class="kpi-card-meta">{meta_html}</div>
        </div>
        """
        column.markdown(card_html, unsafe_allow_html=True)

    # ensure we never divide by zero when there are no comments yet
    n_total_comments = n_total_comments or 1

    kpi_cards = [
        (
            "<span style='font-size:28px'><b>Topics</b></span>",
            total_topics,
            f"<span>{total_topics} topics</span><span>{n_total_comments} distinct comments</span>"
        ),
        (
            "<span style='font-size:28px'><b>Love</b></span>",
            f"{int(n_love_comments / n_total_comments * 100)}%",
            f"<span>{len(love_topics)} topics</span><span>{n_love_comments} comments</span>"
        ),
        (
            "<span style='font-size:28px'><b>Hate</b></span>",
            f"{int(n_hate_comments / n_total_comments * 100)}%",
            f"<span>{len(hate_topics)} topics</span><span>{n_hate_comments} comments</span>"
        ),
        (
            "<span style='font-size:28px'><b>Requests</b></span>",
            f"{int(n_request_comments / n_total_comments * 100)}%",
            f"<span>{len(request_topics)} topics</span><span>{n_request_comments} comments</span>"
        ),
        (
            "<span style='font-size:28px'><b>Suggestion</b></span>",
            f"{int(n_suggestion_comments / n_total_comments * 100)}%",
            f"<span>{len(suggestion_topics)} topics</span><span>{n_suggestion_comments} comments</span>"
        ),
    ]

    cols = st.columns(5)
    for col, (title_html, value, meta_html) in zip(cols, kpi_cards):
        with col:
            container = st.container(border=True)
            render_kpi_card(container, title_html, value, meta_html)
    # ---------------------------------------------------------------------------
    # 3) ROW — Share of Categories (Pie chart)  |  Tags Word Cloud (matplotlib)
    # ---------------------------------------------------------------------------
    # Build DataFrame from topics list
    df = pd.DataFrame(variables['topics'])

    # Aggregate comment counts by category
    category_counts = df.groupby('category')['total_comments'].sum()

    category_colors = {
        "Love": "#ff2b6b",
        "Hate": "#ff6250",
        "Request": "#c24bff",
        "Suggestion": "#ffb84b",
        "Question": "#4b9bff",
        "Humor": "#6eed60",
        "Other": "#ffffffee"
    }

    # Match colors to the order of labels
    labels = category_counts.index
    # logger.info("labels : %s",labels)
    values = category_counts.values
    colors = [category_colors.get(cat, "#A2C5C7FF")
              for cat in labels]  # default gray if not mapped

    # Create Pie Chart
    fig1 = go.Figure(data=[go.Pie(
        labels=category_counts.index,
        values=category_counts.values,
        hole=0.55,   # donut style for modern look
        marker=dict(colors=colors, line=dict(
            color="#150304", width=2))   # 🔹 apply custom colors
    )])

    fig1.update_layout(
        title=dict(text="Share of Categories in Total Comments",
                   font=dict(color="#f0e6e6", size=14)),
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#f0e6e6"),
        margin=dict(l=10, r=10, t=45, b=10),
        autosize=True,
        legend=dict(
            orientation="h",
            y=-0.15,
            x=0.5,
            xanchor="center",
            font=dict(size=14, color="#f0e6e6")
        )
    )
    # Collect tags
    tags = []
    for vid in variables["video_info"]:
        tags.extend(vid.get("tags", []))

    # Build word cloud
    text = " ".join(tags)
    text += " tags"
    wordcloud = WordCloud(
        # width=800,
        height=440,
        background_color="#150304",
        colormap="autumn"
    ).generate(text)

    # Object-oriented Matplotlib
    fig2, ax = plt.subplots(figsize=(10, 5))
    fig2.patch.set_facecolor("#150304")
    ax.set_facecolor("#150304")

    ax.imshow(wordcloud, interpolation="bilinear")
    ax.axis("off")
    ax.set_title("Tags", color="#f0e6e6")

    row2_col1, row2_col2 = st.columns(2)

    with row2_col1:
        st.markdown('<div class="section-title"><span class="glow-dot"></span>Share of Categories in Comments</div>',
                    unsafe_allow_html=True)
        pie_chart_frame = st.container(border=True, height=440)
        with pie_chart_frame:
            # PLUG IN HERE: your Plotly pie chart figure, e.g.
            st.plotly_chart(fig1, use_container_width=True)

    with row2_col2:
        st.markdown('<div class="section-title"><span class="glow-dot"></span>Tags of the Video</div>',
                    unsafe_allow_html=True)
        wordcloud_frame = st.container(border=True, height=440)
        with wordcloud_frame:
            # PLUG IN HERE: this one is matplotlib (plt), not plotly, so use
            # st.pyplot() instead of st.plotly_chart(), e.g.
            st.pyplot(fig2, use_container_width=True)

    st.write("")  # spacing

    # ---------------------------------------------------------------------------
    # 4) ROW — Topic Distribution (by likes/comments/replies) | Topics over time
    # ---------------------------------------------------------------------------

    # Example topic names
    topic_names = [t['name'] for t in variables['topics']]

    # Example values
    by_comments = [t['total_comments'] for t in variables['topics']]
    by_likes = [t['total_likes'] for t in variables['topics']]
    by_replies = [t['total_replies'] for t in variables['topics']]

    # Suppose by_comments is your values
    max_val = max(by_comments)
    threshold = 1   # 30% of the largest bar

    # Build textposition list: "inside" if >=30%, else "outside"
    text_positions = [
        "inside" if val >= threshold else "outside"
        for val in by_comments
    ]

    fig3 = go.Figure()

    # Default trace (comments)
    fig3.add_trace(go.Bar(
        y=topic_names,
        x=by_comments,
        name="Comments",
        orientation="h",
        marker=dict(color="#ff3b3b"),
        text=topic_names,
        textposition=text_positions,
        insidetextanchor="start",
        textfont=dict(color="#f0e6e6", size=11),
        cliponaxis=False,
    ))

    # Add buttons to switch data
    fig3.update_layout(
        updatemenus=[
            dict(
                # position="bottom",
                type="buttons",
                direction="right",
                x=0.8, y=-0.22,
                showactive=True,
                bgcolor="#f0e6e6",
                bordercolor="#ff3b3b",
                font=dict(color="#150304"),
                buttons=[
                    dict(
                        # position="bottom",
                        label="By Comments",
                        method="update",
                        args=[{"x": [by_comments], "name": "Comments"},
                              {"title": "Topic Distribution by Comments"}]
                    ),
                    dict(
                        label="By Likes",
                        method="update",
                        args=[{"x": [by_likes], "name": "Likes"},
                              {"title": "Topic Distribution by Likes"}]
                    ),
                    dict(
                        label="By Replies",
                        method="update",
                        args=[{"x": [by_replies], "name": "Replies"},
                              {"title": "Topic Distribution by Replies"}]
                    )
                ]
            )
        ],

        yaxis=dict(title=None, showticklabels=False, tickfont={"size": 15},
                   categoryorder="total ascending", color="#f0e6e6"),
        xaxis=dict(title="Count", tickfont=dict(
            size=11, color="#f0e6e6"), color="#f0e6e6"),

        # xaxis_title="Count",
        # yaxis_title="Topics",
        height=460,
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(size=14, color="#f0e6e6"),
        margin=dict(l=10, r=10, t=45, b=60),
        autosize=True,
    )

    # Build DataFrame from comments list
    df = pd.DataFrame(variables['comments'])
    df['publishedAt'] = pd.to_datetime(
        df['publishedAt']).dt.date  # bucket by day

    # Pivot: time vs topic counts
    topics_data = df.groupby(['publishedAt', 'topic_name']
                             ).size().unstack(fill_value=0)

    fig4 = go.Figure()

    line_palette = ["#ff3b3b", "#ff9d3b",
                    "#ff3ba0", "#3bd1ff", "#8a3bff", "#ffd23b"]
    for i, topic in enumerate(topics_data.columns):
        fig4.add_trace(go.Scatter(
            x=topics_data.index,
            y=topics_data[topic],
            mode="lines",
            name=topic,
            line=dict(color=line_palette[i % len(line_palette)], width=2)
        ))

    fig4.update_layout(

        xaxis=dict(
            type="date",
            tickformatstops=[
                # Daily zoom → show day + month
                dict(dtickrange=[None, 86400000], value="%d %b"),

                # Monthly zoom → show month + day
                dict(dtickrange=[86400000, 2678400000], value="%d %b"),

                # Yearly zoom → show month names
                dict(dtickrange=[2678400000, 31536000000], value="%b %Y"),

                # Multi‑year zoom → show years
                dict(dtickrange=[31536000000, None], value="%Y"),
            ],
            rangeselector=dict(
                buttons=list([
                    dict(count=1, label="D", step="day", stepmode="backward"),
                    dict(count=1, label="M", step="month", stepmode="backward"),
                    dict(count=1, label="Y", step="year", stepmode="backward"),
                    dict(step="all", label="ALL")
                ]),
                bgcolor="#f0e6e6",
                # bordercolor="rgba(255,90,90,0.35)",
                font=dict(size=14, color="#000000")
            ),
            # rangeslider=dict(visible=True),
            tickformat="%Y-%m-%d",   # removes time part, shows only date
            color="#f0e6e6"
        ),
        yaxis=dict(title="N Comments", color="#f0e6e6"),
    )
    fig4.update_layout(
        legend=dict(
            orientation="h",        # horizontal legend
            x=0.5, y=-0.2,          # place below chart
            xanchor="center",
            traceorder="normal",
            font=dict(size=14),
            itemsizing="constant",

        ),
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#f0e6e6"),
        height=460,
        margin=dict(l=10, r=10, t=45, b=10),
        autosize=True,
    )

    row3_col1, row3_col2 = st.columns(2)

    with row3_col1:
        st.markdown('<div class="section-title"><span class="glow-dot"></span>Topic Distribution (by Likes, Comments, Replies)</div>',
                    unsafe_allow_html=True)
        topic_dist_frame = st.container(border=True, height=520)
        with topic_dist_frame:
            # PLUG IN HERE: your Plotly horizontal bar chart, e.g.
            st.plotly_chart(fig3, use_container_width=True)

    with row3_col2:
        st.markdown('<div class="section-title"><span class="glow-dot"></span>Topics Discussed Over Time</div>',
                    unsafe_allow_html=True)
        topic_time_frame = st.container(border=True, height=520)
        with topic_time_frame:
            # PLUG IN HERE: your Plotly line chart, e.g.
            st.plotly_chart(fig4, use_container_width=True)

    st.write("")  # spacing

    # ---------------------------------------------------------------------------
    # 5) DETAILED TOPIC EXPLORER — one expander per topic
    #    (▼ Editing / ▼ Music / ▼ Thumbnail ... each with Summary, Creator
    #    Takeaway, Representative comment, Top comments)
    # ---------------------------------------------------------------------------
    st.markdown('<div class="section-title"><span class="glow-dot"></span>Detailed Topic Explorer</div>',
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
    topics = pd.DataFrame(variables.get("topics", []))

    categories = (
        topics.groupby("category")
        .apply(lambda x: x.to_dict("records"))
        .to_dict()
    )

    topic_explorer_expanders = []  # array container, one expander per topic
    for catname, cat in categories.items():
        ct = st.expander(f"{catname}")
        with ct:
            for topic in cat:
                exp = st.expander(f"{topic.get('name', 'Topic')}")
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
                            st.write(
                                f"— {comment['authorDisplayName']} : {comment['textOriginal']} ")
                topic_explorer_expanders.append(exp)

    if topics.empty:
        st.caption(
            "No topics found in `variables['topics']` yet — this section will populate once gather_data() returns topic data.")

except Exception as E:
    import winsound
    import sys
    logger.exception(E.with_traceback(sys.exc_info()[2]))
    winsound.Beep(1000, 1000)
