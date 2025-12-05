package com.example.fx.dto;

import java.math.BigDecimal;
import java.time.LocalDateTime;

public class ExchangeRateDto {

    private String baseCurrency;
    private String quoteCurrency;
    private BigDecimal rate;
    private LocalDateTime rateTime;

    public ExchangeRateDto() {
    }

    public ExchangeRateDto(String baseCurrency, String quoteCurrency, BigDecimal rate, LocalDateTime rateTime) {
        this.baseCurrency = baseCurrency;
        this.quoteCurrency = quoteCurrency;
        this.rate = rate;
        this.rateTime = rateTime;
    }

    public String getBaseCurrency() {
        return baseCurrency;
    }

    public void setBaseCurrency(String baseCurrency) {
        this.baseCurrency = baseCurrency;
    }

    public String getQuoteCurrency() {
        return quoteCurrency;
    }

    public void setQuoteCurrency(String quoteCurrency) {
        this.quoteCurrency = quoteCurrency;
    }

    public BigDecimal getRate() {
        return rate;
    }

    public void setRate(BigDecimal rate) {
        this.rate = rate;
    }

    public LocalDateTime getRateTime() {
        return rateTime;
    }

    public void setRateTime(LocalDateTime rateTime) {
        this.rateTime = rateTime;
    }
}
