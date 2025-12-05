package com.example.fx.external;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.IOException;
import java.net.HttpURLConnection;
import java.net.URL;

public class HttpClientHelper {

    public static String get(String urlStr) throws IOException {
        URL url = new URL(urlStr);

        HttpURLConnection con = (HttpURLConnection) url.openConnection();
        con.setRequestMethod("GET");

        // Timeout
        con.setConnectTimeout(10000);
        con.setReadTimeout(10000);

        // Expect JSON
        con.setRequestProperty("Accept", "application/json");

        int status = con.getResponseCode();

        BufferedReader in = new BufferedReader(
                new InputStreamReader(
                        status >= 200 && status < 300
                                ? con.getInputStream()
                                : con.getErrorStream()
                )
        );

        String inputLine;
        StringBuilder content = new StringBuilder();

        while ((inputLine = in.readLine()) != null) {
            content.append(inputLine);
        }

        in.close();
        con.disconnect();

        return content.toString();
    }
}
