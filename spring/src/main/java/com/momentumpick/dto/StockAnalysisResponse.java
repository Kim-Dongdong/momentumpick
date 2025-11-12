package com.momentumpick.dto;

import java.util.List;

import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
public class StockAnalysisResponse {

	private String analysisDate;

	private List<StockAnalysisDetailDto> topRisers;

	private List<StockAnalysisDetailDto> topFallers;

	private List<StockAnalysisDetailDto> topVolume;

	private List<StockAnalysisDetailDto> macdGoldenCross;

	private List<StockAnalysisDetailDto> bbBreakout;
}
