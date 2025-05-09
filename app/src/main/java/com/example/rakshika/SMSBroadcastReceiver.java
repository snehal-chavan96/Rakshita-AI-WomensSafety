package com.example.rakshika;
import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.widget.Toast;

public class SMSBroadcastReceiver extends BroadcastReceiver {
    @Override
    public void onReceive(Context context, Intent intent) {
        int resultCode = getResultCode();
        if (resultCode == android.app.Activity.RESULT_OK) {
            Toast.makeText(context, "SOS Alert Sent!", Toast.LENGTH_SHORT).show();
        } else {
            Toast.makeText(context, "Failed to send SMS", Toast.LENGTH_SHORT).show();
        }
    }
}

