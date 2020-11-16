import React, { Component } from 'react';
import RankedItem from './../ranked-item/ranked-item.jsx';
import Slider from './../slider/slider.jsx';
import './app.css';


class App extends Component {


    constructor(props)
    {
        super(props);
        this.state = {ranked_songs: [], ranked_artists: [], ranked_albums: [], values: [.500, .500, .500, .500]};
        this.search = this.search.bind(this);
        this.handleSlider = this.handleSlider.bind(this);
        this.getRankVals = this.getRankVals.bind(this);
    }


    async search(e)
    {
        var user_prefs = this.getRankVals();
        const response = await fetch('https://spotify-mood-search.herokuapp.com/rank' + user_prefs).then(res => res.json());
        this.setState({ranked_songs: response["ranked_songs"], ranked_artists: response["ranked_artists"], ranked_albums: response["ranked_albums"]});
    }


    getRankVals()
    {
        //assign value to each of these spotify stats
        var acousticness = 0.0;       //rating of how acoustic a song sounds
        var danceability = 0.0;       //how suitable a track is for dancing
        var energy = 0.0;             //measure of intensity and activeness
        var instrumentalness = 0.0;   //prediction of no vocals in a song. 1.0 means 100% sure no vocals in the song
        var liveness = 0.0;           //detects the presence of the audience in the song
        var speechiness = 0.0;        //detects the presence of spoken words in the song
        var valence = 0.0;            //rating of positivity. positiveness is 1.0  while negativeness is 0.0
        

        //this is the values of the sliders
        var slider1_val = this.state.values[0];
        var slider2_val = this.state.values[1];
        var slider3_val = this.state.values[2];
        var slider4_val = this.state.values[3];


        //slider 1 = somber -> cheerful  (valence, danceability -> valence, danceability)
        //slider 2 = peaceful -> excited (acousticness, energy -> energy, danceability)
        //slider 3 = bored -> busy (speechiness -> insturmentalness)
        //slider 4 = conscious -> natural (liveness -> liveness, acousticness)


        acousticness = (1-slider2_val)*.5 + slider4_val*.5; //(1-slider2_val) beacuse if slider is .1 that means its very relaxed==acoustic so you want to weight it high eg. 1-.2 = .8 
        danceability = slider1_val*.3 + slider2_val*.7;     //.3 and .7 is the weighting between somber->cheerful and peaceful->excited in measuring danceability
        energy = slider2_val;                               //energy has a direct relationship to peaceful -> excited
        instrumentalness = slider3_val;                     //distracted -> concentrated meaning vocals in song -> instrumentals. so like study music
        liveness = slider4_val;                             //
        speechiness = (1-slider3_val);                      //
        valence = slider1_val;                              //measure of positivity has a direct relationship to somber -> cheerful


        return '/' + acousticness + '/' + danceability + '/' + energy + '/' + instrumentalness + '/' + liveness + '/' + speechiness + '/' + valence;
    }


    handleSlider(e, i)
    {
        var tempValues = this.state.values;
        tempValues[i] = e.target.value;
        this.setState({value: tempValues})
    }


    render()
    {
        return(

            <div id="background">
                <div className="headingBox">
                    <h1 className="heading">Spotify Mood Search</h1>
                    <div className="headingUnderline"></div>
                </div>
                <div id="inputArea">
                    <div id="inputBox">
                        <h1 className="inputHeading">I feel...</h1>
                        <div className="sliders"> 
                            <Slider leftLabel="Somber" rightLabel="Cheerful" onChange={this.handleSlider.bind(this)} index={0} value={this.state.values[0]}></Slider>
                            <Slider leftLabel="Peaceful" rightLabel="Excited" onChange={this.handleSlider.bind(this)} index={1} value={this.state.values[1]}></Slider>
                            <Slider leftLabel="Bored" rightLabel="Busy" onChange={this.handleSlider.bind(this)} index={2} value={this.state.values[2]}></Slider>
                            <Slider leftLabel="Reserved" rightLabel="Intimate" onChange={this.handleSlider.bind(this)} index={3} value={this.state.values[3]}></Slider>
                        </div>
                        <div onClick={this.search} className="submitBtn">
                            <h3>Search</h3>
                        </div>
                    </div>
                </div>
                <div id="outputArea">
                    <div id="songOutput" className="outputBox">
                        <div className="outputBoxHeader">
                            <h1>Songs</h1>
                        </div>
                        <div className="itemArea">
                            {
                                this.state.ranked_songs.map((song, index) =>
                                
                                    <RankedItem key={song.songName + " " + index} item={song} type="song" className={index===0 ? "rankedItem first" : (index===this.state.ranked_songs.length-1 ? "rankedItem last" : "rankedItem middle")}></RankedItem>
                                )
                            }
                        </div>
                    </div>
                    <div id="artistOutput" className="outputBox">
                        <div className="outputBoxHeader">
                            <h1>Artists</h1>
                        </div>
                        <div className="itemArea">
                            {
                                this.state.ranked_artists.map((artist, index) =>
                                
                                    <RankedItem key={artist.artistName + " " + index} item={artist} type="artist" className={index===0 ? "rankedItem first" : (index===this.state.ranked_artists.length-1 ? "rankedItem last" : "rankedItem middle")}></RankedItem>
                                )
                            }
                        </div>
                    </div>
                    <div id="albumOutput" className="outputBox">
                        <div className="outputBoxHeader">
                            <h1>Albums</h1>
                        </div>
                        <div className="itemArea">
                            {
                                this.state.ranked_albums.map((album, index) => 
                                
                                    <RankedItem key={album.albumName + " " + album} item={album} type="album" className={index===0 ? "rankedItem first" : (index===this.state.ranked_albums.length-1 ? "rankedItem last" : "rankedItem middle")}></RankedItem>
                                )
                            }
                        </div>
                    </div>
                </div>
            </div>
        );
    }
}


export default App;