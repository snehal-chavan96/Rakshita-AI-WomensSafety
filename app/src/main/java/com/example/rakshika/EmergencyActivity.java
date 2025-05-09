package com.example.rakshika;

import android.Manifest;
import android.app.PendingIntent;
import android.content.Context;
import android.content.Intent;
import android.net.Uri;

import android.content.pm.PackageManager;
import android.util.Log;


import android.Manifest;
import android.os.Bundle;
import android.telephony.SmsManager;
import android.widget.ImageButton;
import android.widget.Toast;
import android.location.Location;
import android.location.LocationManager;
import android.os.Bundle;
import android.telephony.SmsManager;
import android.widget.Button;
import android.widget.Toast;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.app.ActivityCompat;
import androidx.core.content.ContextCompat;

public class EmergencyActivity extends AppCompatActivity {
    private static final String EMERGENCY_CONTACT = "9130729050"; // Correct number added

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_dashboard); // Ensure the correct layout file is used

        // Request SMS permissions
        ActivityCompat.requestPermissions(this, new String[]{Manifest.permission.SEND_SMS}, 1);

        ImageButton btnShareLocation = findViewById(R.id.sos_btn);
        btnShareLocation.setOnClickListener(v -> shareLocation());
    }

    private void shareLocation() {
        String message = "📍 Help Me  My current location: https://maps.google.com/?q=18.6776,73.8987";
        try {
            SmsManager smsManager = SmsManager.getDefault();
            smsManager.sendTextMessage(EMERGENCY_CONTACT, null, message, null, null);
            Toast.makeText(this, "Location Sent!", Toast.LENGTH_SHORT).show();
        } catch (Exception e) {
            e.printStackTrace();
            Toast.makeText(this, "Failed to send location", Toast.LENGTH_SHORT).show();
        }
    }
}



