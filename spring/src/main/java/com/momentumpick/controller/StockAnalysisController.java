package com.momentumpick.controller;

import java.util.Optional;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.autoconfigure.AutoConfigureOrder;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RestController;

import com.momentumpick.apiPayload.ApiResponse;
import com.momentumpick.apiPayload.code.status.ErrorStatus;
import com.momentumpick.apiPayload.exception.handler.DBHandler;
import com.momentumpick.converter.StockAnalysisConverter;
import com.momentumpick.domain.entity.StockAnalysis;
import com.momentumpick.dto.StockAnalysisResponse;
import com.momentumpick.service.StockAnalysisService;

import lombok.RequiredArgsConstructor;

@RestController
@RequiredArgsConstructor
public class StockAnalysisController {

	private final StockAnalysisService stockAnalysisService;

	private final StockAnalysisConverter stockAnalysisConverter;

	// 주식 분석 데이터를 FastAPI에서 가져와 DB에 저장하는 API
	@GetMapping("/api/stock-analysis")
	public ApiResponse<String> fetchAndSaveStockAnalysis() {
		try {
			// FastAPI에서 주식 분석 데이터를 가져와 DB에 저장
			stockAnalysisService.saveStockAnalysis();
			return ApiResponse.onSuccess("주식 분석 데이터가 DB에 저장되었습니다.");
		} catch (Exception e) {
			// 예외가 발생하면 오류 메시지를 반환
			throw new DBHandler(ErrorStatus.DB_EXCEPTION);
		}
	}

	// 특정 ID에 해당하는 주식 분석 결과를 DB에서 조회하여 반환
	@GetMapping("/api/stock-analysis/{id}")
	public ResponseEntity<StockAnalysisResponse> getStockAnalysisById(@PathVariable Long id) {
		Optional<StockAnalysis> stockAnalysisOptional = stockAnalysisService.getStockAnalysisById(id);

		if (stockAnalysisOptional.isPresent()) {
			// StockAnalysis 엔티티를 DTO로 변환하여 반환
			StockAnalysis stockAnalysis = stockAnalysisOptional.get();
			StockAnalysisResponse response = stockAnalysisConverter.convertToDto(stockAnalysis);
			return ResponseEntity.ok(response);
		} else {
			// 결과가 없을 경우 404 Not Found 응답
			return ResponseEntity.status(404).body(null);
		}
	}

}
