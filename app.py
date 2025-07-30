<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🌓 동양타로</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Arial', sans-serif;
            background: linear-gradient(135deg, #0d1421, #1a1a2e, #16213e);
            color: #fff;
            min-height: 100vh;
            overflow-x: hidden;
        }
        
        /* 배경 별들 */
        .stars-bg {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            pointer-events: none;
            z-index: -1;
        }
        
        .star-bg {
            position: absolute;
            width: 2px;
            height: 2px;
            background: #ffd700;
            border-radius: 50%;
            animation: twinkle 3s infinite alternate;
        }
        
        @keyframes twinkle {
            0% { opacity: 0.3; transform: scale(1); }
            100% { opacity: 1; transform: scale(1.2); }
        }
        
        /* 로그인 화면 */
        .login-screen {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            min-height: 100vh;
            padding: 20px;
        }
        
        .login-title {
            font-size: 3rem;
            margin-bottom: 2rem;
            text-align: center;
            background: linear-gradient(45deg, #ffd700, #ffed4e);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            text-shadow: 0 0 30px rgba(255, 215, 0, 0.3);
        }
        
        .login-description {
            max-width: 600px;
            text-align: center;
            background: rgba(255, 255, 255, 0.1);
            padding: 30px;
            border-radius: 20px;
            margin-bottom: 30px;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 215, 0, 0.2);
        }
        
        .login-input {
            padding: 15px 25px;
            font-size: 1.1rem;
            border: 2px solid #ffd700;
            border-radius: 50px;
            background: rgba(255, 255, 255, 0.1);
            color: #fff;
            text-align: center;
            margin-top: 20px;
            width: 300px;
            backdrop-filter: blur(10px);
        }
        
        .login-input::placeholder {
            color: rgba(255, 255, 255, 0.7);
        }
        
        .login-input:focus {
            outline: none;
            box-shadow: 0 0 20px rgba(255, 215, 0, 0.5);
            transform: scale(1.05);
        }
        
        /* 메인 화면 */
        .main-container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }
        
        .header {
            text-align: center;
            margin-bottom: 30px;
        }
        
        .main-title {
            font-size: 2.5rem;
            margin-bottom: 10px;
            background: linear-gradient(45deg, #ffd700, #ffed4e);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        
        .subtitle {
            font-size: 1.2rem;
            color: #c9b037;
            margin-bottom: 20px;
        }
        
        .welcome-message {
            background: linear-gradient(135deg, rgba(255, 215, 0, 0.1), rgba(255, 215, 0, 0.05));
            padding: 15px 30px;
            border-radius: 50px;
            border: 1px solid rgba(255, 215, 0, 0.3);
            display: inline-block;
        }
        
        /* 모드 선택 */
        .mode-selection {
            background: rgba(255, 255, 255, 0.05);
            padding: 30px;
            border-radius: 20px;
            margin-bottom: 30px;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 215, 0, 0.2);
        }
        
        .mode-title {
            text-align: center;
            font-size: 1.5rem;
            color: #ffd700;
            margin-bottom: 20px;
        }
        
        .mode-buttons {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-bottom: 20px;
        }
        
        .mode-btn {
            padding: 15px 20px;
            background: rgba(255, 215, 0, 0.1);
            border: 2px solid transparent;
            border-radius: 15px;
            color: #fff;
            font-size: 1rem;
            cursor: pointer;
            transition: all 0.3s ease;
            text-align: center;
        }
        
        .mode-btn:hover {
            background: rgba(255, 215, 0, 0.2);
            border-color: #ffd700;
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(255, 215, 0, 0.3);
        }
        
        .mode-btn.active {
            background: rgba(255, 215, 0, 0.3);
            border-color: #ffd700;
            color: #ffd700;
        }
        
        /* 카드 영역 */
        .card-area {
            background: rgba(255, 255, 255, 0.05);
            padding: 30px;
            border-radius: 20px;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 215, 0, 0.2);
            min-height: 400px;
        }
        
        .draw-button {
            display: block;
            margin: 0 auto 30px;
            padding: 15px 40px;
            background: linear-gradient(45deg, #ffd700, #c9b037);
            border: none;
            border-radius: 50px;
            color: #1a1a2e;
            font-size: 1.2rem;
            font-weight: bold;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        
        .draw-button:hover {
            transform: translateY(-3px);
            box-shadow: 0 10px 25px rgba(255, 215, 0, 0.4);
        }
        
        /* 카드 스타일 */
        .card {
            width: 150px;
            height: 225px;
            border-radius: 15px;
            position: relative;
            cursor: pointer;
            transition: all 0.5s ease;
            margin: 0 auto;
        }
        
        .card:hover {
            transform: translateY(-10px) scale(1.05);
            box-shadow: 0 20px 40px rgba(255, 215, 0, 0.3);
        }
        
        /* 카드 뒷면 (별자리 패턴) */
        .card-back {
            width: 100%;
            height: 100%;
            background: linear-gradient(45deg, #0d1421, #1a1a2e);
            border: 3px solid #c9b037;
            border-radius: 15px;
            position: relative;
            overflow: hidden;
        }
        
        .card-stars {
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
        }
        
        .card-star {
            position: absolute;
            width: 3px;
            height: 3px;
            background: #ffd700;
            border-radius: 50%;
            animation: cardTwinkle 2s infinite alternate;
        }
        
        .card-star:nth-child(1) { top: 20%; left: 15%; animation-delay: 0s; }
        .card-star:nth-child(2) { top: 30%; left: 80%; animation-delay: 0.5s; }
        .card-star:nth-child(3) { top: 60%; left: 20%; animation-delay: 1s; }
        .card-star:nth-child(4) { top: 80%; left: 70%; animation-delay: 1.5s; }
        .card-star:nth-child(5) { top: 40%; left: 50%; animation-delay: 0.3s; width: 4px; height: 4px; }
        .card-star:nth-child(6) { top: 70%; left: 40%; animation-delay: 0.8s; }
        .card-star:nth-child(7) { top: 25%; left: 60%; animation-delay: 1.2s; }
        
        .card-constellation {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            width: 80px;
            height: 80px;
            border: 2px solid rgba(255, 215, 0, 0.3);
            border-radius: 50%;
            background: rgba(255, 215, 0, 0.05);
        }
        
        @keyframes cardTwinkle {
            0% { opacity: 0.3; }
            100% { opacity: 1; }
        }
        
        /* 카드 앞면 */
        .card-front {
            width: 100%;
            height: 100%;
            background: #fff;
            border-radius: 15px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.2rem;
            color: #333;
            border: 3px solid #ffd700;
        }
        
        /* 카드 그리드 */
        .cards-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
            gap: 30px;
            margin-bottom: 30px;
        }
        
        .card-info {
            text-align: center;
            margin-top: 15px;
        }
        
        .card-meaning {
            background: rgba(255, 255, 255, 0.1);
            padding: 15px;
            border-radius: 10px;
            margin-top: 10px;
            backdrop-filter: blur(5px);
            border: 1px solid rgba(255, 215, 0, 0.2);
        }
        
        /* 특별 버튼들 */
        .special-button {
            background: rgba(255, 215, 0, 0.1);
            border: 2px solid #ffd700;
            padding: 10px 20px;
            border-radius: 25px;
            color: #ffd700;
            cursor: pointer;
            transition: all 0.3s ease;
            margin: 5px;
            display: inline-block;
        }
        
        .special-button:hover {
            background: rgba(255, 215, 0, 0.2);
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(255, 215, 0, 0.3);
        }
        
        /* 양자택일 입력 */
        .choice-input {
            width: 100%;
            padding: 12px 20px;
            margin: 10px 0;
            background: rgba(255, 255, 255, 0.1);
            border: 2px solid rgba(255, 215, 0, 0.3);
            border-radius: 10px;
            color: #fff;
            font-size: 1rem;
            backdrop-filter: blur(5px);
        }
        
        .choice-input::placeholder {
            color: rgba(255, 255, 255, 0.6);
        }
        
        .choice-input:focus {
            outline: none;
            border-color: #ffd700;
            box-shadow: 0 0 10px rgba(255, 215, 0, 0.3);
        }
        
        /* 월별 선택 */
        .month-selector {
            text-align: center;
            margin-bottom: 20px;
        }
        
        .month-select {
            padding: 10px 20px;
            background: rgba(255, 255, 255, 0.1);
            border: 2px solid rgba(255, 215, 0, 0.3);
            border-radius: 10px;
            color: #fff;
            font-size: 1rem;
            backdrop-filter: blur(5px);
        }
        
        .month-select:focus {
            outline: none;
            border-color: #ffd700;
        }
        
        /* 홈 버튼 */
        .home-button {
            position: fixed;
            top: 20px;
            right: 20px;
            background: rgba(255, 215, 0, 0.2);
            border: 2px solid #ffd700;
            padding: 10px 20px;
            border-radius: 25px;
            color: #ffd700;
            cursor: pointer;
            transition: all 0.3s ease;
            backdrop-filter: blur(10px);
        }
        
        .home-button:hover {
            background: rgba(255, 215, 0, 0.3);
            transform: scale(1.05);
        }
        
        /* 반응형 디자인 */
        @media (max-width: 768px) {
            .main-title {
                font-size: 2rem;
            }
            
            .login-title {
                font-size: 2rem;
            }
            
            .mode-buttons {
                grid-template-columns: 1fr;
            }
            
            .cards-grid {
                grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
                gap: 20px;
            }
            
            .card {
                width: 120px;
                height: 180px;
            }
        }
        
        /* 숨김 클래스 */
        .hidden {
            display: none !important;
        }
        
        /* 조언 카드 섹션 */
        .advice-section {
            margin-top: 30px;
            padding-top: 30px;
            border-top: 2px solid rgba(255, 215, 0, 0.3);
        }
        
        .advice-title {
            text-align: center;
            color: #ffd700;
            font-size: 1.3rem;
            margin-bottom: 20px;
        }
        
        /* 최종 결론 카드 */
        .conclusion-section {
            margin-top: 30px;
            padding: 20px;
            background: rgba(255, 215, 0, 0.05);
            border-radius: 15px;
            border: 1px solid rgba(255, 215, 0, 0.2);
        }
    </style>
</head>
<body>
    <!-- 배경 별들 -->
    <div class="stars-bg" id="starsBg"></div>
    
    <!-- 로그인 화면 -->
    <div id="loginScreen" class="login-screen">
        <h1 class="login-title">🌓 동양타로</h1>
        <div class="login-description">
            <p style="font-size: 1.5rem; font-weight: bold; color: #ffd700; margin-bottom: 15px; text-shadow: 0 0 10px rgba(255, 215, 0, 0.5);">오늘, 당신의 운명에 귀 기울이세요.</p>
            <p style="font-size: 1.1rem; margin-bottom: 10px; color: #e0e0e0;">동양의 오랜 지혜가 담긴 타로가 당신의 삶에 깊은 통찰과 명쾌한 해답을 선사합니다.</p>
            <p style="font-size: 1.1rem; margin-bottom: 10px; color: #e0e0e0;">사랑, 직업, 재물 등 모든 고민에 대한 당신만의 길을 지금 바로 동양 타로에서 찾아보세요.</p>
            <p style="font-size: 1.1rem; color: #e0e0e0;">숨겨진 운명의 실타래를 풀어내고, 더 나은 내일을 위한 지혜를 얻을 시간입니다.</p>
        </div>
        <input type="text" id="loginInput" class="login-input" placeholder="아이디를 입력하세요" />
    </div>
    
    <!-- 메인 화면 -->
    <div id="mainScreen" class="main-container hidden">
        <div class="home-button" onclick="goHome()">🏠 처음으로</div>
        
        <div class="header">
            <h1 class="main-title">🌓 동양타로</h1>
            <p class="subtitle">한 장의 카드가 내 마음을 말하다</p>
            <div class="welcome-message" id="welcomeMessage">환영합니다.</div>
        </div>
        
        <div class="mode-selection">
            <h3 class="mode-title">🔮 카드 모드</h3>
            <div class="mode-buttons">
                <button class="mode-btn" onclick="selectMode('three-cards')">3카드 보기</button>
                <button class="mode-btn" onclick="selectMode('one-card')">원카드</button>
                <button class="mode-btn" onclick="selectMode('advice-card')">오늘의조언카드</button>
                <button class="mode-btn" onclick="selectMode('choice')">양자택일</button>
                <button class="mode-btn" onclick="selectMode('monthly')">12개월운보기 (월별)</button>
            </div>
        </div>
        
        <div class="card-area" id="cardArea">
            <p style="text-align: center; color: #c9b037; font-size: 1.2rem;">위에서 원하는 모드를 선택해주세요</p>
        </div>
    </div>

    <script>
        // 전역 변수
        let currentUser = '';
        let currentMode = '';
        let currentCards = [];
        let subCards = {};
        let adviceCard = null;
        let finalChoiceCard = null;
        
        // 관리자 및 사용자 ID
        const ADMIN_IDS = ["cotty23"];
        const USER_IDS = ["cotty00", "teleecho", "37nim", "ckss12"];
        
        // 임시 카드 데이터 (실제로는 서버에서 가져와야 함)
        const cardData = {
            "card1.jpg": { upright: "새로운 시작과 희망을 의미합니다.", reversed: "지연과 좌절을 나타냅니다." },
            "card2.jpg": { upright: "사랑과 조화를 상징합니다.", reversed: "갈등과 오해를 경고합니다." },
            "card3.jpg": { upright: "성공과 성취를 예고합니다.", reversed: "실패와 실망을 암시합니다." },
            "card4.jpg": { upright: "지혜와 직관을 의미합니다.", reversed: "혼란과 착각을 경고합니다." },
            "card5.jpg": { upright: "변화와 전환을 나타냅니다.", reversed: "정체와 저항을 의미합니다." }
        };
        
        // 배경 별들 생성
        function createBackgroundStars() {
            const starsBg = document.getElementById('starsBg');
            for (let i = 0; i < 50; i++) {
                const star = document.createElement('div');
                star.className = 'star-bg';
                star.style.left = Math.random() * 100 + '%';
                star.style.top = Math.random() * 100 + '%';
                star.style.animationDelay = Math.random() * 3 + 's';
                starsBg.appendChild(star);
            }
        }
        
        // 로그인 처리
        document.getElementById('loginInput').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                login();
            }
        });
        
        function login() {
            const userId = document.getElementById('loginInput').value.trim();
            if (!userId) return;
            
            if (ADMIN_IDS.includes(userId) || USER_IDS.includes(userId)) {
                currentUser = userId;
                document.getElementById('loginScreen').classList.add('hidden');
                document.getElementById('mainScreen').classList.remove('hidden');
                document.getElementById('welcomeMessage').textContent = `${userId}님 환영합니다.`;
                
                // 로그인 로그 기록 (실제로는 서버에 전송)
                console.log(`Login: ${userId} at ${new Date()}`);
            } else {
                alert('등록되지 않은 사용자입니다.');
            }
        }
        
        // 홈으로 돌아가기
        function goHome() {
            currentMode = '';
            currentCards = [];
            subCards = {};
            adviceCard = null;
            finalChoiceCard = null;
            
            // 모든 모드 버튼 비활성화
            document.querySelectorAll('.mode-btn').forEach(btn => {
                btn.classList.remove('active');
            });
            
            // 카드 영역 초기화
            document.getElementById('cardArea').innerHTML = `
                <p style="text-align: center; color: #c9b037; font-size: 1.2rem;">위에서 원하는 모드를 선택해주세요</p>
            `;
        }
        
        // 모드 선택
        function selectMode(mode) {
            currentMode = mode;
            
            // 모든 버튼 비활성화 후 선택된 버튼 활성화
            document.querySelectorAll('.mode-btn').forEach(btn => {
                btn.classList.remove('active');
            });
            event.target.classList.add('active');
            
            // 카드 영역 초기화
            currentCards = [];
            subCards = {};
            adviceCard = null;
            finalChoiceCard = null;
            
            switch(mode) {
                case 'three-cards':
                    setupThreeCards();
                    break;
                case 'one-card':
                    setupOneCard();
                    break;
                case 'advice-card':
                    setupAdviceCard();
                    break;
                case 'choice':
                    setupChoice();
                    break;
                case 'monthly':
                    setupMonthly();
                    break;
            }
        }
        
        // 카드 생성 함수
        function createCard(cardName, direction, size = 'normal') {
            const cardDiv = document.createElement('div');
            cardDiv.className = 'card';
            if (size === 'large') {
                cardDiv.style.width = '200px';
                cardDiv.style.height = '300px';
            }
            
            const cardBack = document.createElement('div');
            cardBack.className = 'card-back';
            cardBack.innerHTML = `
                <div class="card-stars">
                    <div class="card-star"></div>
                    <div class="card-star"></div>
                    <div class="card-star"></div>
                    <div class="card-star"></div>
                    <div class="card-star"></div>
                    <div class="card-star"></div>
                    <div class="card-star"></div>
                </div>
                <div class="card-constellation"></div>
            `;
            
            cardDiv.appendChild(cardBack);
            
            // 클릭 시 카드 뒤집기 (실제 구현 시 필요)
            cardDiv.onclick = () => {
                // 여기에 카드 뒤집기 애니메이션과 실제 카드 이미지 표시 로직 추가
                console.log(`Card clicked: ${cardName}, ${direction}`);
            };
            
            return cardDiv;
        }
        
        // 카드 의미 가져오기
        function getCardMeaning(cardName, direction) {
            const card = cardData[cardName];
            if (!card) return "등록된 해석이 없습니다.";
            return direction === "정방향" ? card.upright : card.reversed;
        }
        
        // 랜덤 카드 뽑기
        function drawRandomCards(count, exclude = []) {
            const allCards = Object.keys(cardData);
            const availableCards = allCards.filter(card => !exclude.includes(card));
            const selectedCards = [];
            
            for (let i = 0; i < count && i < availableCards.length; i++) {
                const randomIndex = Math.floor(Math.random() * availableCards.length);
                const selectedCard = availableCards.splice(randomIndex, 1)[0];
                const direction = Math.random() < 0.5 ? "정방향" : "역방향";
                selectedCards.push({ name: selectedCard, direction: direction });
            }
            
            return selectedCards;
        }
        
        // 3카드 설정
        function setupThreeCards() {
            const cardArea = document.getElementById('cardArea');
            cardArea.innerHTML = `
                <button class="draw-button" onclick="drawThreeCards()">🔮 3장 뽑기</button>
                <div id="threeCardsResult"></div>
            `;
        }
        
        function drawThreeCards() {
            currentCards = drawRandomCards(3);
            const resultDiv = document.getElementById('threeCardsResult');
            
            let html = '<div class="cards-grid">';
            currentCards.forEach((card, index) => {
                html += `
                    <div>
                        <div class="card-info">
                            ${createCard(card.name, card.direction).outerHTML}
                            <div class="card-meaning">
                                <strong>${card.direction}</strong><br>
                                ${getCardMeaning(card.name, card.direction)}
                            </div>
                            ${card.direction === "역방향" ? 
                                `<button class="special-button" onclick="showSubCard('${card.name}', ${index})">🔁 보조카드 보기</button>` : 
                                ''
                            }
                            <div id="subcard-${index}"></div>
                        </div>
                    </div>
                `;
            });
            html += '</div>';
            
            html += `
                <div style="text-align: center; margin-top: 20px;">
                    <button class="special-button" onclick="showAdviceForThreeCards()">🌟 조언카드 보기</button>
                </div>
                <div id="adviceCardResult"></div>
            `;
            
            resultDiv.innerHTML = html;
        }
        
        function showSubCard(mainCardName, index) {
            if (subCards[mainCardName]) return;
            
            const excludeCards = currentCards.map(c => c.name);
            const subCard = drawRandomCards(1, excludeCards)[0];
            subCards[mainCardName] = subCard;
            
            const subcardDiv = document.getElementById(`subcard-${index}`);
            subcardDiv.innerHTML = `
                <div class="advice-section">
                    <h4 class="advice-title">보조카드</h4>
                    ${createCard(subCard.name, subCard.direction).outerHTML}
                    <div class="card-meaning">
                        <strong>${subCard.direction}</strong><br>
                        ${getCardMeaning(subCard.name, subCard.direction)}
                    </div>
                </div>
            `;
        }
        
        function showAdviceForThreeCards() {
            if (adviceCard) return;
            
            const excludeCards = currentCards.map(c => c.name).concat(Object.keys(subCards));
            adviceCard = drawRandomCards(1, excludeCards)[0];
            
            const adviceDiv = document.getElementById('adviceCardResult');
            adviceDiv.innerHTML = `
                <div class="advice-section">
                    <h3 class="advice-title">🧭 3카드에 대한 조언</h3>
                    <div style="text-align: center;">
                        ${createCard(adviceCard.name, adviceCard.direction, 'large').outerHTML}
                        <div class="card-meaning">
                            <strong>${adviceCard.direction}</strong><br>
                            ${getCardMeaning(adviceCard.name, adviceCard.direction)}
                        </div>
                    </div>
                </div>
            `;
        }
        
        // 원카드 설정
        function setupOneCard() {
            const cardArea = document.getElementById('cardArea');
            cardArea.innerHTML = `
                <button class
