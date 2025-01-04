package org.example;

import com.google.gson.Gson;
import com.google.gson.reflect.TypeToken;
import java.net.HttpURLConnection;
import java.net.URL;
import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.nio.charset.StandardCharsets;
import java.util.List;
import java.util.Arrays;

public class Main {
    public static void main(String[] args) {
        // Define the URL for the POST request
        String urlString = "http://localhost:8080/process_coordinates";  // Replace with your API URL

        // Define the JSON body for the request
        String jsonBody = "{\n" +
                "  \"upper_lat\": 40,\n" +
                "  \"lower_lat\": 39.9,\n" +
                "  \"upper_long\": -83,\n" +
                "  \"lower_long\": -82.9,\n" +
                "  \"num_x_slice\": 5,\n" +
                "  \"num_y_slice\": 5,\n" +
                "  \"gs_lat\": 30,\n" +
                "  \"gs_long\": -80,\n" +
                "  \"gs_height\": 100,\n" +
                "  \"offset\": 0\n" +
                "}";

        // Fetch JSON data from the URL by sending the POST request
        String jsonData = postJsonData(urlString, jsonBody);

        if (jsonData != null) {
            // Create a Gson instance
            Gson gson = new Gson();

            // Define the type of the data
            TypeToken<List<List<double[]>>> typeToken = new TypeToken<List<List<double[]>>>() {};

            // Deserialize the JSON data into a List of List of double arrays
            List<List<double[]>> data = gson.fromJson(jsonData, typeToken.getType());

            // Print the data correctly
            for (List<double[]> outerList : data) {
                for (double[] array : outerList) {
                    System.out.println(Arrays.toString(array));  // Print contents of each double[] array
                }
            }
        }
    }

    // Method to send a POST request with JSON body and get the response
    private static String postJsonData(String urlString, String jsonBody) {
        StringBuilder result = new StringBuilder();
        try {
            // Create a URL object from the string
            URL url = new URL(urlString);

            // Open an HTTP connection
            HttpURLConnection connection = (HttpURLConnection) url.openConnection();
            connection.setRequestMethod("POST");  // Set the request method to POST
            connection.setDoOutput(true);        // Allow sending a request body
            connection.setRequestProperty("Accept", "*/*");
            connection.setRequestProperty("Content-Type", "application/json");
            connection.setRequestProperty("User-Agent", "Java HTTP Client");

            // Send the JSON body
            try (OutputStream os = connection.getOutputStream()) {
                byte[] input = jsonBody.getBytes(StandardCharsets.UTF_8);
                os.write(input, 0, input.length);
            }

            // Read the response if the connection was successful
            int responseCode = connection.getResponseCode();
            if (responseCode == HttpURLConnection.HTTP_OK) {
                try (BufferedReader reader = new BufferedReader(new InputStreamReader(connection.getInputStream()))) {
                    String line;
                    while ((line = reader.readLine()) != null) {
                        result.append(line);
                    }
                }
            } else {
                System.out.println("Failed to fetch data. HTTP Status: " + responseCode);
                return null;
            }

        } catch (Exception e) {
            e.printStackTrace();
            return null;
        }

        return result.toString();
    }
}
