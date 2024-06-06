import * as React from 'react';
import { styled, useTheme } from '@mui/material/styles';
import Box from '@mui/material/Box';
import Drawer from '@mui/material/Drawer';
import CssBaseline from '@mui/material/CssBaseline';
import MuiAppBar from '@mui/material/AppBar';
import Toolbar from '@mui/material/Toolbar';
import List from '@mui/material/List';
import Typography from '@mui/material/Typography';
import Divider from '@mui/material/Divider';
import IconButton from '@mui/material/IconButton';
import MenuIcon from '@mui/icons-material/Menu';
import ChevronLeftIcon from '@mui/icons-material/ChevronLeft';
import ChevronRightIcon from '@mui/icons-material/ChevronRight';
import ListItem from '@mui/material/ListItem';
import ListItemButton from '@mui/material/ListItemButton';
import ListItemIcon from '@mui/material/ListItemIcon';
import ListItemText from '@mui/material/ListItemText';
import { useMediaQuery } from '@mui/material';
import { Link } from 'react-router-dom';
import HomeIcon from '@mui/icons-material/Home';
import TableChartIcon from '@mui/icons-material/TableChart';
import DashboardIcon from '@mui/icons-material/Dashboard';
import PersonIcon from '@mui/icons-material/Person';
import Cookies from 'js-cookie';
import { useNavigate } from 'react-router-dom';
import Person2Icon from '@mui/icons-material/Person2';
import {InputBase} from '@mui/material';
import SearchIcon from '@mui/icons-material/Search';
import { useState } from 'react';


const drawerWidth = 240;
const username = Cookies.get('user');


const Main = styled('main', { shouldForwardProp: (prop) => prop !== 'open' })(
  ({ open }) => ({
    flexGrow: 1,
    padding: '16px', // replace theme.spacing(3) with static value
    transition: 'margin 225ms cubic-bezier(0.4, 0, 0.2, 1) 0ms', // replace theme.transitions.create and theme.transitions.easing.sharp with static value
    marginLeft: `-${drawerWidth}px`,
    ...(open && {
      transition: 'margin 225ms cubic-bezier(0, 0, 0.2, 1) 0ms', // replace theme.transitions.create and theme.transitions.easing.easeOut with static value
      marginLeft: 0,
    }),
  }),
);

const AppBar = styled(MuiAppBar, {
  shouldForwardProp: (prop) => prop !== 'open',
})(({ open }) => ({
  transition: 'margin 225ms cubic-bezier(0.4, 0, 0.2, 1) 0ms, width 225ms cubic-bezier(0.4, 0, 0.2, 1) 0ms', // replace theme.transitions.create and theme.transitions.easing.sharp with static value
  ...(open && {
    width: `calc(100% - ${drawerWidth}px)`,
    marginLeft: `${drawerWidth}px`,
    transition: 'margin 225ms cubic-bezier(0, 0, 0.2, 1) 0ms, width 225ms cubic-bezier(0, 0, 0.2, 1) 0ms', // replace theme.transitions.create and theme.transitions.easing.easeOut with static value
  }),
}));

const DrawerHeader = styled('div')(() => ({
  display: 'flex',
  alignItems: 'center',
  padding: '0 8px', // replace theme.spacing(0, 1) with static value
  justifyContent: 'flex-end',
}));

const Search = styled('div')(() => ({
  position: 'relative',
  borderRadius: '4px', // replace theme.shape.borderRadius with static value
  backgroundColor: 'rgba(255, 255, 255, 0.15)', // replace alpha(theme.palette.common.white, 0.15) with static value
  '&:hover': {
    backgroundColor: 'rgba(255, 255, 255, 0.25)', // replace alpha(theme.palette.common.white, 0.25) with static value
  },
  marginRight: '8px', // replace theme.spacing(2) with static value
  marginLeft: 0,
  width: '50%',
}));

const SearchIconWrapper = styled('div')(() => ({
  padding: '0 16px', // replace theme.spacing(0, 2) with static value
  height: '100%',
  position: 'absolute',
  pointerEvents: 'none',
  display: 'flex',
  alignItems: 'center',
  justifyContent: 'center',
}));

const StyledInputBase = styled(InputBase)(() => ({
  color: 'inherit',
  '& .MuiInputBase-input': {
    padding: '10px 10px 10px 0',
    paddingLeft: `calc(1em + 25px)`,
    transition: 'width 300ms cubic-bezier(0.4, 0, 0.2, 1) 0ms',
    width: '100%',
  },
}));

export default function PersistentDrawerLeft() {
  const [searchTerm, setSearchTerm] = useState('');
  const handleSearch = (event) => {
    setSearchTerm(event.target.value);
  }
  const navigate = useNavigate();
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('sm'));
  const drawerWidth = isMobile ? '100%' : 240;
  const [open, setOpen] = React.useState(false);

  const handleDrawerOpen = () => {
    setOpen(true);
  };

  const handleDrawerClose = () => {
    setOpen(false);
  };

  const handleLogout = () => {
    Cookies.remove('user');
    Cookies.remove('role');
    Cookies.remove('userId');
    window.location.reload();
  };

  return (
    <Box sx={{ display: 'flex' }}>
      <CssBaseline />
      <AppBar position="fixed" open={open}>
        <Toolbar>
          <IconButton
            color="inherit"
            aria-label="open drawer"
            onClick={handleDrawerOpen}
            edge="start"
            sx={{ mr: 2, ...(open && { display: 'none' }) }}
          >
            <MenuIcon />
          </IconButton>
          <Typography variant="h6" noWrap component="div" sx={{ flexGrow: 1 }} onClick={() => navigate('/')}>
            Menu
          </Typography>
          <Search>
          <SearchIconWrapper>
            <SearchIcon />
          </SearchIconWrapper>
          <StyledInputBase
            placeholder="Search…"
            inputProps={{ 'aria-label': 'search' }}
            value={searchTerm}
            onChange={handleSearch}
          />
        </Search>
          {username && (
            <Typography variant='h6' noWrap component="div" color="inherit" onClick={handleLogout}>
              Logout
            </Typography>
          )}
        </Toolbar>
      </AppBar>
      <Drawer
        sx={{
          width: drawerWidth,
          flexShrink: 0,
          '& .MuiDrawer-paper': {
            width: drawerWidth,
            boxSizing: 'border-box',
          },
        }}
        variant="persistent"
        anchor="left"
        open={open}
      >
        <DrawerHeader>
          <IconButton onClick={handleDrawerClose}>
            {theme.direction === 'ltr' ? <ChevronLeftIcon /> : <ChevronRightIcon />}
          </IconButton>
        </DrawerHeader>

        <ListItem disablePadding>
        {username ? (
          <div style={{paddingLeft:'20px'}}>Welcome, {username}</div>
        ) : (
          <ListItemButton component={Link} to='/login' onClick={handleDrawerClose}>
            <ListItemText primary='Login' />
          </ListItemButton>
        )}
        </ListItem>
        
        <Divider />

        <List>
          {[
            { text: 'Home', icon: <HomeIcon />, path: '/' },
            { text: 'Collection', icon: <TableChartIcon />, path: '/collection' },
            { text: 'Dashboard', icon: <DashboardIcon />, path: '/dashboard' },
            /*{ { text: 'Borrow', icon: <BookIcon/>, path: '/borrow' }, }*/
            { text: 'Profile', icon: <Person2Icon/>, path: '/profile' },
            { text: 'Register', icon: <PersonIcon/>, path: '/register' }



            /* { text: 'Drafts', icon: <DraftsIcon />, path: '/drafts' },*/
          ].map((item, index) => (
            <ListItem key={item.text} disablePadding>
              <ListItemButton component={Link} to={item.path} onClick={handleDrawerClose}>
                <ListItemIcon>
                  {item.icon}
                </ListItemIcon>
                <ListItemText primary={item.text} />
              </ListItemButton>
            </ListItem>
          ))}
        </List>

      </Drawer>
      <Main open={open}>
        <DrawerHeader />
      </Main>
    </Box>
  );
}
