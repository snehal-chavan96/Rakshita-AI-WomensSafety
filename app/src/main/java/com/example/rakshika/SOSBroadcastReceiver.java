package com.example.rakshika;

import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.location.Location;
import android.location.LocationManager;
import android.telephony.SmsManager;
import android.widget.Toast;
import androidx.core.content.ContextCompat;
import android.Manifest;
import android.content.pm.PackageManager;

public class SOSBroadcastReceiver extends BroadcastReceiver {
    private static final String EMERGENCY_CONTACT = "9130729050";

    @Override
    public void onReceive(Context context, Intent intent) {
        if (intent != null && "com.example.rakshika.SEND_SOS".equals(intent.getAction())) {
            sendSOS(context);
        }
    }

    private void sendSOS(Context context) {
        if (ContextCompat.checkSelfPermission(context, Manifest.permission.SEND_SMS) == PackageManager.PERMISSION_GRANTED) {
            String message = "🚨 HELP! I need assistance. My location: " + getLocation(context);
            try {
                SmsManager smsManager = SmsManager.getDefault();
                smsManager.sendTextMessage(EMERGENCY_CONTACT, null, message, null, null);
                Toast.makeText(context, "SOS Alert Sent!", Toast.LENGTH_LONG).show();
            } catch (Exception e) {
                Toast.makeText(context, "Failed to send SOS", Toast.LENGTH_LONG).show();
            }
        } else {
            Toast.makeText(context, "SMS permission not granted!", Toast.LENGTH_LONG).show();
        }
    }

    private String getLocation(Context context) {
        try {
            LocationManager locationManager = (LocationManager) context.getSystemService(Context.LOCATION_SERVICE);
            if (ContextCompat.checkSelfPermission(context, Manifest.permission.ACCESS_FINE_LOCATION) == PackageManager.PERMISSION_GRANTED) {
                Location location = locationManager.getLastKnownLocation(LocationManager.GPS_PROVIDER);
                if (location != null) {
                    return "https://maps.google.com/?q=" + location.getLatitude() + "," + location.getLongitude();
                }
            }
        } catch (SecurityException e) {
            e.printStackTrace();
        }
        return "Location not available";
    }
}
