package com.example.fx.service;

import com.example.fx.entity.Currency;
import com.example.fx.exception.NotFoundException;
import com.example.fx.repository.CurrencyRepository;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;

@Service
@Transactional
public class CurrencyService {

    private final CurrencyRepository currencyRepository;

    public CurrencyService(CurrencyRepository currencyRepository) {
        this.currencyRepository = currencyRepository;
    }

    @Transactional(readOnly = true)
    public List<Currency> getAll() {
        return currencyRepository.findAllByOrderByCodeAsc();
    }

    @Transactional(readOnly = true)
    public Currency getById(Long id) {
        return currencyRepository.findById(id)
                .orElseThrow(() -> new NotFoundException("Currency not found"));
    }

    public Currency create(Currency currency) {
        return currencyRepository.save(currency);
    }

    public Currency update(Long id, Currency update) {
        Currency existing = getById(id);
        existing.setCode(update.getCode());
        existing.setName(update.getName());
        return currencyRepository.save(existing);
    }

    public void delete(Long id) {
        currencyRepository.deleteById(id);
    }
}
