package edu.neu.madcourse.myinstagram;

import android.app.Application;

import com.parse.Parse;
import com.parse.ParseObject;

import okhttp3.OkHttpClient;

public class ParseApplication extends Application {




    @Override
    public void onCreate() {
        super.onCreate();

        // Register your parse models
        ParseObject.registerSubclass(Post.class);

        Parse.initialize(new Parse.Configuration.Builder(this)
                .applicationId("EYvVF6zEa7llUf55Ts4WVDpDpHAqKCMnlpFXV9RO")
                .clientKey("fpkvDM6f5nW5ch3Zyo8Y8fNUZiOrD1IbniMyDWhe")
                .server("https://parseapi.back4app.com")
                .build()
        );
    }
}
