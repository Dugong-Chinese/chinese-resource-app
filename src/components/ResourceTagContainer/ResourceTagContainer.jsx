import React, { Component } from "react";
import { withStyles } from '@material-ui/core/styles';

import ResourceTag from '../ResourceTag/ResourceTag';

const useStyles = theme => ({
  container: {
    display: 'flex',
    flexDirection: 'row',
    flexWrap: 'wrap',
    // backgroundColor: '#696B6D',
  },

  tagText: {
    color: 'white'
  },


});


// https://www.sitepoint.com/javascript-generate-lighter-darker-color/
function ColorLuminance(hex, lum) {
  // validate hex string
  hex = String(hex).replace(/[^0-9a-f]/gi, '');
  if (hex.length < 6) {
    hex = hex[0] + hex[0] + hex[1] + hex[1] + hex[2] + hex[2];
  }
  lum = lum || 0;

  // convert to decimal and change luminosity
  var rgb = "#", c, i;
  for (i = 0; i < 3; i++) {
    c = parseInt(hex.substr(i * 2, 2), 16);
    c = Math.round(Math.min(Math.max(0, c + (c * lum)), 255)).toString(16);
    rgb += ("00" + c).substr(c.length);
  }

  return rgb;
}


class _ResourceTagContainer extends Component {

  render() {
    // TODO: use this component for editing as well as viewing tags?
    const { classes, tagsList, editingEnabled } = this.props;

    const renderedTags = [];

    for (let item of tagsList) {
      let { name, color } = item;
      color = color || '#696B6D';
      renderedTags.push(<ResourceTag name={name} color={color} deleteColor={ColorLuminance(color, -0.3)} />);
    }
    return <div className={classes.container}>
      {renderedTags}
    </div>
  }
}

export default withStyles(useStyles)(_ResourceTagContainer);