package com.example.fx.external;

import com.example.fx.dto.OandaDailyData;
import com.example.fx.dto.OandaResponseWrapper;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;

@Component
public class OandaClient {

    @Value("${fx.oanda.base-url}")
    private String baseUrl;

    private final ObjectMapper mapper = new ObjectMapper();

    public OandaDailyData getDailyRate(String base, String quote,
                                       String startDate, String endDate) {

        try {
            String url = String.format(
                    "%s/cc-api/currencies?base=%s&quote=%s&data_type=chart&start_date=%s&end_date=%s",
                    baseUrl, base, quote, startDate, endDate
            );

            String json = HttpClientHelper.get(url);

            OandaResponseWrapper wrapper =
                    mapper.readValue(json, OandaResponseWrapper.class);

            if (wrapper.response == null || wrapper.response.isEmpty()) {
                return null;
            }

            return wrapper.response.get(0);

        } catch (Exception e) {
            throw new RuntimeException("Failed to call OANDA API", e);
        }
    }
}
