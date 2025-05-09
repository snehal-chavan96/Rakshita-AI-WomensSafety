package com.example.rakshika;

import android.content.Intent;
import android.os.Bundle;
import android.util.Log;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;

import androidx.activity.EdgeToEdge;
import androidx.appcompat.app.AppCompatActivity;

import org.json.JSONObject;

import java.io.BufferedReader;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.net.HttpURLConnection;
import java.net.URL;

public class SignUp extends AppCompatActivity {

    EditText usernameInput, passwordInput, emailInput;
    Button signUP;
    TextView loginPrompt;


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        EdgeToEdge.enable(this);
        setContentView(R.layout.activity_sign_up);

        usernameInput = findViewById(R.id.username);
        passwordInput = findViewById(R.id.password);
        emailInput = findViewById(R.id.email);
        signUP = findViewById(R.id.signUpButton);
        loginPrompt = findViewById(R.id.loginPrompt);

        signUP.setOnClickListener(v -> {
            String username = usernameInput.getText().toString().trim();
            String password = passwordInput.getText().toString().trim();
            String email = emailInput.getText().toString().trim();

            if (username.isEmpty() || password.isEmpty() || email.isEmpty()) {
                Toast.makeText(SignUp.this, "All fields are required", Toast.LENGTH_SHORT).show();
                return;
            }

            new Thread(() -> {
                try {
                    // ✅ Use your actual local IP address here
                    URL url = new URL("http://172.22.106.82:5000/signup");
                    HttpURLConnection conn = (HttpURLConnection) url.openConnection();
                    conn.setRequestMethod("POST");
                    conn.setRequestProperty("Content-Type", "application/json");
                    conn.setDoOutput(true);

                    JSONObject json = new JSONObject();
                    json.put("username", username);
                    json.put("password", password);
                    json.put("email", email);

                    OutputStream os = conn.getOutputStream();
                    os.write(json.toString().getBytes("UTF-8"));
                    os.flush();
                    os.close();

                    int responseCode = conn.getResponseCode();
                    Log.d("DEBUG", "Response code: " + responseCode);

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
                    Log.d("DEBUG", "Server response: " + response.toString());

                    runOnUiThread(() -> {
                        if (responseCode == HttpURLConnection.HTTP_OK) {
                            Toast.makeText(SignUp.this, "Signup successful!", Toast.LENGTH_LONG).show();
                            Intent intent = new Intent(SignUp.this, Dashboard.class);
                            intent.putExtra("username", username);  // ✅ Send the username
                            startActivity(intent);
                            finish();
                        } else {
                            Toast.makeText(SignUp.this, "Signup failed: " + response, Toast.LENGTH_LONG).show();
                        }
                    });


                } catch (Exception e) {
                    Log.e("SignUpError", "Exception during signup", e);
                    runOnUiThread(() ->
                            Toast.makeText(SignUp.this, "Error: " + e.getMessage(), Toast.LENGTH_LONG).show()
                    );
                }
            }).start();
        });

        loginPrompt.setOnClickListener(v -> {
            Intent intent = new Intent(SignUp.this, Login.class);
            startActivity(intent);
        });
    }
}
