package com.mobvacc.videorecorder;

import java.io.IOException;

import android.content.Context;
import android.hardware.Camera;
import android.media.CamcorderProfile;
import android.media.MediaRecorder;
import android.util.AttributeSet;
import android.util.Log;
import android.view.SurfaceHolder;
import android.view.SurfaceView;

public class vcorderView extends SurfaceView implements
SurfaceHolder.Callback{
	
	MediaRecorder recorder;
	Camera camera;
	SurfaceHolder holder;
	String outputFile = "/sdcard/default.mp4";

    public vcorderView(Context context)
    {
        super(context);
        init();
    }
	
	public vcorderView(Context context, AttributeSet attrs) {
		super(context, attrs);
		init();
	}
	
    public vcorderView(Context context, AttributeSet attrs, int defStyle) {
        super(context, attrs, defStyle);
        init();
    }

	public void init(){
		holder = getHolder();
		holder.addCallback(this);
		holder.setType(SurfaceHolder.SURFACE_TYPE_PUSH_BUFFERS);
		

	    
	    recorder = new MediaRecorder();    
		

	    recorder.setVideoSource(MediaRecorder.VideoSource.DEFAULT);
	    recorder.setOutputFormat(MediaRecorder.OutputFormat.MPEG_4);
	    recorder.setVideoSize(720,480);
	    recorder.setVideoEncoder(MediaRecorder.VideoEncoder.DEFAULT);
	    
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
    	recorder.release();
    }

}
