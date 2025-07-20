import streamlit as st
from PIL import Image
import os
import random
import pandas as pd
import json
from datetime import datetime

# ✅ 허용된 이메일 목록
ALLOWED_USERS = ["cotty23", "teleecho", "cotty00"]

# ✅ 카드 해석 딕셔너리 (초기값)
card_meanings = {}

# ✅ JSON 불러오기 기능
if os.path.exists("card_meanings.json"):
    with open("card_meanings.json", "r", encoding="utf-8") as f:
        card_meanings = json.load(f)

# ✅ 로그인 처리
if "user" not in st.session_state:
    st.markdown("## 🔐 로그인")
    email = st.text_input("아이디를 입력하세요")
    if st.button("로그인"):
        if email in ALLOWED_USERS:
            st.session_state.user = email
            st.success(f"{email} 님 환영합니다.")
            st.rerun()
        else:
            st.error("접근 권한이 없습니다.")
    st.stop()

# 세션 초기화
for key in ["mode", "cards", "reversed", "extra_cards", "advice_card", "question_yes", "question_no", "history"]:
    if key not in st.session_state:
        st.session_state[key] = [] if key in ["cards", "reversed", "extra_cards", "history"] else ""

img_folder = "카드이미지"

def load_cards():
    if not os.path.exists(img_folder):
        st.error(f"이미지 폴더가 없습니다: {img_folder}")
        return []
    return [f for f in os.listdir(img_folder) if f.lower().endswith(('png', 'jpg', 'jpeg'))]

def draw_cards(n):
    card_pool = load_cards()
    if len(card_pool) < n:
        return []
    cards = random.sample(card_pool, n)
    directions = [random.choice(['정방향', '역방향']) for _ in range(n)]
    return list(zip(cards, directions))

def show_card(card, direction, width=200):
    img = Image.open(os.path.join(img_folder, card))
    if direction == "역방향":
        img = img.rotate(180)
    st.image(img, caption=f"{card} ({direction})", width=width)

def interpret_result(card_name, direction):
    result = card_meanings.get(card_name, {})
    parts = []
    if "이미지설명" in result:
        parts.append(f"🖼️ {result['이미지설명']}")
    if "의미요약" in result:
        parts.append(f"🧭 {result['의미요약']}")
    parts.append(result.get(direction, "💬 이 카드에 대한 해석이 준비 중입니다."))
    if "조언" in result:
        parts.append(f"📝 {result['조언']}")
    return "\n\n".join(parts)

def save_result(title, card_data):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = {"시간": timestamp, "타입": title, "카드 정보": card_data}
    st.session_state.history.append(entry)

def download_history():
    if st.session_state.history:
        df = pd.DataFrame(st.session_state.history)
        csv = df.to_csv(index=False).encode('utf-8-sig')
        st.download_button("📥 결과 다운로드 (CSV)", data=csv, file_name="타로_기록.csv", mime="text/csv")

# ✅ 관리자 모드
if st.session_state.user == "cotty23":
    with st.expander("🛠 관리자 전용: 카드 해석 등록 및 관리"):
        all_cards = load_cards()
        selected_existing = st.selectbox("📁 등록된 카드 선택 (수정 또는 확인)", ["선택 안함"] + list(card_meanings.keys()))

        if selected_existing != "선택 안함":
            data = card_meanings.get(selected_existing, {})
            desc = st.text_area("🖼️ 이미지 설명", value=data.get("이미지설명", ""))
            summary = st.text_area("🧭 카드 의미 요약", value=data.get("의미요약", ""))
            정 = st.text_area("✅ 정방향 해석 입력", value=data.get("정방향", ""))
            역 = st.text_area("⛔ 역방향 해석 입력", value=data.get("역방향", ""))
            tip = st.text_area("📌 조언 메시지", value=data.get("조언", ""))
            if st.button("💾 수정 저장"):
                card_meanings[selected_existing] = {
                    "이미지설명": desc,
                    "의미요약": summary,
                    "정방향": 정,
                    "역방향": 역,
                    "조언": tip
                }
                with open("card_meanings.json", "w", encoding="utf-8") as f:
                    json.dump(card_meanings, f, ensure_ascii=False, indent=2)
                st.success(f"'{selected_existing}' 해석이 수정되었습니다.")
                st.rerun()

        unregistered = [fname for fname in all_cards if fname not in card_meanings]
        if unregistered:
            st.markdown("---")
            st.markdown("## 📌 신규 카드 해석 등록")
            selected_card = st.selectbox("🃏 해석이 등록되지 않은 카드 선택", unregistered)
            desc = st.text_area("🖼️ 이미지 설명", key="desc_new")
            summary = st.text_area("🧭 카드 의미 요약", key="summary_new")
            정 = st.text_area("✅ 정방향 해석 입력", key="정_new")
            역 = st.text_area("⛔ 역방향 해석 입력", key="역_new")
            tip = st.text_area("📌 조언 메시지", key="tip_new")
            if st.button("💾 해석 저장"):
                card_meanings[selected_card] = {
                    "이미지설명": desc,
                    "의미요약": summary,
                    "정방향": 정,
                    "역방향": 역,
                    "조언": tip
                }
                with open("card_meanings.json", "w", encoding="utf-8") as f:
                    json.dump(card_meanings, f, ensure_ascii=False, indent=2)
                st.success(f"'{selected_card}' 해석이 저장되었습니다.")
                st.rerun()

        df = pd.DataFrame([
            {"카드": k, "정방향": v.get("정방향", ""), "역방향": v.get("역방향", ""), "조언": v.get("조언", "")}
            for k, v in card_meanings.items()
        ])
        csv = df.to_csv(index=False).encode("utf-8-sig")
        st.download_button("📄 전체 카드 해석 CSV 다운로드", data=csv, file_name="card_meanings.csv", mime="text/csv")

# 사용자 모드 이하 동일 (생략 가능)
