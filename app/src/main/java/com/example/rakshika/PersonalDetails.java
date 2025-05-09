package com.example.rakshika;

import android.content.Intent;
import android.os.Bundle;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;

import androidx.appcompat.app.AppCompatActivity;

import org.json.JSONObject;

import java.io.BufferedReader;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.net.HttpURLConnection;
import java.net.URL;

public class PersonalDetails extends AppCompatActivity {

    EditText contactInput, addressInput, trustedContactsInput;
    Button submitBtn;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_personal_details); // make sure layout name matches

        contactInput = findViewById(R.id.contactInput);
        addressInput = findViewById(R.id.addressInput);
        trustedContactsInput = findViewById(R.id.trustedContactsInput);
        submitBtn = findViewById(R.id.submitBtn);

        // Get username passed from previous activity
        String username = getIntent().getStringExtra("username");

        submitBtn.setOnClickListener(v -> {
            String contact = contactInput.getText().toString().trim();
            String address = addressInput.getText().toString().trim();
            String trustedContacts = trustedContactsInput.getText().toString().trim();

            if (contact.isEmpty() || address.isEmpty() || trustedContacts.isEmpty()) {
                Toast.makeText(PersonalDetails.this, "Please fill all fields", Toast.LENGTH_SHORT).show();
                return;
            }

            new Thread(() -> {
                try {
                    URL url = new URL("http://192.168.1.38:5000/update_details");
                    HttpURLConnection conn = (HttpURLConnection) url.openConnection();
                    conn.setRequestMethod("POST");
                    conn.setRequestProperty("Content-Type", "application/json");
                    conn.setDoOutput(true);

                    JSONObject json = new JSONObject();
                    json.put("username", username);
                    json.put("contact", contact);
                    json.put("address", address);
                    json.put("trusted_contacts", trustedContacts);

                    OutputStream os = conn.getOutputStream();
                    os.write(json.toString().getBytes("UTF-8"));
                    os.flush();
                    os.close();

                    int responseCode = conn.getResponseCode();

                    InputStream is = (responseCode >= 200 && responseCode < 400)
                            ? conn.getInputStream()
                            : conn.getErrorStream();

                    BufferedReader reader = new BufferedReader(new InputStreamReader(is));
                    StringBuilder response = new StringBuilder();
                    String line;
                    while ((line = reader.readLine()) != null) {
                        response.append(line);
                    }
                    reader.close();

                    runOnUiThread(() -> {
                        if (responseCode == HttpURLConnection.HTTP_OK) {
                            Toast.makeText(PersonalDetails.this, "Details updated successfully", Toast.LENGTH_LONG).show();
                            Intent intent = new Intent(PersonalDetails.this, Dashboard.class);
                            startActivity(intent);
                            finish();
                        } else {
                            Toast.makeText(PersonalDetails.this, "Update failed: " + response, Toast.LENGTH_LONG).show();
                        }
                    });

                } catch (Exception e) {
                    runOnUiThread(() ->
                            Toast.makeText(PersonalDetails.this, "Error: " + e.getMessage(), Toast.LENGTH_LONG).show()
                    );
                }
            }).start();
        });
    }
}
