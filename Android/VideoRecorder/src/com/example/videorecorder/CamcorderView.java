package com.example.videorecorder;

import java.io.IOException;

import com.example.videorecorder.R;
import android.content.Context;
import android.graphics.Canvas;
import android.hardware.Camera;
import android.media.CamcorderProfile;
import android.media.MediaRecorder;
import android.util.AttributeSet;
import android.util.Log;
import android.view.SurfaceHolder;
import android.view.SurfaceView;
import android.widget.TextView;

public class CamcorderView extends SurfaceView implements
		SurfaceHolder.Callback {

	MediaRecorder recorder;
	Camera camera;
	SurfaceHolder holder;
	String outputFile = "/sdcard/default.mp4";

	public CamcorderView(Context context, AttributeSet attrs) {
		super(context, attrs);
		holder = getHolder();
		holder.addCallback(this);
		holder.setType(SurfaceHolder.SURFACE_TYPE_PUSH_BUFFERS);
		

		try{
			camera = Camera.open();
			Camera.Parameters param = camera.getParameters();
			param.set("cam_mode", 1);
	    	param.setPreviewSize(1280, 720);
	    	param.setFocusMode(Camera.Parameters.FOCUS_MODE_INFINITY);
	    	camera.setParameters(param);
			camera.setPreviewDisplay(holder);
		    camera.unlock();
		} catch (IOException e) {
			e.printStackTrace();
		}
		
	    recorder = new MediaRecorder();
	    recorder.setCamera(camera);

	    
	    recorder.setAudioSource(MediaRecorder.AudioSource.MIC);
	    recorder.setVideoSource(MediaRecorder.VideoSource.CAMERA);

	  
	    CamcorderProfile profile = CamcorderProfile.get(CamcorderProfile.QUALITY_720P);
	    profile.videoFrameWidth = 1280;
	    profile.videoFrameHeight = 720;
	    recorder.setProfile(profile);


	    
		//////////////////////////
		//recorder.setVideoSource(MediaRecorder.VideoSource.CAMERA);
		//recorder.setOutputFormat(MediaRecorder.OutputFormat.THREE_GPP);
		//recorder.setVideoSize(1920, 1080);
		//recorder.setVideoEncoder(MediaRecorder.VideoEncoder.H263);
		//recorder.setVideoFrameRate(30);
	    //
		      
	}

	public void surfaceCreated(SurfaceHolder holder) {
		recorder.setOutputFile(outputFile);
		recorder.setPreviewDisplay(holder.getSurface());
		if (recorder != null) {
			try {
				recorder.prepare();
			} catch (IllegalStateException e) {
				Log.e("IllegalStateException", e.toString());
			} catch (IOException e) {
				Log.e("IOException", e.toString());
			}
		}
	}
	
	public void surfaceChanged(SurfaceHolder holder, int format, int width,
			int height) {
	}

	public void surfaceDestroyed(SurfaceHolder holder) {
	}

	public void setOutputFile(String filename)
	{
		outputFile = filename;
		recorder.setOutputFile(filename);
	}
	
    public void startRecording()
    {
    	recorder.start();
    }
    
    public void stopRecording()
    {
    	recorder.stop();
    	try {
			camera.reconnect();
		} catch (IOException e) {
			e.printStackTrace();
		}
    	camera.stopPreview();
    	camera.release();
    	recorder.release();
    }
    

}