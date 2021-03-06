package com.mobvacc.videorecorder;

import android.os.Bundle;
import android.app.Activity;
import android.view.Menu;

import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;
import java.text.SimpleDateFormat;
import java.util.Date;
import com.mobvacc.videorecorder.R;
import com.mobvacc.videorecorder.R.id;
import com.mobvacc.videorecorder.R.layout;


import android.content.Context;
import android.content.pm.ActivityInfo;
import android.hardware.Sensor;
import android.hardware.SensorEvent;
import android.hardware.SensorEventListener;
import android.hardware.SensorManager;
import android.os.Environment;
import android.util.Log;
import android.view.KeyEvent;
import android.view.Window;

public class MainActivity extends Activity implements SensorEventListener{

	private SensorManager mSensorManager;
	private Sensor mAccelerometer;
    private vcorderView camcorderView; 
    private boolean recording = false; 
    FileOutputStream outputAcc;

    @Override 
    public void onCreate(Bundle savedInstanceState) { 
         super.onCreate(savedInstanceState); 
         requestWindowFeature(Window.FEATURE_NO_TITLE); 
         setRequestedOrientation(ActivityInfo.SCREEN_ORIENTATION_LANDSCAPE); 
         setContentView(R.layout.activity_main);
         setRequestedOrientation(ActivityInfo.SCREEN_ORIENTATION_LANDSCAPE);
         Date date=new Date();
         String dateString =date.toString().replace(" ", "_").replace(":", "_");
         String filename="/sdcard/rec"+dateString+".mp4";
         String Accfilename="acc"+dateString+".txt";
         //camera init
         //
         camcorderView = (vcorderView) findViewById(R.id.vcorderView1); 
         camcorderView.setOutputFile(filename);
         
         //accelerometer init
         mSensorManager = (SensorManager) getSystemService(Context.SENSOR_SERVICE);
         mAccelerometer = mSensorManager.getDefaultSensor(Sensor.TYPE_LINEAR_ACCELERATION);
         
         //open accelerometer file
         File file = new File(Environment.getExternalStorageDirectory() + File.separator +  Accfilename);

         //write the bytes in file
         if(!file.exists())
         {
	          try {
				file.createNewFile();
			} catch (IOException e) {
				e.printStackTrace();
			}
         }     
         try {
			outputAcc = new FileOutputStream(file);
		} catch (FileNotFoundException e) {
			e.printStackTrace();
		}

     } 

    
    @Override 
    public boolean onKeyDown(int keyCode, KeyEvent event) 
    { 
        if (keyCode == KeyEvent.KEYCODE_VOLUME_UP) 
        { 
      	  if (recording) { 
      		  	camcorderView.stopRecording();
      		  	mSensorManager.unregisterListener(this);
      		  	try {
					outputAcc.close();
				} catch (IOException e) {
					e.printStackTrace();
				}
               finish(); 
           } else { 
               recording = true;
 	          	mSensorManager.registerListener(this, mAccelerometer , SensorManager.SENSOR_DELAY_FASTEST);
               camcorderView.startRecording(); 
               
   		    SimpleDateFormat fecha = new SimpleDateFormat("HH:mm:ss.SSS");
   		    String fecha_str = fecha.format(new Date());
   			String output = fecha_str+"\n";
   			try {
   				outputAcc.write(output.getBytes());
   			} catch (IOException e) {
   				e.printStackTrace();
   			}
   			
           } 
            return true; 
        } 
        return super.onKeyDown(keyCode, event); 
    }

	@Override
	public void onAccuracyChanged(Sensor sensor, int accuracy) {
		
	}

	@Override
	public void onSensorChanged(SensorEvent event) {
		
	    SimpleDateFormat fecha = new SimpleDateFormat("HH:mm:ss.SSS");
	    String fecha_str = fecha.format(new Date());
		
		//esto es así porque la pantalla está girada 
		float x = event.values[1];
		float y = event.values[0];
		float z = event.values[2];
		String output = Float.toString(x)+" "+Float.toString(y)+" "+" "+fecha_str+"\n";
		try {
			outputAcc.write(output.getBytes());
		} catch (IOException e) {
			e.printStackTrace();
		}
	}	     
    
    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // Inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.main, menu);
        return true;
    }
    
}


