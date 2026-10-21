"""
Jessica's Pregnancy & Childbirth Knowledge Base
Comprehensive clinical and practical guidance tailored for newly pregnant mothers.
"""

from typing import Dict, Any, List, Tuple
import re

# Emergency red flag keywords for instant safety response
RED_FLAG_PATTERNS = [
    r"heavy bleed", r"gush of blood", r"bright red blood",
    r"severe headach", r"vision blurry", r"seeing spots", r"flashing lights",
    r"severe cramp", r"severe abdominal pain", r"sharp stabbing pain",
    r"fever", r"chills", r"chest pain", r"shortness of breath",
    r"decreased movement", r"haven't felt baby", r"baby not moving",
    r"swelling in face", r"sudden swelling hands", r"seizure",
    r"fluid leaking", r"water broke early", r"water broke before 37"
]

TOPICS_KNOWLEDGE: List[Dict[str, Any]] = [
    {
        "id": "morning_sickness",
        "keywords": ["morning sickness", "nausea", "throwing up", "vomit", "sick in morning", "hyperemesis", "queasy"],
        "title": "Morning Sickness & Nausea Relief",
        "summary": "Morning sickness is very common in the first trimester due to surging hCG and estrogen levels. Despite the name, it can happen at any time of day.",
        "tips": [
            "**Eat small, frequent meals**: Don't let your stomach get completely empty, which worsens nausea.",
            "**Morning crackers**: Keep plain saltines or dry crackers on your bedside table and eat a few before sitting up.",
            "**Ginger power**: Real ginger tea, ginger candies, or ginger ale can soothe stomach spasms.",
            "**Vitamin B6 & Unisom**: Many OBs recommend Vitamin B6 (pyridoxine) combined with doxylamine (Unisom sleeptabs). Ask your doctor for proper dosage.",
            "**Cold & bland foods**: Cold foods tend to have less smell; try chilled watermelon, applesauce, yogurt, or smoothies.",
            "**Acupressure**: Sea-Bands (acupressure wristbands targeting the P6 pressure point) offer non-medicinal relief."
        ],
        "warning": "If you cannot keep liquids down for 24+ hours, lose more than 5% of your pre-pregnancy weight, or feel dizzy/faint, contact your OB/GYN immediately — you may need treatment for Hyperemesis Gravidarum (HG)."
    },
    {
        "id": "cramping_spotting",
        "keywords": ["cramp", "cramping", "spotting", "brown discharge", "pink discharge", "implantation", "light blood"],
        "title": "Early Cramping & Light Spotting",
        "summary": "Mild cramping and light spotting in early pregnancy are surprisingly common and frequently normal as your body undergoes massive changes.",
        "tips": [
            "**Implantation bleeding**: Around 10-14 days after conception, a light pink or brownish spotting can occur as the blastocyst embeds into the uterine wall.",
            "**Uterine stretching**: Mild menstrual-like aches are common as blood flow increases and the uterus starts growing.",
            "**Cervical sensitivity**: Pregnancy makes the cervix extra vascular. Light spotting after intercourse, a pap smear, or pelvic exam is common and usually harmless.",
            "**Rest & hydration**: Dehydration causes uterine irritability and mild cramps. Drink a tall glass of water and rest on your side."
        ],
        "warning": "Seek prompt medical care if spotting becomes bright red like a period, is accompanied by severe one-sided abdominal or shoulder pain (rule out ectopic pregnancy), or includes passing clots."
    },
    {
        "id": "first_trimester_fatigue",
        "keywords": ["tired", "exhausted", "fatigue", "sleepy", "low energy", "drained"],
        "title": "First Trimester Extreme Fatigue",
        "summary": "Feeling overwhelmingly exhausted during weeks 4 to 12 is completely normal! Your body is literally building an entirely new organ (the placenta) and your blood volume is expanding.",
        "tips": [
            "**Surging progesterone**: This hormone acts as a natural sedative. Honor what your body is asking for and take naps without guilt.",
            "**Listen to your body**: Lower your expectations for non-essential chores. Resting *is* productive right now.",
            "**Hydrate & check iron**: Dehydration and anemia (low iron) worsen fatigue. Drink 8-10 glasses of water daily and ensure your prenatal contains iron.",
            "**Gentle 15-minute walks**: Mild fresh-air movement can boost endorphins when you feel sluggish.",
            "**Good news**: Most moms experience a significant burst of energy when entering the second trimester around week 13-14!"
        ]
    },
    {
        "id": "foods_to_eat_and_avoid",
        "keywords": ["food", "diet", "eat", "avoid", "sushi", "caffeine", "coffee", "cheese", "deli meat", "fish", "mercury", "alcohol"],
        "title": "Pregnancy Nutrition & Foods to Avoid",
        "summary": "Good nutrition fuels your baby's development, but food safety is equally vital to prevent Listeria, Salmonella, and Toxoplasma.",
        "tips": [
            "**Foods to Avoid or Limit**:",
            "- ❌ **Raw/undercooked meats, sushi, & raw oysters**: High risk of bacterial contamination or parasites.",
            "- ❌ **Unpasteurized cheeses & milk**: Soft cheeses like brie, feta, or blue cheese must explicitly say 'Made with Pasteurized Milk'.",
            "- ❌ **Cold deli meats & hot dogs**: Reheat until steaming hot (165°F) to kill any potential Listeria.",
            "- ❌ **High-mercury fish**: Avoid shark, swordfish, king mackerel, and tilefish. Safe low-mercury fish include salmon, canned light tuna, shrimp, and tilapia (up to 2-3 servings/week).",
            "- ❌ **Alcohol & tobacco**: No safe amount has been established during pregnancy.",
            "- ⚠️ **Caffeine**: Keep under **200 mg/day** (roughly one 12 oz cup of brewed coffee).",
            "**Foods to Embrace**:",
            "- 🥑 **Avocados, nuts & seeds**: Healthy fats for baby's brain development.",
            "- 🥬 **Dark leafy greens**: Packed with folate, calcium, and iron.",
            "- 🍳 **Eggs**: Rich in choline, critical for baby's neural tube and cognitive growth.",
            "- 🥛 **Greek yogurt, fortified milk**: Essential for baby's bone and tooth buds."
        ]
    },
    {
        "id": "prenatal_vitamins",
        "keywords": ["vitamin", "prenatal", "folic acid", "folate", "iron", "dha", "supplements", "omega 3"],
        "title": "Prenatal Vitamins & Key Nutrients",
        "summary": "Prenatal vitamins fill nutritional gaps and are essential from pre-conception through breastfeeding.",
        "tips": [
            "**Folic Acid / Folate (at least 400 - 800 mcg daily)**: Prevents major neural tube defects like spina bifida. Critical in the first 28 days.",
            "**Iron (27 mg daily)**: Supports your expanding blood volume and prevents maternal anemia.",
            "**DHA / Omega-3 (200-300 mg daily)**: Essential for baby's brain and retinal eye development.",
            "**Calcium & Vitamin D (1,000 mg Calcium / 600 IU Vit D)**: Supports baby's skeletal development while protecting maternal bone density.",
            "**Stomach Tip**: If your prenatal pill makes you nauseous, take it at bedtime with a small snack, or switch to chewable/gummy vitamins (check if gummies have iron; you may need iron separately)."
        ]
    },
    {
        "id": "second_trimester_highlights",
        "keywords": ["second trimester", "trimester 2", "week 13", "week 14", "week 20", "anatomy scan", "quickening", "kicks", "gender ultrasound"],
        "title": "The Second Trimester (Weeks 13–27)",
        "summary": "Often called the 'Golden Trimester'! Energy rebounds, morning sickness usually fades, and you'll begin feeling those magical fluttery kicks.",
        "tips": [
            "**Anatomy Scan (18-22 Weeks)**: A detailed level-2 ultrasound examining baby's heart chambers, brain, spine, kidneys, and limbs. You can also find out the sex if desired!",
            "**Quickening (Baby Kicks)**: First movements feel like popping bubbles, light butterflies, or gas bubbles, usually felt between weeks 16-22 (often later if you have an anterior placenta).",
            "**Round Ligament Pain**: Sharp, jabbing twinges in your lower groin when coughing, standing quickly, or rolling over. Wearing a maternity belly band can help immensely.",
            "**Glucose Tolerance Test**: Typically performed between weeks 24-28 to screen for gestational diabetes."
        ]
    },
    {
        "id": "third_trimester_prep",
        "keywords": ["third trimester", "trimester 3", "week 28", "week 32", "week 36", "swollen feet", "back pain", "sleep position", "braxton hicks"],
        "title": "The Third Trimester (Weeks 28–40+)",
        "summary": "Baby is gaining fat, practicing breathing, and packing on weight. You are nearing the finish line!",
        "tips": [
            "**Safe Sleep Position**: Sleep on your side (preferably left) with a pillow between knees to maximize uterine blood flow and avoid compressing the inferior vena cava.",
            "**Braxton Hicks Contractions**: 'Practice contractions' that feel like painless or mild tightening across the belly. They are irregular, do not get closer together, and ease up with water and walking.",
            "**Kick Counting**: From week 28 onward, choose a quiet time daily. Baby should move 10 times within 2 hours. If movements slow down noticeably, call your labor triage.",
            "**Swollen Feet & Ankles**: Elevate your legs, stay hydrated, avoid tight socks, and wear compression stockings if standing for long periods."
        ]
    },
    {
        "id": "stages_of_labor",
        "keywords": ["labor", "stages of labor", "labor stage", "active labor", "latent labor", "transition", "pushing", "delivery", "placenta"],
        "title": "The 3 Stages of Childbirth & Labor",
        "summary": "Labor is a gradual physiological progression divided into three distinct stages.",
        "tips": [
            "**Stage 1: Cervical Dilation (0 to 10 cm)**:",
            "  - *Early / Latent Phase (0-5 cm)*: Contractions are mild to moderate, 5-20 min apart. Best spent relaxing at home, hydrating, and resting.",
            "  - *Active Phase (6-8 cm)*: Contractions become intense, 3-4 min apart lasting 60 seconds. Time to go to the birth center or hospital!",
            "  - *Transition Phase (8-10 cm)*: The most intense, rapid phase. Lasts 30-90 minutes with powerful contractions. Emotional shaking, hot flashes, or nausea are normal.",
            "**Stage 2: Pushing & Baby Delivery (10 cm to Birth)**:",
            "  - Mother pushes with uterine contractions. Can last from 20 minutes to a few hours for first-time moms.",
            "  - Baby crowns, head delivers, and baby is welcomed into the world!",
            "**Stage 3: Delivery of the Placenta**:",
            "  - Occurs 5 to 30 minutes after baby is born. Mild contractions gently detach the placenta."
        ]
    },
    {
        "id": "when_to_go_to_hospital",
        "keywords": ["when to go", "5-1-1", "511 rule", "hospital time", "contractions timing", "amniotic fluid", "water broke"],
        "title": "When to Go to the Hospital: The 5-1-1 Rule",
        "summary": "For a healthy, full-term first pregnancy, OBs and midwives standardly recommend following the **5-1-1 rule** before heading in.",
        "tips": [
            "**The 5-1-1 Rule Defined**:",
            "  - Contractions are **5 minutes apart** (from start of one to start of the next).",
            "  - Each contraction lasts **1 full minute** (60 seconds).",
            "  - This consistent pattern has continued for at least **1 full hour**.",
            "**Water Breaks (Rupture of Membranes)**: Note the **COAT**: Color, Odor, Amount, Time. Call your hospital even if you don't have contractions yet.",
            "**Bloody Show vs Heavy Bleeding**: A pink/brownish mucus plug discharge is normal; bright red heavy bleeding requires immediate evaluation.",
            "**Listen to Your Intuition**: If pain is unmanageable or something feels wrong, never hesitate to call your labor & delivery triage unit."
        ]
    },
    {
        "id": "pain_relief_and_epidural",
        "keywords": ["epidural", "pain relief", "pain management", "natural birth", "gas", "nitrous oxide", "hypnobirthing", "spinal"],
        "title": "Labor Pain Relief & Management Options",
        "summary": "Every birth is unique. You have the right to choose the pain relief strategy that aligns with your wishes and comfort.",
        "tips": [
            "**Medical Pain Relief**:",
            "  - **Epidural**: An anesthesiologist places a tiny catheter in the epidural space of your lower back, numbing from the waist down while keeping you awake and alert.",
            "  - **Nitrous Oxide ('Laughing Gas')**: Self-administered via mask during contractions to ease anxiety and take the edge off pain without motor impairment.",
            "  - **IV Narcotics**: Short-acting pain medications used during early-to-mid active labor to allow rest between contractions.",
            "**Non-Pharmacological Relief**:",
            "  - **Hydrotherapy**: Warm shower or labor tub (often called nature's epidural).",
            "  - **Movement & Birth Ball**: Pelvic rocking, swaying, sitting on birthing balls opens up the pelvic inlet.",
            "  - **Counter-pressure**: Partner or doula applying firm pressure to the sacrum relieves back labor.",
            "  - **Breathing & Hypnobirthing**: Deep belly breathing (in 4 counts, out 6 counts) calms the sympathetic nervous system."
        ]
    },
    {
        "id": "c_section",
        "keywords": ["c section", "c-section", "cesarean", "caesarean", "surgical birth", "c section recovery"],
        "title": "Cesarean Birth (C-Section) & Recovery",
        "summary": "Whether planned (e.g. breech presentation, placenta previa) or unplanned during labor, a C-section is a safe, valid, and miraculous way to bring your baby into the world.",
        "tips": [
            "**The Procedure**: Takes about 45 minutes total (baby arrives in the first 10-15 minutes). Regional anesthesia (spinal block) keeps you awake and pain-free.",
            "**Gentle / Family-Centered C-Section**: Ask for lowered drapes at birth, immediate skin-to-skin in the OR, and personal music.",
            "**Hospital Stay**: Typically 2-3 nights for monitoring and pain management.",
            "**Recovery Tips**:",
            "  - Wear high-waisted cotton underwear or disposable recovery undies that don't press on the incision.",
            "  - Hold a firm pillow against your abdomen when coughing, laughing, or standing.",
            "  - Take prescribed pain medication on schedule; don't wait for pain to spike.",
            "  - Avoid lifting anything heavier than baby for 6 weeks."
        ]
    },
    {
        "id": "hospital_bag_essentials",
        "keywords": ["hospital bag", "packing bag", "pack", "what to pack", "bag checklist", "labor bag"],
        "title": "Hospital Bag Checklist Essentials",
        "summary": "Pack your bag around week 34-36 so you are relaxed and prepared whenever baby decides to make their debut.",
        "tips": [
            "**For Mama**:",
            "  - ID, insurance card, birth plan copies, long phone charging cable (10 ft).",
            "  - Nursing bras (wireless), button-down pajama set, slip-on non-skid slippers, warm socks.",
            "  - Toiletries: Lip balm (hospital air is very dry!), dry shampoo, hair ties, travel body wash.",
            "  - Going-home outfit: Loose, comfortable maternity clothing (think soft joggers or maxi dress).",
            "**For Baby**:",
            "  - Properly installed infant car seat (required to leave hospital!).",
            "  - 2-3 sleepers/onesies (sizes NB and 0-3M), swaddle blanket, scratch mittens, hat.",
            "  - Pediatrician contact info.",
            "**For Partner / Support Person**:",
            "  - Snacks, refillable water bottle, change of clothes, camera, pillow & blanket from home."
        ]
    },
    {
        "id": "postpartum_and_fourth_trimester",
        "keywords": ["postpartum", "fourth trimester", "after birth", "lochia", "baby blues", "postpartum depression", "ppd", "breastfeeding", "recovery after birth"],
        "title": "The Fourth Trimester: Postpartum Recovery & Care",
        "summary": "The first 12 weeks after birth are as important for mother as they are for baby. Your body is undergoing rapid hormone shifts and healing.",
        "tips": [
            "**Lochia (Postpartum Bleeding)**: Normal vaginal discharge lasting 4-6 weeks, transitioning from bright red to pink-brown and finally yellowish-white.",
            "**Perineal Care**: Use a peri-bottle with warm water while urinating, witch hazel pads (Tucks), and cooling ice packs (padsicles).",
            "**Baby Blues vs Postpartum Depression (PPD)**:",
            "  - *Baby Blues*: Mild mood swings, crying spells, and anxiety during the first 10-14 days due to huge progesterone drops. Resolves on its own.",
            "  - *PPD / PPA*: Persistent sadness, inability to sleep when baby sleeps, panic attacks, or feelings of detachment lasting beyond 2 weeks. Very treatable with therapy and safe medications — never suffer in silence.",
            "**Rest is Medicine**: Follow the '5-5-5 Rule' if possible: 5 days in bed, 5 days on the bed, 5 days around the bed."
        ]
    },
    {
        "id": "safe_medications",
        "keywords": ["medicine", "medication", "tylenol", "advil", "ibuprofen", "headache", "cold", "allergy", "safe drugs"],
        "title": "Safe Over-the-Counter Medications in Pregnancy",
        "summary": "Always confirm with your specific prenatal provider before taking any new medication, especially in the first trimester.",
        "tips": [
            "**Pain & Fever**: **Acetaminophen (Tylenol)** is generally the safest first-line choice for headaches, body aches, and fever.",
            "❌ **Avoid NSAIDs (Ibuprofen, Advil, Aleve, Aspirin)**: Especially after 20 weeks, as they can cause premature closure of the fetal ductus arteriosus and reduce amniotic fluid.",
            "**Allergies & Colds**: Saline nasal sprays, Loratadine (Claritin), Cetirizine (Zyrtec), Diphenhydramine (Benadryl), plain Robitussin (Duaifenesin/Dextromethorphan).",
            "**Heartburn & Indigestion**: Calcium carbonate (Tums), Famotidine (Pepcid AC).",
            "**Constipation**: Docusate sodium (Colace), Metamucil, Miralax, prune juice."
        ]
    },
    {
        "id": "exercise_and_activities",
        "keywords": ["exercise", "workout", "gym", "yoga", "swimming", "running", "safe exercise", "lifting"],
        "title": "Safe Exercise & Fitness in Pregnancy",
        "summary": "Staying active promotes smoother labor, prevents excessive gestational weight gain, and elevates mood.",
        "tips": [
            "**Best Activities**: Walking, prenatal yoga, swimming (relieves joint pressure!), stationary cycling, and low-impact pilates.",
            "**Pelvic Floor & Kegels**: Practice both contracting *and* fully relaxing your pelvic floor muscles for birth.",
            "**The 'Talk Test'**: You should be able to carry on a conversation while exercising without gasping for breath.",
            "**Avoid**: Contact sports, hot yoga (avoid overheating baby), activities with a fall risk (horseback riding, skiing), and lying flat on your back after 20 weeks."
        ]
    }
]

# Quick FAQ suggestions to present on screen
FAQS = [
    "What foods should I avoid in pregnancy?",
    "How can I relieve severe morning sickness?",
    "Is light cramping or spotting normal?",
    "What are the 3 stages of labor?",
    "What is the 5-1-1 rule for going to the hospital?",
    "What should I pack in my hospital bag?",
    "Is Tylenol safe? What medications are okay?",
    "What are warning signs I should call my doctor for?"
]

def check_for_red_flags(query: str) -> bool:
    """Checks if the user's inquiry matches clinical urgent warning signs."""
    q = query.lower()
    for pattern in RED_FLAG_PATTERNS:
        if re.search(pattern, q):
            return True
    return False

def get_red_flag_response() -> str:
    """Returns an empathetic, urgent safety alert message."""
    return (
        "🚨 **IMPORTANT SAFETY NOTICE — PLEASE READ CAREFULLY** 🚨\n\n"
        "Mama, your symptoms mention something that requires **immediate medical evaluation** by a healthcare professional.\n\n"
        "**Please do NOT wait to see if it improves. Take these steps right away:**\n"
        "1. **Call your OB/GYN or Midwife's 24/7 on-call line**, or go directly to the nearest **Hospital Labor & Delivery Triage / Emergency Room**.\n"
        "2. If you are experiencing heavy bright-red bleeding, severe continuous abdominal/shoulder pain, sudden severe swelling in your hands or face with headache/vision changes, or haven't felt baby move in your third trimester, these are urgent signs.\n"
        "3. Have your partner or a loved one drive you so you can remain calm and seated.\n\n"
        "❤️ *Your care team is there 24 hours a day specifically to check on you and baby. Never feel bad or embarrassed about going in to be checked!*"
    )

def search_knowledge_base(query: str) -> Tuple[Dict[str, Any], int]:
    """Scores topics against user query and returns the best matching topic."""
    q = query.lower()
    best_match = None
    best_score = 0

    for topic in TOPICS_KNOWLEDGE:
        score = 0
        for kw in topic["keywords"]:
            if kw in q:
                score += len(kw.split()) * 3
        # Match topic title words
        for title_word in topic["title"].lower().split():
            if len(title_word) > 3 and title_word in q:
                score += 2

        if score > best_score:
            best_score = score
            best_match = topic

    return best_match, best_score

def format_topic_response(topic: Dict[str, Any], user_query: str) -> str:
    """Formats a warm, supportive response from Jessica using topic information."""
    intro_options = [
        f"Hi mama! I'm so glad you asked about **{topic['title']}**.",
        f"Congratulations on your pregnancy journey! Let's talk about **{topic['title']}**.",
        f"I hear you, mama! Here is what you need to know about **{topic['title']}**:"
    ]
    # Pick intro based on query length hash
    intro = intro_options[len(user_query) % len(intro_options)]

    response_lines = [
        f"{intro}\n",
        f"{topic['summary']}\n",
        "### Key Highlights & Advice:"
    ]

    for tip in topic["tips"]:
        response_lines.append(f"- {tip}")

    if "warning" in topic and topic["warning"]:
        response_lines.append(f"\n> ⚠️ **Doctor's Note**: {topic['warning']}")

    response_lines.append(
        "\n*Remember mama: Every pregnancy is wonderfully unique. Always run specific medical symptoms by your OB/GYN, midwife, or maternal health provider!*"
    )

    return "\n".join(response_lines)

def generate_jessica_response(user_query: str, chat_history: List[Dict[str, str]] = None) -> str:
    """Primary response handler incorporating empathy, topic matching, and greetings."""
    q = user_query.strip().lower()

    # 1. Immediate Red Flag Check
    if check_for_red_flags(q):
        return get_red_flag_response()

    # 2. Friendly Greetings
    greetings = ["hello", "hi", "hey", "good morning", "good evening", "how are you", "who are you"]
    if any(q.startswith(g) or q == g for g in greetings):
        return (
            "👋 **Hello beautiful mama-to-be!** I'm **Jessica**, your virtual pregnancy and childbirth companion.\n\n"
            "I'm here to support you with trustworthy information on:\n"
            "- 🌸 **First, Second & Third Trimester changes and symptoms**\n"
            "- 👶 **Baby's weekly development & kick counting**\n"
            "- 🥗 **Pregnancy nutrition, vitamins & safe medications**\n"
            "- 🏥 **Labor preparation, the 5-1-1 rule & pain management**\n"
            "- 🎒 **Hospital bag packing & postpartum recovery**\n\n"
            "How many weeks along are you, or what question is on your mind today?"
        )

    # 3. Thank you / Gratitude
    if any(thanks in q for thanks in ["thank you", "thanks", "helpful", "appreciate"]):
        return (
            "💖 You are so very welcome, mama! You are doing an incredible job carrying and caring for your little one. "
            "Please feel free to ask me anything else whenever you need a reassuring guide!"
        )

    # 4. Search Knowledge Base
    topic, score = search_knowledge_base(user_query)
    if topic and score >= 3:
        return format_topic_response(topic, user_query)

    # 5. Week-by-week calculation / inquiries
    week_match = re.search(r"(\d+)\s*(weeks?|wks?)", q)
    if week_match:
        week_num = int(week_match.group(1))
        return get_week_summary(week_num)

    # 6. Fallback empathetic response
    return (
        f"I hear you, mama! You asked: *\"{user_query}\"*\n\n"
        "While pregnancy brings so many new feelings and questions, here are some grounding principles to keep in mind:\n\n"
        "- 🩺 **Trust your instincts**: If something feels different or off, your prenatal care team is there to support you.\n"
        "- 💧 **Hydration & Rest**: Many common discomforts (headaches, mild cramps, braxton hicks) improve with two large glasses of water and resting on your left side.\n"
        "- 📋 **Note it down**: Keep a small notes list on your phone of questions to ask your doctor or midwife at your next prenatal appointment.\n\n"
        "💡 *Try asking me about specific topics like: **'morning sickness remedies'**, **'what foods to avoid'**, **'stages of labor'**, or **'hospital bag checklist'**!*"
    )

def get_week_summary(week: int) -> str:
    """Returns milestone information for a specific pregnancy week."""
    if week < 1 or week > 42:
        return f"A typical full-term pregnancy spans 40 weeks (divided into three trimesters). Did you mean a week between 1 and 42, mama?"

    fruit_sizes = {
        4: ("Poppy seed", "0.04 inches", "The blastocyst has burrowed into your uterine lining! Early placenta and amniotic sac are developing."),
        6: ("Sweet pea", "0.25 inches", "Baby's tiny heart tube is beating rapidly (around 105-120 bpm). Facial features and limb buds are forming."),
        8: ("Raspberry", "0.6 inches", "Tiny webbed fingers and toes are appearing! Neural pathways are expanding rapidly."),
        10: ("Prune", "1.2 inches", "Baby is officially graduating from embryo to fetus! Tiny tooth buds and vital organs are in place."),
        12: ("Plum", "2.1 inches", "Reflexes are developing (baby can curl toes and open fingers). You're finishing the first trimester!"),
        16: ("Avocado", "4.6 inches", "Baby's eyes can perceive light and their neck is getting stronger. You may start feeling faint flutters."),
        20: ("Banana", "10 inches", "Halfway there! Your 20-week anatomy scan takes place around now. Baby can hear your voice and heartbeat."),
        24: ("Ear of corn", "11.8 inches", "Viability milestone! Baby's lungs are developing surfactant branches and brain wave patterns show sleep-wake cycles."),
        28: ("Eggplant", "14.8 inches", "Welcome to the 3rd trimester! Baby's eyes can open and close, and they can blink."),
        32: ("Jicama / Squash", "16.7 inches", "Baby is practicing breathing movements and storing iron, calcium, and phosphorus."),
        36: ("Papaya", "18.7 inches", "Baby is shedding lanugo (fine hair) and dropping lower into the pelvis ('lightening'). Time to pack the hospital bag!"),
        40: ("Watermelon / Pumpkin", "20 inches", "Full term and ready to meet you! Baby is fully formed and waiting for the right moment to arrive.")
    }

    # Find closest week bracket
    keys = sorted(fruit_sizes.keys())
    closest_week = min(keys, key=lambda k: abs(k - week))
    fruit, length, description = fruit_sizes[closest_week]

    trimester = "First" if week <= 12 else ("Second" if week <= 27 else "Third")

    return (
        f"🌱 **Week {week} of Pregnancy ({trimester} Trimester)**\n\n"
        f"**Baby Size Comparison**: Roughly the size of a **{fruit}** (~{length})!\n\n"
        f"**What's Happening This Week**:\n{description}\n\n"
        "💡 *Tip for Mama*: Stay hydrated, take your daily prenatal vitamin, and take pictures of your growing belly bump!"
    )
