import logo from './logo.svg';
import './App.css';
import { Routes, Route } from 'react-router-dom';
import SwipeableTemporaryDrawer from './pages/NavBar.jsx';
import CollapsibleTable from './pages/table.jsx';
import LandingPage from './pages/LandingPage.jsx';
import NoMatch from './pages/NoMatch.jsx';
import RegisterPage from './pages/register.jsx';
import LoginPage from './pages/login.jsx';
import Borrow from './pages/borrow.jsx';
import Dashboard from './pages/dashboard.jsx';
import EditUser from './pages/edituser.jsx';
import BookInfo from './pages/bookinfo.jsx';
import Profile from './pages/profile.jsx';


export default function App() {
  return (
      <div className='App'>
          <SwipeableTemporaryDrawer />
          <Routes>
              <Route path='/'>
                  <Route index element={<LandingPage />} />
                  <Route path='collection' element={<CollapsibleTable />} />
                  {/* <Route path='dashboard' element={<LandingPage />} /> */}
                  <Route path='register' element={<RegisterPage />} />
                  <Route path='login' element={<LoginPage />} />
                  <Route path='borrow' element={<Borrow />} />
                  <Route path='dashboard' element={<Dashboard />} />
                  <Route path='profile' element={<Profile />} />
                  <Route path='edituser/:userId' element={<EditUser />} />
                  <Route path='book/:id' element={<BookInfo />} />
                  <Route path='*' element={<NoMatch />} />
              </Route>
          </Routes>
      </div>
  )
}