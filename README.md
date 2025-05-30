# ☀️ Solar Industry AI Assistant

A **Streamlit-based** AI assistant that analyzes rooftop images to assess the potential for solar panel installation and calculates ROI for the Indian market.

---

## 🧠 How It Works

1. Upload a satellite/aerial image of a rooftop.
2. The app uses a **vision-capable LLM (Google Gemini)** to:
   - Identify usable rooftop area.
   - Recommend how many 350W solar panels can be installed.
3. Calculates:
   - Estimated energy output.
   - ROI using Indian market rates and government incentives.

---

## ⚙️ Local Setup Instructions

### ✅ Prerequisites

- Python 3.8+
- API Key from Google Gemini
- Recommended: virtual environment
- Code Editor like Visual Studio Code

### 🗂️ Step-by-Step Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/adityagautam473/Solar-Industry-AI-Assistant.git
   cd Solar-Industry-AI-Assistant
   ```

2. **Create and activate a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up your environment variable**:

   Create a `.env` file in the root directory and add:
   ```env
   GEMINI_API_KEY=your_gemini_key_here
   ```

   Or export manually:
   ```bash
   export GEMINI_API_KEY=your_gemini_key_here
   ```

5. **Run the app**:
   ```bash
   streamlit run app.py
   ```

---

## 📁 File Structure

```
.
├── app.py                  # Streamlit UI
├── vision_analysis.py      # Google Gemini Vision API integration
├── roi_calculator.py       # ROI calculation logic
├── requirements.txt        # Required Python packages
├── .env                    # API key (excluded from version control)
└── README.md               # Project documentation
```

---

## 🧪 Example Use Case

1. Upload a rooftop image (e.g., `rooftop.jpg`)
2. App returns:
   ```json
   {
     "usable_area_m2": 60,
     "recommended_panels": 30
   }
   ```
3. ROI Output:
   - Estimated Output: 17,000 kWh/year
   - Payback Period: 4.5 years
   - Total Cost: ₹4,72,500
   - Incentives: ₹1,41,750
   - Net Cost: ₹3,30,750

---

## 🧩 Features

- 🧠 Vision AI analysis (Google Gemini)
- 🏠 Rooftop panel recommendations
- 💰 Detailed ROI & cost breakdown
- 🇮🇳 Market-specific calculations for India
- 🧯 Graceful error handling and validation

---

## 📌 Future Improvements

- Switch to Gemini-native API (when public)
- Add performance metrics on detection accuracy
- Include support for CSV reports/export
- Compare ROI across Indian states with tariff data
- Extend support to commercial buildings

---

## 🛑 Removed/Excluded

- ❌ Deployment (used locally)
- ❌ Gradio (replaced by Streamlit)
- ❌ OpenRouter and non-Gemini models

---

## 📄 License

MIT License (or as applicable)
