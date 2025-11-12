package com.momentumpick.service;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

import com.momentumpick.dto.StockAnalysisResponse;

@Service
public class StockAnalysisApiService {

	private final String FASTAPI_URL = "http://fastapi:8000/api/stock-analysis"; // FastAPI URL

	@Autowired
	private RestTemplate restTemplate;

	public StockAnalysisResponse getStockAnalysis() {
		// FastAPI에서 주식 분석 결과를 가져오는 요청
		return restTemplate.getForObject(FASTAPI_URL, StockAnalysisResponse.class);
	}
}
