package com.example.fx.dto;

import com.fasterxml.jackson.annotation.JsonProperty;

import java.math.BigDecimal;

public class OandaDailyData {

    @JsonProperty("base_currency")
    public String baseCurrency;

    @JsonProperty("quote_currency")
    public String quoteCurrency;

    @JsonProperty("close_time")
    public String closeTime;

    @JsonProperty("average_bid")
    public BigDecimal averageBid;

    @JsonProperty("average_ask")
    public BigDecimal averageAsk;

    @JsonProperty("high_bid")
    public BigDecimal highBid;

    @JsonProperty("high_ask")
    public BigDecimal highAsk;

    @JsonProperty("low_bid")
    public BigDecimal lowBid;

    @JsonProperty("low_ask")
    public BigDecimal lowAsk;
}
