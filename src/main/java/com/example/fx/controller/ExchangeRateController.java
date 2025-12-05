package com.example.fx.controller;

import com.example.fx.dto.ExchangeRateResponseDto;
import com.example.fx.service.ExchangeRateService;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/exchange-rates")
public class ExchangeRateController {

    private final ExchangeRateService exchangeRateService;

    public ExchangeRateController(ExchangeRateService exchangeRateService) {
        this.exchangeRateService = exchangeRateService;
    }

    @GetMapping
    public ExchangeRateResponseDto getLatest(
            @RequestParam String base,
            @RequestParam String quote) {
        return exchangeRateService.getLatestRates(base, quote);
    }

    @PostMapping("/sync")
    public ResponseEntity<Void> sync(
            @RequestParam String base,
            @RequestParam String quote) {
        exchangeRateService.syncRates(base, quote);
        return ResponseEntity.accepted().build();
    }
}
