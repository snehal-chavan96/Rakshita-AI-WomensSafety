package com.example.rakshika;

import android.os.Bundle;
import android.util.Log;
import androidx.appcompat.app.AppCompatActivity;
import okhttp3.*;

        import org.json.JSONObject;
import java.io.IOException;
import android.widget.TextView;

public class Crime_Zone extends AppCompatActivity {

    private final OkHttpClient client = new OkHttpClient();
    private static final String API_URL = "http://172.22.106.82:5000/safer-route";

    private TextView responseText;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_crime_zone);

        responseText = findViewById(R.id.responseText);
        sendRouteRequest("Shivajinagar, Pune", "Viman Nagar, Pune");
    }

    private void sendRouteRequest(String origin, String destination) {
        try {
            JSONObject json = new JSONObject();
            json.put("origin", origin);
            json.put("destination", destination);

            RequestBody body = RequestBody.create(
                    MediaType.parse("application/json"),
                    json.toString()
            );

            Request request = new Request.Builder()
                    .url(API_URL)
                    .post(body)
                    .build();

            client.newCall(request).enqueue(new Callback() {
                @Override
                public void onFailure(Call call, IOException e) {
                    runOnUiThread(() -> responseText.setText("Request failed: " + e.getMessage()));
                }

                @Override
                public void onResponse(Call call, Response response) throws IOException {
                    if (!response.isSuccessful()) {
                        runOnUiThread(() -> responseText.setText("Unexpected response: " + response));
                        return;
                    }

                    String responseData = response.body().string();
                    runOnUiThread(() -> responseText.setText("Response: " + responseData));
                }
            });

        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
