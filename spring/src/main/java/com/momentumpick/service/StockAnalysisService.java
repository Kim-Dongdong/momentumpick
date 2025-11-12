package com.momentumpick.service;

import java.util.Optional;

import com.momentumpick.domain.entity.StockAnalysis;

public interface StockAnalysisService {
	// FastAPI에서 주식 분석 결과를 가져와 DB에 저장
	void saveStockAnalysis();

	// DB에서 주식 분석 결과를 조회
	Optional<StockAnalysis> getStockAnalysisById(Long id);
}
