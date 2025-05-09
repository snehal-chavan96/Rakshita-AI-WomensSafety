package com.example.rakshika;

import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;
import java.io.OutputStream;
import java.net.HttpURLConnection;
import java.net.URL;

import org.json.JSONObject;

import androidx.appcompat.app.AppCompatActivity;
public class Login extends AppCompatActivity {

    EditText username, password;
    Button login_Button;
    TextView signupText;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_login);

        username = findViewById(R.id.username);
        password = findViewById(R.id.password);
        login_Button = findViewById(R.id.loginButton);
        signupText = findViewById(R.id.signupText);

        if (login_Button == null) {
            Toast.makeText(this, "Button not found!", Toast.LENGTH_LONG).show();
            return;
        }

        signupText.setOnClickListener(v -> startActivity(new Intent(Login.this, SignUp.class)));

        login_Button.setOnClickListener(view -> {
            String user = username.getText().toString().trim();
            String pass = password.getText().toString().trim();

            if (user.isEmpty() || pass.isEmpty()) {
                Toast.makeText(Login.this, "All fields are required", Toast.LENGTH_SHORT).show();
                return;
            }

            new Thread(() -> {
                try {
                    URL url = new URL("http://172.22.106.82:5000/login"); // Replace <YOUR_IP>
                    HttpURLConnection conn = (HttpURLConnection) url.openConnection();
                    conn.setRequestMethod("POST");
                    conn.setRequestProperty("Content-Type", "application/json");
                    conn.setDoOutput(true);

                    JSONObject json = new JSONObject();
                    json.put("username", user);
                    json.put("password", pass);

                    OutputStream os = conn.getOutputStream();
                    os.write(json.toString().getBytes("UTF-8"));
                    os.close();

                    int responseCode = conn.getResponseCode();
                    if (responseCode == HttpURLConnection.HTTP_OK) {
                        runOnUiThread(() -> {
                            Toast.makeText(Login.this, "Login Successful!", Toast.LENGTH_SHORT).show();
                            Intent intent = new Intent(Login.this, Dashboard.class);
                            intent.setFlags(Intent.FLAG_ACTIVITY_NEW_TASK | Intent.FLAG_ACTIVITY_CLEAR_TASK);
                            intent.putExtra("username", user);
                            startActivity(intent);
                            finish();
                        });
                    }
                    else {
                        runOnUiThread(() ->
                                Toast.makeText(Login.this, "Invalid credentials!", Toast.LENGTH_SHORT).show()
                        );
                    }

                } catch (Exception e) {
                    runOnUiThread(() ->
                            Toast.makeText(Login.this, "Error: " + e.getMessage(), Toast.LENGTH_LONG).show()
                    );
                }
            }).start();
        });

    }
}
