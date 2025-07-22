import streamlit as st
import random
import os
import pandas as pd
from PIL import Image
import base64 # 이미지 다운로드를 위해 필요

# Streamlit Components를 사용하여 JavaScript 실행 (html2canvas 로드 및 실행)
import streamlit.components.v1 as components

# --- 설정 ---
ADMIN_IDS = ["cotty23"]
USER_IDS = ["cotty00", "teleecho", "37nim", "ckss12"]

CARD_FOLDER = "cards"
CARD_DATA_FILE = "card_data.csv"

# --- 함수 정의 ---

# 카드 데이터 불러오기
def load_card_data():
    if os.path.exists(CARD_DATA_FILE):
        return pd.read_csv(CARD_DATA_FILE)
    else:
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
    
    if not files:
        st.warning("카드 폴더에 이미지가 없거나, 모든 카드가 이미 뽑혔습니다.")
        return []
        
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
if "cards_result" not in st.session_state:
    st.session_state.cards_result = []
if "choice_cards_result" not in st.session_state:
    st.session_state.choice_cards_result = []
if "final_card_result" not in st.session_state:
    st.session_state.final_card_result = None
if "current_mode" not in st.session_state:
    st.session_state.current_mode = "3카드 보기"
if "display_results" not in st.session_state: # 결과를 바로 표시할지 결정하는 플래그
    st.session_state.display_results = False

# --- JavaScript 함수 (html2canvas 로드 및 캡처) ---
# 이 함수는 Streamlit 앱에 삽입되어 브라우저에서 실행됩니다.
def inject_js_for_screenshot(target_id, button_label):
    js_code = f"""
    <script src="https://html2canvas.hertzen.com/dist/html2canvas.min.js"></script>
    <script>
    function downloadDivAsImage(divId, filename) {{
        var element = document.getElementById(divId);
        if (!element) {{
            console.error("Element with ID " + divId + " not found.");
            return;
        }}
        html2canvas(element, {{
            useCORS: true, // 크로스 오리진 이미지 처리 허용 (필요할 경우)
            scale: 2 // 해상도 높이기
        }}).then(function(canvas) {{
            var link = document.createElement('a');
            link.href = canvas.toDataURL('image/png');
            link.download = filename + '.png';
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
        }});
    }}
    </script>
    <button onclick="downloadDivAsImage('{target_id}', 'tarot_result')">{button_label}</button>
    """
    components.html(js_code, height=50)

# --- 로그인 로직 ---
if not st.session_state.login:
    st.set_page_config(page_title="동양타로", layout="centered")
    st.markdown("""
        <h1 style='text-align: center;'>🌓 동양타로</h1>
        <div style='padding: 10px; background-color: #f5f5f5; border-radius: 10px; text-align: center;'>
            <p style='font-size: 24px; font-weight: bold;'>오늘, 당신의 운명에 귀 기울이세요.</p>
            <p style='font-size: 16px;'>동양의 오랜 지혜가 담긴 타로가 당신의 삶에 깊은 통찰과 명쾌한 해답을 선사합니다.</p>
            <p style='font-size: 16px;'>사랑, 직업, 재물 등 모든 고민에 대한 당신만의 길을 지금 바로 동양 타로에서 찾아보세요.</p>
            <p style='font-size: 16px;'>숨겨진 운명의 실타래를 풀어내고, 더 나은 내일을 위한 지혜를 얻을 시간입니다.</p>
        </div>
    """, unsafe_allow_html=True)
    input_id = st.text_input("아이디를 입력하세요", key="login_id_input")
    if input_id:
        st.session_state.login = input_id
        st.rerun()
    st.stop()

user_id = st.session_state.login
is_admin = user_id in ADMIN_IDS
is_user = user_id in USER_IDS

if not (is_admin or is_user):
    st.error("등록되지 않은 사용자입니다. 관리자에게 문의해주세요.")
    st.session_state.login = ""
    st.stop()

st.set_page_config(page_title="동양타로", layout="centered")
st.title("🌓 동양타로")
st.markdown("한 장의 카드가 내 마음을 말하다")
st.success(f"{user_id}님 환영합니다.")

if st.button("🏠 처음으로", key="reset_button"):
    user_id_temp = st.session_state.login
    st.session_state.clear()
    st.session_state.login = user_id_temp
    # Reset default session states after clear
    st.session_state.subcards = {}
    st.session_state.subcard_used = {}
    st.session_state.question = ""
    st.session_state.q1 = ""
    st.session_state.q2 = ""
    st.session_state.cards_result = []
    st.session_state.choice_cards_result = []
    st.session_state.final_card_result = None
    st.session_state.current_mode = "3카드 보기"
    st.session_state.display_results = False # 결과 표시 플래그 초기화
    st.rerun()

# --- 카드 기능 모드 선택 ---
st.subheader("🔮 타로 뽑기")
mode = st.radio("모드 선택", ["3카드 보기", "원카드", "조언카드", "양자택일"], 
                index=["3카드 보기", "원카드", "조언카드", "양자택일"].index(st.session_state.current_mode),
                key="tarot_mode_selection")
st.session_state.current_mode = mode

card_data = load_card_data()

# --- 보조카드 표시 함수 (수정) ---
# 이 함수는 `handle_subcard` 대신 직접 버튼을 배치하고 세션 상태를 업데이트하여 `st.rerun()`을 발생시킵니다.
def display_subcard_logic(main_card_file, exclude_files):
    if main_card_file in st.session_state.subcards:
        st.markdown("---") # 구분선 추가
        st.markdown(f"**보조카드**")
        sub_file, sub_dir = st.session_state.subcards[main_card_file]
        show_card(sub_file, sub_dir, width=120) # 보조카드는 더 작게
        st.markdown(get_card_meaning(card_data, sub_file, sub_dir))
    elif st.button("🔁 보조카드 보기", key=f"sub_button_{main_card_file}"):
        subcard = draw_cards(1, exclude=exclude_files)
        if subcard: # 카드가 정상적으로 뽑혔을 경우에만 처리
            st.session_state.subcards[main_card_file] = subcard[0]
            st.session_state.subcard_used[main_card_file] = True
            st.rerun() # 보조카드 뽑기 후 다시 렌더링


# --- 질문 및 카드 뽑기 로직 ---

# 3카드 보기, 원카드, 조언카드 모드
if mode in ["3카드 보기", "원카드", "조언카드"]:
    st.session_state.question = st.text_input("질문을 입력하세요", value=st.session_state.question, key="question_input")
    
    if st.button("🔮 카드 뽑기", key="draw_cards_button"):
        if not st.session_state.question.strip():
            st.warning("질문을 입력해주세요!")
        else:
            # 이전 결과 초기화
            st.session_state.cards_result = []
            st.session_state.choice_cards_result = []
            st.session_state.final_card_result = None
            st.session_state.subcards = {}
            st.session_state.subcard_used = {}
            st.session_state.display_results = True # 결과 표시 플래그 활성화

            if mode == "3카드 보기":
                st.session_state.cards_result = draw_cards(3)
            elif mode == "원카드":
                st.session_state.cards_result = draw_cards(1)
            elif mode == "조언카드":
                st.session_state.cards_result = draw_cards(1)
            
            st.rerun() # 결과가 업데이트되었으므로 페이지 재실행

    # 결과 표시 영역 (캡처 대상)
    if st.session_state.display_results and st.session_state.cards_result and st.session_state.question.strip():
        # HTML 캡처를 위한 컨테이너 div
        st.markdown(f"<div id='tarot-result-container' style='padding: 20px; border: 1px solid #ddd; border-radius: 10px; background-color: #f9f9f9;'>", unsafe_allow_html=True)
        st.write(f"**질문:** {st.session_state.question}")

        if mode == "3카드 보기":
            cols = st.columns(3)
            for i, (file, direction) in enumerate(st.session_state.cards_result):
                with cols[i]:
                    st.markdown(f"**{i+1}번 카드**")
                    show_card(file, direction, width=150)
                    st.markdown(get_card_meaning(card_data, file, direction))
                    if direction == "역방향": # 역방향일 경우에만 보조카드 로직 호출
                        display_subcard_logic(file, [f for f, _ in st.session_state.cards_result])

        elif mode in ["원카드", "조언카드"]:
            file, direction = st.session_state.cards_result[0]
            show_card(file, direction, width=200)
            st.markdown(get_card_meaning(card_data, file, direction))
            if direction == "역방향": # 역방향일 경우에만 보조카드 로직 호출
                display_subcard_logic(file, [file])
        
        st.markdown(f"</div>", unsafe_allow_html=True) # 컨테이너 div 닫기

        # 이미지 저장 버튼
        inject_js_for_screenshot('tarot-result-container', '📸 결과 이미지로 저장하기')
    elif st.session_state.display_results and not st.session_state.question.strip():
        # 질문이 없는데 결과 표시 플래그가 켜져있으면 초기화
        st.session_state.display_results = False
        st.session_state.cards_result = []
        st.session_state.subcards = {}
        st.session_state.subcard_used = {}


# 양자택일 모드
elif mode == "양자택일":
    st.session_state.q1 = st.text_input("선택 1 질문 입력", value=st.session_state.q1, key="q1_input")
    st.session_state.q2 = st.text_input("선택 2 질문 입력", value=st.session_state.q2, key="q2_input")

    if st.button("🔍 선택별 카드 뽑기", key="draw_binary_button"):
        if not st.session_state.q1.strip() or not st.session_state.q2.strip():
            st.warning("선택 1과 선택 2 질문을 모두 입력해주세요!")
        else:
            # 이전 결과 초기화
            st.session_state.cards_result = []
            st.session_state.choice_cards_result = []
            st.session_state.final_card_result = None
            st.session_state.subcards = {}
            st.session_state.subcard_used = {}
            st.session_state.display_results = True # 결과 표시 플래그 활성화

            st.session_state.choice_cards_result = draw_cards(2)
            st.rerun() # 결과가 업데이트되었으므로 페이지 재실행

    # 결과 표시 영역 (캡처 대상)
    if st.session_state.display_results and st.session_state.choice_cards_result and st.session_state.q1.strip() and st.session_state.q2.strip():
        # HTML 캡처를 위한 컨테이너 div
        st.markdown(f"<div id='tarot-result-container' style='padding: 20px; border: 1px solid #ddd; border-radius: 10px; background-color: #f9f9f9;'>", unsafe_allow_html=True)
        st.write(f"**선택 1:** {st.session_state.q1}")
        st.write(f"**선택 2:** {st.session_state.q2}")
        cols = st.columns(2)
        
        # 선택 1 카드
        with cols[0]:
            st.markdown(f"**선택 1**", help=st.session_state.q1) 
            file1, direction1 = st.session_state.choice_cards_result[0]
            show_card(file1, direction1, width=150)
            st.markdown(get_card_meaning(card_data, file1, direction1))
        
        # 선택 2 카드
        with cols[1]:
            st.markdown(f"**선택 2**", help=st.session_state.q2)
            file2, direction2 = st.session_state.choice_cards_result[1]
            show_card(file2, direction2, width=150)
            st.markdown(get_card_meaning(card_data, file2, direction2))
        
        # 최종 결론 카드 뽑기 버튼
        if st.button("🧭 최종 결론 카드 뽑기", key="draw_final_card_button"):
            current_drawn_files = [f for f, _ in st.session_state.choice_cards_result]
            st.session_state.final_card_result = draw_cards(1, exclude=current_drawn_files)
            if st.session_state.final_card_result: # 카드가 정상적으로 뽑혔을 경우에만 저장
                st.session_state.final_card_result = st.session_state.final_card_result[0]
            else:
                st.session_state.final_card_result = None # 뽑히지 않았다면 None으로 설정
            st.rerun()

        # 최종 결론 카드 결과 표시
        if st.session_state.final_card_result:
            st.markdown("---")
            st.subheader("💡 최종 결론 카드")
            file, direction = st.session_state.final_card_result
            show_card(file, direction, width=200)
            st.markdown(get_card_meaning(card_data, file, direction))
        
        st.markdown(f"</div>", unsafe_allow_html=True) # 컨테이너 div 닫기

        # 이미지 저장 버튼
        inject_js_for_screenshot('tarot-result-container', '📸 결과 이미지로 저장하기')
    elif st.session_state.display_results and (not st.session_state.q1.strip() or not st.session_state.q2.strip()):
        # 질문이 없는데 결과 표시 플래그가 켜져있으면 초기화
        st.session_state.display_results = False
        st.session_state.choice_cards_result = []
        st.session_state.final_card_result = None
