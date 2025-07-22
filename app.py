import streamlit as st
import random
import os
import pandas as pd
from PIL import Image
import streamlit.components.v1 as components # 이미지 저장을 위해 필요

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
        # filename, upright, reversed 컬럼은 반드시 존재해야 합니다.
        return pd.DataFrame(columns=["filename", "upright", "reversed"])

# 카드 데이터 저장하기 (현재 코드에서는 사용되지 않지만, 관리자 기능 등을 위해 유지)
def save_card_data(df):
    df.to_csv(CARD_DATA_FILE, index=False)

# 카드 뽑기 함수 (중복 제외 및 파일 확장자 필터링)
def draw_cards(n=1, exclude=None):
    if not os.path.exists(CARD_FOLDER):
        st.error(f"'{CARD_FOLDER}' 폴더를 찾을 수 없습니다. 카드 이미지를 넣어주세요.")
        return []

    # 지원되는 이미지 파일 확장자 목록
    allowed_extensions = ('.png', '.jpg', '.jpeg', '.gif', '.bmp')
    files = [f for f in os.listdir(CARD_FOLDER) if f.lower().endswith(allowed_extensions)]
    
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
def show_card(file, direction, width=150):
    img_path = os.path.join(CARD_FOLDER, file)
    try:
        img = Image.open(img_path)
        if direction == "역방향":
            img = img.rotate(180)
        # `use_column_width=False` 대신 `use_container_width=False` 사용
        st.image(img, width=width, use_container_width=False) 
        st.caption(f"**{direction}**") # 정방향/역방향 표시 추가 (굵게)
    except FileNotFoundError:
        st.error(f"이미지를 찾을 수 없습니다: {file}")
    except Exception as e:
        st.error(f"이미지 로드 중 오류 발생: {e}")

# --- JavaScript 함수 삽입 (html2canvas 로드 및 캡처) ---
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
        // html2canvas 설정: 크로스 오리진 이미지 허용, 해상도 2배로 높이기
        html2canvas(element, {{
            useCORS: true, 
            scale: 2 
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
    <button onclick="downloadDivAsImage('{target_id}', 'tarot_result')" 
            style="
                background-color: #4CAF50; /* Green */
                border: none;
                color: white;
                padding: 10px 20px;
                text-align: center;
                text-decoration: none;
                display: inline-block;
                font-size: 16px;
                margin: 4px 2px;
                cursor: pointer;
                border-radius: 8px;
            ">
            {button_label}
    </button>
    """
    # Streamlit에 HTML/JS 삽입. height를 충분히 주어야 버튼이 잘 보입니다.
    components.html(js_code, height=60)

# --- 세션 상태 초기화 ---
# 앱이 시작될 때 단 한 번만 실행되도록
if "subcards" not in st.session_state:
    st.session_state.subcards = {} # 각 카드에 대한 보조
