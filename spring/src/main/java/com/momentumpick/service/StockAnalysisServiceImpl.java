package com.momentumpick.service;

import java.util.Optional;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.momentumpick.converter.StockAnalysisConverter;
import com.momentumpick.domain.entity.StockAnalysis;
import com.momentumpick.dto.StockAnalysisResponse;
import com.momentumpick.repository.StockAnalysisRepository;

@Service
public class StockAnalysisServiceImpl implements StockAnalysisService {

	@Autowired
	private StockAnalysisRepository stockAnalysisRepository;

	@Autowired
	private StockAnalysisApiService stockAnalysisApiService;

	@Autowired
	private StockAnalysisConverter stockAnalysisConverter;

	@Override
	public void saveStockAnalysis() {
		// FastAPI에서 데이터 받아오기
		StockAnalysisResponse response = stockAnalysisApiService.getStockAnalysis();

		if (response == null) {
			// 만약 FastAPI에서 데이터가 없으면 예외를 던지거나 처리
			throw new RuntimeException("FastAPI에서 데이터를 가져오는 데 실패했습니다.");
		}

		// 결과를 엔티티로 변환
		StockAnalysis stockAnalysis = stockAnalysisConverter.convertToEntity(response);

		// 엔티티를 DB에 저장
		stockAnalysisRepository.save(stockAnalysis);
	}

	@Override
	public Optional<StockAnalysis> getStockAnalysisById(Long id) {
		return stockAnalysisRepository.findById(id);
	}
}
