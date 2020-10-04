import React, { Component } from "react";

import { withStyles } from '@material-ui/core/styles';
import { grey } from '@material-ui/core/colors';

import Hidden from '@material-ui/core/Hidden';
import Box from '@material-ui/core/Box';

import ImageGallery from 'react-image-gallery';

import { Tab, Tabs, TabList, TabPanel } from 'react-tabs';
import Typography from '@material-ui/core/Typography';
import Button from 'react-bootstrap/Button';

import FavoriteIcon from '@material-ui/icons/Favorite';
import ResourceListingHeader from "../../components/ResourceListingHeader/ResourceListingHeader";

import ResourceTagContainer from '../../components/ResourceTagContainer/ResourceTagContainer';


const useStyles = theme => ({

  content: {
    // padding: theme.spacing(1),
    display: 'flex',
    flexDirection: 'column',
    // TODO: only dark mode mockup done as of time of writing
    backgroundColor: '#2B2D32',
    // occupy all the space
    flex: 1,
    alignItems: 'center',
  },

  contentAreaBgColor: {
    backgroundColor: grey['A400'],
  },

  contentAreaTextColor: {
    color: 'white',
    fontWeight: 'bold'
  },

  inactiveTabColor: {
    backgroundColor: '#212327'
  },

  mainContainer: {
    display: 'flex',
    [theme.breakpoints.up('md')]: {
      flexDirection: 'row',
    },
    [theme.breakpoints.down('sm')]: {
      flexDirection: 'column'
    },
    maxWidth: '80rem',
    padding: '1rem',
  },

  flexDescriptionRelatedContentContainer: {
    flex: 0.6,
    [theme.breakpoints.up('md')]: {
      paddingTop: '23px',
    }
  },

  flexTagsDownloadContainer: {
    flex: 0.4
  },

  // tabs styling below here
  tabPanel: {
    // boxShadow: '2px -1px 2px 0px rgba(0, 0, 0, 0.5)',
    padding: '1rem',
    color: 'white'
  },

  baseTab: {
    display: 'inline-block',
    // border: '1px solid white',
    borderBottom: 'none',
    // bottom: -1px;
    position: 'relative',
    listStyle: 'none',
    padding: '6px 12px',
    cursor: 'pointer',

    // border: 'none',
    borderRadius: '5px 5px 0 0',
    marginLeft: '5px',
    marginRight: '5px',
    backgroundColor: '#212327',
  },

  selectedTab: {
    display: 'inline-block',
    border: '1px solid white',
    borderBottom: 'none',
    position: 'relative',
    listStyle: 'none',
    padding: '6px 12px',
    cursor: 'pointer',
    borderRadius: '5px 5px 0 0',
    marginLeft: '5px',
    marginRight: '5px',
    // backgroundColor: '#212327',
  },


  actionBtnsContainer: {
    height: '60px',
    display: 'flex',
    flexDirection: 'row'
  },

  rightResourceDetails: {
    padding: theme.spacing(0.5)
  },

  downloadPurchaseLinks: {
    // TODO: cater for dark and light mode?
    backgroundColor: '#2B2D32',
    margin: theme.spacing(1),
    padding: theme.spacing(2),
    borderRadius: '5px',
  }
});

const actionButtonStyles = theme => ({
  button: {
    margin: '5px',
    flex: '1',
    fontWeight: 'bold',
    borderRadius: '10px',
    display: 'flex',
    flexDirection: 'row',
    justifyContent: 'center',
    alignItems: 'center',
    [theme.breakpoints.down('sm')]: {
      fontSize: '2.9vw'
    }
  }
});

class _ActionButton extends Component {
  render() {
    const { classes, icon, name, color } = this.props;
    return <Button className={classes.button} style={{ backgroundColor: color, borderColor: color, }}>
      {/* <FavoriteIcon /> */}
      {icon}
      {!!icon && !!name && <div style={{ width: '5px', }} />}
      {name}
    </Button>
  }
}

const ActionButton = withStyles(actionButtonStyles)(_ActionButton);

const dataRowStyles = theme => ({
  leftContainer: {
    flex: 0.3,
    textAlign: 'right',
  },

  rightContainer: {
    flex: 0.7,
    display: 'flex',
    alignItems: 'center',
    // background: 'red'
  },

  leftText: {
    color: grey['400'],
  }
});

class _DataRow extends Component {

  render() {
    const { classes, leftText, right } = this.props;
    return <div style={{ display: 'flex', flexDirection: 'row' }}>
      <div className={classes.leftContainer}>
        <Typography className={classes.leftText}>
          <Box fontWeight="fontWeightBold">
            {leftText}
          </Box>
        </Typography>
      </div>

      <div className={classes.rightContainer}>
        {right}
      </div>
    </div>
  }
}
const DataRow = withStyles(dataRowStyles)(_DataRow);



class ResourceScreen extends Component {
  constructor(props) {
    super(props);
    this.state = {
      tabIndex: 0,
    }
  }

  componentWillMount() {
    const { classes } = this.props;
  }

  setTabIndex = (tabIndex) => {
    this.setState({ tabIndex });
  }

  render() {
    const { classes } = this.props;
    const { tabIndex } = this.state;

    const resourceListingHeader = <>
      <ResourceListingHeader />
      {/* gradient divider */}
      <div style={{ background: 'linear-gradient(90deg, rgba(255,255,255,0) 15%, rgba(144,144,144,1) 40%, rgba(144,144,144,1) 60%, rgba(255,255,255,0) 85%)', height: '3px', marginBottom: '1rem' }} />
    </>
    return <>
      <div className={classes.content}>
        <div className={classes.mainContainer}>

          <Hidden mdUp>
            {resourceListingHeader}
          </Hidden>

          <div className={classes.flexDescriptionRelatedContentContainer}>
            <Tabs selectedIndex={tabIndex}
              onSelect={index => this.setTabIndex(index)}>

              <TabList>
                <Tab className={`${classes.contentAreaBgColor} ${tabIndex == 0 ? classes.selectedTab : classes.baseTab}`}>
                  <Typography className={classes.contentAreaTextColor}>
                    DESCRIPTION
                </Typography>
                </Tab>

                {/* <Tab disabled>Luigi</Tab> */}
                <Tab className={`${classes.contentAreaBgColor} ${tabIndex == 1 ? classes.selectedTab : classes.baseTab}`}>
                  <Typography className={classes.contentAreaTextColor}>
                    RELATED CONTENT
                  </Typography>
                </Tab>

              </TabList>

              <TabPanel className={`${classes.tabPanel} ${classes.contentAreaBgColor} ${tabIndex == 0 ? 'react-tabs__tab-panel--selected' : 'react-tabs__tab-panel'}`}>

                <ImageGallery showBullets items={[
                  {
                    original: 'https://picsum.photos/id/1018/1000/600/',
                    thumbnail: 'https://picsum.photos/id/1018/250/150/',
                  },
                  {
                    original: 'https://picsum.photos/id/1015/1000/600/',
                    thumbnail: 'https://picsum.photos/id/1015/250/150/',
                  },
                  {
                    original: 'https://picsum.photos/id/1019/1000/600/',
                    thumbnail: 'https://picsum.photos/id/1019/250/150/',
                  },
                ]} />


                <p>
                  <b>Mario</b> (<i>Japanese: マリオ Hepburn: Mario, [ma.ɾʲi.o]</i>) (<i>English:
        /ˈmɑːrioʊ/; Italian: [ˈmaːrjo]</i>) is a fictional character in the Mario video
        game franchise, owned by Nintendo and created by Japanese video game designer
        Shigeru Miyamoto. Serving as the company's mascot and the eponymous protagonist
        of the series, Mario has appeared in over 200 video games since his creation.
        Depicted as a short, pudgy, Italian plumber who resides in the Mushroom
        Kingdom, his adventures generally center upon rescuing Princess Peach from the
        Koopa villain Bowser. His younger brother and sidekick is Luigi.
      </p>
                <p>
                  Source:{' '}
                  <a href="https://en.wikipedia.org/wiki/Mario" target="_blank">
                    Wikipedia
        </a>
                </p>

              </TabPanel>

              <TabPanel className={`${classes.tabPanel} ${classes.contentAreaBgColor} ${tabIndex == 1 ? 'react-tabs__tab-panel--selected' : 'react-tabs__tab-panel'}`}>
                <p>
                  <b>Luigi</b> (<i>Japanese: ルイージ Hepburn: Ruīji, [ɾɯ.iː.dʑi̥]</i>) (<i>English: /luˈiːdʒi/;
        Italian: [luˈiːdʒi]</i>) is a fictional character featured in video games and related media
        released by Nintendo. Created by prominent game designer Shigeru Miyamoto, Luigi is portrayed
        as the slightly younger but taller fraternal twin brother of Nintendo's mascot Mario, and
        appears in many games throughout the Mario franchise, often as a sidekick to his brother.
      </p>
                <p>
                  Source:{' '}
                  <a href="https://en.wikipedia.org/wiki/Luigi" target="_blank">
                    Wikipedia
        </a>
                </p>
              </TabPanel>

            </Tabs>
          </div>

          <div className={classes.flexTagsDownloadContainer}>
            {/* three buttons */}
            <div className={classes.actionBtnsContainer}>
              <ActionButton name={'Favorite'.toUpperCase()} color={'#9C253A'} icon={<FavoriteIcon />} />
              <ActionButton name={'Purchased?'.toUpperCase()} color={'#57A831'} />
              <ActionButton color={'#000'} name={'Blacklist'.toUpperCase()} />
            </div>

            <div className={`${classes.contentAreaBgColor} ${classes.rightResourceDetails}`} style={{ flex: 1, }}>

              <Hidden smDown>
                {resourceListingHeader}
              </Hidden>

              {/* beginning of the tags */}
              <DataRow leftText="Focus:" right={<ResourceTagContainer tagsList={DUMMY_TAGS.focus} />} />

              <DataRow leftText="Proficiency:" right={<ResourceTagContainer tagsList={DUMMY_TAGS.proficiency} />} />

              <DataRow leftText="Content:" right={<ResourceTagContainer tagsList={DUMMY_TAGS.content} />} />

              <DataRow leftText="Genre:" right={<ResourceTagContainer tagsList={DUMMY_TAGS.genre} />} />

              <DataRow leftText="Group:" right={<ResourceTagContainer tagsList={DUMMY_TAGS.group} />} />

              <DataRow leftText="Length:" right={

                <Typography style={{ paddingLeft: '5px', color: 'white' }}>
                  <Box fontWeight="fontWeightMedium">
                    442 pages
                  </Box>
                </Typography>


              } />
              <DataRow leftText="ISBN:" right={

                <Typography style={{ paddingLeft: '5px', color: 'white' }}>
                  <Box fontWeight="fontWeightMedium">
                    97581234567890
                  </Box>
                </Typography>
              } />
              <DataRow leftText="Language:" right={<ResourceTagContainer tagsList={DUMMY_TAGS.language} />} />
              <DataRow leftText="Format(s):" right={<ResourceTagContainer tagsList={DUMMY_TAGS.formats} />} />
              <DataRow leftText="Audience:" right={<ResourceTagContainer tagsList={DUMMY_TAGS.audience} />} />

              <div className={classes.downloadPurchaseLinks} >

                <Typography variant="caption" style={{
                  color: 'white'
                }} >
                  <Box fontWeight="fontWeightBold">
                    Mobile App Download Links:
                  </Box>
                </Typography>

                <div style={{ display: 'flex', alignItems: 'center', paddingBottom: '0.5rem' }}>
                  <i className="fab fa-apple fa-2x" style={{ color: 'white', paddingRight: '5px', flex: 0.1 }} />
                  <Typography variant="body2" style={{
                    color: 'white',
                  }}>
                    <a style={{ flex: 0.9 }} target="_blank" href="https://apple.com">Sample App Name</a>
                  </Typography>
                </div>

                <div style={{ display: 'flex', alignItems: 'center', paddingBottom: '0.5rem' }}>
                  <i className="fab fa-google-play fa-2x" style={{ color: 'white', paddingRight: '5px', flex: 0.1 }} />
                  <Typography variant="body2" style={{
                    color: 'white',
                  }}>
                    <a style={{ flex: 0.9 }} target="_blank" href="https://google.com">Sample App Name</a>
                  </Typography>
                </div>

                <Typography variant="body2" style={{
                  color: 'white',
                }}>
                  * NB: Available in all regions except the ABC and XYZ app stores.
                </Typography>


              </div>

            </div>
          </div>
        </div >
      </div >
    </>
  }
}

const DUMMY_TAGS = {
  focus: [{ name: 'Reading', color: '#6A3739' }, { name: 'Speaking', color: '#364C72' }, { name: 'Writing', color: '#42723E' }, { name: 'Listing', color: '#817441' }],

  proficiency: [{ name: 'Legacy' }, { name: 'Beginner' }, { name: 'Intermediate' }],

  content: [{ name: 'OCR' }, { name: 'Dictionary' }, { name: 'Grammar' }, { name: 'Idioms' }, { name: 'Flashcards' }, { name: 'News' }, { name: 'History' }],

  genre: [{ name: 'Detective' }, { name: 'Thriller' }, { name: 'Romance' },],

  group: [{ name: 'BLCUP' }, { name: 'Mandarin Companion' },],

  language: [{ name: 'English' }, { name: 'Simplified Chinese' }, { name: 'Pinyin' }],

  formats: [{ name: 'Audiobook' }, { name: 'Website' }, { name: 'Digitized' }],

  audience: [{ name: 'Foreign Student' }, { name: 'Natives' }, { name: 'Linguistics' }]

};

export default withStyles(useStyles)(ResourceScreen);