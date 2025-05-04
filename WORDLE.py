import streamlit as st
import hashlib
import random

# Large word list (5-letter words, uppercase, ~100 words; expandable to 1000+)
WORDS = [
    'ABOUT', 'ABOVE', 'ACTOR', 'ADULT', 'ALIVE', 'ALONE', 'ALONG', 'ALTER', 'AMONG', 'ANGEL',
    'ANGRY', 'APPLE', 'APPLY', 'ARROW', 'ASIDE', 'AUDIO', 'AWARD', 'AWARE', 'BASIC', 'BEACH',
    'BEGIN', 'BEING', 'BELLE', 'BIRTH', 'BLACK', 'BLADE', 'BLIND', 'BLOCK', 'BLOOD', 'BOARD',
    'BRAIN', 'BRAND', 'BREAD', 'BREAK', 'BRICK', 'BRIEF', 'BRING', 'BROAD', 'BROWN', 'BUILD',
    'BUNCH', 'BURST', 'CABLE', 'CALLS', 'CANDY', 'CARRY', 'CAUSE', 'CHAIN', 'CHAIR', 'CHART',
    'CHASE', 'CHEAP', 'CHECK', 'CHEST', 'CHIEF', 'CHILD', 'CHOSE', 'CIVIL', 'CLAIM', 'CLASS',
    'CLEAN', 'CLEAR', 'CLIMB', 'CLOCK', 'CLOSE', 'CLOUD', 'COACH', 'COAST', 'COLOR', 'COUNT',
    'COURT', 'COVER', 'CRAFT', 'CRANE', 'CRASH', 'CRAZY', 'CREAM', 'CRIME', 'CROWD', 'CROWN',
    'CURVE', 'CYCLE', 'DAILY', 'DANCE', 'DATED', 'DEATH', 'DELAY', 'DEPTH', 'DIARY', 'DIRTY',
    'DOUBT', 'DRAFT', 'DRAIN', 'DRAMA', 'DRAWN', 'DREAM', 'DRINK', 'DRIVE', 'EAGLE', 'EARLY',
    'EARTH', 'EIGHT', 'ELITE', 'EMPTY', 'ENEMY', 'ENJOY', 'ENTER', 'EQUAL', 'ERROR', 'EVENT',
    'EVERY', 'EXACT', 'EXIST', 'EXTRA', 'FAITH', 'FALSE', 'FANCY', 'FATAL', 'FEVER', 'FIELD',
    'FIGHT', 'FINAL', 'FIRST', 'FLAME', 'FLASH', 'FLOOR', 'FOCUS', 'FORCE', 'FORGE', 'FRAME',
    'FRESH', 'FRONT', 'FRUIT', 'FULLY', 'FUNNY', 'GIANT', 'GIVEN', 'GLASS', 'GLOVE', 'GOALS',
    'GRACE', 'GRADE', 'GRAIN', 'GRAND', 'GRAPE', 'GRASS', 'GREAT', 'GREEN', 'GROUP', 'GUARD',
    'GUESS', 'GUEST', 'GUIDE', 'HAPPY', 'HEART', 'HEAVY', 'HELLO', 'HONEY', 'HONOR', 'HOUSE',
    'HUMAN', 'HUMOR', 'IDEAL', 'IMAGE', 'INDEX', 'INNER', 'ISSUE', 'JOINT', 'JOKER', 'JUDGE',
    'JUICE', 'KNIFE', 'KNOCK', 'LABEL', 'LARGE', 'LAUGH', 'LAYER', 'LEARN', 'LEMON', 'LEVEL',
    'LIGHT', 'LIMIT', 'LIVES', 'LOCAL', 'LOGIC', 'LOOSE', 'LOWER', 'LUCKY', 'LUNCH', 'MAGIC',
    'MAJOR', 'MAKER', 'MARCH', 'MATCH', 'MAYBE', 'MEANS', 'MEDAL', 'METAL', 'METER', 'MIDST',
    'MIGHT', 'MINOR', 'MODEL', 'MONEY', 'MONTH', 'MOUSE', 'MOUTH', 'MOVIE', 'MUSIC', 'NIGHT',
    'NOISE', 'NORTH', 'NOVEL', 'NURSE', 'OCEAN', 'OFFER', 'OFTEN', 'ORDER', 'OTHER', 'OUTER',
    'OWNER', 'PAINT', 'PANEL', 'PAPER', 'PARTY', 'PATCH', 'PAUSE', 'PEACE', 'PHASE', 'PHONE',
    'PHOTO', 'PIECE', 'PILOT', 'PITCH', 'PLACE', 'PLAIN', 'PLANE', 'PLANT', 'PLATE', 'POINT',
    'POUND', 'POWER', 'PRESS', 'PRICE', 'PRIDE', 'PRIME', 'PRINT', 'PRIOR', 'PRIZE', 'PROOF',
    'PROUD', 'QUICK', 'QUIET', 'RADIO', 'RAISE', 'RANGE', 'RAPID', 'RATIO', 'REACH', 'REACT',
    'READY', 'REALM', 'REBEL', 'REFER', 'REIGN', 'RELAX', 'REPLY', 'RIDER', 'RIFLE', 'RIGHT',
    'RIVAL', 'RIVER', 'ROBOT', 'ROCKY', 'ROUND', 'ROUTE', 'ROYAL', 'RURAL', 'SAINT', 'SALAD',
    'SALES', 'SCALE', 'SCENE', 'SCORE', 'SEATS', 'SENSE', 'SERVE', 'SEVEN', 'SHADE', 'SHAKE',
    'SHAPE', 'SHARE', 'SHARP', 'SHELF', 'SHELL', 'SHINE', 'SHIRT', 'SHOCK', 'SHOOT', 'SHORT',
    'SHOWN', 'SIGHT', 'SINCE', 'SIXTH', 'SKILL', 'SLEEP', 'SLIDE', 'SMALL', 'SMART', 'SMILE',
    'SMOKE', 'SNAKE', 'SOLID', 'SOLVE', 'SORRY', 'SOUND', 'SOUTH', 'SPACE', 'SPARE', 'SPEAK',
    'SPEED', 'SPEND', 'SPICE', 'SPILL', 'SPIRIT', 'SPLIT', 'SPORT', 'SQUAD', 'STAGE', 'STAIR',
    'STAKE', 'STAND', 'START', 'STATE', 'STEAM', 'STEEL', 'STICK', 'STILL', 'STOCK', 'STONE',
    'STORE', 'STORM', 'STORY', 'STRIP', 'STUDY', 'STUFF', 'STYLE', 'SUGAR', 'SUITE', 'SUPER',
    'SWEET', 'SWING', 'TABLE', 'TASTE', 'TEACH', 'TEAMS', 'TENTH', 'TERMS', 'TESTS', 'THANK',
    'THEME', 'THICK', 'THING', 'THINK', 'THIRD', 'THROW', 'TIGHT', 'TIMES', 'TITLE', 'TODAY',
    'TOKEN', 'TOPIC', 'TOTAL', 'TOUCH', 'TOUGH', 'TOWER', 'TRACE', 'TRACK', 'TRADE', 'TRAIL',
    'TRAIN', 'TREAT', 'TREND', 'TRIAL', 'TRIBE', 'TRICK', 'TROOP', 'TRUCK', 'TRULY', 'TRUST',
    'TRUTH', 'TUTOR', 'TWICE', 'TWIST', 'UNCLE', 'UNDER', 'UNION', 'UNITE', 'UNTIL', 'UPPER',
    'UPSET', 'URBAN', 'USAGE', 'USUAL', 'VALID', 'VALUE', 'VIDEO', 'VIRUS', 'VISIT', 'VITAL',
    'VOICE', 'VOTER', 'WAGON', 'WAIST', 'WASTE', 'WATCH', 'WATER', 'WHEEL', 'WHERE', 'WHICH',
    'WHILE', 'WHITE', 'WHOLE', 'WHOSE', 'WIDEN', 'WIDTH', 'WOMAN', 'WORLD', 'WORRY', 'WORST',
    'WORTH', 'WOULD', 'WOUND', 'WRITE', 'WRONG', 'YIELD', 'YOUNG', 'YOUTH'
]

# Game logic
def check_guess(guess, target):
    result = []
    target_letters = list(target)
    guess = guess.upper()
    for i, (g, t) in enumerate(zip(guess, target)):
        if g == t:
            result.append('green')
            target_letters[i] = None
        elif g in target_letters:
            result.append('yellow')
            target_letters[target_letters.index(g)] = None
        else:
            result.append('gray')
    return result

# Hint system
def get_hint(guesses):
    if not guesses:
        return 'CRANE'  # Common starting word for large list
    if guesses and guesses[0].upper() == 'APPLE':
        # Suggest words with frequent letters after APPLE
        strategy = ['HOUSE', 'TRAIN', 'SMILE', 'RIVER', 'SNAKE']
        for word in strategy:
            if word not in guesses and word in WORDS:
                return word
    # Fallback: Suggest a random word not yet guessed
    available = [w for w in WORDS if w not in guesses]
    return random.choice(available) if available else None

# Authentication functions
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def add_user(username, name, password):
    username = username.lower()  # Case-insensitive usernames
    if username in st.session_state['users']:
        return False
    st.session_state['users'][username] = {
        'name': name,
        'password': hash_password(password)
    }
    return True

def verify_user(username, password):
    username = username.lower()
    if username in st.session_state['users']:
        return st.session_state['users'][username]['password'] == hash_password(password)
    return False

# User stats
def calculate_stats(username):
    if username not in st.session_state['user_history'] or not st.session_state['user_history'][username]:
        return {
            'games_played': 0,
            'wins': 0,
            'win_rate': 0,
            'current_streak': 0,
            'max_streak': 0,
            'avg_attempts': 0
        }
    
    history = st.session_state['user_history'][username]
    games_played = len(history)
    wins = sum(1 for game in history if game['won'])
    win_rate = round(wins / games_played * 100, 1)
    
    # Calculate streaks
    current_streak = 0
    max_streak = 0
    temp_streak = 0
    
    for game in reversed(history):
        if game['won']:
            temp_streak += 1
            current_streak = temp_streak
        else:
            temp_streak = 0
        max_streak = max(max_streak, temp_streak)
    
    # Average attempts for wins
    won_games = [game for game in history if game['won']]
    avg_attempts = round(sum(len(game['guesses']) for game in won_games) / len(won_games), 1) if won_games else 0
    
    return {
        'games_played': games_played,
        'wins': wins,
        'win_rate': win_rate,
        'current_streak': current_streak,
        'max_streak': max_streak,
        'avg_attempts': avg_attempts
    }

# Build keyboard with colored keys based on guesses
def build_keyboard(guesses, target_word):
    keyboard = [
        ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P'],
        ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L'],
        ['Z', 'X', 'C', 'V', 'B', 'N', 'M']
    ]
    
    letter_status = {}
    
    for guess in guesses:
        result = check_guess(guess, target_word)
        for i, letter in enumerate(guess):
            if letter not in letter_status:
                letter_status[letter] = result[i]
            elif result[i] == 'green':
                letter_status[letter] = 'green'
            elif result[i] == 'yellow' and letter_status[letter] != 'green':
                letter_status[letter] = 'yellow'
    
    keyboard_html = '<div class="keyboard-container">'
    
    for row in keyboard:
        keyboard_html += '<div class="keyboard-row">'
        for key in row:
            key_color = ''
            if key in letter_status:
                key_color = letter_status[key]
            keyboard_html += f'<div class="keyboard-key {key_color}">{key}</div>'
        keyboard_html += '</div>'
    
    keyboard_html += '</div>'
    return keyboard_html

# Streamlit app
def main():
    # Set page config
    st.set_page_config(
        page_title="Wordle Game",
        page_icon="🎮",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # Add modern CSS styles
    st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;700&family=Poppins:wght@400;600;700&display=swap" rel="stylesheet">
    <style>
        /* Global styles */
        * {
            font-family: 'Roboto', sans-serif;
        }
        h1, h2, h3, h4, h5, h6 {
            font-family: 'Poppins', sans-serif;
        }
        .main-header {
            background: linear-gradient(135deg, #6366F1 0%, #8B5CF6 100%);
            color: white;
            padding: 2rem;
            border-radius: 1rem;
            margin-bottom: 2rem;
            text-align: center;
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
        }
        .stApp {
            background-color: #F9FAFB;
        }
        
        /* Game board styles */
        .game-container {
            max-width: 600px;
            margin: auto;
            background-color: white;
            border-radius: 1rem;
            padding: 2rem;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        }
        .letter-box {
            width: 62px;
            height: 62px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 2rem;
            font-weight: bold;
            border: 2px solid #d1d5db;
            margin: 4px;
            text-transform: uppercase;
            border-radius: 12px;
            transition: all 0.3s ease;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }
        .letter-box.filled {
            border-color: #9CA3AF;
            transform: scale(1.02);
        }
        .green { 
            background-color: #10B981; 
            color: white; 
            border-color: #10B981;
            animation: flip 0.5s ease forwards;
        }
        .yellow { 
            background-color: #F59E0B; 
            color: white; 
            border-color: #F59E0B;
            animation: flip 0.5s ease forwards;
        }
        .gray { 
            background-color: #6B7280; 
            color: white; 
            border-color: #6B7280;
            animation: flip 0.5s ease forwards;
        }
        @keyframes flip {
            0% { transform: rotateX(0); }
            50% { transform: rotateX(90deg); }
            100% { transform: rotateX(0); }
        }
        
        /* Form styles */
        .guess-form {
            background-color: white;
            padding: 1.5rem;
            border-radius: 1rem;
            margin-top: 1.5rem;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        }
        .input-field {
            text-transform: uppercase;
            font-size: 1.2rem;
            padding: 0.75rem 1rem;
            border-radius: 0.5rem;
            border: 2px solid #d1d5db;
            width: 100%;
            max-width: 300px;
            outline: none;
            transition: border-color 0.3s ease;
        }
        .input-field:focus {
            border-color: #6366F1;
        }
        
        /* Stats and history styles */
        .stats-container {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
            gap: 1rem;
            margin-top: 1.5rem;
        }
        .stat-card {
            background-color: white;
            padding: 1rem;
            border-radius: 0.5rem;
            text-align: center;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
        }
        .stat-value {
            font-size: 1.8rem;
            font-weight: bold;
            color: #4F46E5;
        }
        .stat-label {
            font-size: 0.875rem;
            color: #6B7280;
        }
        .history-container {
            background-color: white;
            padding: 1.5rem;
            border-radius: 1rem;
            margin-top: 1.5rem;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        }
        .history-item {
            padding: 0.75rem;
            border-radius: 0.5rem;
            margin-bottom: 0.75rem;
            background-color: #F3F4F6;
        }
        .history-item:hover {
            background-color: #E5E7EB;
        }
        .history-header {
            font-weight: bold;
            margin-bottom: 0.5rem;
        }
        .history-detail {
            margin-left: 1rem;
            font-size: 0.875rem;
            color: #4B5563;
        }
        
        /* Keyboard styles */
        .keyboard-container {
            margin-top: 2rem;
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 0.35rem;
        }
        .keyboard-row {
            display: flex;
            gap: 0.35rem;
        }
        .keyboard-key {
            width: 36px;
            height: 48px;
            display: flex;
            align-items: center;
            justify-content: center;
            background-color: #E5E7EB;
            border-radius: 0.375rem;
            font-weight: bold;
            cursor: pointer;
            user-select: none;
        }
        .keyboard-key.green {
            background-color: #10B981;
            color: white;
        }
        .keyboard-key.yellow {
            background-color: #F59E0B;
            color: white;
        }
        .keyboard-key.gray {
            background-color: #6B7280;
            color: white;
        }
        
        /* Sidebar styles */
        .sidebar-content {
            background-color: white;
            padding: 1.5rem;
            border-radius: 1rem;
            margin-bottom: 1rem;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        }
        .sidebar-header {
            font-size: 1.5rem;
            font-weight: bold;
            margin-bottom: 1rem;
            color: #4F46E5;
        }
        .sidebar .stButton>button {
            width: 100%;
            border-radius: 0.5rem;
            font-weight: bold;
            padding: 0.5rem 1rem;
            transition: all 0.3s ease;
        }
        .sidebar .stButton>button:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        }
        
        /* Game info styles */
        .game-info {
            background-color: white;
            padding: 1rem;
            border-radius: 0.5rem;
            margin-top: 1rem;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
        }
        .info-heading {
            font-weight: bold;
            margin-bottom: 0.5rem;
            color: #4F46E5;
        }
        
        /* Modal styles */
        .modal {
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background-color: white;
            padding: 2rem;
            border-radius: 1rem;
            z-index: 1000;
            box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
            text-align: center;
            max-width: 90%;
            width: 400px;
        }
        .modal-overlay {
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background-color: rgba(0, 0, 0, 0.5);
            z-index: 999;
        }
        .modal-title {
            font-size: 1.5rem;
            font-weight: bold;
            margin-bottom: 1rem;
        }
        .modal-content {
            margin-bottom: 1.5rem;
        }
        .modal-button {
            background-color: #4F46E5;
            color: white;
            padding: 0.75rem 1.5rem;
            border-radius: 0.5rem;
            border: none;
            font-weight: bold;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        .modal-button:hover {
            background-color: #4338CA;
            transform: translateY(-2px);
        }
        
        /* Responsive styles */
        @media (max-width: 768px) {
            .letter-box {
                width: 52px;
                height: 52px;
                font-size: 1.75rem;
                margin: 3px;
            }
            .keyboard-key {
                width: 28px;
                height: 40px;
                font-size: 0.875rem;
            }
            .stats-container {
                grid-template-columns: repeat(2, 1fr);
            }
        }
        @media (max-width: 640px) {
            .letter-box {
                width: 45px;
                height: 45px;
                font-size: 1.5rem;
                margin: 2px;
            }
            .keyboard-key {
                width: 24px;
                height: 36px;
                font-size: 0.75rem;
            }
        }
    </style>
    """, unsafe_allow_html=True)

    # Initialize session state
    if 'users' not in st.session_state:
        st.session_state['users'] = {}
    if 'user_history' not in st.session_state:
        st.session_state['user_history'] = {}
    if 'authentication_status' not in st.session_state:
        st.session_state['authentication_status'] = False
    if 'username' not in st.session_state:
        st.session_state['username'] = None
    if 'name' not in st.session_state:
        st.session_state['name'] = None
    if 'show_rules' not in st.session_state:
        st.session_state['show_rules'] = False

    # Sidebar for login/signup
    with st.sidebar:
        st.markdown('<div class="sidebar-content">', unsafe_allow_html=True)
        st.markdown('<div class="sidebar-header">🎮 Wordle Game</div>', unsafe_allow_html=True)
        
        if not st.session_state['authentication_status']:
            tab1, tab2 = st.tabs(["Login", "Sign Up"])
            
            with tab1:
                with st.form("login_form"):
                    username = st.text_input('Username', key='login_username')
                    password = st.text_input('Password', type='password', key='login_password')
                    login_submitted = st.form_submit_button('Login', use_container_width=True)
                    
                    if login_submitted:
                        if username and password:
                            if verify_user(username, password):
                                st.session_state['authentication_status'] = True
                                st.session_state['username'] = username.lower()
                                st.session_state['name'] = st.session_state['users'][username.lower()]['name']
                                if username.lower() not in st.session_state['user_history']:
                                    st.session_state['user_history'][username.lower()] = []
                                st.success(f'Welcome back, {st.session_state["name"]}!')
                                st.rerun()
                            else:
                                st.error('Incorrect username or password')
                        else:
                            st.error('Please enter both username and password')
            
            with tab2:
                with st.form("signup_form"):
                    new_username = st.text_input('Username', key='signup_username')
                    new_name = st.text_input('Full Name', key='signup_name')
                    new_password = st.text_input('Password', type='password', key='signup_password')
                    confirm_password = st.text_input('Confirm Password', type='password', key='confirm_password')
                    signup_submitted = st.form_submit_button('Sign Up', use_container_width=True)
                    
                    if signup_submitted:
                        if new_username and new_name and new_password:
                            if new_password != confirm_password:
                                st.error('Passwords do not match')
                            elif len(new_password) < 6:
                                st.error('Password must be at least 6 characters')
                            else:
                                if add_user(new_username, new_name, new_password):
                                    st.session_state['user_history'][new_username.lower()] = []
                                    st.success('Account created! You can now login.')
                                else:
                                    st.error('Username already exists')
                        else:
                            st.error('Please fill all fields')
        else:
            # User is logged in
            st.markdown(f'<div style="text-align: center; margin-bottom: 1rem;">👤 <b>{st.session_state["name"]}</b></div>', unsafe_allow_html=True)
            
            if st.button('Rules', use_container_width=True):
                st.session_state['show_rules'] = not st.session_state['show_rules']
            
            if st.button('Logout', use_container_width=True):
                st.session_state['authentication_status'] = False
                st.session_state['username'] = None
                st.session_state['name'] = None
                st.session_state.pop('game_state', None)
                st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Game rules
        if st.session_state['show_rules']:
            st.markdown('<div class="sidebar-content">', unsafe_allow_html=True)
            st.markdown('<div class="sidebar-header">How to Play</div>', unsafe_allow_html=True)
            st.markdown("""
            1. Guess the WORDLE in 6 tries.
            2. Each guess must be a valid 5-letter word.
            3. After each guess, the color of the tiles will change:
               - 🟩 **Green**: The letter is correct and in the right position.
               - 🟨 **Yellow**: The letter is in the word but in the wrong position.
               - ⬛ **Gray**: The letter is not in the word.
            4. The same letter can appear multiple times in a word.
            5. All words are in English.
            """)
            st.markdown('</div>', unsafe_allow_html=True)

    # Main content
    if not st.session_state['authentication_status']:
        # Welcome screen for non-authenticated users
        st.markdown("""
        <div class="main-header">
            <h1 style="font-size: 3rem; margin-bottom: 1rem;">🎮 WORDLE</h1>
            <p style="font-size: 1.2rem; opacity: 0.9;">The addictive word-guessing game</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Grid of feature cards
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div style="background-color: white; padding: 1.5rem; border-radius: 1rem; height: 100%; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);">
                <h3 style="color: #4F46E5; font-size: 1.5rem; margin-bottom: 1rem;">🧩 How to Play</h3>
                <p>Guess the hidden five-letter word in six attempts. After each guess, the color of the tiles will indicate how close you are.</p>
                <ul style="margin-top: 1rem;">
                    <li style="margin-bottom: 0.5rem;">🟩 <strong>Green</strong>: Letter is correct and in the right position</li>
                    <li style="margin-bottom: 0.5rem;">🟨 <strong>Yellow</strong>: Letter is in the word but in wrong position</li>
                    <li style="margin-bottom: 0.5rem;">⬜ <strong>Gray</strong>: Letter is not in the word</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div style="background-color: white; padding: 1.5rem; border-radius: 1rem; height: 100%; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);">
                <h3 style="color: #4F46E5; font-size: 1.5rem; margin-bottom: 1rem;">✨ Features</h3>
                <ul style="margin-top: 0;">
                    <li style="margin-bottom: 0.5rem;">🎯 <strong>Daily Challenge</strong>: New word every day</li>
                    <li style="margin-bottom: 0.5rem;">📊 <strong>Stats Tracking</strong>: Monitor your progress</li>
                    <li style="margin-bottom: 0.5rem;">💡 <strong>Hints</strong>: Get help when stuck</li>
                    <li style="margin-bottom: 0.5rem;">🔄 <strong>Game History</strong>: Review your past games</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        # Footer with login prompt
        st.markdown("""
        <div style="text-align: center; margin-top: 2rem; padding: 1rem; background-color: white; border-radius: 1rem; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);">
            <p style="font-size: 1.2rem; font-weight: bold; color: #4F46E5;">Ready to play?</p>
            <p>Login or sign up using the sidebar to start your Wordle journey!</p>
        </div>
        """, unsafe_allow_html=True)
        
        return

    # Initialize game state for authenticated users
    if 'game_state' not in st.session_state:
        st.session_state['game_state'] = {
            'target_word': random.choice(WORDS),
            'guesses': [],
            'attempts': 0,
            'game_over': False,
            'won': False
        }

    # Game interface
    game_state = st.session_state['game_state']
    username = st.session_state['username']
    
    # Main game header
    st.markdown("""
    <div class="main-header">
        <h1 style="font-size: 2.5rem; margin-bottom: 0.5rem;">🎮 WORDLE</h1>
        <p style="font-size: 1.1rem; opacity: 0.9;">Guess the 5-letter word in six tries</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Game layout
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Game board container
        st.markdown('<div class="game-container">', unsafe_allow_html=True)
        
        # Game board
        for i in range(6):
            cols = st.columns(5)
            guess = game_state['guesses'][i] if i < len(game_state['guesses']) else ''
            colors = check_guess(guess, game_state['target_word']) if i < len(game_state['guesses']) else []
            
            for j in range(5):
                with cols[j]:
                    letter = guess[j] if j < len(guess) else ''
                    color_class = colors[j] if j < len(colors) else ''
                    filled_class = 'filled' if letter else ''
                    st.markdown(f'<div class="letter-box {color_class} {filled_class}">{letter}</div>', unsafe_allow_html=True)
        
        # Virtual keyboard
        if not game_state['game_over']:
            st.markdown(build_keyboard(game_state['guesses'], game_state['target_word']), unsafe_allow_html=True)
        
        # Guess input form
        if not game_state['game_over']:
            st.markdown('<div class="guess-form">', unsafe_allow_html=True)
            with st.form(key='guess_form', clear_on_submit=True):
                col1, col2 = st.columns([3, 1])
                with col1:
                    guess = st.text_input('Enter your guess:', 
                                         max_chars=5, 
                                         key='guess_input',
                                         help='Type a 5-letter word and press Submit').upper()
                with col2:
                    submit = st.form_submit_button('Submit', use_container_width=True)
                
                hint_col, spacer_col = st.columns([1, 3])
                with hint_col:
                    hint_button = st.form_submit_button('Get Hint', use_container_width=True)
                
                if submit and guess:
                    if len(guess) != 5:
                        st.error('Please enter a 5-letter word')
                    elif guess.upper() not in WORDS:
                        st.error('Not a valid word in our dictionary')
                    elif guess.upper() in game_state['guesses']:
                        st.error('You already guessed this word')
                    else:
                        game_state['guesses'].append(guess.upper())
                        game_state['attempts'] += 1
                        
                        if guess.upper() == game_state['target_word']:
                            game_state['game_over'] = True
                            game_state['won'] = True
                            st.session_state['user_history'][username].append({
                                'game_id': len(st.session_state['user_history'][username]) + 1,
                                'target_word': game_state['target_word'],
                                'guesses': game_state['guesses'].copy(),
                                'won': True
                            })
                            # Success will be shown after rerun
                        elif game_state['attempts'] >= 6:
                            game_state['game_over'] = True
                            st.session_state['user_history'][username].append({
                                'game_id': len(st.session_state['user_history'][username]) + 1,
                                'target_word': game_state['target_word'],
                                'guesses': game_state['guesses'].copy(),
                                'won': False
                            })
                            # Error will be shown after rerun
                        
                        st.session_state['game_state'] = game_state
                        st.rerun()
                
                if hint_button:
                    hint_word = get_hint(game_state['guesses'])
                    if hint_word:
                        st.info(f'💡 Hint: Try guessing "{hint_word}"')
                    else:
                        st.warning('No more hints available')
            st.markdown('</div>', unsafe_allow_html=True)
        
        # New game button (shows when game is over)
        if game_state['game_over']:
            # Show game result
            if game_state['won']:
                attempts = len(game_state['guesses'])
                st.markdown(f"""
                <div style="background-color: #10B981; color: white; padding: 1rem; border-radius: 0.5rem; margin: 1rem 0; text-align: center;">
                    <h3 style="margin-bottom: 0.5rem;">🎉 Congratulations!</h3>
                    <p>You guessed <strong>{game_state['target_word']}</strong> in {attempts} {attempts == 1 and 'try' or 'tries'}!</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div style="background-color: #EF4444; color: white; padding: 1rem; border-radius: 0.5rem; margin: 1rem 0; text-align: center;">
                    <h3 style="margin-bottom: 0.5rem;">Game Over</h3>
                    <p>The word was <strong>{game_state['target_word']}</strong></p>
                </div>
                """, unsafe_allow_html=True)
                
            if st.button('Start New Game', type='primary', use_container_width=True):
                st.session_state['game_state'] = {
                    'target_word': random.choice(WORDS),
                    'guesses': [],
                    'attempts': 0,
                    'game_over': False,
                    'won': False
                }
                st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)

    # Right sidebar with stats and history
    with col2:
        # Player stats
        stats = calculate_stats(username)
        st.markdown('<div style="background-color: white; padding: 1.5rem; border-radius: 1rem; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);">', unsafe_allow_html=True)
        st.markdown('<h3 style="font-size: 1.25rem; margin-bottom: 1rem; color: #4F46E5;">📊 Your Stats</h3>', unsafe_allow_html=True)
        
        st.markdown('<div class="stats-container">', unsafe_allow_html=True)
        
        # Stat cards
        stat_items = [
            {"label": "Games", "value": stats['games_played']},
            {"label": "Win %", "value": f"{stats['win_rate']}%"},
            {"label": "Streak", "value": stats['current_streak']},
            {"label": "Max Streak", "value": stats['max_streak']}
        ]
        
        for item in stat_items:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-value">{item['value']}</div>
                <div class="stat-label">{item['label']}</div>
            </div>
            """, unsafe_allow_html=True)
            
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Game History
        if username in st.session_state['user_history'] and st.session_state['user_history'][username]:
            st.markdown('<div class="history-container">', unsafe_allow_html=True)
            st.markdown('<h3 style="font-size: 1.25rem; margin-bottom: 1rem; color: #4F46E5;">🕰️ Game History</h3>', unsafe_allow_html=True)
            
            # Show last 5 games
            recent_games = st.session_state['user_history'][username][-5:]
            
            for game in reversed(recent_games):
                outcome = "Won ✅" if game['won'] else "Lost ❌"
                attempts = len(game['guesses'])
                
                st.markdown(f"""
                <div class="history-item">
                    <div class="history-header">Game {game["game_id"]}: {outcome}</div>
                    <div class="history-detail">Word: <strong>{game["target_word"]}</strong></div>
                    <div class="history-detail">Attempts: {attempts}/6</div>
                </div>
                """, unsafe_allow_html=True)
                
            if len(st.session_state['user_history'][username]) > 5:
                st.markdown('<div style="text-align: center; margin-top: 1rem; font-size: 0.875rem; color: #6B7280;">Showing 5 most recent games</div>', unsafe_allow_html=True)
                
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="background-color: white; padding: 1.5rem; border-radius: 1rem; margin-top: 1.5rem; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1); text-align: center;">
                <h3 style="font-size: 1.25rem; margin-bottom: 1rem; color: #4F46E5;">🕰️ Game History</h3>
                <p style="color: #6B7280;">No games played yet. Start playing to build your history!</p>
            </div>
            """, unsafe_allow_html=True)

if __name__ == '__main__':
    main()
