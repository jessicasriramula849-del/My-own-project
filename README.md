# 🌸 Jessica's Chatbot for Newly Pregnant Mothers
> *All the information you need to know about childbirth and pregnancy — from positive test to delivery room.*

A warm, empathetic, and comprehensive Streamlit web application designed specifically for newly expectant mothers, partners, and families navigating pregnancy and childbirth.

---

## ✨ Features

- **💬 Conversational AI Companion (Jessica)**:
  - Empathetic persona answering questions on symptoms, trimesters, morning sickness, nutrition, medications, and labor preparation.
  - Quick-action FAQ pills for instant answers with a single click.
  - Automatic clinical red flag detection with high-priority safety guidance.
  - Clear medical disclaimers to ensure mother and baby safety.

- **📅 Due Date & Bump Milestone Tracker**:
  - Calculates estimated due date using Naegele's rule based on Last Menstrual Period (LMP) or Conception Date.
  - Trimester progress bar and days remaining countdown.
  - Weekly baby fruit size comparisons and developmental milestones (Weeks 1 to 42).

- **🎒 Interactive Hospital Bag Checklist**:
  - Comprehensive checklists for Mama, Baby, and Partner/Support Person.
  - Real-time packing progress bar.

- **⏱️ Labor Contraction Timer & 5-1-1 Rule Guide**:
  - Explains the clinical **5-1-1 rule** for knowing when to head to the hospital or birth center.
  - Interactive contraction logger tracking duration, frequency interval, and intensity with automatic 5-1-1 alert triggers.

- **🚨 Red Flags & Doctor Guide**:
  - Dedicated reference for urgent symptoms (preeclampsia warning signs, heavy bleeding, fluid leakage, decreased fetal movement).
  - Clinical guidelines, warning signs breakdown, and hospital triage recommendations.

---

## 🚀 How to Run the App

1. Open your terminal / command prompt.
2. Navigate to this directory:
   ```bash
   cd "C:\Users\pc\.gemini\antigravity\scratch\pregnancy-chatbot"
   ```
3. Run the Streamlit application:
   ```bash
   python -m streamlit run app.py
   ```
4. Streamlit will launch your browser at `http://localhost:8501`.

---

## 📁 Project Architecture

- **`app.py`**: Main Streamlit user interface, custom pastel styling, tabbed navigation, and session state management.
- **`knowledge_base.py`**: Clinical and practical knowledge base covering trimesters, childbirth, labor stages, pain relief, safe nutrition, and red flags.
- **`.streamlit/config.toml`**: Custom warm blush theme configuration.
- **`requirements.txt`**: Minimal requirements (`streamlit`).
