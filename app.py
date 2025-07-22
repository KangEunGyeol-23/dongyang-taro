import streamlit as st
import random
import os
import pandas as pd
from PIL import Image

# --- 설정 ---
ADMIN_IDS = ["cotty23"]
USER_IDS = ["cotty00", "teleecho", "37nim", "ckss12"]

CARD_FOLDER = "cards" # 'cards' 폴더가 현재 스크립트와 같은 경로에 있는지 확인하세요.
CARD_DATA_FILE = "card_data.csv" # 'card_data.csv' 파일이 현재 스크립트와 같은 경로에 있는지 확인하세요.

# --- 함수 정의 ---

# 카드 데이터 불러오기
def load_card_data():
    if os.path.exists(CARD_DATA_FILE):
        return pd.read_csv(CARD_DATA_FILE)
    else:
        # 파일이 없을 경우, 컬럼 정의를 명확히 하여 빈 DataFrame 생성
        return pd.DataFrame(columns=["filename", "upright", "reversed"])

# 카드 데이터 저장하기 (현재 코드에서는 사용되지 않지만, 관리자 기능 등을 위해 유지)
def save_card_data(df):
    df.to_csv(CARD_DATA_FILE, index=False)

# 카드 뽑기 함수 (중복 제외)
def draw_cards(n=1, exclude=None):
    if not os.path.exists(CARD_FOLDER):
        st.error(f"'{CARD_FOLDER}' 폴더를 찾을 수 없습니다. 카드 이미지를 넣어주세요.")
        return []

    files = [f for f in os.listdir(CARD_FOLDER) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]
    
    if exclude:
        files = [f for f in files if f not in exclude]
    
    # files 리스트가 비어있을 경우 에러 방지
    if not files:
        st.warning("카드 폴더에 이미지가 없거나, 모든 카드가 이미 뽑혔습니다.")
        return []
        
    # 뽑아야 할 카드 수가 남은 카드 수보다 많을 경우를 대비
    num_to_draw = min(n, len(files))
    selected = random.sample(files, num_to_draw)
    cards = [(file, random.choice(["정방향", "역방향"])) for file in selected]
    return cards

# 카드 해석 가져오기
def get_card_meaning(df, filename, direction):
    row = df[df["filename"] == filename]
    if not row.empty:
        if direction == "정방향":
            return row.iloc[0]["upright"]
        else:
            return row.iloc[0]["reversed"]
    return "**[해석 없음]** 이 카드의 해석이 등록되지 않았습니다."

# 카드 이미지 표시
def show_card(file, direction, width=150): # 카드 폭을 약간 줄여서 가로 배열 시 공간 확보
    img_path = os.path.join(CARD_FOLDER, file)
    try:
        img = Image.open(img_path)
        if direction == "역방향":
            img = img.rotate(180)
        st.image(img, width=width, use_column_width=False) # use_column_width=False로 고정 폭 유지
        st.caption(f"{direction}") # 정방향/역방향 표시 추가
    except FileNotFoundError:
        st.error(f"이미지를 찾을 수 없습니다: {file}")
    except Exception as e:
        st.error(f"이미지 로드 중 오류 발생: {e}")

# --- 세션 상태 초기화 ---
# 앱이 시작될 때 단 한 번만 실행되도록
if "subcards" not in st.session_state:
    st.session_state.subcards = {}
if "subcard_used" not in st.session_state:
    st.session_state.subcard_used = {}
if "question" not in st.session_state:
    st.session_state.question = ""
if "q1" not in st.session_state:
    st.session_state.q1 = ""
if "q2" not in st.session_state:
    st.session_state.q2 = ""
if "login" not in st.session_state:
    st.session_state.login = ""
if "cards_result" not in st.session_state: # 카드 뽑기 결과 저장용 (3카드, 원카드, 조언카드)
    st.session_state.cards_result = []
if "choice_cards_result" not in st.session_state: # 양자택일 결과 저장용
    st.session_state.choice_cards_result = []
if "current_mode" not in st.session_state: # 현재 선택된 모드 저장용
    st.session_state.current_mode = "3카드 보기" # 초기 모드 설정

# --- 로그인 로직 ---
if not st.session_state.login:
    st.set_page_config(page_title="동양타로", layout="centered")
    st.title("🌓 동양타로")
    st.markdown("""
    "오늘, 당신의 운명에 귀 기울이세요."

    동양의 오랜 지혜가 담긴 타로가 당신의 삶에 깊은 통찰과 명쾌한 해답을 선사합니다.

    사랑, 직업, 재물 등 모든 고민에 대한 당신만의 길을 지금 바로 동양 타로에서 찾아보세요.

    숨겨진 운명의 실타래를 풀어내고, 더 나은 내일을 위한 지혜를 얻을 시간입니다.
    """)
    input_
