# ☀️ Solar Industry AI Assistant (Fixed Version)

A Streamlit app that analyzes rooftop images to provide solar panel recommendations and ROI insights for India.

## 🌐 How It Works
1. Upload a satellite or aerial image of a rooftop.
2. The AI analyzes usable surface area and estimates panel fit.
3. ROI is calculated with Indian costs and government incentives.

## 🔧 What's Fixed
- ✅ Updated to use OpenRouter API with working vision model
- ✅ Comprehensive error handling for API failures
- ✅ Fixed ROI calculation KeyError
- ✅ Better JSON parsing from AI responses
- ✅ Graceful handling of failed analyses

## 🔐 Setup API Key

### For Hugging Face Spaces:
1. Go to your Space → ⚙ Settings → Secrets
2. Add: `OPENROUTER_API_KEY`: `sk-or-v1-...`

### For Local Development:
```bash
export OPENROUTER_API_KEY="sk-or-v1-your-key-here"
```

## 🏁 Run Locally
```bash
pip install -r requirements.txt
streamlit run app.py
```

## 🔑 Get API Key
1. Visit [OpenRouter.ai](https://openrouter.ai)
2. Sign up for a free account
3. Generate an API key
4. Set it as environment variable

## 📋 Features
- 🔍 AI-powered rooftop analysis
- 💰 ROI calculation with Indian market rates
- 🏛️ Government subsidy calculations
- 📊 Detailed cost breakdown
- ⚡ Error handling and validation