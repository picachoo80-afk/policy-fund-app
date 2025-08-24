# main.py
import streamlit as st
from datetime import date
import csv, os
import pandas as pd
from pathlib import Path

# ========= 기본 설정 =========
st.set_page_config(
    page_title="광명파트너스 | 정책자금 맞춤 도우미",
    page_icon="📊",
    layout="wide",
)
BRAND = "광명파트너스"
BLOG_URL = "https://blog.naver.com/kwangmyung80"
CONTACT_PHONE = "1877-2312"
KAKAO_LINK = "https://open.kakao.com/o/shxgLPsh"
ADMIN_PIN = "070913"

# ========= 스타일 =========
st.markdown("""
<style>
.block-container {padding-top: 1.25rem; padding-bottom: 2rem;}
.card { border: 1px solid #e6e6e6; border-radius: 12px; padding: 16px 18px; margin-bottom: 14px; background: #fff; }
.result-card{ border:1px solid #E5EAF2; border-radius:14px; padding:14px 16px; margin:10px 0; background:#F9FBFF; }
.badge {display:inline-block; padding:2px 8px; border-radius:999px; font-size:12px; font-weight:600; margin-left:6px;
  background:#EEF2FF; color:#334155; border:1px solid #E5E7EB;}
.small {font-size: 13px; color:#6b7280;}
hr.soft {border:none; border-top:1px dashed #e5e7eb; margin:10px 0;}
.sidebar-links a {display:block; margin:6px 0;}
</style>
""", unsafe_allow_html=True)

# ========= 경로/파일 =========
APP_DIR = Path(__file__).parent if "__file__" in globals() else Path(".")
CONTACTS_CSV = APP_DIR / "contacts.csv"

def append_contact_csv(name, phone, memo):
    CONTACTS_CSV.parent.mkdir(parents=True, exist_ok=True)
    file_exists = CONTACTS_CSV.exists()
    with CONTACTS_CSV.open("a", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        if not file_exists:
            w.writerow(["이름", "연락처", "메모", "신청일"])
        w.writerow([name, phone, memo, date.today().isoformat()])

def load_contacts_df():
    if CONTACTS_CSV.exists():
        try:
            return pd.read_csv(CONTACTS_CSV, encoding="utf-8")
        except Exception:
            return pd.read_csv(CONTACTS_CSV, encoding="cp949")
    return pd.DataFrame(columns=["이름", "연락처", "메모", "신청일"])

# ========= 사이드바 =========
with st.sidebar:
    st.markdown("### 🧭 사용 방법")
    st.markdown("- ① 기본정보 입력 → ② 추가 체크 → ③ 제출")
    st.markdown("- 결과 하단 안내문구와 상담 신청을 확인하세요.")
    st.markdown("---")
    st.markdown("### ☎ 상담/문의")
    st.markdown('<div class="sidebar-links">', unsafe_allow_html=True)
    st.markdown(f"- 대표번호: **{CONTACT_PHONE}**")
    st.markdown(f"- 블로그: [광명파트너스  블로그]({BLOG_URL})")
    st.markdown(f"- 카카오채널: [바로 연결하기]({KAKAO_LINK})")
    st.markdown('</div>', unsafe_allow_html=True)
    st.caption("👉 상담은 무료이며, 실제 신청은 고객님 명의로만 진행됩니다.")

# ========= 헤더 =========
st.markdown("## 📊 광명파트너스 – 정책자금 맞춤 도우미")
st.caption("정부 정책자금 진단 및 상담 연계 서비스")
st.markdown(
    f"📞 대표번호: **{CONTACT_PHONE}**  ·  🔗 블로그: [바로가기]({BLOG_URL})  ·  💬 카카오채널: [연결하기]({KAKAO_LINK})"
)
st.markdown("---")

# ========= 유틸 =========
from datetime import date
def years_between(d: date, ref: date | None = None) -> float:
    if ref is None: ref = date.today()
    return (ref - d).days / 365.25

def months_between(d: date, ref: date | None = None) -> float:
    if ref is None: ref = date.today()
    return (ref.year - d.year) * 12 + (ref.month - d.month) + (ref.day - d.day) / 30

def fmt_money(n: int) -> str:
    try: return f"{int(n):,}"
    except: return str(n)

def build_date_or_error(year: int, month: int, day: int, label: str):
    try:
        return date(year, month, day), None
    except Exception:
        return None, f"{label}: 올바르지 않은 날짜입니다."

# ========= 입력 폼 =========
with st.form("basic_form", clear_on_submit=False):
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("#### ① 기본정보")

    c1, c2 = st.columns(2)
    with c1:
        biz_type = st.radio("사업자 유형", ["개인사업자", "법인사업자"], index=0, horizontal=True)
    with c2:
        region = st.text_input("사업장 지역 (예: 경기도 안산시)", "경기도 안산시")

    st.markdown("**대표자 생년월일**")
    by, bm, bd = st.columns(3)
    with by: birth_year = st.number_input("연(Year)", 1900, 2025, 1980, step=1)
    with bm: birth_month = st.number_input("월(Month)", 1, 12, 1, step=1)
    with bd: birth_day = st.number_input("일(Day)", 1, 31, 1, step=1)

    st.markdown("**개업 연월일**")
    sy, sm, sd = st.columns(3)
    with sy: biz_year = st.number_input("연(Year)", 1900, 2025, 2024, step=1, key="biz_y")
    with sm: biz_month = st.number_input("월(Month)", 1, 12, 1, step=1, key="biz_m")
    with sd: biz_day = st.number_input("일(Day)", 1, 31, 1, step=1, key="biz_d")

    l1, l2 = st.columns(2)
    with l1:
        credit_nice = st.number_input("NICE 신용점수", 0, 1000, 700, step=1)
        sales = st.number_input("연 매출 (원)", 0, step=1_000_000, value=100_000_000)
        st.caption(f"입력값: {fmt_money(sales)} 원")
    with l2:
        credit_kcb  = st.number_input("KCB 신용점수", 0, 1000, 680, step=1)
        loan_amount = st.number_input("현재 대출 총액 (원)", 0, step=1_000_000, value=0)
        st.caption(f"입력값: {fmt_money(loan_amount)} 원")

    assets = st.number_input("자산 총액 (부동산·주식·자동차·임차보증금 등)", 0, step=1_000_000, value=0)
    st.caption(f"입력값: {fmt_money(assets)} 원")

    t1, t2, t3 = st.columns(3)
    with t1: biz_sector = st.text_input("사업자등록증상 **업종** (예: 음식점업)", "음식점업")
    with t2: biz_item   = st.text_input("사업자등록증상 **업태** (예: 한식)", "한식")
    with t3: employees  = st.number_input("4대보험 직원 수", 0, step=1, value=0)

    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("#### ② 추가 체크")

    st.markdown("**혁신성장촉진자금 - 혁신형 해당 여부**")
    a1, a2, a3 = st.columns(3)
    with a1:
        flag_export = st.checkbox("수출 실적 있음")
        flag_growth10 = st.checkbox("최근 2년 연속 매출 10%↑")
    with a2:
        flag_smart_factory = st.checkbox("스마트공장 도입")
        flag_strong_local  = st.checkbox("강한소상공인/로컬크리에이터")
    with a3:
        flag_postgrad = st.checkbox("졸업후보기업")

    st.markdown("**혁신성장촉진자금 - 일반형 해당 여부**")
    b1, b2, b3, b4 = st.columns(4)
    with b1: flag_smart_tech = st.checkbox("스마트기술 활용")
    with b2: flag_baeknyeon  = st.checkbox("백년소공인/백년가게")
    with b3: flag_social     = st.checkbox("사회적경제기업")
    with b4: flag_academy    = st.checkbox("신사업창업사관학교 수료(1년 이내)")

    # ✅ 재도전특별자금 조건(신규)
    st.markdown("**재도전특별자금 해당 여부**")
    c1, c2 = st.columns(2)
    with c1:
        flag_restartup = st.checkbox("재창업 경험 있음(폐업 후 재창업)")
    with c2:
        flag_debtrehab = st.checkbox("신용회복/채무조정 성실 이행 중 또는 이수")

    st.markdown("**일시적 경영애로 사유**")
    flag_distress = st.checkbox("매출 10% 이상 감소(또는 예외사유 증빙)")

    submitted = st.form_submit_button("✅ ③ 제출하고 분석 결과 보기")

# ========= 분석 출력 =========
def show_results_and_notice(birth, biz_start):
    # 입력 요약
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("#### 🧾 입력 요약")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.write(f"- 사업자 유형: **{biz_type}**")
        st.write(f"- 지역: **{region}**")
        st.write(f"- 업종/업태: **{biz_sector} / {biz_item}**")
    with c2:
        st.write(f"- 대표자 생년월일: **{birth.isoformat()}**")
        st.write(f"- 개업 연월일: **{biz_start.isoformat()}**")
        st.write(f"- 직원 수: **{employees}명**")
    with c3:
        st.write(f"- NICE/KCB: **{credit_nice} / {credit_kcb}**")
        st.write(f"- 연 매출: **{fmt_money(sales)}원**")
        st.write(f"- 대출/자산: **{fmt_money(loan_amount)}원 / {fmt_money(assets)}원**")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("### 🔎 분석 결과")
    age = int(years_between(birth))
    biz_months = months_between(biz_start)

    results = []
    # 최소 게이트
    if (sales >= 10_000_000) and (credit_nice > 515) and (credit_kcb > 454) and (biz_months >= 3):
        # 일반경영안정자금
        if (credit_nice >= 665) and (credit_kcb >= 630):
            results.append({
                "name":"일반경영안정자금",
                "range":"2,000만원 ~ 7,000만원",
                "rate":"연 3.28% (기준 2.68% +0.6%p)",
                "notes":"은행 및 보증 조건에 따라 실금리는 달라질 수 있습니다.",
                "link":"https://ols.sbiz.or.kr/"
            })
        # 신용취약 소상공인자금
        if (515 <= credit_nice <= 839) or (515 <= credit_kcb <= 839):
            results.append({
                "name":"신용취약 소상공인자금",
                "range":"최대 3,000만원 (연 1회)",
                "rate":"연 4.28% (기준 2.68% +1.6%p)",
                "notes":"신용관리교육 필수. 세부 한도/조건은 심사에 따라 달라집니다.",
                "link":"https://ols.sbiz.or.kr/"
            })
        # 청년 전용 자금 (업력 전역 제약 없음, 전역 게이트만 충족)
        if age <= 39 and (credit_nice >= 620 and credit_kcb >= 620):
            results.append({
                "name":"청년 전용 자금(공고별)",
                "range":"공고별 한도 (예: 1~2억원)",
                "rate":"연 2.68% (기준 2.68% +0.0%p)",
                "notes":"세부요건·금리는 공고마다 상이합니다.",
                "link":"https://www.kosmes.or.kr/"
            })
        # 혁신성장촉진자금
        if any([flag_export, flag_growth10, flag_smart_factory, flag_strong_local, flag_postgrad,
                flag_smart_tech, flag_baeknyeon, flag_social, flag_academy]):
            results.append({
                "name":"혁신성장촉진자금",
                "range":"운전 2억원 / 시설 10억원 (예시)",
                "rate":"연 3.08% (기준 2.68% +0.4%p)",
                "notes":"혁신형/일반형 증빙 필요. 금리는 유형·공고에 따라 달라질 수 있습니다.",
                "link":"https://www.sbiz24.kr/"
            })
        # 일시적 경영애로자금
        if flag_distress and (sales <= 104_000_000):
            results.append({
                "name":"일시적 경영애로자금",
                "range":"최대 7,000만원",
                "rate":"연 2.68% (기준 2.68% +0.0%p)",
                "notes":"매출감소 등 일시적 애로 사유를 증빙해야 합니다.",
                "link":"https://ols.sbiz.or.kr/"
            })
        # ✅ 재도전특별자금 (신규 로직)
        # - 조건: (재창업 경험 있음 OR 신용회복·채무조정 성실 이행)
        if (flag_restartup or flag_debtrehab):
            results.append({
                "name":"재도전특별자금",
                "range":"희망형 최대 1억원 / 일반형 최대 7천만원",
                "rate":"희망형 연 3.28% (기준 2.68% +0.6%p) / 일반형 연 4.28% (기준 2.68% +1.6%p)",
                "notes":"재창업·채무조정 성실 이행 등 재도약 소상공인 대상. 5년(2년 거치+3년 분할). 우대금리 최대 0.6%p 감면.",
                "link":"https://ols.sbiz.or.kr/"
            })

    # 출력
    if results:
        for r in results:
            st.markdown(f"""<div class="result-card">
                <div style='display:flex;justify-content:space-between;align-items:center;'>
                    <div style='font-size:16px; font-weight:800;'>{r['name']}</div>
                    <span class="badge">분석</span>
                </div>
                <div class='small'>예상 한도: <b>{r['range']}</b></div>
                <div class='small'>예상 금리: <b>{r['rate']}</b></div>
                <hr class="soft" />
                <div class='small'>{r['notes']}</div>
                <div style='margin-top:6px;'>👉 <a href="{r.get('link','')}" target="_blank">신청 안내 바로가기</a></div>
            </div>""", unsafe_allow_html=True)
    else:
        msg=[]
        if sales < 10_000_000: msg.append("연 매출 1,000만원 미만")
        if credit_nice <= 515 or credit_kcb <= 454: msg.append("신용점수 낮음(NICE 515 이하 또는 KCB 454 이하)")
        if months_between(biz_start) < 3: msg.append("개업 3개월 미만")
        st.info("현재 조건에 맞는 자금을 찾지 못했습니다." + (" ("+" · ".join(msg)+")" if msg else ""))

    # 안내 박스
    st.markdown("""
<div style="border-left:6px solid #1f6feb;background:#eaf2ff;padding:14px 16px;border-radius:8px;margin:12px 0 4px 0;">
<b>안내</b><br/>
💡 정책자금 승인 여부와 조건은 신용 점수나 매출뿐 아니라 <b>사업계획서·기술력·대표자 상황</b> 등에 따라 달라질 수 있습니다.
또한 <b>복수 자금 활용</b>, <b>시차를 둔 추가 신청</b> 등 운용 방식에 따라 결과가 달라질 수 있습니다.<br/><br/>
※ 본 자료는 참고용이며, 실제 심사는 기관 정책 및 신청인 신용 상태에 따라 달라질 수 있습니다.
</div>
""", unsafe_allow_html=True)

if submitted:
    birth, e1 = build_date_or_error(int(birth_year), int(birth_month), int(birth_day), "대표자 생년월일")
    start, e2 = build_date_or_error(int(biz_year), int(biz_month), int(biz_day), "개업 연월일")
    if e1: st.error(e1)
    if e2: st.error(e2)
    if not (e1 or e2):
        show_results_and_notice(birth, start)

# ========= 상담 신청(개인정보 동의: 체크박스 '폼 바깥') =========
st.markdown("### 📞 상담 신청하기")
st.caption("정확한 심사 가능 여부와 맞춤 전략은 상담을 통해 확인할 수 있습니다.")

agree = st.checkbox("✅ 개인정보 수집·이용에 동의합니다.", help=(
    "수집 항목: 이름, 연락처, 메모(선택)\n"
    "수집 목적: 정책자금 상담 신청 접수 및 연락\n"
    "보유 기간: 상담 종료 후 1년 이내 파기\n"
    "동의를 거부할 권리가 있으며, 미동의 시 상담 신청이 제한될 수 있습니다."
))

with st.form("contact_form", clear_on_submit=True):
    name = st.text_input("이름")
    phone = st.text_input("연락처 (휴대폰 번호)")
    memo = st.text_area("추가 메모 (선택)")

    submit_contact = st.form_submit_button("📩 상담 신청하기", disabled=not agree)

if submit_contact:
    if not agree:
        st.error("개인정보 수집·이용 동의가 필요합니다.")
    elif not name or not phone:
        st.error("이름과 연락처는 필수 입력입니다.")
    else:
        append_contact_csv(name, phone, memo)
        st.success("✅ 상담 신청이 접수되었습니다. 담당자 확인 후 빠르게 연락드리겠습니다.")

# ========= 하단 연락처 =========
st.markdown("---")
st.subheader("📞 상담 및 문의 채널")
st.markdown(f"- 대표번호: **{CONTACT_PHONE}**")
st.markdown(f"- 블로그: [광명파트너스  블로그]({BLOG_URL})")
st.markdown(f"- 카카오채널: [바로 연결하기]({KAKAO_LINK})")

# ========= 관리자 전용(조회/선택삭제/초기화/다운로드) =========
st.markdown("---")
with st.expander("🔒 관리자 전용 (상담 신청 내역 조회/다운로드/삭제)"):
    pin = st.text_input("관리자 PIN을 입력하세요", type="password")
    if pin == ADMIN_PIN:
        st.success("관리자 인증 완료 ✅")
        st.caption(f"저장 파일 경로: `{CONTACTS_CSV}`")

        df = load_contacts_df()
        if df.empty:
            st.info("현재 저장된 내역이 없습니다.")
        else:
            editor_df = df.copy()
            editor_df["선택"] = False
            edited = st.data_editor(
                editor_df,
                hide_index=True,
                column_config={
                    "선택": st.column_config.CheckboxColumn("선택", help="삭제할 행을 체크하세요."),
                    "이름": st.column_config.TextColumn("이름", disabled=True),
                    "연락처": st.column_config.TextColumn("연락처", disabled=True),
                    "메모": st.column_config.TextColumn("메모", disabled=True),
                    "신청일": st.column_config.TextColumn("신청일", disabled=True),
                },
                use_container_width=True,
                key="admin_editor",
            )
            to_delete = edited[edited["선택"] == True].drop(columns=["선택"])

            d1, d2, d3 = st.columns([1,1,6])
            with d1:
                del_btn = st.button(f"🗑️ 선택 행 삭제 ( {len(to_delete)} 건 )", type="primary", disabled=to_delete.empty)
            with d2:
                wipe_btn = st.button("🧹 전체 삭제(초기화)")
            with d3:
                refresh_btn = st.button("🔄 새로고침")

            if del_btn and not to_delete.empty:
                merged = df.merge(to_delete, how="left", indicator=True)
                new_df = merged[merged["_merge"] == "left_only"].drop(columns=["_merge"])
                new_df.to_csv(CONTACTS_CSV, index=False, encoding="utf-8-sig")
                st.success(f"✅ {len(to_delete)}건 삭제 완료")
                st.rerun()

            if wipe_btn:
                CONTACTS_CSV.unlink(missing_ok=True)
                st.success("✅ 모든 상담 신청 내역을 삭제했습니다.")
                st.rerun()

            if refresh_btn:
                st.rerun()

            csv_bytes = df.to_csv(index=False, encoding="utf-8-sig").encode("utf-8-sig")
            st.download_button("⬇️ CSV 다운로드", data=csv_bytes, file_name="contacts.csv", mime="text/csv")
    elif pin:
        st.error("PIN이 올바르지 않습니다.")

# ========= 푸터 =========
st.caption(f"ⓒ {date.today().year} {BRAND}")

