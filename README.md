# 운동봇

매일 운동 루틴을 (1) 아침 텔레그램 알림 + (2) 핸드폰 웹앱으로 보고 기록.

- 분할: 3분할(PPL) + 하이록스 컨디셔닝 — 가슴 주 2회 (약점 보강)
- 데이터 단일 소스: **`workouts.json`** — 봇/웹 둘 다 여기서 읽음. 일정 바꾸려면 이 파일만 수정.

## 웹앱 (핸드폰)

`index.html` — 의존성 없는 단일 파일. GitHub Pages로 배포해서 폰 홈화면에 추가.

- **보기**: 주간 일정 + 오늘 운동 + 식단 체크
- **기록**: 종목별 세트(무게×렙)·완료·메모, 컨디션·종합평가·식단 체크
- **저장**: `log/YYYY-MM-DD.md` 를 GitHub API로 자동 커밋 (⚙️에서 PAT 1회 입력)

### 배포 (GitHub Pages)
저장소 Settings → Pages → Source: `main` / `/ (root)`.
배포 URL: `https://goedwin.github.io/workout-bot/`

### PAT 발급 (기록 자동 커밋용)
[Fine-grained token](https://github.com/settings/tokens?type=beta) 발급 — **이 repo만**, 권한 **Contents: Read & write**.
앱 ⚙️ 설정에 토큰 입력 (이 기기 브라우저 localStorage 에만 저장됨).

### 로컬에서 보기
`file://` 로 열면 fetch가 막히므로 서버로 띄울 것:
```bash
cd ~/workout-bot
python3 -m http.server 8910
# http://localhost:8910/index.html
```

---

## 텔레그램 봇

### 1) 봇 세팅 (5분)
1. 텔레그램 **@BotFather** → `/newbot` → **봇 토큰** 받기
2. **@userinfobot** → 메시지 보내면 **본인 Chat ID** 알려줌
3. `.env` 에 저장:
   ```bash
   cp .env.example .env   # 열어서 채우기
   ```

### 2) 설치
```bash
cd ~/workout-bot
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 3) 테스트
```bash
python bot.py            # 오늘 운동 (env 없어도 콘솔 출력)
python bot.py monday     # 특정 요일 (테스트)
```

### 4) 매일 아침 자동 전송 (cron)
```bash
crontab -e
```
```
0 7 * * * /Users/edwin/workout-bot/.venv/bin/python /Users/edwin/workout-bot/bot.py >> /Users/edwin/workout-bot/cron.log 2>&1
```

## 운동 수정

`workouts.json` 의 `days` 만 고치면 봇·웹 둘 다 반영. `daily_reminder` 는 식단/생활 체크 항목.

## 향후 (스마트 버전)

- 어제 기록·컨디션 기반으로 Claude API가 오늘 운동 동적 생성
- 부상/피로 → 회복일 자동 변환
- 기록 누적 → 주간 볼륨/진행 트래킹
