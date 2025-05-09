package com.example.rakshika;

import android.content.Intent;
import android.os.Bundle;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;

import androidx.appcompat.app.AppCompatActivity;

import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.toolbox.JsonObjectRequest;
import com.android.volley.toolbox.Volley;

import org.json.JSONObject;

public class PersonalDetailsActivity extends AppCompatActivity {

    EditText contactInput, addressInput, trustedContactsInput;
    Button submitBtn;

    String postUrl = "http://172.22.106.82:5000/update_details"; // Replace with actual URL

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_personal_details);

        contactInput = findViewById(R.id.contactInput);
        addressInput = findViewById(R.id.addressInput);
        trustedContactsInput = findViewById(R.id.trustedContactsInput);
        submitBtn = findViewById(R.id.submitBtn);

        submitBtn.setOnClickListener(v -> sendDetailsToServer());
    }

    private void sendDetailsToServer() {
        String contact = contactInput.getText().toString().trim();
        String address = addressInput.getText().toString().trim();
        String trustedContacts = trustedContactsInput.getText().toString().trim();

        // You can retrieve the username from previous activity via intent if needed
        // Example:
        // String username = getIntent().getStringExtra("username");

        try {
            JSONObject json = new JSONObject();
            json.put("contact", contact);
            json.put("address", address);
            json.put("trusted_contacts", trustedContacts);

            RequestQueue queue = Volley.newRequestQueue(this);
            JsonObjectRequest request = new JsonObjectRequest(Request.Method.POST, postUrl, json,
                    response -> {
                        Toast.makeText(this, "Details updated successfully", Toast.LENGTH_SHORT).show();
                        startActivity(new Intent(PersonalDetailsActivity.this, Dashboard.class));
                        finish();
                    },
                    error -> Toast.makeText(this, "Error: " + error.toString(), Toast.LENGTH_SHORT).show()
            );

            queue.add(request);

        } catch (Exception e) {
            e.printStackTrace();
            Toast.makeText(this, "Error preparing request", Toast.LENGTH_SHORT).show();
        }
    }
}
