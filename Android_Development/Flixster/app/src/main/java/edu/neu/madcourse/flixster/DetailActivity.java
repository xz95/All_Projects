package edu.neu.madcourse.flixster;

import androidx.appcompat.app.AppCompatActivity;

import android.os.Bundle;
import android.widget.RatingBar;
import android.widget.TextView;

import org.parceler.Parcels;

import edu.neu.madcourse.flixster.models.Movie;

public class DetailActivity extends AppCompatActivity {

    private static final String YOUTUBE_API_KEY = "AIzaSyDQORpJa7ci2PgeWikmPVInONiXvxd4FzY";

    TextView tvTitle;
    TextView tvOverview;
    RatingBar ratingBar;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_detail);

        tvTitle = findViewById(R.id.tvTitle);
        tvOverview = findViewById(R.id.tvOverview);
        ratingBar = findViewById(R.id.ratingBar);


        Movie movie = Parcels.unwrap(getIntent().getParcelableExtra("movie"));
        tvOverview.setText(movie.getOverview());
        tvTitle.setText(movie.getTitle());
        ratingBar.setRating((float)movie.getRating());
    }
}