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

# 카드 불러오기
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
        def get_unregistered_cards():
            return [fname for fname in load_cards() if fname not in card_meanings]

        unregistered = get_unregistered_cards()
        if not unregistered:
            st.success("✅ 모든 카드에 해석이 등록되어 있습니다.")
        else:
            selected_card = st.selectbox("🃏 해석이 등록되지 않은 카드 선택", unregistered)
            st.markdown("""
                ✅ 카드 설명 구성 형식 (예시 기준)

                👔 동양타로 카드: [카드명]

                🖼️ 이미지 설명 (시각적 키워드)

                🧭 카드 의미 요약

                🟢 정방향 해석 (앱 표시용)
                - 💬 요약 메시지
                - 항목 정리 (• ...)

                🔴 역방향 해석 (앱 표시용)
                - 💬 요약 메시지
                - 항목 정리 (• ...)

                📌 조언 메시지
            """)
            desc = st.text_area("🖼️ 이미지 설명")
            summary = st.text_area("🧭 카드 의미 요약")
            정 = st.text_area("✅ 정방향 해석 입력")
            역 = st.text_area("⛔ 역방향 해석 입력")
            tip = st.text_area("📌 조언 메시지")
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

# 🔮 사용자 모드 (타로 뽑기 UI)
if st.session_state.user != "cotty23":
    st.markdown("---")
    st.markdown("<h2 style='text-align:center;'>🌗 동양타로</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;'>\"한 장의 카드가 내 마음을 말하다\"</p>", unsafe_allow_html=True)
    st.markdown("---")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔮 3카드 보기"):
            st.session_state.cards = draw_cards(3)
            st.session_state.extra_cards = [None] * 3
            st.session_state.mode = "3카드"
            st.rerun()
    with col2:
        if st.button("✨ 원카드"):
            st.session_state.cards = draw_cards(1)
            st.session_state.extra_cards = [None]
            st.session_state.mode = "원카드"
            st.rerun()

    col3, col4 = st.columns(2)
    with col3:
        if st.button("🔀 양자택일"):
            st.session_state.cards = []
            st.session_state.extra_cards = [None, None]
            st.session_state.question_yes = ""
            st.session_state.question_no = ""
            st.session_state.mode = "양자택일"
            st.rerun()
    with col4:
        if st.button("🗣 오늘의 조언"):
            st.session_state.cards = draw_cards(1)
            st.session_state.extra_cards = [None]
            st.session_state.mode = "조언카드"
            st.rerun()

mode = st.session_state.mode
if mode == "3카드":
    st.markdown("## 🃏 3장의 카드")
    cols = st.columns(3)
    for i, (card, direction) in enumerate(st.session_state.cards):
        with cols[i]:
            show_card(card, direction)
            st.markdown(interpret_result(card, direction))
            if direction == "역방향" and st.session_state.extra_cards[i] is None:
                if st.button(f"🔁 보조카드 ({i+1})"):
                    st.session_state.extra_cards[i] = draw_cards(1)[0]
                    st.rerun()

    col_extras = st.columns(3)
    for i in range(3):
        if st.session_state.extra_cards[i] is not None:
            extra_card, extra_dir = st.session_state.extra_cards[i]
            with col_extras[i]:
                st.markdown("**→ 보조카드**")
                show_card(extra_card, extra_dir)
                st.markdown(interpret_result(extra_card, extra_dir))

    save_result("3카드", st.session_state.cards)
    download_history()
    if st.button("처음으로 ⭯"):
        st.session_state.mode = None
        st.rerun()

elif mode == "원카드":
    st.markdown("## 🃏 한 장의 카드")
    card, direction = st.session_state.cards[0]
    show_card(card, direction)
    st.markdown(interpret_result(card, direction))

    if direction == "역방향" and st.session_state.extra_cards[0] is None:
        if st.button("🔁 보조카드"):
            st.session_state.extra_cards[0] = draw_cards(1)[0]
            st.rerun()

    if st.session_state.extra_cards[0] is not None:
        extra_card, extra_dir = st.session_state.extra_cards[0]
        st.markdown("**→ 보조카드**")
        show_card(extra_card, extra_dir)
        st.markdown(interpret_result(extra_card, extra_dir))

    save_result("원카드", [st.session_state.cards[0]])
    download_history()
    if st.button("처음으로 ⭯"):
        st.session_state.mode = None
        st.rerun()

elif mode == "조언카드":
    st.markdown("## 🗣 오늘의 조언 카드")
    card, direction = st.session_state.cards[0]
    show_card(card, direction)
    st.markdown(interpret_result(card, direction))

    if direction == "역방향" and st.session_state.extra_cards[0] is None:
        if st.button("🔁 보조카드"):
            st.session_state.extra_cards[0] = draw_cards(1)[0]
            st.rerun()

    if st.session_state.extra_cards[0] is not None:
        extra_card, extra_dir = st.session_state.extra_cards[0]
        st.markdown("**→ 보조카드**")
        show_card(extra_card, extra_dir)
        st.markdown(interpret_result(extra_card, extra_dir))

    save_result("조언카드", [st.session_state.cards[0]])
    download_history()
    if st.button("처음으로 ⭯"):
        st.session_state.mode = None
        st.rerun()

elif mode == "양자택일":
    st.markdown("## 🔀 양자택일 카드")
    st.session_state.question_yes = st.text_input("Yes에 해당하는 질문:", value=st.session_state.question_yes)
    st.session_state.question_no = st.text_input("No에 해당하는 질문:", value=st.session_state.question_no)

    if st.button("카드 보기"):
        st.session_state.cards = draw_cards(2)
        st.session_state.extra_cards = [None, None]
        st.rerun()

    if st.session_state.cards:
        cols = st.columns(2)
        for i, (card, direction) in enumerate(st.session_state.cards):
            label = "Yes" if i == 0 else "No"
            with cols[i]:
                st.markdown(f"#### {label} - {st.session_state.question_yes if i == 0 else st.session_state.question_no}")
                show_card(card, direction)
                st.markdown(interpret_result(card, direction))
                if direction == "역방향" and st.session_state.extra_cards[i] is None:
                    if st.button(f"🔁 보조카드 ({label})"):
                        st.session_state.extra_cards[i] = draw_cards(1)[0]
                        st.rerun()

        col_extras = st.columns(2)
        for i in range(2):
            if st.session_state.extra_cards[i] is not None:
                extra_card, extra_dir = st.session_state.extra_cards[i]
                with col_extras[i]:
                    st.markdown("**→ 보조카드**")
                    show_card(extra_card, extra_dir)
                    st.markdown(interpret_result(extra_card, extra_dir))

        save_result("양자택일", st.session_state.cards)
        download_history()
        if st.button("처음으로 ⭯"):
            st.session_state.mode = None
            st.rerun()
