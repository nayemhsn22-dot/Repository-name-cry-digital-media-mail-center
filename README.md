# CRY DIGITAL MEDIA — Premium Mail Center

A cinematic Streamlit interface for Gmail SMTP and a configurable JSON email API, with session-level sending totals and delivery history.

## Run locally
1. Install Python 3.10+.
2. `pip install -r requirements.txt`
3. `streamlit run app.py`

## Deploy
Push these files to a GitHub repository you control, then deploy `app.py` from https://share.streamlit.io/.

## Important limitations
- Gmail SMTP uses a Google App Password.
- The Email API option sends a generic JSON POST. Provider-specific APIs may require an adapter.
- Dashboard totals and history are session-level only; they are not permanent database records.
- “Sent” means the sending server accepted the request, not guaranteed inbox delivery or read status.
- Credentials are not stored in files. Do not commit secrets to GitHub; use Streamlit Secrets or enter credentials at runtime.
- Batch cap is 100 recipients per run. Send only to authorized recipients and respect provider rules.
