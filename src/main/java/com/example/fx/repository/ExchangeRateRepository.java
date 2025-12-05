package com.example.fx.repository;

import com.example.fx.entity.ExchangeRate;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;

public interface ExchangeRateRepository extends JpaRepository<ExchangeRate, Long> {

    List<ExchangeRate> findByBaseCurrencyAndQuoteCurrencyOrderByRateTimeDesc(String baseCurrency, String quoteCurrency);
}
