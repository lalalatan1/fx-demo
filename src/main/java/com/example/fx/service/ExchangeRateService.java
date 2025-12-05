package com.example.fx.service;

import com.example.fx.dto.*;
import com.example.fx.entity.ExchangeRate;
import com.example.fx.external.OandaClient;
import com.example.fx.repository.ExchangeRateRepository;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.OffsetDateTime;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

@Service
@Transactional
public class ExchangeRateService {

    private static final Logger log = LoggerFactory.getLogger(ExchangeRateService.class);

    private final OandaClient oandaClient;
    private final ExchangeRateRepository exchangeRateRepository;

    @Value("${fx.oanda.start-date}")
    private String startDate;

    @Value("${fx.oanda.end-date}")
    private String endDate;

    public ExchangeRateService(OandaClient oandaClient, ExchangeRateRepository exchangeRateRepository) {
        this.oandaClient = oandaClient;
        this.exchangeRateRepository = exchangeRateRepository;
    }

    public List<ExchangeRate> syncRates(String base, String quote) {

        OandaDailyData data = oandaClient.getDailyRate(base, quote, startDate, endDate);

        if (data == null) {
            return List.of();
        }

        ExchangeRate rate = new ExchangeRate();
        rate.setBaseCurrency(data.baseCurrency);
        rate.setQuoteCurrency(data.quoteCurrency);
        rate.setRate(data.averageAsk); // dùng ask hoặc bid tuỳ yêu cầu
        rate.setRateTime(OffsetDateTime.parse(data.closeTime).toLocalDateTime());

        return List.of(exchangeRateRepository.save(rate));
    }

    @Transactional(readOnly = true)
    public ExchangeRateResponseDto getLatestRates(String base, String quote) {
        List<ExchangeRate> list = exchangeRateRepository
                .findByBaseCurrencyAndQuoteCurrencyOrderByRateTimeDesc(base, quote);

        if (list.isEmpty()) {
            return new ExchangeRateResponseDto(null, Collections.emptyList());
        }

        LocalDateTime newestTime = list.get(0).getRateTime();
        List<ExchangeRateDto> result = new ArrayList<>();
        for (ExchangeRate er : list) {
            ExchangeRateDto dto = new ExchangeRateDto(
                    er.getBaseCurrency(),
                    er.getQuoteCurrency(),
                    er.getRate(),
                    er.getRateTime()
            );
            result.add(dto);
        }

        DateTimeFormatter fmt = DateTimeFormatter.ofPattern("yyyy/MM/dd HH:mm:ss");
        String updateTime = newestTime.format(fmt);
        return new ExchangeRateResponseDto(updateTime, result);
    }
}
