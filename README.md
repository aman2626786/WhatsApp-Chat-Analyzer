# WhatsApp Chat Analyzer

A Streamlit web app to analyze WhatsApp chat exports.

## Features
- Upload and analyze WhatsApp chat files
- Visualize message statistics, timelines, and activity maps
- User-wise and overall analysis

## Deployment (Render)
1. Fork or clone this repository.
2. Push to your own GitHub repo.
3. Connect your repo to [Render.com](https://render.com/).
4. Render will auto-detect `render.yaml` and deploy the app.

## Local Development
```bash
pip install -r requirements.txt
streamlit run app.py
```

## File Structure
- `app.py` : Main Streamlit app
- `preprocessor.py` : Data cleaning and parsing
- `helper.py` : Analysis and visualization helpers
- `stop_hinglish.txt` : Stopwords file

## License
MIT 