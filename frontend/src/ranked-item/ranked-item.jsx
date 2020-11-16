import React, { Component } from 'react';
import altAlbum from './img/music-album.png';
import './ranked-item.css'


class RankedItem extends Component {


    constructor(props)
    {
        super(props)

        this.state = {img: altAlbum, expandedView: false}
        this.expand = this.expand.bind(this);
    }

    
    async componentDidMount()
    {
        var id = ""
        if(this.props.type === "song")
            id = this.props.item.albumID
        else if(this.props.type === "artist")
            id = this.props.item.artistID
        else
            id = this.props.item.albumID

        var item_image;
        await fetch('https://spotify-mood-search.herokuapp.com/img/' + id).then(response => response.blob()).then(image => {item_image = URL.createObjectURL(image)});
        this.setState({img: item_image});
    }


    expand()
    {
        var temp = !this.state.expandedView;
        this.setState({expandedView: temp});
    }
    

    render()
    {

        if(this.props.type === "song")
        {
            if(this.state.expandedView)
            {
                return(
                    
                    <div onClick={this.expand} className={this.props.className + " expandedSong"}>
                        <img src={this.state.img} alt="" className="itemPicture"></img>
                        <div  className="partition"></div>
                        <div className="itemContent">
                            <p>
                                {this.props.item.songName}
                            </p>
                            <p>
                                By {this.props.item.artistName}
                            </p>
                        </div>
                        <div className="secondPartition"></div>
                        <iframe className="spotifySongPlayer" src={"https://open.spotify.com/embed/track/" + this.props.item.songID} frameBorder="0" allow="encrypted-media"></iframe>
                    </div>
                );
            }
            else
            {
                return(
                    
                    <div onClick={this.expand} className={this.props.className}>
                        <img src={this.state.img} alt="" className="itemPicture"></img>
                        <div  className="partition"></div>
                        <div className="itemContent">
                            <p>
                                {this.props.item.songName}
                            </p>
                            <p>
                                By {this.props.item.artistName}
                            </p>
                        </div>
                    </div>
                );                
            }
        }
        else if(this.props.type === "artist")
        {
            if(this.state.expandedView)
            {
                return(
                    
                    <div onClick={this.expand} className={this.props.className + " expandedArtist"}>
                        <img src={this.state.img} alt="" className="itemPicture"></img>
                        <div className="partition"></div>
                        <div className="itemContent">
                            <p>
                                {this.props.item.artistName}
                            </p>
                        </div>
                        <div className="secondPartition"></div>
                        <iframe className="spotifyArtistPlayer" src={"https://open.spotify.com/embed/artist/" + this.props.item.artistID} frameBorder="0" allow="encrypted-media"></iframe>
                    </div>
                );
            }
            else
            {
                return(
                    
                    <div onClick={this.expand} className={this.props.className}>
                        <img src={this.state.img} alt="" className="itemPicture"></img>
                        <div className="partition"></div>
                        <div className="itemContent">
                            <p>
                                {this.props.item.artistName}
                            </p>
                        </div>
                    </div>
                );                
            }                        
        }
        else
        {
            if(this.state.expandedView)
            {
                return(

                    <div onClick={this.expand} className={this.props.className + " expandedArtist"}>
                        <img src={this.state.img} alt="" className="itemPicture"></img>
                        <div className="partition"></div>
                        <div className="itemContent">
                            <p>
                                {this.props.item.albumName}
                            </p>
                            <p>
                                By {this.props.item.artistName}
                            </p>
                        </div>
                        <div className={this.state.expandedView ? "secondPartition" : "hidden"}></div>
                        <iframe className="spotifyArtistPlayer" src={"https://open.spotify.com/embed/album/" + this.props.item.albumID} frameBorder="0" allow="encrypted-media"></iframe>
                    </div>
                );
            }
            else
            {
                return(

                    <div onClick={this.expand} className={this.props.className}>
                        <img src={this.state.img} alt="" className="itemPicture"></img>
                        <div className="partition"></div>
                        <div className="itemContent">
                            <p>
                                {this.props.item.albumName}
                            </p>
                            <p>
                                By {this.props.item.artistName}
                            </p>
                        </div>
                    </div>
                );                
            }

        }
    }
}


export default RankedItem