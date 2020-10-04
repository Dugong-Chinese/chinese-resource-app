import React, { Component } from "react";
import { withStyles } from '@material-ui/core/styles';
import Typography from '@material-ui/core/Typography';
import Box from '@material-ui/core/Box';
import { grey } from '@material-ui/core/colors';

const resourceListingHeaderStyles = theme => ({
  resourceNameContainer: {
    display: 'flex',
    flexDirection: 'row',
  },

  mainTitleText: {
    color: 'white',
    fontWeight: 'bold'
  },

  subTitleText: {
    color: grey['600'],
  }
});

const leftMetadataStyles = theme => ({
  leftMetadataContainer: {
    padding: '5px',
    margin: '5px',
    borderRadius: '5px',
    minWidth: '3rem',
    textAlign: 'center'
  },

  metadataText: {
    borderRadius: '5px',
    color: 'white',
    fontWeight: 'bold',
  }
})

class _LeftMetadata extends Component {
  render() {
    const { classes, text, color } = this.props;
    return <div className={classes.leftMetadataContainer} style={{ backgroundColor: color }}>
      <Typography fontWeight={500} className={classes.metadataText}>
        {text}
      </Typography>
    </div>
  }
}

const LeftMetadata = withStyles(leftMetadataStyles)(_LeftMetadata);

const adIconStyles = theme => ({
  iconContainer: {
    backgroundColor: '#F1BA40',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    borderRadius: '5px',
    padding: '5px',
    margin: '5px',
  }
})

class _ADIcon extends Component {
  render() {
    const { classes } = this.props;
    return <div className={classes.iconContainer}>
      <Typography variant="h4">
        <Box fontWeight="fontWeightBold">
          AD
        </Box>
      </Typography>
    </div>
  }
}

const ADIcon = withStyles(adIconStyles)(_ADIcon);


class ResourceListingHeader extends Component {

  constructor(props) {
    super(props);
  }

  render() {
    const { ad, classes } = this.props;
    return <div className={classes.resourceNameContainer}>
      {/* <div style={{ height: '3rem', width: '3rem', backgroundColor: 'red' }} /> */}

      <div>
        <LeftMetadata color={'#EB5758'} text={'Format'.toUpperCase()} />
        <LeftMetadata color={'#372C9A'} text={'Pricing'.toUpperCase()} />
      </div>

      {/* the names should occupy as much space as possible */}
      <div style={{ flex: 1, display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center' }}>
        <Typography variant="h5" className={classes.mainTitleText}>
          RESOURCE LISTING NAME
        </Typography>

        <Typography className={classes.subTitleText}>
          RESOURCE LISTING NAME IN CHINESE
        </Typography>

      </div>

      <ADIcon />

    </div>
  }
}

export default withStyles(resourceListingHeaderStyles)(ResourceListingHeader);