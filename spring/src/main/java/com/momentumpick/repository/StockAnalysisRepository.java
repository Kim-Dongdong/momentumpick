package com.momentumpick.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import com.momentumpick.domain.entity.StockAnalysis;

@Repository
public interface StockAnalysisRepository extends JpaRepository<StockAnalysis, Long> {
}
