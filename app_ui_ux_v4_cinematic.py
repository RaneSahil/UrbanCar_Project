from pathlib import Path
import io

import joblib
import pandas as pd
import streamlit as st

st.set_page_config(page_title="UrbanKart Customer Intelligence Hub", page_icon="🛍️", layout="wide")


# --- UrbanKart UI/UX refresh: Swiss editorial + warm tech ---
st.markdown(r"""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Manrope:wght@400;500;600;700;800&display=swap');
:root{--bg:#070809;--panel:#101214;--panel2:#151719;--ink:#f3f4f2;--muted:#a2a7a5;--line:#303433;--lime:#d7f36b;--accent:#c6e75b}
.stApp{
  background:
    radial-gradient(ellipse at 50% -15%,rgba(197,219,147,.09),transparent 42rem),
    radial-gradient(ellipse at 100% 55%,rgba(120,138,115,.055),transparent 30rem),
    #070809!important;
  color:var(--ink)!important;font-family:'Manrope',sans-serif!important;
}
.stApp:before{
  content:"";position:fixed;inset:0;pointer-events:none;z-index:0;opacity:.22;
  background:
    repeating-radial-gradient(ellipse at 50% 120%,transparent 0 14px,rgba(210,220,206,.13) 15px,transparent 16px 26px);
  mask-image:linear-gradient(to bottom,transparent 0%,#000 36%,#000 100%);
  animation:cinematic-drift 28s linear infinite;
}
[data-testid="stHeader"]{background:rgba(7,8,9,.86)!important;backdrop-filter:blur(16px)}
[data-testid="stToolbar"]{right:1rem}
[data-testid="stSidebar"]{
  background:rgba(12,14,14,.97)!important;border-right:1px solid #282c2a!important;
}
[data-testid="stSidebar"] *{color:#e7e9e5}
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p,
[data-testid="stSidebar"] [data-testid="stCaptionContainer"]{color:#929a95!important}
[data-testid="stSidebar"] [aria-selected="true"]{
  background:#202421!important;border:1px solid #41483c!important;border-radius:8px!important;
}
[data-testid="stSidebar"] [aria-selected="true"] *{color:var(--lime)!important}
.block-container{max-width:1500px;padding-top:2.1rem;padding-bottom:4rem;position:relative;z-index:1}
h1,h2,h3,h4{font-family:'Manrope',sans-serif!important;color:#f5f6f2!important;letter-spacing:-.045em}
h1{font-size:clamp(2.3rem,4.5vw,4.25rem)!important;font-weight:600!important;line-height:1.02!important}
h2{font-size:clamp(1.55rem,2.4vw,2.15rem)!important;font-weight:600!important}
h3{font-size:1.2rem!important;font-weight:650!important}
p,label,.stCaption,[data-testid="stCaptionContainer"]{color:#b4bab5!important}
[data-testid="stMetric"]{
  background:linear-gradient(145deg,rgba(24,27,26,.97),rgba(13,15,15,.97))!important;
  border:1px solid #343936!important;border-radius:4px!important;padding:1.15rem 1.3rem!important;
  box-shadow:none!important;transition:border-color .25s ease,transform .25s ease;
}
[data-testid="stMetric"]:hover{border-color:#737d65!important;transform:translateY(-2px)}
[data-testid="stMetricLabel"]{color:#aab1aa!important;font-size:.82rem!important;letter-spacing:.025em}
[data-testid="stMetricValue"]{color:#f4f5ef!important;font-family:'Manrope',sans-serif!important;font-weight:600!important}
[data-testid="stMetricDelta"]{color:var(--lime)!important}
.stButton>button,[data-testid="stFormSubmitButton"]>button,[data-testid="stDownloadButton"]>button{
  min-height:2.8rem;border-radius:3px!important;font-family:'Manrope',sans-serif!important;
  font-size:.84rem!important;font-weight:700!important;letter-spacing:.015em;
  transition:transform .2s ease,background .2s ease,border-color .2s ease;
}
.stButton>button[kind="primary"],[data-testid="stFormSubmitButton"]>button[kind="primary"]{
  background:var(--lime)!important;color:#10120c!important;border:1px solid var(--lime)!important;
  box-shadow:0 0 0 rgba(215,243,107,0);
}
.stButton>button[kind="primary"]:hover,[data-testid="stFormSubmitButton"]>button[kind="primary"]:hover{
  background:#e5ff8c!important;transform:translateY(-2px);box-shadow:0 8px 28px rgba(215,243,107,.13)!important;
}
.stButton>button[kind="secondary"],[data-testid="stDownloadButton"]>button{
  background:#171a18!important;color:#e9ece5!important;border:1px solid #444a44!important;
}
.stButton>button[kind="secondary"]:hover,[data-testid="stDownloadButton"]>button:hover{
  border-color:var(--lime)!important;transform:translateY(-1px);
}
.stTextInput input,.stNumberInput input,.stTextArea textarea,[data-baseweb="select"]>div,[data-baseweb="input"]{
  color:#f2f4ef!important;-webkit-text-fill-color:#f2f4ef!important;
  background:#171a19!important;border:1px solid #3a403d!important;border-radius:3px!important;
}
.stTextInput input::placeholder,.stTextArea textarea::placeholder{
  color:#838b85!important;-webkit-text-fill-color:#838b85!important;opacity:1!important;
}
[data-testid="stNumberInput"] button{color:#e8ebe4!important;background:#202421!important;border-color:#3a403d!important}
[data-testid="stNumberInput"] button:hover{color:var(--lime)!important;border-color:#7b866c!important}
[data-testid="stSlider"] [role="slider"]{background:var(--lime)!important;border-color:var(--lime)!important;box-shadow:0 0 0 3px rgba(215,243,107,.12)!important}
[data-testid="stSlider"] [data-baseweb="slider"]>div>div{background:var(--lime)!important}
[data-testid="stSlider"] [data-testid="stTickBar"]{background:#444a45!important}
[data-testid="stForm"]{
  background:rgba(15,17,16,.88)!important;border:1px solid #303632!important;
  border-radius:5px!important;padding:1.45rem 1.5rem!important;
}
[data-testid="stVerticalBlockBorderWrapper"]{border-color:#303632!important;border-radius:5px!important}
hr{border-color:#2c312e!important}
.stProgress>div>div{background:var(--lime)!important}
[data-testid="stDataFrame"],[data-testid="stTable"]{border:1px solid #343a36!important;border-radius:4px!important;overflow:hidden}
[data-testid="stDataFrame"] *{color:#e6e9e3}
div[data-testid="stAlert"]{background:#171b17!important;border:1px solid #4c5a3b!important;border-radius:4px!important;color:#eff4e8!important}
[data-testid="stExpander"]{background:#111413!important;border:1px solid #303632!important;border-radius:4px!important}
[data-testid="stFileUploader"] section,[data-testid="stFileUploader"] [data-testid="stFileUploaderDropzone"]{
  background:#111413!important;border:1px dashed #596252!important;border-radius:4px!important;
}
[data-testid="stFileUploader"] *{color:#e8ece5!important}
[data-testid="stCode"],.stCode,pre,code{color:#e9f4c9!important}
[data-testid="stCode"]{background:#111413!important;border:1px solid #343a36!important;border-radius:4px!important}
.uk-hero{
  position:relative;isolation:isolate;overflow:hidden;margin:.15rem 0 2.1rem;
  padding:clamp(1.7rem,4.5vw,4.2rem);border:1px solid #505650;border-radius:3px;
  background:
    radial-gradient(ellipse at 84% 20%,rgba(201,218,176,.12),transparent 18rem),
    linear-gradient(125deg,rgba(22,25,23,.98),rgba(8,10,9,.96) 70%);
  box-shadow:0 24px 70px rgba(0,0,0,.2);animation:hero-in .8s cubic-bezier(.2,.7,.2,1) both;
}
.uk-hero:before{
  content:"";position:absolute;z-index:-1;width:52%;height:140%;right:-5%;top:-20%;
  border:1px solid rgba(218,231,207,.16);border-radius:50%;
  box-shadow:0 0 0 24px rgba(218,231,207,.018),0 0 0 48px rgba(218,231,207,.018),0 0 0 72px rgba(218,231,207,.018);
  transform:rotate(-18deg);animation:orbit 22s ease-in-out infinite alternate;
}
.uk-hero:after{
  content:"";position:absolute;z-index:-1;width:7px;height:7px;right:17%;top:32%;
  border-radius:50%;background:var(--lime);box-shadow:0 0 22px rgba(215,243,107,.5);
  animation:signal 3s ease-in-out infinite;
}
.uk-hero .uk-eyebrow{
  color:var(--lime)!important;text-transform:uppercase;letter-spacing:.22em;
  font-family:'DM Mono',monospace!important;font-size:.68rem;font-weight:500;margin-bottom:1.4rem;
}
.uk-hero h1{color:#f4f5f0!important;max-width:880px;margin:0 0 1.1rem;font-weight:600!important}
.uk-hero p{color:#b7beb8!important;max-width:740px;font-size:1rem;line-height:1.85}
.uk-hero .uk-pill{
  display:inline-block;margin:1.15rem .45rem 0 0;padding:.38rem .65rem;
  border:1px solid #464d46;border-radius:2px;background:rgba(255,255,255,.025);
  color:#dce2d9!important;font-family:'DM Mono',monospace!important;font-size:.66rem;
  text-transform:uppercase;letter-spacing:.07em;
}
.uk-section-note{color:#a9b0aa!important;margin-top:-.45rem;margin-bottom:1rem}
@keyframes hero-in{from{opacity:0;transform:translateY(14px)}to{opacity:1;transform:translateY(0)}}
@keyframes orbit{from{transform:translate3d(0,-1%,0) rotate(-18deg)}to{transform:translate3d(-3%,2%,0) rotate(-8deg)}}
@keyframes signal{0%,100%{opacity:.35;transform:scale(.8)}50%{opacity:1;transform:scale(1.25)}}
@keyframes cinematic-drift{from{transform:translateY(0)}to{transform:translateY(28px)}}
@media(prefers-reduced-motion:reduce){*,*:before,*:after{animation:none!important;transition:none!important}}
@media(max-width:700px){.block-container{padding:1rem .75rem 2rem}.uk-hero{padding:1.4rem}h1{font-size:2.35rem!important}.uk-hero:before{width:70%;right:-22%}}
</style>
""", unsafe_allow_html=True)

ROOT = Path(__file__).resolve().parent
REGRESSION_PATH = ROOT / "urbankart_best_regression_model.joblib"
REVIEWS_PATH = ROOT / "UrbanKart_HuggingFace_NLP_Customer_Reviews.csv"
SENTIMENT_MODEL = "cardiffnlp/twitter-roberta-base-sentiment-latest"
REVIEW_CANDIDATES = ("review_text", "review", "customer_review", "feedback", "text")


@st.cache_resource(show_spinner=False)
def load_regression_artifact(path: str, modified: float):
    artifact = joblib.load(path)
    if not isinstance(artifact, dict) or not {"model", "features", "model_name"}.issubset(artifact):
        raise ValueError("Model artifact must contain 'model', 'features', and 'model_name'.")
    return artifact


@st.cache_resource(show_spinner=False)
def load_sentiment_pipeline(model_name: str):
    from transformers import pipeline
    return pipeline("sentiment-analysis", model=model_name, tokenizer=model_name)


@st.cache_data(show_spinner=False)
def read_csv_bytes(data: bytes) -> pd.DataFrame:
    return pd.read_csv(io.BytesIO(data))


def find_review_column(columns):
    lookup = {str(c).strip().lower(): c for c in columns}
    for candidate in REVIEW_CANDIDATES:
        if candidate in lookup:
            return lookup[candidate]
    return next((c for c in columns if "review" in str(c).lower() or "feedback" in str(c).lower()), None)


def sentiment_label(value):
    value = str(value).strip().lower()
    return value.replace("label_", "label ") if value.startswith("label_") else value


def predict_reviews(classifier, texts, batch_size=16):
    predictions = []
    texts = [str(t).strip() for t in texts]
    for start in range(0, len(texts), batch_size):
        predictions.extend(classifier(texts[start:start + batch_size], truncation=True, max_length=512, batch_size=batch_size))
    return ([sentiment_label(p.get("label", "unknown")) for p in predictions],
            [float(p.get("score", 0.0)) for p in predictions])


def analyze_dataframe(df, review_col, classifier):
    result = df.copy()
    reviews = result[review_col].fillna("").astype(str).str.strip()
    valid = reviews.ne("")
    result["predicted_sentiment"] = "not analyzed (empty review)"
    result["sentiment_confidence"] = float("nan")
    if valid.any():
        labels, scores = predict_reviews(classifier, reviews.loc[valid].tolist())
        result.loc[valid, "predicted_sentiment"] = labels
        result.loc[valid, "sentiment_confidence"] = scores
    return result, int(valid.sum())


def revenue_page():
    st.markdown(
        "<section class='uk-hero'>"
        "<div class='uk-eyebrow'>URBANKART · CUSTOMER INTELLIGENCE</div>"
        "<h1>Turn customer signals<br>into smarter decisions.</h1>"
        "<p>Explore estimated annual revenue and understand customer feedback in one focused workspace. "
        "Use the prediction tools below to turn customer-level inputs into practical business insight.</p>"
        "<span class='uk-pill'>Revenue intelligence</span>"
        "<span class='uk-pill'>Predictive analytics</span>"
        "<span class='uk-pill'>Customer-first decisions</span>"
        "</section>",
        unsafe_allow_html=True,
    )
    st.subheader("Revenue prediction")
    st.markdown("<p class='uk-section-note'>Estimate annual customer revenue from profile, engagement, purchase, loyalty and service metrics.</p>", unsafe_allow_html=True)
    st.divider()
    if not REGRESSION_PATH.exists():
        st.error(f"Model file not found: `{REGRESSION_PATH.name}`. Keep it in the same folder as `app.py`.")
        return
    try:
        artifact = load_regression_artifact(str(REGRESSION_PATH), REGRESSION_PATH.stat().st_mtime)
        model, features, model_name = artifact["model"], artifact["features"], artifact["model_name"]
    except Exception as exc:
        st.error(f"Could not load regression model: {exc}")
        st.info("Check the saved artifact format and install compatible scikit-learn/joblib versions.")
        return
    st.caption(f"Model: **{model_name}** · {len(features)} input features")
    with st.form("revenue_prediction_form", border=True):
        st.header("Customer profile")
        st.caption("Enter the customer's current profile and engagement metrics. All fields keep the existing model defaults.")
        c1, c2, c3 = st.columns(3)
        with c1:
            age = st.number_input("Age", min_value=18, max_value=100, value=30)
            income = st.number_input("Annual Income (₹)", min_value=0.0, value=500000.0, step=10000.0)
            tenure = st.number_input("Customer Tenure (Months)", min_value=0, max_value=300, value=24)
            website_visits = st.number_input("Monthly Website Visits", min_value=0, max_value=1000, value=10)
            app_sessions = st.number_input("Monthly App Sessions", min_value=0, max_value=1000, value=10)
            purchase_frequency = st.number_input("Monthly Purchase Frequency", min_value=0.0, value=3.0, step=0.5)
        with c2:
            average_order_value = st.number_input("Average Order Value (₹)", min_value=0.0, value=2000.0, step=100.0)
            discount_usage_rate = st.slider("Discount Usage Rate", 0.0, 1.0, 0.2)
            orders_last_12m = st.number_input("Orders in Last 12 Months", min_value=0, max_value=1000, value=24)
            days_since_purchase = st.number_input("Days Since Last Purchase", min_value=0, max_value=3650, value=15)
            return_rate = st.slider("Return Rate", 0.0, 1.0, 0.05)
        with c3:
            support_tickets = st.number_input("Support Tickets in Last 12 Months", min_value=0, max_value=100, value=1)
            satisfaction = st.number_input("Customer Satisfaction Score", min_value=0.0, max_value=10.0, value=7.0)
            payment_delays = st.number_input("Payment Delay Count", min_value=0, max_value=100, value=0)
            loyalty_points = st.number_input("Loyalty Points", min_value=0, max_value=1000000, value=500)
            marketing_response = st.slider("Marketing Response Rate", 0.0, 1.0, 0.2)
        submitted = st.form_submit_button("🔮 Predict Annual Revenue", type="primary", use_container_width=True)
    if submitted:
        customer = {
            "Age": age, "Income": income, "Customer_Tenure_Months": tenure,
            "Website_Visits_Monthly": website_visits, "App_Sessions_Monthly": app_sessions,
            "Purchase_Frequency_Monthly": purchase_frequency, "Average_Order_Value": average_order_value,
            "Discount_Usage_Rate": discount_usage_rate, "Orders_Last_12M": orders_last_12m,
            "Days_Since_Last_Purchase": days_since_purchase, "Return_Rate": return_rate,
            "Support_Tickets_12M": support_tickets, "Customer_Satisfaction_Score": satisfaction,
            "Payment_Delay_Count": payment_delays, "Loyalty_Points": loyalty_points,
            "Marketing_Response_Rate": marketing_response,
        }
        missing = [feature for feature in features if feature not in customer]
        if missing:
            st.error(f"The input form does not provide these saved-model features: {missing}")
            return
        try:
            input_df = pd.DataFrame([customer]).reindex(columns=features)
            prediction = float(model.predict(input_df)[0])
            st.divider()
            st.header("Your revenue estimate")
            m1, m2 = st.columns(2)
            m1.metric("Estimated Annual Revenue", f"₹{max(0.0, prediction):,.2f}")
            m2.metric("Model Used", str(model_name))
            if prediction < 0:
                st.warning("The model returned a negative estimate; the displayed value is floored at ₹0.")
            st.caption("This is a model estimate, not a guaranteed outcome. Actual customer revenue may differ.")
        except Exception as exc:
            st.error(f"Prediction failed: {exc}")
    with st.expander("About this model"):
        st.write(f"**Model:** {model_name}")
        st.write("**Target:** `Annual_Revenue`")
        st.write(f"**Input features:** {len(features)}")


def feedback_page():
    st.markdown(
        "<section class='uk-hero'>"
        "<div class='uk-eyebrow'>VOICE OF THE CUSTOMER · NLP ANALYTICS</div>"
        "<h1>Listen closely.<br>Understand what matters.</h1>"
        "<p>Turn customer reviews into a clearer picture of sentiment. Analyze a single message for a quick read, "
        "or process a dataset to discover patterns across customer feedback.</p>"
        "<span class='uk-pill'>Sentiment analysis</span>"
        "<span class='uk-pill'>Review intelligence</span>"
        "<span class='uk-pill'>Batch insights</span>"
        "</section>",
        unsafe_allow_html=True,
    )
    st.caption("Hugging Face Transformers · Three-class sentiment analysis")
    st.markdown("Predictions are **negative**, **neutral**, or **positive**, with a confidence score.")
    with st.sidebar:
        st.subheader("NLP model")
        st.code(SENTIMENT_MODEL, language=None)
        st.caption("The model downloads on first use; internet access is required unless cached.")
        st.caption("Confidence is a model score, not a guarantee of correctness.")
    st.divider()
    st.header("01 · Dataset overview")
    uploaded = st.file_uploader("Optional: upload a customer review CSV", type=["csv"], key="feedback_csv_uploader")
    dataset, source = None, None
    try:
        if uploaded is not None:
            data = uploaded.getvalue()
            source = uploaded.name
        elif REVIEWS_PATH.exists():
            data = REVIEWS_PATH.read_bytes()
            source = REVIEWS_PATH.name
        else:
            data = None
        if data is not None:
            dataset = read_csv_bytes(data)
    except Exception as exc:
        st.error(f"Could not read the review CSV: {exc}")
    review_col = find_review_column(dataset.columns) if dataset is not None else None
    if dataset is not None:
        a, b, c = st.columns(3)
        a.metric("Dataset rows", f"{len(dataset):,}")
        b.metric("Columns", f"{len(dataset.columns):,}")
        c.metric("Empty review cells", f"{dataset[review_col].isna().sum():,}" if review_col else "Unknown")
        st.write(f"**Loaded file:** `{source}`")
        if review_col:
            st.success(f"Review-text column identified: `{review_col}`")
        else:
            st.error("No review-text column found. Expected `review_text` or a similarly named column.")
        with st.expander("Preview first five rows"):
            st.dataframe(dataset.head(), use_container_width=True)
    else:
        st.warning(f"`{REVIEWS_PATH.name}` not found in the project root. Place it beside `app.py` or upload a CSV.")
    st.divider()
    st.header("02 · Single-review analysis")
    review = st.text_area("Customer feedback", placeholder="The delivery was quick and the product quality was excellent.", height=120, key="single_review_text")
    if st.button("Analyze review", type="primary", key="analyze_single_review"):
        if not review.strip():
            st.warning("Enter a review before running sentiment analysis.")
        else:
            try:
                with st.spinner("Loading model and analyzing review..."):
                    classifier = load_sentiment_pipeline(SENTIMENT_MODEL)
                    result = classifier(review.strip(), truncation=True, max_length=512)[0]
                label, score = sentiment_label(result.get("label", "unknown")), float(result.get("score", 0.0))
                if label == "positive":
                    st.success(f"Predicted sentiment: **{label.title()}**")
                elif label == "negative":
                    st.error(f"Predicted sentiment: **{label.title()}**")
                else:
                    st.info(f"Predicted sentiment: **{label.title()}**")
                x, y = st.columns([2, 1])
                x.progress(max(0.0, min(1.0, score)), text="Model confidence")
                y.metric("Confidence score", f"{score:.1%}")
            except Exception as exc:
                st.error(f"Could not load or run the sentiment model: {exc}")
                st.info("Check internet access and confirm compatible `transformers` and `torch` are installed.")
    st.divider()
    st.header("03 · Batch sentiment analysis")
    if dataset is not None and review_col is not None:
        if len(dataset) == 0:
            st.warning("The dataset has no rows to analyze.")
        else:
            row_limit = st.number_input("Rows to analyze (start small)", min_value=1, max_value=len(dataset), value=min(100, len(dataset)), step=100 if len(dataset) >= 100 else 1, key="feedback_row_limit")
            if st.button("Run batch sentiment analysis", key="run_feedback_batch", use_container_width=True):
                try:
                    selected = dataset.head(int(row_limit)).copy()
                    nonempty = selected[review_col].fillna("").astype(str).str.strip().ne("").sum()
                    if not nonempty:
                        st.warning("No non-empty reviews in the selected rows.")
                    else:
                        with st.spinner(f"Analyzing {nonempty:,} reviews in batches..."):
                            classifier = load_sentiment_pipeline(SENTIMENT_MODEL)
                            results, count = analyze_dataframe(selected, review_col, classifier)
                        st.session_state["urbankart_feedback_results"] = results
                        st.success(f"Analysis complete: {count:,} non-empty reviews analyzed.")
                except Exception as exc:
                    st.error(f"Batch analysis failed: {exc}")
                    st.info("Check model download/network access, memory, and installed dependencies.")
    results = st.session_state.get("urbankart_feedback_results")
    if isinstance(results, pd.DataFrame):
        st.subheader("Batch results")
        valid = results[results["predicted_sentiment"] != "not analyzed (empty review)"]
        if not valid.empty:
            distribution = valid["predicted_sentiment"].value_counts().rename_axis("Sentiment").reset_index(name="Reviews")
            left, right = st.columns([1, 1.5])
            with left:
                st.markdown("**Sentiment distribution**")
                st.bar_chart(distribution.set_index("Sentiment"))
                percentages = valid["predicted_sentiment"].value_counts(normalize=True).mul(100).rename_axis("Sentiment").reset_index(name="Percentage")
                percentages["Percentage"] = percentages["Percentage"].map(lambda v: f"{v:.1f}%")
                st.dataframe(percentages, hide_index=True, use_container_width=True)
            with right:
                st.markdown("**Prediction preview**")
                st.dataframe(results.head(100), use_container_width=True)
        else:
            st.warning("No non-empty reviews were available to analyze.")
        st.download_button("Download analyzed reviews as CSV", data=results.to_csv(index=False).encode("utf-8-sig"), file_name="UrbanKart_Customer_Feedback_Sentiment_Results.csv", mime="text/csv", use_container_width=True)
    st.caption("This model was pretrained on Twitter text. Customer reviews may differ from its training domain; validate predictions before business use.")


pages = {
    "Customer Intelligence": [
        st.Page(revenue_page, title="Revenue Prediction", icon="💰", default=True),
        st.Page(feedback_page, title="Customer Feedback Analysis", icon="💬"),
    ]
}
st.navigation(pages).run()
