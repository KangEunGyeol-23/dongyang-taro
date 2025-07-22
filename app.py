import streamlit as st
import random
import os
import pandas as pd
from PIL import Image

# --- 설정 ---
ADMIN_IDS = ["cotty23"]
USER_IDS = ["cotty00", "teleecho", "37nim", "ckss12"]

CARD_FOLDER = "cards"  # 'cards' 폴더가 현재 스크립트와 같은 경로에 있는지 확인하세요.
CARD_DATA_FILE = "card_data.csv"  # 'card_data.csv' 파일이 현재 스크립트와 같은 경로에 있는지 확인하세요.

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
        st.caption(f"**{direction}**") # 정방향/역방향 표시 추가 (굵게)
    except FileNotFoundError:
        st.error(f"이미지를 찾을 수 없습니다: {file}")
    except Exception as e:
        st.error(f"이미지 로드 중 오류 발생: {e}")

# --- 세션 상태 초기화 ---
# 앱이 시작될 때 단 한 번만 실행되도록
if "subcards" not in st.session_state:
    st.session_state.subcards = {} # 각 카드에 대한 보조카드 정보를 저장 (키: 메인 카드 파일명)
if "subcard_used" not in st.session_state:
    st.session_state.subcard_used = {} # 특정 메인 카드에 대해 보조카드를 이미 뽑았는지 여부 (키: 메인 카드 파일명)
if "question" not in st.session_state:
    st.session_state.question = ""
if "q1" not in st.session_state:
    st.session_state.q1 = ""
if "q2" not in st.session_state:
    st.session_state.q2 = ""
if "login" not in st.session_state:
    st.session_state.login = ""
if "cards_result" not in st.session_state: # 3카드, 원카드, 조언카드 결과
    st.session_state.cards_result = []
if "choice_cards_result" not in st.session_state: # 양자택일 결과 (메인 2장)
    st.session_state.choice_cards_result = []
if "final_card_result" not in st.session_state: # 양자택일 최종 결론 카드 결과
    st.session_state.final_card_result = None
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
    input_id = st.text_input("아이디를 입력하세요", key="login_id_input")
    if input_id:
        st.session_state.login = input_id
        st.rerun() # 로그인 후 페이지 새로고침하여 메인 화면으로 이동
    st.stop() # 로그인 전에는 여기서 앱 실행 중단

user_id = st.session_state.login
is_admin = user_id in ADMIN_IDS
is_user = user_id in USER_IDS

if not (is_admin or is_user):
    st.error("등록되지 않은 사용자입니다. 관리자에게 문의해주세요.")
    st.session_state.login = "" # 잘못된 ID면 로그인 상태 초기화
    st.stop() # 등록되지 않은 사용자는 앱 사용 불가

# --- 메인 앱 로직 ---
st.set_page_config(page_title="동양타로", layout="centered")
st.title("🌓 동양타로")
st.markdown("\"한 장의 카드가 내 마음을 말하다\"")
st.success(f"{user_id}님 환영합니다.")

# '처음으로' 버튼 (로그아웃 및 세션 초기화)
if st.button("🏠 처음으로", key="reset_button"):
    # 로그인 ID는 유지하고 나머지 세션 상태만 초기화
    user_id_temp = st.session_state.login
    st.session_state.clear() # 모든 세션 상태 초기화
    st.session_state.login = user_id_temp # 로그인 ID만 다시 설정
    # 새롭게 초기화된 세션 상태를 반영하기 위해 필요한 기본값 재설정
    st.session_state.subcards = {}
    st.session_state.subcard_used = {}
    st.session_state.question = ""
    st.session_state.q1 = ""
    st.session_state.q2 = ""
    st.session_state.cards_result = []
    st.session_state.choice_cards_result = []
    st.session_state.final_card_result = None
    st.session_state.current_mode = "3카드 보기"
    st.rerun() # 변경된 세션 상태를 반영하여 페이지 새로고침

# --- 타로 기능 모드 선택 ---
st.subheader("🔮 타로 뽑기")
# 라디오 버튼의 기본값 설정 및 현재 선택된 모드 세션 상태에 저장
mode = st.radio("모드 선택", ["3카드 보기", "원카드", "조언카드", "양자택일"], 
                index=["3카드 보기", "원카드", "조언카드", "양자택일"].index(st.session_state.current_mode),
                key="tarot_mode_selection")
st.session_state.current_mode = mode # 현재 선택된 모드를 세션 상태에 업데이트

card_data = load_card_data() # 카드 데이터 불러오기

# --- 질문 및 카드 뽑기 로직 ---

# 3카드 보기, 원카드, 조언카드 모드
if mode in ["3카드 보기", "원카드", "조언카드"]:
    # 질문 입력 필드는 모드가 변경되어도 유지되도록 key 설정
    st.session_state.question = st.text_input("질문을 입력하세요", value=st.session_state.question, key="question_input")
    
    if st.button("🔮 카드 뽑기", key="draw_cards_button"):
        if not st.session_state.question.strip(): # 질문이 비어있으면 경고
            st.warning("질문을 입력해주세요!")
        else:
            st.write(f"**질문:** {st.session_state.question}")
            
            # 이전 결과 초기화 (이전 질문 결과와 보조카드 초기화)
            st.session_state.cards_result = []
            st.session_state.choice_cards_result = []
            st.session_state.final_card_result = None
            st.session_state.subcards = {}
            st.session_state.subcard_used = {}
            
            if mode == "3카드 보기":
                st.session_state.cards_result = draw_cards(3)
                
            elif mode == "원카드":
                st.session_state.cards_result = draw_cards(1)
            
            elif mode == "조언카드":
                st.session_state.cards_result = draw_cards(1)
            
            # 결과가 업데이트되었으므로 페이지 재실행
            st.rerun()

    # '카드 뽑기' 버튼을 누르지 않았지만, 세션에 이미 결과가 있는 경우 다시 보여줌 (페이지 새로고침 시)
    if st.session_state.cards_result:
        # 질문이 비어있으면 이전에 뽑은 카드도 보이지 않도록 함
        if not st.session_state.question.strip():
            st.session_state.cards_result = [] # 질문 없으면 카드도 지움
            st.session_state.subcards = {}
            st.session_state.subcard_used = {}
        else:
            st.write(f"**질문:** {st.session_state.question}")
            if mode == "3카드 보기":
                cols = st.columns(3)
                for i, (file, direction) in enumerate(st.session_state.cards_result):
                    with cols[i]:
                        st.markdown(f"**{i+1}번 카드**")
                        show_card(file, direction, width=150)
                        st.markdown(get_card_meaning(card_data, file, direction))
                        
                        # 보조카드 버튼 및 표시 로직
                        if direction == "역방향" and file not in st.session_state.subcard_used:
                            if st.button(f"🔁 보조카드 보기 ({i+1})", key=f"sub_button_{file}"):
                                main_cards_filenames = [f for f, _ in st.session_state.cards_result]
                                subcard = draw_cards(1, exclude=main_cards_filenames)[0]
                                st.session_state.subcards[file] = subcard
                                st.session_state.subcard_used[file] = True
                                st.rerun() # 보조카드 뽑기 후 다시 렌더링
                        
                        if file in st.session_state.subcards:
                            st.markdown("---")
                            st.markdown(f"**{i+1}번 카드 보조카드**")
                            sub_file, sub_dir = st.session_state.subcards[file]
                            show_card(sub_file, sub_dir, width=120) # 보조카드는 더 작게
                            st.markdown(get_card_meaning(card_data, sub_file, sub_dir))

            elif mode in ["원카드", "조언카드"]:
                file, direction = st.session_state.cards_result[0] # 원카드/조언카드는 1장만 있음
                show_card(file, direction, width=200) # 메인 카드는 약간 더 크게
                st.markdown(get_card_meaning(card_data, file, direction))
                
                # 보조카드 버튼 및 표시 로직
                if direction == "역방향" and file not in st.session_state.subcard_used:
                    if st.button("🔁 보조카드 보기", key=f"sub_button_{file}"):
                        subcard = draw_cards(1, exclude=[file])[0]
                        st.session_state.subcards[file] = subcard
                        st.session_state.subcard_used[file] = True
                        st.rerun() # 보조카드 뽑기 후 다시 렌더링
                
                if file in st.session_state.subcards:
                    st.markdown("---")
                    st.markdown(f"**보조카드**")
                    sub_file, sub_dir = st.session_state.subcards[file]
                    show_card(sub_file, sub_dir, width
