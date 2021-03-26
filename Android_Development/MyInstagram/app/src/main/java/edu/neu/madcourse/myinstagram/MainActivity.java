package edu.neu.madcourse.myinstagram;

import android.content.Intent;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.net.Uri;
import android.os.Environment;
import android.provider.MediaStore;
import androidx.annotation.Nullable;
import androidx.appcompat.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.MenuItem;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ImageView;
import android.widget.Toast;

import androidx.annotation.NonNull;
import androidx.core.content.FileProvider;
import androidx.fragment.app.Fragment;
import androidx.fragment.app.FragmentManager;

import com.google.android.material.bottomnavigation.BottomNavigationItemView;
import com.google.android.material.bottomnavigation.BottomNavigationView;
import com.parse.FindCallback;
import com.parse.LogInCallback;
import com.parse.ParseException;
import com.parse.ParseFile;
import com.parse.ParseQuery;
import com.parse.ParseUser;
import com.parse.SaveCallback;

import java.io.File;
import java.util.List;

import fragments.ComposeFragment;
import fragments.PostsFragment;
import fragments.ProfileFragment;

public class MainActivity extends AppCompatActivity {
    public static final String TAG = "MainActivity";
    public static final int CAPTURE_IMAGE_ACTIVITY_REQUEST_CODE = 42;

    private BottomNavigationView bottomNavigation;
    public String photoFileName = "photo.jpg";
    private File photoFile;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        final FragmentManager fragmentManager = getSupportFragmentManager();
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        bottomNavigation = findViewById(R.id.bottomNavigation);

        bottomNavigation.setOnNavigationItemSelectedListener(
                new BottomNavigationView.OnNavigationItemSelectedListener() {
                    @Override
                    public boolean onNavigationItemSelected(@NonNull MenuItem item) {
                        Fragment fragment;
                        switch (item.getItemId()) {
                            case R.id.action_home:
                                // do something here
                                Toast.makeText(MainActivity.this, "Home",
                                        Toast.LENGTH_SHORT).show();
                                fragment = new PostsFragment();
                                break;
                            case R.id.action_compose:
                                // do something here
                                Toast.makeText(MainActivity.this, "Compose",
                                        Toast.LENGTH_SHORT).show();
                                fragment = new ComposeFragment();
                                break;
                            case R.id.action_profile:
                                // do something here
                                Toast.makeText(MainActivity.this, "Profile",
                                        Toast.LENGTH_SHORT).show();
                                fragment = new ProfileFragment();
                                break;
                            default:
                                fragment = new ComposeFragment();
                                break;
                        }
                        fragmentManager.beginTransaction().replace(R.id.flContainer, fragment).commit();
                        return true;
                    }
        });
        // Set default selection
        bottomNavigation.setSelectedItemId(R.id.action_home);
    }
}