import streamlit as st
import datetime
import time
from typing import List, Dict

from knowledge_base import (
    generate_jessica_response,
    get_week_summary,
    FAQS,
    check_for_red_flags,
    get_red_flag_response
)

# Page configuration
st.set_page_config(
    page_title="Jessica's Pregnancy & Childbirth Chatbot",
    page_icon="🌸",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling (Warm, calming, maternal aesthetic)
st.markdown("""
<style>
    /* Main container styling */
    .main-header {
        background: linear-gradient(135deg, #fce7f3 0%, #fff1f2 50%, #fdf2f8 100%);
        padding: 2.2rem 2rem;
        border-radius: 20px;
        margin-bottom: 1.5rem;
        border: 1px solid #fbcfe8;
        box-shadow: 0 4px 15px rgba(224, 109, 146, 0.08);
    }
    
    .main-title {
        color: #831843;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        font-size: 2.2rem;
        font-weight: 750;
        margin-bottom: 0.4rem;
        letter-spacing: -0.02em;
    }
    
    .main-subtitle {
        color: #9d174d;
        font-size: 1.15rem;
        font-weight: 450;
        line-height: 1.5;
        margin-bottom: 0.8rem;
    }

    .badge-pill {
        display: inline-block;
        background-color: #fce7f3;
        color: #9d174d;
        border: 1px solid #f472b6;
        padding: 0.3rem 0.8rem;
        border-radius: 9999px;
        font-size: 0.82rem;
        font-weight: 600;
        margin-right: 0.5rem;
    }
    
    .disclaimer-card {
        background-color: #fffbeb;
        border-left: 4px solid #f59e0b;
        padding: 0.85rem 1.2rem;
        border-radius: 0 10px 10px 0;
        margin-top: 1rem;
        font-size: 0.88rem;
        color: #78350f;
    }

    .emergency-card {
        background: linear-gradient(135deg, #fff1f2 0%, #ffe4e6 100%);
        border: 1px solid #fda4af;
        border-left: 5px solid #e11d48;
        padding: 1.2rem;
        border-radius: 12px;
        margin-bottom: 1rem;
    }

    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
    }

    .stTabs [data-baseweb="tab"] {
        background-color: #fdf2f8;
        border-radius: 10px 10px 0 0;
        padding: 10px 18px;
        font-weight: 600;
        color: #831843;
        border: 1px solid #fce7f3;
        border-bottom: none;
    }

    .stTabs [aria-selected="true"] {
        background-color: #fbcfe8 !important;
        color: #701a75 !important;
        font-weight: 700;
    }

    /* Chat bubble tweaks */
    [data-testid="stChatMessage"] {
        background-color: #ffffff;
        border: 1px solid #fce7f3;
        border-radius: 16px;
        padding: 1rem;
        margin-bottom: 0.75rem;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.02);
    }

    .topic-pill-btn {
        background-color: #fdf2f8;
        border: 1px solid #fbcfe8;
        color: #9d174d;
        border-radius: 20px;
        padding: 4px 12px;
        margin: 4px;
        display: inline-block;
        font-size: 0.85rem;
        cursor: pointer;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session states
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": (
                "🌸 **Welcome, mama!** I'm **Jessica**, your pregnancy and childbirth companion.\n\n"
                "Whether you're holding a positive test, managing morning sickness, planning for labor, "
                "or wondering what to pack in your hospital bag, I'm here to give you calm, medically vetted, "
                "and comforting guidance.\n\n"
                "✨ *How are you feeling today, or what would you like to explore?*"
            )
        }
    ]

if "contraction_logs" not in st.session_state:
    st.session_state.contraction_logs = []

# SIDEBAR: Persona, Emergency Help, Trimester Quick Links
with st.sidebar:
    st.markdown("### 👩‍⚕️ About Jessica")
    st.markdown(
        """
        **Jessica** is your virtual pregnancy guide, created to provide newly expectant mothers 
        with reliable information on prenatal health, fetal development, labor stages, and postpartum recovery.
        """
    )
    
    st.markdown("---")
    st.markdown("### 🚨 Urgent Medical Guidance")
    st.info(
        "**Symptoms Requiring Immediate Evaluation:**\n"
        "- Heavy bright red vaginal bleeding\n"
        "- Severe abdominal or one-sided shoulder pain\n"
        "- Severe throbbing headache with blurry vision or spots\n"
        "- Sudden noticeable swelling in face or hands\n"
        "- Marked decrease or absence of baby's movement\n\n"
        "🏥 **Action Advice**: Proceed promptly to your nearest maternity hospital, Labor & Delivery triage unit, or local emergency medical department."
    )

    st.markdown("### 💜 Emotional & Mental Wellness")
    st.markdown(
        """
        Pregnancy brings profound hormonal and emotional shifts.
        - **Rest & Grace**: Give yourself permission to slow down and rest without guilt.
        - **Open Dialogue**: Share feelings of anxiety, sadness, or exhaustion with your partner, loved ones, or prenatal care provider.
        - **Maternal Support**: Seek certified perinatal counselors, postpartum doulas, or local maternal support circles for guided support.
        """
    )

    st.markdown("---")
    st.markdown("### ⚙️ Settings & Tools")
    if st.button("🗑️ Clear Chat History", use_container_width=True):
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": "🌸 Chat refreshed! Hello mama, what would you like to learn about pregnancy or childbirth today?"
            }
        ]
        st.rerun()

    st.markdown("<br><center><small>Made with ❤️ for expectant mothers everywhere</small></center>", unsafe_allow_html=True)


# Main Header Banner
st.markdown("""
<div class="main-header">
    <span class="badge-pill">👶 Pregnancy & Labor Companion</span>
    <span class="badge-pill">🩺 Clinical Guidance</span>
    <span class="badge-pill">💖 Empathetic Care</span>
    <h1 class="main-title">Jessica's Chatbot for Newly Pregnant Mothers</h1>
    <p class="main-subtitle">All the information you need to know about childbirth and pregnancy — from your first positive test to welcoming your baby.</p>
</div>
""", unsafe_allow_html=True)

# Main Navigation Tabs
tabs = st.tabs([
    "💬 Chat with Jessica",
    "📅 Due Date & Bump Tracker",
    "🎒 Hospital Bag Checklist",
    "⏱️ Contraction Timer & 5-1-1 Rule",
    "🚨 Red Flags & Doctor Guide"
])

# ==========================================
# TAB 1: CHAT WITH JESSICA
# ==========================================
with tabs[0]:
    st.markdown("#### 💡 Frequently Asked Questions & Quick Topics")
    st.caption("Click any question below to ask Jessica instantly:")

    col_a, col_b, col_c, col_d = st.columns(4)
    quick_queries = [
        ("🤢 Morning Sickness", "How can I relieve severe morning sickness?"),
        ("🥑 Nutrition & Diet", "What foods should I eat and avoid during pregnancy?"),
        ("⚡ Early Cramping", "Is light cramping or spotting normal in early pregnancy?"),
        ("🏥 Stages of Labor", "What are the 3 stages of labor and what happens?"),
        ("⏱️ The 5-1-1 Rule", "What is the 5-1-1 rule for going to the hospital?"),
        ("💊 Safe Medications", "What over the counter medications are safe for headache and colds?"),
        ("🎒 Hospital Bag", "What are the essential items to pack in my hospital bag?"),
        ("💉 Epidural & Pain Relief", "What are my pain relief and epidural options during birth?")
    ]

    clicked_prompt = None
    for idx, (label, query_text) in enumerate(quick_queries):
        target_col = [col_a, col_b, col_c, col_d][idx % 4]
        if target_col.button(label, key=f"quick_btn_{idx}", use_container_width=True):
            clicked_prompt = query_text

    st.markdown("---")

    # Display Conversation History
    for message in st.session_state.messages:
        avatar = "🌸" if message["role"] == "assistant" else "🤰"
        with st.chat_message(message["role"], avatar=avatar):
            st.markdown(message["content"])

    # Handle clicked quick prompt or typed user input
    user_input = st.chat_input("Ask Jessica anything about your symptoms, trimesters, birth plan, or baby...")

    prompt_to_process = clicked_prompt if clicked_prompt else user_input

    if prompt_to_process:
        # Display user message
        st.session_state.messages.append({"role": "user", "content": prompt_to_process})
        with st.chat_message("user", avatar="🤰"):
            st.markdown(prompt_to_process)

        # Generate response
        with st.chat_message("assistant", avatar="🌸"):
            with st.spinner("Jessica is typing..."):
                time.sleep(0.4) # Gentle realistic pacing
                response = generate_jessica_response(prompt_to_process, st.session_state.messages)
                st.markdown(response)

        st.session_state.messages.append({"role": "assistant", "content": response})
        st.rerun()

    st.markdown("""
    <div class="disclaimer-card">
        <strong>⚠️ Medical Disclaimer:</strong> Jessica is an educational AI companion designed to provide supportive, 
        evidence-based information. Jessica is <em>not</em> a substitute for individualized clinical judgment, diagnosis, 
        or medical treatment. Always consult with your OB/GYN, midwife, or certified prenatal healthcare provider for 
        medical concerns.
    </div>
    """, unsafe_allow_html=True)


# ==========================================
# TAB 2: DUE DATE & BUMP TRACKER
# ==========================================
with tabs[1]:
    st.markdown("### 📅 Due Date & Weekly Development Tracker")
    st.write("Calculate your estimated delivery date and see what milestone baby is reaching this week!")

    calc_col1, calc_col2 = st.columns([1, 2])

    with calc_col1:
        calc_method = st.radio(
            "Calculation Method:",
            ["First Day of Last Menstrual Period (LMP)", "Exact Conception Date", "I already know my current week"]
        )

        today = datetime.date.today()

        if calc_method == "First Day of Last Menstrual Period (LMP)":
            lmp_date = st.date_input("First day of last period:", value=today - datetime.timedelta(days=70))
            # Naegele's rule: LMP + 280 days
            estimated_due = lmp_date + datetime.timedelta(days=280)
            days_pregnant = (today - lmp_date).days
            current_weeks = max(1, min(42, days_pregnant // 7))
            current_days = max(0, days_pregnant % 7)

        elif calc_method == "Exact Conception Date":
            conception_date = st.date_input("Date of ovulation / conception:", value=today - datetime.timedelta(days=56))
            # Conception + 266 days
            estimated_due = conception_date + datetime.timedelta(days=266)
            days_pregnant = (today - conception_date).days + 14
            current_weeks = max(1, min(42, days_pregnant // 7))
            current_days = max(0, days_pregnant % 7)

        else:
            current_weeks = st.slider("Select your current week:", min_value=1, max_value=42, value=16)
            current_days = 0
            days_from_start = current_weeks * 7
            lmp_date = today - datetime.timedelta(days=days_from_start)
            estimated_due = lmp_date + datetime.timedelta(days=280)

    with calc_col2:
        trimester_name = "1st Trimester" if current_weeks <= 12 else ("2nd Trimester (Golden Trimester)" if current_weeks <= 27 else "3rd Trimester (Final Stretch!)")
        days_left = max(0, (estimated_due - today).days)

        # Milestone Card
        st.markdown(f"""
        <div style="background-color: #ffffff; border: 2px solid #fbcfe8; border-radius: 16px; padding: 1.5rem; margin-bottom: 1rem;">
            <h3 style="color: #831843; margin-top: 0;">🎉 You are roughly <strong>{current_weeks} weeks and {current_days} days</strong> along!</h3>
            <p style="font-size: 1.1rem; color: #4a5568;">
                🌟 <strong>Estimated Due Date</strong>: <span style="color: #be185d; font-weight: bold;">{estimated_due.strftime('%B %d, %Y')}</span><br>
                ⏳ <strong>Days Remaining</strong>: ~{days_left} days until your estimated birth date<br>
                🌿 <strong>Trimester Stage</strong>: <strong>{trimester_name}</strong>
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.progress(min(1.0, current_weeks / 40.0), text=f"Pregnancy Progress: {int((current_weeks/40.0)*100)}% to Full Term")

        # Week details from knowledge base
        st.markdown(get_week_summary(current_weeks))

    st.markdown("---")
    st.markdown("### 🌟 Trimester Milestones at a Glance")
    t1_col, t2_col, t3_col = st.columns(3)
    with t1_col:
        st.markdown("""
        **🌱 First Trimester (Weeks 1-12)**
        - **Baby**: Heart starts beating at ~6 weeks; organs form.
        - **Mama**: Morning sickness, tender breasts, extreme fatigue.
        - **Checkups**: First prenatal appointment & dating ultrasound (~8-10 weeks).
        """)
    with t2_col:
        st.markdown("""
        **🌼 Second Trimester (Weeks 13-27)**
        - **Baby**: Begins hearing voices; anatomy scan at week 20; first kicks!
        - **Mama**: Energy boost, round ligament pain, pregnancy glow.
        - **Checkups**: Anatomy ultrasound & glucose tolerance screening.
        """)
    with t3_col:
        st.markdown("""
        **🌺 Third Trimester (Weeks 28-40+)**
        - **Baby**: Rapid weight gain, lung maturation, turns head-down.
        - **Mama**: Braxton Hicks, frequent urination, nesting instinct.
        - **Checkups**: Bi-weekly then weekly visits, Group B Strep test at 36w.
        """)


# ==========================================
# TAB 3: HOSPITAL BAG CHECKLIST
# ==========================================
with tabs[2]:
    st.markdown("### 🎒 Interactive Hospital Bag Checklist")
    st.write("Check off items as you pack them. We recommend having your bags packed by **Week 34-36**!")

    # Checklist data in session state
    checklist_defaults = {
        "mom_docs": ("ID, Health Insurance Card, & Hospital Pre-registration papers", True),
        "mom_birth_plan": ("Printed copies of your Birth Preferences / Birth Plan", False),
        "mom_charger": ("Extra-long phone charging cable (10 ft) or portable power bank", True),
        "mom_clothes": ("2 comfy, loose nursing nightgowns or button-down pajamas", False),
        "mom_slippers": ("Non-slip grip socks & easy slip-on slides/slippers", False),
        "mom_toiletries": ("Toiletries (lip balm, hair ties, toothbrush, dry shampoo, lotion)", False),
        "mom_going_home": ("Loose, comfortable going-home outfit (maternity leggings or dress)", False),
        "mom_nursing_bra": ("2 wire-free nursing bras and nipple balm (lanolin or silverettes)", False),
        
        "baby_car_seat": ("Infant Car Seat (installed & inspected in car!)", True),
        "baby_outfits": ("2-3 Going-home outfits (sizes Newborn AND 0-3 Months)", False),
        "baby_swaddles": ("2 Velcro or zip swaddles & soft receiving blanket", False),
        "baby_hat_mittens": ("Baby hat and scratch mittens", False),
        "baby_pediatrician": ("Pediatrician name & clinic office address", False),

        "partner_clothes": ("Change of comfortable clothes & layer/jacket", False),
        "partner_snacks": ("High-protein snacks, electrolyte powders, mints", False),
        "partner_pillow": ("Pillow and blanket from home (with non-white pillowcase)", False),
        "partner_camera": ("Camera or charged phones with storage cleared for photos", False),
    }

    for key, (label, default_val) in checklist_defaults.items():
        if key not in st.session_state:
            st.session_state[key] = default_val

    # Progress calculation
    total_items = len(checklist_defaults)
    packed_items = sum(1 for k in checklist_defaults if st.session_state.get(k, False))
    pack_percent = int((packed_items / total_items) * 100)

    st.progress(pack_percent / 100.0, text=f"Bag Packing Progress: {packed_items}/{total_items} items packed ({pack_percent}%)")

    col_m, col_b, col_p = st.columns(3)

    with col_m:
        st.markdown("#### 🤰 For Mama")
        st.session_state["mom_docs"] = st.checkbox(checklist_defaults["mom_docs"][0], value=st.session_state["mom_docs"])
        st.session_state["mom_birth_plan"] = st.checkbox(checklist_defaults["mom_birth_plan"][0], value=st.session_state["mom_birth_plan"])
        st.session_state["mom_charger"] = st.checkbox(checklist_defaults["mom_charger"][0], value=st.session_state["mom_charger"])
        st.session_state["mom_clothes"] = st.checkbox(checklist_defaults["mom_clothes"][0], value=st.session_state["mom_clothes"])
        st.session_state["mom_slippers"] = st.checkbox(checklist_defaults["mom_slippers"][0], value=st.session_state["mom_slippers"])
        st.session_state["mom_toiletries"] = st.checkbox(checklist_defaults["mom_toiletries"][0], value=st.session_state["mom_toiletries"])
        st.session_state["mom_going_home"] = st.checkbox(checklist_defaults["mom_going_home"][0], value=st.session_state["mom_going_home"])
        st.session_state["mom_nursing_bra"] = st.checkbox(checklist_defaults["mom_nursing_bra"][0], value=st.session_state["mom_nursing_bra"])

    with col_b:
        st.markdown("#### 👶 For Baby")
        st.session_state["baby_car_seat"] = st.checkbox(checklist_defaults["baby_car_seat"][0], value=st.session_state["baby_car_seat"])
        st.session_state["baby_outfits"] = st.checkbox(checklist_defaults["baby_outfits"][0], value=st.session_state["baby_outfits"])
        st.session_state["baby_swaddles"] = st.checkbox(checklist_defaults["baby_swaddles"][0], value=st.session_state["baby_swaddles"])
        st.session_state["baby_hat_mittens"] = st.checkbox(checklist_defaults["baby_hat_mittens"][0], value=st.session_state["baby_hat_mittens"])
        st.session_state["baby_pediatrician"] = st.checkbox(checklist_defaults["baby_pediatrician"][0], value=st.session_state["baby_pediatrician"])

    with col_p:
        st.markdown("#### 👫 For Partner / Support")
        st.session_state["partner_clothes"] = st.checkbox(checklist_defaults["partner_clothes"][0], value=st.session_state["partner_clothes"])
        st.session_state["partner_snacks"] = st.checkbox(checklist_defaults["partner_snacks"][0], value=st.session_state["partner_snacks"])
        st.session_state["partner_pillow"] = st.checkbox(checklist_defaults["partner_pillow"][0], value=st.session_state["partner_pillow"])
        st.session_state["partner_camera"] = st.checkbox(checklist_defaults["partner_camera"][0], value=st.session_state["partner_camera"])

    st.markdown("💡 *Pro-tip: Hospitals provide mesh underwear, giant pads, peri-bottles, and diapers for baby during your stay. Save your space for personal comfort items!*")


# ==========================================
# TAB 4: CONTRACTION TIMER & 5-1-1
# ==========================================
with tabs[3]:
    st.markdown("### ⏱️ Labor Contraction Timer & The 5-1-1 Rule")

    st.markdown("""
    <div style="background-color: #fdf2f8; border: 1px solid #f472b6; border-radius: 12px; padding: 1.2rem; margin-bottom: 1.5rem;">
        <h4 style="color: #831843; margin-top: 0;">What is the 5-1-1 Rule?</h4>
        <p style="color: #4a5568; margin-bottom: 0;">
            Most OB/GYNs and midwives advise coming to the hospital when your contractions are:
            <br>• <strong>5 minutes apart</strong> (measured from the start of one contraction to the start of the next).
            <br>• Lasting <strong>1 full minute</strong> (60 seconds) in duration.
            <br>• Consistent for at least <strong>1 full hour</strong>.
        </p>
    </div>
    """, unsafe_allow_html=True)

    t_col1, t_col2 = st.columns([1, 1])

    with t_col1:
        st.subheader("Contraction Logger")
        st.write("Log your recent contractions to analyze frequency and duration:")

        with st.form("contraction_form", clear_on_submit=True):
            duration_sec = st.slider("Contraction Duration (seconds):", min_value=15, max_value=120, value=60, step=5)
            interval_min = st.slider("Time since previous contraction started (minutes):", min_value=1.0, max_value=30.0, value=5.0, step=0.5)
            intensity = st.select_slider("Intensity Level:", options=["Mild (can talk)", "Moderate (need focus)", "Strong (cannot talk)"])
            submitted = st.form_submit_button("➕ Log Contraction")

            if submitted:
                now_str = datetime.datetime.now().strftime("%I:%M %p")
                st.session_state.contraction_logs.insert(0, {
                    "time": now_str,
                    "duration": f"{duration_sec}s",
                    "interval": f"{interval_min}m",
                    "intensity": intensity,
                    "is_511": (duration_sec >= 50 and interval_min <= 5.5 and intensity != "Mild (can talk)")
                })
                st.success(f"Logged contraction at {now_str}!")

    with t_col2:
        st.subheader("Recent Contraction History")
        if st.session_state.contraction_logs:
            # Check 5-1-1 alert
            recent_matches = sum(1 for c in st.session_state.contraction_logs[:5] if c["is_511"])
            if recent_matches >= 3:
                st.markdown("""
                <div class="emergency-card">
                    <h4 style="color: #9f1239; margin-top: 0;">🔔 5-1-1 Pattern Detected!</h4>
                    <p style="color: #881337; margin-bottom: 0;">
                        Your recent logs match the 5-1-1 active labor pattern. 
                        <strong>It's time to call your labor & delivery triage unit or head to the birth center!</strong>
                    </p>
                </div>
                """, unsafe_allow_html=True)

            for log in st.session_state.contraction_logs[:8]:
                badge = "🔥 5-1-1 Match" if log["is_511"] else "⏱️ Normal"
                st.markdown(
                    f"**{log['time']}** — Duration: `{log['duration']}` | Interval: `{log['interval']}` | {log['intensity']} *({badge})*"
                )

            if st.button("Clear Contraction Logs"):
                st.session_state.contraction_logs = []
                st.rerun()
        else:
            st.info("No contractions logged yet. Use the logger on the left when labor begins!")


# ==========================================
# TAB 5: RED FLAGS & DOCTOR GUIDE
# ==========================================
with tabs[4]:
    st.markdown("### 🚨 When to Call Your Doctor or Go to Labor & Delivery Immediately")
    st.write(
        "Never hesitate or feel self-conscious about contacting your maternity triage unit. "
        "Labor and delivery nurses and OB/GYNs are staffed 24/7 specifically to evaluate you and baby."
    )

    rf_col1, rf_col2 = st.columns(2)

    with rf_col1:
        st.markdown("""
        <div class="emergency-card">
            <h4 style="color: #be123c; margin-top: 0;">🩸 Bleeding & Fluid Leaks</h4>
            <ul>
                <li><strong>Heavy Vaginal Bleeding</strong>: Bleeding like a heavy period or soaking a pad within an hour.</li>
                <li><strong>Leaking Amniotic Fluid</strong>: Continuous trickle or sudden gush of watery fluid (especially before 37 weeks, or if green/brown tinged).</li>
                <li><strong>Severe Continuous Abdominal Pain</strong>: Sharp, constant uterine pain that doesn't let up between contractions (possible placental abruption).</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="emergency-card">
            <h4 style="color: #be123c; margin-top: 0;">👶 Fetal Movement Changes</h4>
            <ul>
                <li><strong>Decreased Movement (Third Trimester)</strong>: Noticeable reduction or cessation of baby kicks, rolls, or hiccups.</li>
                <li><strong>Kick Count Rule</strong>: Baby should complete at least 10 kicks or movements within a 2-hour window when resting quietly. If not reached, call triage immediately.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with rf_col2:
        st.markdown("""
        <div class="emergency-card">
            <h4 style="color: #be123c; margin-top: 0;">⚡ Preeclampsia Warning Signs</h4>
            <ul>
                <li><strong>Severe, Throbbing Headache</strong> that does not improve after drinking water and taking acetaminophen.</li>
                <li><strong>Visual Disturbances</strong>: Blurry vision, seeing floating spots, flashes of light, or sensitivity to light.</li>
                <li><strong>Sudden Severe Swelling</strong> in your face, hands, or around your eyes.</li>
                <li><strong>Right Upper Quadrant Pain</strong>: Sharp pain under your right ribs near your liver.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="emergency-card">
            <h4 style="color: #be123c; margin-top: 0;">🌡️ Infection & General Illness</h4>
            <ul>
                <li><strong>High Fever & Chills</strong>: Oral temperature of 100.4°F (38°C) or higher.</li>
                <li><strong>Severe Nausea / Inability to Hydrate</strong>: Inability to keep liquids down for 24+ hours.</li>
                <li><strong>Pain or Burning During Urination</strong> (possible UTI that can trigger preterm contractions).</li>
                <li><strong>Painful Calf Swelling / Redness</strong> (rule out Deep Vein Thrombosis).</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    st.success(
        "🌸 **Remember**: It is ALWAYS better to get checked and have everything turn out fine than to wait and wonder. "
        "Maternal healthcare teams love reassuring expectant mothers!"
    )
