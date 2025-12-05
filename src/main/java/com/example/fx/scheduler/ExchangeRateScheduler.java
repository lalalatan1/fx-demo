package com.example.fx.scheduler;

import com.example.fx.service.ExchangeRateService;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Component;

@Component
public class ExchangeRateScheduler {

    private static final Logger log = LoggerFactory.getLogger(ExchangeRateScheduler.class);

    private final ExchangeRateService exchangeRateService;

    @Value("${fx.oanda.base-currencies}")
    private String baseCurrencies;

    @Value("${fx.oanda.quote}")
    private String quote;

    public ExchangeRateScheduler(ExchangeRateService exchangeRateService) {
        this.exchangeRateService = exchangeRateService;
    }

    // Every 5 minutes
    @Scheduled(cron = "0 */1 * * * *")  // mỗi 1 phút
    public void syncRates() {
        if (baseCurrencies == null || baseCurrencies.isEmpty()) {
            return;
        }
        String[] bases = baseCurrencies.split(",");
        for (String base : bases) {
            String trimmed = base.trim();
            if (trimmed.isEmpty()) {
                continue;
            }
            try {
                log.info("Scheduled sync for base={} quote={}", trimmed, quote);
                exchangeRateService.syncRates(trimmed, quote);
            } catch (Exception ex) {
                log.error("Error during scheduled sync for base={} quote={}", trimmed, quote, ex);
            }
        }
    }
}
