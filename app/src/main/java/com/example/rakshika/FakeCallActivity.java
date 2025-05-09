package com.example.rakshika;

import android.app.Activity;
import android.media.MediaPlayer;
import android.net.Uri;
import android.os.Bundle;
import android.widget.Button;
import android.widget.VideoView;

public class FakeCallActivity extends Activity {
    private VideoView videoView;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_fake_call);

        //Initialize VideoView
        videoView = findViewById(R.id.fake_call_video);

        //Set video path from res/raw
        Uri videoUri = Uri.parse("android.resource://" + getPackageName() + "/" + R.raw.fake_call);
        videoView.setVideoURI(videoUri);

        //Start playing the fake call video
        videoView.setOnPreparedListener(mp -> videoView.start());

        //End Call Button
        Button endCall = findViewById(R.id.end_call);
        endCall.setOnClickListener(v -> {
            if (videoView.isPlaying()) {
                videoView.stopPlayback();
            }
            finish(); //Close the fake call screen
          });
    }
    @Override
    protected void onDestroy() {
        super.onDestroy();
        if (videoView.isPlaying()) {
            videoView.stopPlayback();
        }
    }
}
