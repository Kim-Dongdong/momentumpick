import pandas as pd
from pykrx import stock
from datetime import datetime
import warnings
from flask import Flask, jsonify
import logging

# Flask 앱 초기화
app = Flask(__name__)

# ★★★ 한글이 JSON에서 깨지지 않고 정상 출력되도록 설정 ★★★
app.config['JSON_AS_ASCII'] = False

# 경고 메시지 무시
warnings.filterwarnings('ignore')

# 로깅 설정 (콘솔에 진행 상황을 표시하기 위함)
logging.basicConfig(level=logging.INFO)

def run_stock_analysis():
    """
    Jupyter Notebook의 핵심 분석 로직을 실행하고
    결과 DataFrame들을 딕셔너리 형태로 반환합니다.
    """
    
    # --- 1. 기본 설정 (노트북과 동일) ---
    today = datetime.now().strftime('%Y%m%d')
    start_date = (datetime.now() - pd.DateOffset(days=90)).strftime('%Y%m%d')
    latest_trading_day = stock.get_nearest_business_day_in_a_week(today)

    # --- 2. 분석 파라미터 (노트북과 동일) ---
    N_DAYS = 5
    TOP_N = 5
    MIN_AVG_VOLUME = 50000
    MIN_AVG_PRICE = 1000

    logging.info(f"분석 기준일: {latest_trading_day} (데이터 조회: {start_date}부터)")

    # --- 3. KOSPI 전 종목 티커 가져오기 (노트북과 동일) ---
    try:
        tickers_kospi = stock.get_market_ticker_list(market="KOSPI", date=latest_trading_day)
        all_tickers = tickers_kospi
        logging.info(f"총 분석 대상 종목 수: {len(all_tickers)}개 (KOSPI 한정)")
    except Exception as e:
        logging.error(f"KOSPI 티커 목록 조회 실패: {e}")
        return {"error": f"KOSPI 티커 목록 조회 실패: {e}"}

    results_list = []

    # --- 4. 전 종목 반복 분석 (노트북과 동일) ---
    for i, ticker in enumerate(all_tickers):
        if (i + 1) % 100 == 0:
            logging.info(f"진행 중... {i+1}/{len(all_tickers)} ({ticker})")

        try:
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
                "Close(원)": latest_close,
                "Change_5D(%)": change_5d,
                "Avg_Vol_5D": volume_5d_avg,
                "MACD_Signal": "Golden Cross" if macd_golden_cross else "-",
                "BB_Signal": "Breakout" if bb_breakout else "Inside"
            })
        except Exception as e:
            continue

    # --- 9. 결과 집계 (노트북 Cell 2 로직 통합) ---
    if not results_list:
        logging.warning("분석 조건을 만족하는 종목이 없습니다.")
        return {"message": "분석 조건을 만족하는 종목이 없습니다.", "data": {}}

    results_df = pd.DataFrame(results_list)
    
    # 각 조건별 DataFrame 생성
    top_risers = results_df.sort_values(by="Change_5D(%)", ascending=False).head(TOP_N)
    top_fallers = results_df.sort_values(by="Change_5D(%)", ascending=True).head(TOP_N)
    top_volume = results_df.sort_values(by="Avg_Vol_5D", ascending=False).head(TOP_N)
    macd_cross_stocks = results_df[results_df['MACD_Signal'] == "Golden Cross"]
    bb_breakout_stocks = results_df[results_df['BB_Signal'] == "Breakout"]

    # --- 10. (★수정) 결과를 JSON으로 반환하기 위해 딕셔너리로 변환 ---
    # .to_dict(orient='records')는 DataFrame을 Python 딕셔너리 리스트로 변환합니다.
    # 예: [{"Ticker": "005930", "Name": "삼성전자"}, ...]
    
    analysis_data = {
        "top_risers": top_risers.to_dict(orient='records'),
        "top_fallers": top_fallers.to_dict(orient='records'),
        "top_volume": top_volume.to_dict(orient='records'),
        "macd_golden_cross": macd_cross_stocks.to_dict(orient='records'),
        "bb_breakout": bb_breakout_stocks.to_dict(orient='records')
    }
    
    return analysis_data


@app.route('/api/stock-analysis', methods=['GET'])
def get_stock_analysis():
    """
    API 엔드포인트: /api/stock-analysis
    GET 요청을 받으면, 실시간으로 주식 분석을 실행하고 결과를 JSON으로 반환합니다.
    """
    logging.info("API 요청 수신... 주식 분석을 시작합니다.")
    
    try:
        # (★중요) 분석 함수 실행
        data = run_stock_analysis()
        
        if "error" in data:
            return jsonify(data), 500 # 서버 오류
        
        logging.info("분석 완료. JSON 데이터를 반환합니다.")
        
        # (★중요) 최종 결과를 JSON으로 변환하여 반환
        return jsonify({
            "analysis_date": stock.get_nearest_business_day_in_a_week(datetime.now().strftime('%Y%m%d')),
            "results": data
        })
        
    except Exception as e:
        logging.error(f"API 처리 중 심각한 오류 발생: {e}")
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    # (참고: port=5001로 설정하여 기본 포트 5000과의 충돌 방지)
    app.run(debug=True, port=5001)