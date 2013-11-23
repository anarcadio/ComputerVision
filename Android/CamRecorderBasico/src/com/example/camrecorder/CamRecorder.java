package com.example.camrecorder;

import java.util.Date;
import com.mobvcasting.camcorder.R;
import com.mobvcasting.camcorder.R.id;
import com.mobvcasting.camcorder.R.layout;

import android.app.Activity;
import android.content.pm.ActivityInfo;
import android.os.Bundle;
import android.util.Log;
import android.view.KeyEvent;
import android.view.Window;

public class CamRecorder extends Activity {

	     private CamcorderView camcorderView; 
	     private boolean recording = false; 

	     /** Called when the activity is first created. */ 
	     @Override 
	     public void onCreate(Bundle savedInstanceState) { 
	          super.onCreate(savedInstanceState); 
	          requestWindowFeature(Window.FEATURE_NO_TITLE); 
	          setRequestedOrientation(ActivityInfo.SCREEN_ORIENTATION_LANDSCAPE); 
	          setContentView(R.layout.camcorder_preview); 
	          
	          setRequestedOrientation(ActivityInfo.SCREEN_ORIENTATION_LANDSCAPE);
	          Date date=new Date();
	          String filename="/sdcard/rec"+date.toString().replace(" ", "_").replace(":", "_")+".3gp";
	          camcorderView = (CamcorderView) findViewById(R.id.camcorder_preview); 
	          camcorderView.setOutputFile(filename);
 	     } 
	     
         @Override 
         public boolean onKeyDown(int keyCode, KeyEvent event) 
         { 
             if (keyCode == KeyEvent.KEYCODE_VOLUME_UP) 
             { 
           	  if (recording) { 
           		  	camcorderView.stopRecording();
                    finish(); 
                } else { 
                    recording = true; 
                    camcorderView.startRecording(); 
                } 
                 return true; 
             } 
             return super.onKeyDown(keyCode, event); 
         }	     
}