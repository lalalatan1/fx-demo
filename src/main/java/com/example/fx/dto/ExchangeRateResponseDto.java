package com.example.fx.dto;

import java.util.List;

public class ExchangeRateResponseDto {

    private String updateTime;
    private List<ExchangeRateDto> rates;

    public ExchangeRateResponseDto() {
    }

    public ExchangeRateResponseDto(String updateTime, List<ExchangeRateDto> rates) {
        this.updateTime = updateTime;
        this.rates = rates;
    }

    public String getUpdateTime() {
        return updateTime;
    }

    public void setUpdateTime(String updateTime) {
        this.updateTime = updateTime;
    }

    public List<ExchangeRateDto> getRates() {
        return rates;
    }

    public void setRates(List<ExchangeRateDto> rates) {
        this.rates = rates;
    }
}
