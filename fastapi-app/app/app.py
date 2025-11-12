import pandas as pd
from pykrx import stock
from datetime import datetime
import warnings
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import logging

# FastAPI 앱 초기화
app = FastAPI()

# 경고 메시지 무시
warnings.filterwarnings('ignore')

# 로깅 설정 (콘솔에 진행 상황을 표시하기 위함)
logging.basicConfig(level=logging.INFO)

class StockAnalysisResponse(BaseModel):
    analysis_date: str
    top_risers: list
    top_fallers: list
    top_volume: list
    macd_golden_cross: list
    bb_breakout: list

def run_stock_analysis():
    """
    Jupyter Notebook의 핵심 분석 로직을 실행하고
    결과 DataFrame들을 딕셔너리 형태로 반환합니다.
    """

    # --- 1. 기본 설정 (노트북과 동일) ---
    today = datetime.now().strftime('%Y%m%d')
    start_date = (datetime.now() - pd.DateOffset(days=90)).strftime('%Y%m%d')

    # ★★★ 수정: get_nearest_business_day_in_a_week()는 인자를 받지 않음 ★★★
    try:
        latest_trading_day = stock.get_nearest_business_day_in_a_week()
    except Exception as e:
        logging.error(f"영업일 조회 실패: {e}")
        # 오늘 날짜 사용
        latest_trading_day = today

    # --- 2. 분석 파라미터 (노트북과 동일) ---
    N_DAYS = 5
    TOP_N = 5
    MIN_AVG_VOLUME = 50000
    MIN_AVG_PRICE = 1000

    logging.info(f"분석 기준일: {latest_trading_day} (데이터 조회: {start_date}부터)")

    # --- 3. KOSPI 전 종목 티커 가져오기 (노트북과 동일) ---
    all_tickers = []
    max_retries = 3

    for retry in range(max_retries):
        try:
            import time
            if retry > 0:
                logging.info(f"재시도 {retry}/{max_retries}...")
                time.sleep(2 * retry)  # 재시도 시 대기 시간 증가

            tickers_kospi = stock.get_market_ticker_list(market="KOSPI", date=latest_trading_day)

            if tickers_kospi and len(tickers_kospi) > 0:
                all_tickers = tickers_kospi
                logging.info(f"총 분석 대상 종목 수: {len(all_tickers)}개 (KOSPI 한정)")
                break
            else:
                logging.warning(f"빈 티커 목록 반환됨 (시도 {retry + 1}/{max_retries})")

        except Exception as e:
            logging.error(f"KOSPI 티커 목록 조회 실패 (시도 {retry + 1}/{max_retries}): {str(e)}", exc_info=True)

            if retry == max_retries - 1:
                # 마지막 재시도 실패 시 샘플 티커 사용
                logging.warning("전체 티커 조회 실패. 주요 종목으로 테스트합니다.")
                all_tickers = ['005930', '000660', '035420', '051910', '068270',
                               '005380', '035720', '006400', '105560', '055550']  # 주요 10개 종목
                logging.info(f"샘플 분석 대상: {len(all_tickers)}개 종목")
                break

    if not all_tickers:
        return {
            "error": "티커 목록을 가져올 수 없습니다.",
            "analysis_date": latest_trading_day,
            "top_risers": [],
            "top_fallers": [],
            "top_volume": [],
            "macd_golden_cross": [],
            "bb_breakout": []
        }

    results_list = []

    # --- 4. 전 종목 반복 분석 (노트북과 동일) ---
    for i, ticker in enumerate(all_tickers):
        if (i + 1) % 100 == 0:
            logging.info(f"진행 중... {i+1}/{len(all_tickers)} ({ticker})")

        try:
            import time
            time.sleep(0.1)  # API 레이트 리미팅 방지

            df = stock.get_market_ohlcv(start_date, latest_trading_day, ticker)
            if len(df) < 35:
                continue

            close_n_days_ago = df.iloc[-N_DAYS]['종가']
            latest_close = df.iloc[-1]['종가']

            if close_n_days_ago == 0: continue

            change_5d = ((latest_close - close_n_days_ago) / close_n_days_ago) * 100
            volume_5d_avg = df.iloc[-N_DAYS:]['거래량'].mean()
            price_5d_avg = df.iloc[-N_DAYS:]['종가'].mean()

            if volume_5d_avg < MIN_AVG_VOLUME or price_5d_avg < MIN_AVG_PRICE:
                continue

            ema_fast = df['종가'].ewm(span=12, adjust=False).mean()
            ema_slow = df['종가'].ewm(span=26, adjust=False).mean()
            df['MACD'] = ema_fast - ema_slow
            df['MACD_Signal'] = df['MACD'].ewm(span=9, adjust=False).mean()

            df['BB_Mid'] = df['종가'].rolling(window=20).mean()
            df['BB_Std'] = df['종가'].rolling(window=20).std()
            df['BB_Upper'] = df['BB_Mid'] + (df['BB_Std'] * 2)

            latest_indicators = df.iloc[-1]
            prev_indicators = df.iloc[-2]

            macd_golden_cross = (prev_indicators['MACD'] < prev_indicators['MACD_Signal']) and \
                                (latest_indicators['MACD'] > latest_indicators['MACD_Signal'])

            bb_breakout = latest_close > latest_indicators['BB_Upper']
            company_name = stock.get_market_ticker_name(ticker)

            results_list.append({
                "Ticker": ticker,
                "Name": company_name,
                "Close(원)": float(latest_close) if pd.notna(latest_close) else 0.0,
                "Change_5D(%)": float(change_5d) if pd.notna(change_5d) else 0.0,
                "Avg_Vol_5D": float(volume_5d_avg) if pd.notna(volume_5d_avg) else 0.0,
                "MACD_Signal": "Golden Cross" if macd_golden_cross else "-",
                "BB_Signal": "Breakout" if bb_breakout else "Inside"
            })
        except Exception as e:
            logging.debug(f"종목 {ticker} 분석 실패: {str(e)}")
            continue

    # --- 9. 결과 집계 (노트북 Cell 2 로직 통합) ---
    if not results_list:
        logging.warning("분석 조건을 만족하는 종목이 없습니다.")
        return {
            "message": "분석 조건을 만족하는 종목이 없습니다.",
            "analysis_date": latest_trading_day,
            "top_risers": [],
            "top_fallers": [],
            "top_volume": [],
            "macd_golden_cross": [],
            "bb_breakout": []
        }

    results_df = pd.DataFrame(results_list)

    # 각 조건별 DataFrame 생성
    top_risers = results_df.sort_values(by="Change_5D(%)", ascending=False).head(TOP_N)
    top_fallers = results_df.sort_values(by="Change_5D(%)", ascending=True).head(TOP_N)
    top_volume = results_df.sort_values(by="Avg_Vol_5D", ascending=False).head(TOP_N)
    macd_cross_stocks = results_df[results_df['MACD_Signal'] == "Golden Cross"]
    bb_breakout_stocks = results_df[results_df['BB_Signal'] == "Breakout"]

    # --- 10. 결과를 JSON으로 반환하기 위해 딕셔너리로 변환 ---
    # NaN 값을 None으로 변환하여 JSON 직렬화 문제 방지
    analysis_data = {
        "analysis_date": latest_trading_day,
        "top_risers": top_risers.replace({pd.NA: None, float('nan'): None, float('inf'): None, float('-inf'): None}).to_dict(orient='records'),
        "top_fallers": top_fallers.replace({pd.NA: None, float('nan'): None, float('inf'): None, float('-inf'): None}).to_dict(orient='records'),
        "top_volume": top_volume.replace({pd.NA: None, float('nan'): None, float('inf'): None, float('-inf'): None}).to_dict(orient='records'),
        "macd_golden_cross": macd_cross_stocks.replace({pd.NA: None, float('nan'): None, float('inf'): None, float('-inf'): None}).to_dict(orient='records'),
        "bb_breakout": bb_breakout_stocks.replace({pd.NA: None, float('nan'): None, float('inf'): None, float('-inf'): None}).to_dict(orient='records')
    }

    return analysis_data

# health check
@app.get("/healthz")
def health_check():
    return {"status": "ok"}

# API 엔드포인트 설정
@app.get("/api/stock-analysis", response_model=StockAnalysisResponse)
async def get_stock_analysis():
    """
    GET 요청을 받으면 주식 분석을 실행하고 결과를 JSON으로 반환하는 API 엔드포인트.
    """
    logging.info("API 요청 수신... 주식 분석을 시작합니다.")

    try:
        # 주식 분석 함수 실행
        data = run_stock_analysis()

        if "error" in data:
            raise HTTPException(status_code=500, detail=data["error"])

        logging.info("분석 완료. JSON 데이터를 반환합니다.")

        # 결과를 직접 반환 (analysis_date가 이미 포함됨)
        return data

    except Exception as e:
        logging.error(f"API 처리 중 오류 발생: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# FastAPI 서버 실행
if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
