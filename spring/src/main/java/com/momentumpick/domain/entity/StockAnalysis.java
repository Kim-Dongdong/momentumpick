package com.momentumpick.domain.entity;

import java.util.List;

import jakarta.persistence.CascadeType;
import jakarta.persistence.ElementCollection;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.OneToMany;
import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
@Entity
public class StockAnalysis {

	@Id
	@GeneratedValue(strategy = GenerationType.IDENTITY)
	private Long id;

	private String analysisDate;

	@OneToMany(cascade = CascadeType.ALL)
	private List<StockAnalysisDetail> topRisers;

	@OneToMany(cascade = CascadeType.ALL)
	private List<StockAnalysisDetail> topFallers;

	@OneToMany(cascade = CascadeType.ALL)
	private List<StockAnalysisDetail> topVolume;

	@OneToMany(cascade = CascadeType.ALL)
	private List<StockAnalysisDetail> macdGoldenCross;

	@OneToMany(cascade = CascadeType.ALL)
	private List<StockAnalysisDetail> bbBreakout;

	// Getters and Setters
}
