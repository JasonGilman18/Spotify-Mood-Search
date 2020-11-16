import React, { Component } from 'react';
import './slider.css'


class Slider extends Component{

    constructor(props)
    {
        super(props);
        this.state = {value: this.props.value};
    }


    componentWillReceiveProps(newProp)
    {
        this.setState({value: newProp.value});
    }


    render()
    {
        return(

            <div className="sliderContainer">
                <div className="sliderLabels">
                    <h3>{this.props.leftLabel}</h3>
                    <h3>{this.props.rightLabel}</h3>
                </div>
                <input className="slider" type="range" min="0" max="1" step=".001" onChange={(e) => this.props.onChange(e, this.props.index)} value={this.state.value}></input>
            </div>
        );
    }
}


export default Slider;