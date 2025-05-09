package com.example.rakshika;

import android.Manifest;
import android.app.PendingIntent;
import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.content.IntentFilter;
import android.content.pm.PackageManager;
import android.location.Location;
import android.location.LocationManager;
import android.net.Uri;
import android.os.Build;
import android.os.Bundle;
import android.os.Handler;
import android.speech.RecognitionListener;
import android.speech.RecognizerIntent;
import android.speech.SpeechRecognizer;
import android.telephony.TelephonyManager;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.ImageButton;
import android.widget.Toast;

import androidx.appcompat.app.AppCompatActivity;
import androidx.core.app.ActivityCompat;

import java.util.ArrayList;
import java.util.Locale;

public class Dashboard extends AppCompatActivity {

    private static final String EMERGENCY_CONTACT = "9579461607";
    private static final String EMERGENCY_CALL_NUMBER = "9579461607";
    private SpeechRecognizer speechRecognizer;
    private Intent speechRecognizerIntent;
    private final Handler handler = new Handler();
    private static final int PERMISSION_REQUEST_CODE = 101;
    private static final String TAG = "Dashboard";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_dashboard);

        requestPermissions();

        Button PersonalDetails_btn = findViewById(R.id.PersonalDetails_btn);
        ImageButton btnShareLocation = findViewById(R.id.sos_btn);
        ImageButton safeRoute = findViewById(R.id.SafeRoute_btn);
        ImageButton fakeCallBtn = findViewById(R.id.FakeCall_btn);
//        ImageButton crimeZoneBtn = findViewById(R.id.CrimeZone_btn);  // Crime zone button

        btnShareLocation.setOnClickListener(v -> sendSOSAlert());
        safeRoute.setOnClickListener(v -> startActivity(new Intent(this, MapsActivity.class)));
//        crimeZoneBtn.setOnClickListener(v -> startActivity(new Intent(Dashboard.this, Crime_Zone.class))); // Open Crime_Zone Activity

        PersonalDetails_btn.setOnClickListener(v -> startActivity(new Intent(this, PersonalDetails.class)));
        fakeCallBtn.setOnClickListener(v -> startActivity(new Intent(this, FakeCallActivity.class)));


        ImageButton button = findViewById(R.id.CrimeZone_btn);
        button.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                String url = "http://172.22.106.82:5500/index.html";
                Intent intent = new Intent(Intent.ACTION_VIEW);
                intent.setData(Uri.parse(url));
                startActivity(intent);
            }
        });

        initializeVoiceRecognition();
        logSimInfo();
    }

    private void requestPermissions() {
        ActivityCompat.requestPermissions(this, new String[]{
                Manifest.permission.SEND_SMS,
                Manifest.permission.CALL_PHONE,
                Manifest.permission.RECORD_AUDIO,
                Manifest.permission.ACCESS_FINE_LOCATION
        }, PERMISSION_REQUEST_CODE);
    }

    private void initializeVoiceRecognition() {
        speechRecognizer = SpeechRecognizer.createSpeechRecognizer(this);
        speechRecognizerIntent = new Intent(RecognizerIntent.ACTION_RECOGNIZE_SPEECH);
        speechRecognizerIntent.putExtra(RecognizerIntent.EXTRA_LANGUAGE_MODEL, RecognizerIntent.LANGUAGE_MODEL_FREE_FORM);
        speechRecognizerIntent.putExtra(RecognizerIntent.EXTRA_LANGUAGE, Locale.getDefault());

        speechRecognizer.setRecognitionListener(new RecognitionListener() {
            @Override public void onReadyForSpeech(Bundle params) {}
            @Override public void onBeginningOfSpeech() {}
            @Override public void onRmsChanged(float rmsdB) {}
            @Override public void onBufferReceived(byte[] buffer) {}
            @Override public void onEndOfSpeech() { restartListeningWithDelay(); }
            @Override public void onError(int error) { restartListeningWithDelay(); }

            @Override
            public void onResults(Bundle results) {
                ArrayList<String> matches = results.getStringArrayList(SpeechRecognizer.RESULTS_RECOGNITION);
                if (matches != null) {
                    for (String result : matches) {
                        if (result.toLowerCase().contains("hey rakshika")) {
                            sendSOSAlert();
                            break;
                        }
                    }
                }
                restartListeningWithDelay();
            }

            @Override public void onPartialResults(Bundle partialResults) {}
            @Override public void onEvent(int eventType, Bundle params) {}
        });

        speechRecognizer.startListening(speechRecognizerIntent);
    }

    private void restartListeningWithDelay() {
        handler.postDelayed(() -> {
            if (speechRecognizer != null) {
                speechRecognizer.startListening(speechRecognizerIntent);
            }
        }, 2000);
    }

    private void sendSOSAlert() {
        String location = getLocation();
        String message = "🚨 HELP! I need assistance. My location: " + location;
        sendSOSMessage(message);
        callEmergency();
    }

    private void sendSOSMessage(String message) {
        try {
            Intent smsIntent = new Intent(Intent.ACTION_SENDTO);
            smsIntent.setData(Uri.parse("smsto:" + EMERGENCY_CONTACT));
            smsIntent.putExtra("sms_body", message);
            smsIntent.setPackage("com.google.android.apps.messaging"); // Google Messages

            if (smsIntent.resolveActivity(getPackageManager()) != null) {
                startActivity(smsIntent);
                Toast.makeText(this, "Sending SOS via Messages...", Toast.LENGTH_SHORT).show();
            } else {
                // fallback to generic chooser if Google Messages not available
                Intent fallbackIntent = new Intent(Intent.ACTION_SENDTO);
                fallbackIntent.setData(Uri.parse("smsto:" + EMERGENCY_CONTACT));
                fallbackIntent.putExtra("sms_body", message);
                startActivity(Intent.createChooser(fallbackIntent, "Choose SMS app"));
                Toast.makeText(this, "Google Messages not found. Using default app...", Toast.LENGTH_SHORT).show();
            }
        } catch (Exception e) {
            Toast.makeText(this, "Failed to send SMS: " + e.getMessage(), Toast.LENGTH_LONG).show();
        }
    }

    private void callEmergency() {
        try {
            Intent callIntent = new Intent(Intent.ACTION_CALL);
            callIntent.setData(Uri.parse("tel:" + EMERGENCY_CALL_NUMBER));
            if (ActivityCompat.checkSelfPermission(this, Manifest.permission.CALL_PHONE) == PackageManager.PERMISSION_GRANTED) {
                startActivity(callIntent);
            } else {
                Toast.makeText(this, "Call permission not granted", Toast.LENGTH_SHORT).show();
            }
        } catch (Exception e) {
            Toast.makeText(this, "Failed to make a call", Toast.LENGTH_SHORT).show();
        }
    }

    private String getLocation() {
        if (ActivityCompat.checkSelfPermission(this, Manifest.permission.ACCESS_FINE_LOCATION) == PackageManager.PERMISSION_GRANTED) {
            LocationManager locationManager = (LocationManager) getSystemService(LOCATION_SERVICE);
            Location location = locationManager.getLastKnownLocation(LocationManager.GPS_PROVIDER);
            if (location != null) {
                return "https://maps.google.com/?q=" + location.getLatitude() + "," + location.getLongitude();
            }
        }
        return "Location not available";
    }

    private void logSimInfo() {
        TelephonyManager manager = (TelephonyManager) getSystemService(Context.TELEPHONY_SERVICE);
        Log.d(TAG, "SIM State: " + manager.getSimState());
        Log.d(TAG, "Network Operator: " + manager.getNetworkOperatorName());
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.KITKAT) {
            String defaultSmsApp = android.provider.Telephony.Sms.getDefaultSmsPackage(this);
            Log.d(TAG, "Default SMS App: " + defaultSmsApp);
            if (!getPackageName().equals(defaultSmsApp)) {
                Toast.makeText(this, "Note: App is not default SMS app. SMS may not send on Android 10+", Toast.LENGTH_LONG).show();
            }
        }
    }
}
