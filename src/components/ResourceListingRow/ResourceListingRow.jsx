import React, { Component } from "react";
import { Chart, Doughnut } from 'react-chartjs-2';
import { Container, InputGroup, Form, FormControl, Button, Dropdown, DropdownButton, } from 'react-bootstrap';

import { withStyles } from '@material-ui/core/styles';
import { deepOrange, deepPurple, grey } from '@material-ui/core/colors';
import Typography from '@material-ui/core/Typography'
import Box from '@material-ui/core/Box';

const MOCKUP_FOREGROUND_GREY = '#929292';

const data = {
  labels: [
    'A1',
    'B2',
    'C2'
  ],
  datasets: [{
    data: [300, 50, 100],
    backgroundColor: [
      '#FF6384',
      '#36A2EB',
      '#FFCE56'
    ],
    hoverBackgroundColor: [
      '#FF6384',
      '#36A2EB',
      '#FFCE56'
    ]
  }]
};

const useStyles = theme => ({
  listingRowContainer: {
    flexDirection: 'row', display: 'flex',
    padding: theme.spacing(0.5),
    // alignItems: 'center',
    // justifyContent: 'center',
    maxWidth: '50rem',
    minHeight: '7rem',
    backgroundColor: '#545659',
    [theme.breakpoints.up('sm')]: {
      borderRadius: '1rem',
      padding: theme.spacing(1.5),
      boxShadow: "6px 7px 5px 0px rgba(0,0,0,0.75);",
      marginBottom: '1.5rem'
    },
    [theme.breakpoints.down('xs')]: {
      borderBottom: `1px solid ${grey[400]};`
    }
  },

  dualImgContainer: {
    display: 'flex',
    [theme.breakpoints.up('md')]: {
      flexDirection: 'row'
    },
    [theme.breakpoints.down('sm')]: {
      flexDirection: 'column'
    },
    flexGrow: 0.3,
    flexShrink: 1,
    flexBasis: '0%',
    paddingRight: theme.spacing(0.5),
    [theme.breakpoints.up('sm')]: {
      paddingRight: theme.spacing(1.5),
    }
  },

  previewImg: {
    flex: 1, minWidth: 0, objectFit: 'cover', maxWidth: '100%', maxHeight: '100%', borderRadius: '5px'
  },

  catAffixContainer: {
    paddingLeft: theme.spacing(0.5),
    paddingRight: theme.spacing(0.5),
    boxShadow: "6px 11px 20px -11px rgba(0,0,0,0.82)"
  },

  blogTagContainer: {
    paddingLeft: theme.spacing(0.5),
    paddingRight: theme.spacing(0.5),
    margin: theme.spacing(0.5),
    backgroundColor: grey[900],
    boxShadow: "6px 11px 20px -11px rgba(0,0,0,0.82)"
  },

  separator: {
    width: theme.spacing(0.5),
    height: theme.spacing(0.5),
  },

  resourceSummaryContainer: {
    display: 'flex',
    flexDirection: 'column',
    flex: 0.7,
  },

  cefrContainer: {
    // backgroundColor: 'black',
    // flex: 0.1,
    paddingRight: theme.spacing(1),
    marginBottom: theme.spacing(1),
    marginTop: theme.spacing(1),
    display: 'flex',
    alignItems: 'center'
  }

});

const CategoryAffix = withStyles(useStyles)((props) => {
  const { classes, bgColor, fgColor, text } = props;
  return <div className={classes.catAffixContainer} style={{ backgroundColor: bgColor }}>
    <Typography variant="caption" style={{ color: fgColor }}>
      {text}
    </Typography>
  </div>
});

const BlockTag = withStyles(useStyles)((props) => {
  const { classes, text } = props;
  return <div className={classes.blogTagContainer}>
    <Typography variant="caption" style={{ color: MOCKUP_FOREGROUND_GREY }}>
      <Box fontWeight={700}>
        {text.toUpperCase()}
      </Box>
    </Typography>
  </div>
});

class ResourceListingRow extends Component {

  componentWillMount() {
    Chart.pluginService.register({
      beforeDraw: function (chart) {
        var width = chart.chart.width,
          height = chart.chart.height,
          ctx = chart.chart.ctx;

        ctx.restore();
        // var fontSize = (height / 114).toFixed(2);
        ctx.font = /*fontSize + */"bold 0.75rem helvetica";
        ctx.fillStyle = "white";
        ctx.textBaseline = "middle";

        var text = "CEFR",
          textX = Math.round((width - ctx.measureText(text).width) / 2),
          textY = height / 2;

        ctx.fillText(text, textX, textY);
        ctx.save();
      }
    });
  }

  render() {
    const { classes } = this.props;
    return <div className={classes.listingRowContainer}>
      <div className={classes.dualImgContainer}>
        <img src="https://picsum.photos/130" className={classes.previewImg} />

        <div className={classes.separator} />

        <img src="https://picsum.photos/131" className={classes.previewImg} />

      </div>

      <div className={classes.resourceSummaryContainer}>
        <div style={{ flexDirection: 'row', display: 'flex', flexWrap: 'wrap' }}>
          <CategoryAffix bgColor='#C1433F' fgColor='white' text='FREEMIUM' />
          <div className={classes.separator} />
          <CategoryAffix bgColor='#372C9A' fgColor='white' text='$100' />

          <Typography variant="body" style={{ color: 'grey', fontWeight: 'bold' }}>
            ~ sub-content
        </Typography>
        </div>

        <Typography variant="body" style={{ color: 'white', fontWeight: 'bold' }}>
          {"This is a very long resource listing name that spans many lines".toUpperCase()}
        </Typography>

        <div style={{ flexDirection: 'row', display: 'flex' }} >
          {/* tag container */}
          <div style={{ minWidth: 0, flexDirection: 'row', display: 'flex', flexWrap: 'wrap', alignSelf: 'flex-start' }}>
            <BlockTag text={'tag'} />
            <BlockTag text={'tag'} />
            <BlockTag text={'tag'} />
            <BlockTag text={'tag'} />
            <BlockTag text={'tag'} />
            <BlockTag text={'tag'} />
            <BlockTag text={'tag'} />
            <BlockTag text={'tag'} />
            <BlockTag text={'tag'} />
            <BlockTag text={'tag'} />
            <BlockTag text={'tag'} />
          </div>


          <div className={classes.cefrContainer}>
            <Doughnut legend={{ display: false }}
              layout={{ padding: -50 }}
              options={{ cutoutPercentage: 60 }}
              height={100} width={100} data={data} />
          </div>

        </div>



        <div style={{ flexDirection: 'row', display: 'flex', flexWrap: 'wrap', justifyContent: 'space-between', marginTop: 'auto' }}>

          <div style={{ display: 'flex', flexDirection: 'row' }}>
            <i className="fa fa-thumbs-up pr-1" style={{ color: MOCKUP_FOREGROUND_GREY, fontSize: '1.2rem' }} />
            <Typography variant="caption" style={{ color: MOCKUP_FOREGROUND_GREY, fontWeight: 'bold' }}>
              {"3 UPVOTES".toUpperCase()}
            </Typography>
          </div>


          <Typography variant="caption" className="pr-1" style={{ color: MOCKUP_FOREGROUND_GREY, fontWeight: 'bold' }}>
            {"Publisher/Group Name".toUpperCase()}
          </Typography>
        </div>
      </div>

    </div>
  }
}


export default withStyles(useStyles)(ResourceListingRow);