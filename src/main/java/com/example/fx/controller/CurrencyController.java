package com.example.fx.controller;

import com.example.fx.entity.Currency;
import com.example.fx.service.CurrencyService;
import jakarta.validation.Valid;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/currencies")
public class CurrencyController {

    private final CurrencyService currencyService;

    public CurrencyController(CurrencyService currencyService) {
        this.currencyService = currencyService;
    }

    @GetMapping
    public List<Currency> getAll() {
        return currencyService.getAll();
    }

    @GetMapping("/{id}")
    public Currency getById(@PathVariable Long id) {
        return currencyService.getById(id);
    }

    @PostMapping
    public ResponseEntity<Currency> create(@Valid @RequestBody Currency currency) {
        Currency saved = currencyService.create(currency);
        return ResponseEntity.status(HttpStatus.CREATED).body(saved);
    }

    @PutMapping("/{id}")
    public Currency update(@PathVariable Long id, @Valid @RequestBody Currency currency) {
        return currencyService.update(id, currency);
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<Void> delete(@PathVariable Long id) {
        currencyService.delete(id);
        return ResponseEntity.noContent().build();
    }
}
