# FX Demo - Java Interview Test

## Build & Run

```bash
mvn clean package
java -jar target/fx-demo-0.0.1-SNAPSHOT.jar
```

H2 console: `http://localhost:8080/h2-console` (JDBC URL: `jdbc:h2:mem:fxdb`)

Swagger UI: `http://localhost:8080/swagger-ui.html`

## APIs

- `GET /api/currencies`
- `GET /api/currencies/{id}`
- `POST /api/currencies`
- `PUT /api/currencies/{id}`
- `DELETE /api/currencies/{id}`

- `GET /api/exchange-rates?base=EUR&quote=USD`
- `POST /api/exchange-rates/sync?base=EUR&quote=USD`

## Scheduler

Every 5 minutes it will call OANDA public FX API for base currencies
configured in `fx.oanda.base-currencies` and store rates in H2.
