package com.momentumpick.dto;

import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
public class StockAnalysisDetailDto {

	private String ticker;
	private String name;

	// "Close(원)"을 필드명으로 사용
	private double close;

	// "Change_5D(%)"을 필드명으로 사용
	private double change5D;

	// "Avg_Vol_5D"를 필드명으로 사용
	private double avgVol5D;

	// MACD Signal
	private String macdSignal;

	// Bollinger Band Signal
	private String bbSignal;
}
