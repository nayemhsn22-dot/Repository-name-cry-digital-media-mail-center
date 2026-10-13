import os, re, json, time, smtplib
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
import streamlit as st

APP_NAME = "CRY DIGITAL MEDIA"
MAX_RECIPIENTS = 100
st.set_page_config(page_title="CRY DIGITAL MEDIA | Mail Center", page_icon="✉️", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@400;500;600;700&display=swap');
:root { --bg:#070b14; --panel:#101827; --panel2:#121e31; --line:rgba(133,171,220,.18); --cyan:#51e4ff; --blue:#4778ff; --muted:#9baec8; }
.stApp { background: radial-gradient(ellipse at 78% 0%, #14294b 0%, #0a1020 36%, #070b14 76%); color:#eef5ff; font-family:'DM Sans',sans-serif; }
[data-testid="stHeader"] { background:transparent; }
[data-testid="stSidebar"] { background:linear-gradient(180deg,#0b1220,#080d17); border-right:1px solid var(--line); }
[data-testid="stSidebar"] * { color:#dce9ff; }
.block-container { max-width:1400px; padding-top:1.5rem; padding-bottom:3rem; }
h1,h2,h3 { font-family:'Space Grotesk',sans-serif !important; letter-spacing:-.035em; }
.hero { position:relative; overflow:hidden; padding:30px 34px; border:1px solid rgba(81,228,255,.28); border-radius:24px; background:linear-gradient(115deg,rgba(19,34,58,.97),rgba(13,20,37,.90) 58%,rgba(22,33,67,.88)); box-shadow:0 20px 60px rgba(0,0,0,.25); }
.hero:after { content:""; position:absolute; width:340px; height:340px; right:-100px; top:-190px; border-radius:50%; border:1px solid rgba(81,228,255,.2); box-shadow:0 0 0 28px rgba(81,228,255,.025),0 0 0 58px rgba(81,228,255,.02); }
.eyebrow { color:#67e8ff; text-transform:uppercase; font-size:.72rem; letter-spacing:.2em; font-weight:700; }
.hero h1 { font-size:clamp(2rem,4vw,3.2rem); margin:.3rem 0 .15rem; color:#fff; }
.hero p { color:#afc2dc; margin:.3rem 0; max-width:700px; }
.pill { display:inline-block; border:1px solid rgba(81,228,255,.3); background:rgba(81,228,255,.08); color:#8ceeff; padding:6px 11px; border-radius:99px; font-size:.75rem; font-weight:600; }
.metric-card { padding:20px 22px; border:1px solid var(--line); border-radius:18px; background:linear-gradient(145deg,rgba(20,31,50,.96),rgba(12,19,32,.96)); min-height:125px; box-shadow:0 10px 28px rgba(0,0,0,.12); }
.metric-label { color:#a7b8d1; font-size:.83rem; font-weight:600; }
.metric-value { font-family:'Space Grotesk',sans-serif; font-size:2rem; color:#fff; font-weight:700; margin-top:7px; }
.metric-foot { color:#68e7ff; font-size:.76rem; margin-top:3px; }
.section-head { padding:2px 0 12px; border-bottom:1px solid var(--line); margin:10px 0 20px; }
.section-head p { color:var(--muted); margin:.2rem 0 0; }
div[data-testid="stForm"], div[data-testid="stExpander"] { border:1px solid var(--line); border-radius:18px; background:rgba(14,22,37,.8); }
.stTextInput input,.stTextArea textarea,.stSelectbox div[data-baseweb="select"],.stNumberInput input { background:#0c1422 !important; color:#f2f7ff !important; border:1px solid #2a3b56 !important; border-radius:10px !important; }
.stTextInput input:focus,.stTextArea textarea:focus { border-color:var(--cyan) !important; box-shadow:0 0 0 1px var(--cyan) !important; }
.stButton>button,.stFormSubmitButton>button { background:linear-gradient(100deg,#386bff,#19c6e6); color:white; border:0; border-radius:11px; min-height:44px; font-weight:700; box-shadow:0 8px 22px rgba(35,115,255,.18); }
.stButton>button:hover,.stFormSubmitButton>button:hover { border:1px solid #8cf2ff; color:#fff; filter:brightness(1.08); }
[data-testid="stMetric"] { background:transparent; }
.stAlert { border-radius:12px; }
hr { border-color:var(--line); }
.small-muted { color:var(--muted); font-size:.82rem; }
[data-testid="stDataFrame"] { border:1px solid var(--line); border-radius:12px; overflow:hidden; }

/* Cinematic motion layer */
@keyframes auroraShift { 0%{background-position:0% 50%;} 50%{background-position:100% 50%;} 100%{background-position:0% 50%;} }
@keyframes riseIn { from{opacity:0; transform:translateY(18px) scale(.99); filter:blur(3px);} to{opacity:1; transform:translateY(0) scale(1); filter:blur(0);} }
@keyframes softPulse { 0%,100%{box-shadow:0 0 0 rgba(81,228,255,0),0 16px 44px rgba(0,0,0,.22);} 50%{box-shadow:0 0 30px rgba(81,228,255,.12),0 16px 44px rgba(0,0,0,.22);} }
@keyframes scanLine { 0%{transform:translateX(-130%) skewX(-18deg);opacity:0;} 15%{opacity:.5;} 70%{opacity:.12;} 100%{transform:translateX(360%) skewX(-18deg);opacity:0;} }
@keyframes orbitGlow { 0%,100%{transform:rotate(0deg) scale(1);opacity:.45;} 50%{transform:rotate(8deg) scale(1.08);opacity:.85;} }
.stApp { background:linear-gradient(125deg,#060a13,#0b1426,#101c35,#080d18,#0b1426); background-size:280% 280%; animation:auroraShift 24s ease infinite; }
.hero { animation:riseIn .75s cubic-bezier(.2,.7,.2,1) both, softPulse 7s ease-in-out infinite; }
.hero:before { content:""; position:absolute; z-index:0; pointer-events:none; top:0; bottom:0; left:0; width:26%; background:linear-gradient(100deg,transparent,rgba(101,234,255,.13),transparent); animation:scanLine 8s ease-in-out infinite; }
.hero:after { animation:orbitGlow 9s ease-in-out infinite; }
.metric-card { animation:riseIn .65s ease-out both; transition:transform .25s ease,border-color .25s ease,background .25s ease; }
.metric-card:hover { transform:translateY(-5px); border-color:rgba(81,228,255,.48); background:linear-gradient(145deg,rgba(24,43,70,.98),rgba(12,19,32,.98)); }
.stButton>button,.stFormSubmitButton>button { transition:transform .2s ease,filter .2s ease,box-shadow .2s ease; position:relative; overflow:hidden; }
.stButton>button:hover,.stFormSubmitButton>button:hover { transform:translateY(-2px); box-shadow:0 10px 30px rgba(36,147,255,.3); }
[data-testid="stSidebar"] { box-shadow:8px 0 35px rgba(0,0,0,.12); }
[data-testid="stSidebar"] [data-testid="stImage"] img { filter:drop-shadow(0 0 14px rgba(81,228,255,.2)); }
div[data-testid="stForm"],div[data-testid="stExpander"] { transition:border-color .25s ease,box-shadow .25s ease; }
div[data-testid="stForm"]:hover,div[data-testid="stExpander"]:hover { border-color:rgba(81,228,255,.32); box-shadow:0 12px 36px rgba(0,0,0,.12); }
h1,h2,h3 { text-shadow:0 0 24px rgba(81,228,255,.07); }
@media (prefers-reduced-motion: reduce) {
  *,*::before,*::after { animation-duration:.01ms !important; animation-iteration-count:1 !important; scroll-behavior:auto !important; transition-duration:.01ms !important; }
}

</style>
""", unsafe_allow_html=True)

ROOT = os.path.dirname(__file__)
logo = os.path.join(ROOT,"assets","cry-digital-media-logo.png")
ceo = os.path.join(ROOT,"assets","ceo-md-maruf-hussain.png")

for key, default in {"history":[],"total_attempted":0,"total_sent":0,"total_failed":0,"last_run":None}.items():
    if key not in st.session_state: st.session_state[key] = default

with st.sidebar:
    if os.path.exists(logo): st.image(logo, use_container_width=True)
    st.markdown("### MAIL OPERATIONS")
    page = st.radio("Workspace", ["Overview", "Compose & Send", "Delivery History", "Settings & Help"], label_visibility="collapsed")
    st.divider()
    st.markdown('<span class="pill">● SYSTEM READY</span>', unsafe_allow_html=True)
    st.caption("CRY DIGITAL MEDIA")
    st.caption("CEO · MD MARUF HUSSAIN")
    st.caption("Batch cap: 100 recipients")
    st.divider()
    st.markdown('<p class="small-muted">Secure your credentials. Never publish app passwords or API keys in source code.</p>', unsafe_allow_html=True)

def hero():
    c1,c2=st.columns([4,1], vertical_alignment="center")
    with c1:
        st.markdown("""<div class="hero"><div class="eyebrow">Cinematic Mail Operations</div>
        <h1>CRY DIGITAL MEDIA</h1><h3 style="color:#9feeff;margin:.1rem 0 .6rem;">Mail Center</h3>
        <p>একটি পরিষ্কার, সহজ এবং পেশাদার workspace থেকে Gmail SMTP অথবা অনুমোদিত Email API পরিচালনা করুন।</p>
        <span class="pill">✦ CINEMATIC UI</span> &nbsp; <span class="pill">SMTP + API</span> &nbsp; <span class="pill">Delivery Analytics</span> &nbsp; <span class="pill">Batch Controls</span>
        <p style="font-size:.8rem;margin-top:15px;">Developed by <b>MD MARUF HUSSAIN</b> · CEO, CRY DIGITAL MEDIA</p></div>""", unsafe_allow_html=True)
    with c2:
        if os.path.exists(ceo): st.image(ceo, width=150)
        st.caption("MD MARUF HUSSAIN · CEO")

def metric(label,value,foot):
    st.markdown(f'<div class="metric-card"><div class="metric-label">{label}</div><div class="metric-value">{value:,}</div><div class="metric-foot">{foot}</div></div>',unsafe_allow_html=True)

def parse_recipients(raw):
    parts = re.split(r"[\s,;]+", raw.strip())
    valid, invalid, seen = [], [], set()
    for item in parts:
        if not item: continue
        if re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", item):
            if item.lower() not in seen:
                valid.append(item); seen.add(item.lower())
        else: invalid.append(item)
    return valid, invalid

def send_smtp(recipients, subject, body, html_mode, user, password, delay_seconds):
    sent, failures = [], []
    server = smtplib.SMTP("smtp.gmail.com",587,timeout=30)
    try:
        server.ehlo(); server.starttls(); server.ehlo()
        server.login(user,password.replace(" ",""))
        for i, recipient in enumerate(recipients):
            msg=MIMEMultipart("alternative")
            msg["From"],msg["To"],msg["Subject"]=user,recipient,subject
            msg.attach(MIMEText(body,"html" if html_mode else "plain","utf-8"))
            try: server.sendmail(user,[recipient],msg.as_string()); sent.append(recipient)
            except Exception as exc: failures.append((recipient,str(exc)))
            if i < len(recipients)-1: time.sleep(delay_seconds)
    finally:
        try: server.quit()
        except Exception: pass
    return sent,failures

def send_api(recipients,subject,body,html_mode,endpoint,token,from_email,delay_seconds):
    sent,failures=[],[]
    for i,recipient in enumerate(recipients):
        payload={"from":from_email,"to":recipient,"subject":subject,"text":"" if html_mode else body,"html":body if html_mode else None}
        headers={"Content-Type":"application/json","Accept":"application/json"}
        if token: headers["Authorization"]="Bearer "+token
        req=Request(endpoint,data=json.dumps(payload).encode(),headers=headers,method="POST")
        try:
            with urlopen(req,timeout=30) as response:
                if 200 <= response.status < 300: sent.append(recipient)
                else: failures.append((recipient,f"HTTP {response.status}"))
        except HTTPError as exc: failures.append((recipient,f"HTTP {exc.code}: {exc.reason}"))
        except (URLError,TimeoutError,ValueError) as exc: failures.append((recipient,str(exc)))
        except Exception as exc: failures.append((recipient,str(exc)))
        if i < len(recipients)-1: time.sleep(delay_seconds)
    return sent,failures

if page == "Overview":
    hero()
    st.markdown('<div class="section-head"><h3>Performance Overview</h3><p>এই সেশনে চালানো মেইল ব্যাচের সারসংক্ষেপ।</p></div>',unsafe_allow_html=True)
    a,b,c,d=st.columns(4)
    with a: metric("TOTAL ATTEMPTED",st.session_state.total_attempted,"All send attempts")
    with b: metric("SUCCESSFULLY SENT",st.session_state.total_sent,"Accepted by sending server")
    with c: metric("FAILED",st.session_state.total_failed,"Could not send")
    with d: metric("BATCHES",len(st.session_state.history),"Runs in this session")
    st.markdown("### Quick actions")
    x,y=st.columns(2)
    with x:
        st.markdown("**✉️ Compose & Send**")
        st.write("প্রাপকের তালিকা, subject ও message দিয়ে নতুন batch শুরু করুন।")
        if st.button("Open Compose Workspace",use_container_width=True): st.session_state["nav_override"]="Compose & Send"; st.rerun()
    with y:
        st.markdown("**📊 Delivery History**")
        st.write("সফল, ব্যর্থ ও মোট recipient-এর আগের ফলাফল দেখুন।")
        if st.button("View Delivery History",use_container_width=True): st.session_state["nav_override"]="Delivery History"; st.rerun()
    st.info("‘Successfully sent’ মানে sending server মেইল গ্রহণ করেছে; এটি recipient-এর inbox-এ পৌঁছানো বা পড়ার নিশ্চয়তা নয়। এই dashboard-এর totals বর্তমান browser session-এ সংরক্ষিত থাকে; স্থায়ী ইতিহাসের জন্য database যোগ করতে হবে.")

elif page == "Compose & Send":
    hero()
    st.markdown('<div class="section-head"><h3>Compose a campaign</h3><p>ধাপে ধাপে তথ্য দিন; পাঠানোর আগে recipient count যাচাই করুন।</p></div>',unsafe_allow_html=True)
    method=st.segmented_control("Sending method",["Gmail SMTP","Email API"],default="Gmail SMTP")
    with st.form("compose_form",clear_on_submit=False):
        recipients_text=st.text_area("Recipients",placeholder="name@example.com\nanother@example.com",height=120,help="এক লাইনে একটি ঠিকানা, অথবা comma দিয়ে আলাদা করুন। সর্বোচ্চ ১০০ জন।")
        subject=st.text_input("Email subject",placeholder="Write a clear subject")
        body=st.text_area("Message body",height=200,placeholder="আপনার মেইল লিখুন…")
        html_mode=st.checkbox("Message body is HTML",value=False)
        delay=st.slider("Delay between recipients (seconds)",1,15,3)
        st.caption("Send only to recipients who have consented or who you are authorized to contact.")
        if method=="Gmail SMTP":
            smtp_user=st.text_input("Gmail address",placeholder="you@gmail.com")
            smtp_pass=st.text_input("Google App Password",type="password",help="Regular Gmail password নয়।")
            api_endpoint=api_token=api_from=""
        else:
            api_endpoint=st.text_input("Provider API endpoint",placeholder="https://api.provider.com/send")
            api_from=st.text_input("Verified sender email",placeholder="mail@yourdomain.com")
            api_token=st.text_input("Bearer API token",type="password")
            smtp_user=smtp_pass=""
        confirm=st.checkbox("I confirm these recipients are authorized and the message complies with provider rules.")
        send=st.form_submit_button("▶  Send email batch",use_container_width=True)
    if send:
        recipients,invalid=parse_recipients(recipients_text)
        if not confirm: st.error("পাঠানোর আগে authorization confirmation দিন।")
        elif not recipients: st.error("কমপক্ষে একটি valid recipient email দিন।")
        elif len(recipients)>MAX_RECIPIENTS: st.error(f"একটি batch-এ সর্বোচ্চ {MAX_RECIPIENTS} জন দেওয়া যাবে।")
        elif not subject.strip() or not body.strip(): st.error("Subject ও message body পূরণ করুন।")
        elif method=="Gmail SMTP" and (not smtp_user.strip() or not smtp_pass): st.error("Gmail address এবং App Password দিন।")
        elif method=="Email API" and (not api_endpoint.strip() or not api_from.strip()): st.error("API endpoint ও verified sender email দিন।")
        else:
            if invalid: st.warning("এই invalid entries বাদ দেওয়া হয়েছে: "+", ".join(invalid[:10]))
            progress=st.progress(0,text=f"Preparing {len(recipients)} recipient(s)…")
            try:
                if method=="Gmail SMTP":
                    sent,failures=send_smtp(recipients,subject.strip(),body,html_mode,smtp_user.strip(),smtp_pass,delay)
                else:
                    sent,failures=send_api(recipients,subject.strip(),body,html_mode,api_endpoint.strip(),api_token,api_from.strip(),delay)
                progress.progress(100,text="Batch complete")
                now=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                st.session_state.total_attempted += len(recipients)
                st.session_state.total_sent += len(sent)
                st.session_state.total_failed += len(failures)
                record={"time":now,"method":method,"subject":subject.strip(),"total":len(recipients),"sent":len(sent),"failed":len(failures),
                        "sent_list":sent,"failures":[{"recipient":r,"reason":e} for r,e in failures]}
                st.session_state.history.insert(0,record); st.session_state.last_run=now
                st.success(f"Batch finished · {len(sent)} sent · {len(failures)} failed")
                m1,m2,m3=st.columns(3)
                with m1: metric("SENT",len(sent),"Accepted by server")
                with m2: metric("FAILED",len(failures),"Errors reported")
                with m3: metric("TOTAL",len(recipients),"Unique valid recipients")
                if sent:
                    with st.expander("Successful recipients"): st.write("\n".join(sent))
                if failures:
                    with st.expander("Failed recipients and reasons",expanded=True):
                        for r,e in failures: st.write(f"- {r}: {e}")
            except Exception as exc:
                st.error(f"Connection or authentication failed: {exc}")
                st.caption("SMTP credentials, network access, provider limits এবং API format যাচাই করুন।")

elif page == "Delivery History":
    hero()
    st.markdown('<div class="section-head"><h3>Delivery History</h3><p>এই browser session-এ চলা batch-এর বিস্তারিত হিসাব।</p></div>',unsafe_allow_html=True)
    a,b,c=st.columns(3)
    with a: metric("TOTAL ATTEMPTED",st.session_state.total_attempted,"Across all batches")
    with b: metric("SUCCESSFULLY SENT",st.session_state.total_sent,"Accepted by server")
    with c: metric("FAILED",st.session_state.total_failed,"Reported errors")
    if st.session_state.history:
        import pandas as pd
        rows=[{"Time":r["time"],"Method":r["method"],"Subject":r["subject"],"Total":r["total"],"Sent":r["sent"],"Failed":r["failed"]} for r in st.session_state.history]
        st.dataframe(pd.DataFrame(rows),use_container_width=True,hide_index=True)
        csvdata=pd.DataFrame(rows).to_csv(index=False).encode("utf-8")
        st.download_button("Download summary CSV",csvdata,"cry-mail-history.csv","text/csv")
        for idx,r in enumerate(st.session_state.history):
            with st.expander(f'{r["time"]} · {r["subject"]} · {r["sent"]}/{r["total"]} sent'):
                st.write(f'Method: {r["method"]} · Failed: {r["failed"]}')
                if r["sent_list"]: st.markdown("**Sent**"); st.write("\n".join(r["sent_list"]))
                if r["failures"]:
                    st.markdown("**Failures**")
                    for f in r["failures"]: st.write(f'- {f["recipient"]}: {f["reason"]}')
    else: st.info("এখনো কোনো batch চালানো হয়নি। Compose & Send থেকে প্রথম batch পাঠালে এখানে হিসাব দেখা যাবে।")
    if st.button("Clear session history",type="secondary"):
        st.session_state.history=[]; st.session_state.total_attempted=0; st.session_state.total_sent=0; st.session_state.total_failed=0; st.rerun()

else:
    hero()
    st.markdown('<div class="section-head"><h3>Settings & Help</h3><p>সংযোগ ও রিপোর্টিং সম্পর্কে গুরুত্বপূর্ণ তথ্য।</p></div>',unsafe_allow_html=True)
    with st.expander("Gmail SMTP setup",expanded=True):
        st.markdown("1. Google Account-এ 2-Step Verification চালু করুন.\n2. Google App Password তৈরি করুন.\n3. Compose & Send-এ Gmail address এবং App Password দিন.\n4. সাধারণ Gmail password ব্যবহার করবেন না.")
    with st.expander("Email API setup"):
        st.markdown("API mode একটি generic JSON POST পাঠায়। Provider অনুযায়ী endpoint, payload fields এবং authentication আলাদা হতে পারে। নিচের schema আপনার provider-এর সঙ্গে মিলিয়ে নিন.")
        st.code(json.dumps({"from":"verified@yourdomain.com","to":"recipient@example.com","subject":"Subject","text":"Plain text body","html":None},indent=2),language="json")
        st.warning("Generic API mode সব provider-এর সঙ্গে স্বয়ংক্রিয়ভাবে কাজ করবে এমন নিশ্চয়তা নেই; provider-specific adapter প্রয়োজন হতে পারে.")
    with st.expander("Dashboard totals & privacy"):
        st.write("Totals বর্তমান Streamlit session-এ গণনা হয়। পেজ reload, session expiry বা app restart হলে এগুলো স্থায়ী নাও থাকতে পারে। স্থায়ী audit log-এর জন্য database ও authentication যোগ করতে হবে.")
        st.write("এই অ্যাপ email opens, inbox placement বা delivery receipts track করে না; sent সংখ্যা মানে sending server request গ্রহণ করেছে.")
    with st.expander("Brand profile"):
        if os.path.exists(ceo): st.image(ceo,width=170)
        st.markdown("**MD MARUF HUSSAIN**  \nChief Executive Officer (CEO)  \nCRY DIGITAL MEDIA")

st.divider()
st.markdown('<p class="small-muted">CRY DIGITAL MEDIA · CEO: MD MARUF HUSSAIN · Send responsibly. Protect all credentials.</p>',unsafe_allow_html=True)
