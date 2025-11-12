package com.momentumpick.converter;

import java.util.List;
import java.util.stream.Collectors;

import org.springframework.stereotype.Component;

import com.momentumpick.domain.entity.StockAnalysis;
import com.momentumpick.domain.entity.StockAnalysisDetail;
import com.momentumpick.dto.StockAnalysisDetailDto;
import com.momentumpick.dto.StockAnalysisResponse;

@Component
public class StockAnalysisConverter {

	public StockAnalysisResponse convertToDto(StockAnalysis stockAnalysis) {
		StockAnalysisResponse response = new StockAnalysisResponse();
		response.setAnalysisDate(stockAnalysis.getAnalysisDate());

		// 각 목록을 DTO로 변환
		response.setTopRisers(convertDetailsToDto(stockAnalysis.getTopRisers()));
		response.setTopFallers(convertDetailsToDto(stockAnalysis.getTopFallers()));
		response.setTopVolume(convertDetailsToDto(stockAnalysis.getTopVolume()));
		response.setMacdGoldenCross(convertDetailsToDto(stockAnalysis.getMacdGoldenCross()));
		response.setBbBreakout(convertDetailsToDto(stockAnalysis.getBbBreakout()));

		return response;
	}

	private List<StockAnalysisDetailDto> convertDetailsToDto(List<StockAnalysisDetail> details) {
		return details.stream()
			.map(detail -> {
				StockAnalysisDetailDto dto = new StockAnalysisDetailDto();
				dto.setTicker(detail.getTicker());
				dto.setName(detail.getName());
				dto.setClose(detail.getClose());
				dto.setChange5D(detail.getChange5D());
				dto.setAvgVol5D(detail.getAvgVol5D());
				dto.setMacdSignal(detail.getMacdSignal());
				dto.setBbSignal(detail.getBbSignal());
				return dto;
			})
			.collect(Collectors.toList());
	}

	public StockAnalysis convertToEntity(StockAnalysisResponse response) {
		StockAnalysis stockAnalysis = new StockAnalysis();
		stockAnalysis.setAnalysisDate(response.getAnalysisDate());

		// Convert each list of StockAnalysisDetailDto to StockAnalysisDetail entity
		stockAnalysis.setTopRisers(convertDetailsToEntity(response.getTopRisers()));
		stockAnalysis.setTopFallers(convertDetailsToEntity(response.getTopFallers()));
		stockAnalysis.setTopVolume(convertDetailsToEntity(response.getTopVolume()));
		stockAnalysis.setMacdGoldenCross(convertDetailsToEntity(response.getMacdGoldenCross()));
		stockAnalysis.setBbBreakout(convertDetailsToEntity(response.getBbBreakout()));

		return stockAnalysis;
	}

	private List<StockAnalysisDetail> convertDetailsToEntity(List<StockAnalysisDetailDto> detailDtos) {
		return detailDtos.stream()
			.map(dto -> {
				StockAnalysisDetail detail = new StockAnalysisDetail();
				detail.setTicker(dto.getTicker());
				detail.setName(dto.getName());
				detail.setClose(dto.getClose());
				detail.setChange5D(dto.getChange5D());
				detail.setAvgVol5D(dto.getAvgVol5D());
				detail.setMacdSignal(dto.getMacdSignal());
				detail.setBbSignal(dto.getBbSignal());
				return detail;
			})
			.collect(Collectors.toList());
	}
}
