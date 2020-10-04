import React, { Component } from "react";
import { withStyles } from '@material-ui/core/styles';
import Typography from '@material-ui/core/Typography';
import Box from '@material-ui/core/Box';

const useStyles = theme => ({
  container: {
    display: 'flex',
    flexDirection: 'row',
    margin: '2px',
    marginLeft: '5px',
    marginRight: '5px',

    borderRadius: '2px',
    backgroundColor: '#696B6D',
    overflow: 'hidden',
  },

  tagText: {
    color: 'white',
    padding: '2px',
  },

});

class _ResourceTag extends Component {
  render() {
    const { name, classes, color, deleteColor } = this.props;
    return <div className={classes.container} style={{ backgroundColor: color }}>
      <Typography variant="caption" className={classes.tagText}>

        <Box fontWeight="fontWeightMedium">
          {name}
        </Box>
      </Typography>

      <div style={{ backgroundColor: deleteColor, paddingLeft: '4px', paddingRight: '4px', cursor: 'pointer' }} >
        <Typography style={{ color: 'white' }}>
          <Box fontWeight="fontWeightBold">
            x
        </Box>
        </Typography>
      </div>
    </div>

  }
}

export default withStyles(useStyles)(_ResourceTag);