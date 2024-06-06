import React, { useState, useEffect } from 'react';
import PropTypes from 'prop-types';
import Box from '@mui/material/Box';
import Collapse from '@mui/material/Collapse';
import IconButton from '@mui/material/IconButton';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Typography from '@mui/material/Typography';
import Paper from '@mui/material/Paper';
import KeyboardArrowDownIcon from '@mui/icons-material/KeyboardArrowDown';
import KeyboardArrowUpIcon from '@mui/icons-material/KeyboardArrowUp';
import TablePagination from '@mui/material/TablePagination';
import {TableSortLabel} from '@mui/material';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

const Status = {
  0: "Borrowed",
  1: "Available",
  2: "Lost",
  3: "Damaged",
};
function CollapsibleTable() {
  const [sort, setSort] = useState({ column: 'bookName', direction: 'asc' });

  const handleSort = (column) => {
    const direction = sort.column === column && sort.direction === 'asc' ? 'desc' : 'asc';
    setSort({ column, direction });
  };

  const [books, setBooks] = useState([]);
  const [page, setPage] = useState(0);
  const [rowsPerPage, setRowsPerPage] = useState(5);

  useEffect(() => {
    const fetchBooks = async () => {
      try {
        const response = await axios.get(`http://localhost:8000/book?page=${page}&per_page=200`);
        setBooks(response.data);
      } catch (error) {
        console.error('Failed to fetch books:', error);
      }
    };
    fetchBooks();
  }, []);

  const handleChangePage = (event, newPage) => {
    setPage(newPage);
  };

  const handleChangeRowsPerPage = (event) => {
    setRowsPerPage(parseInt(event.target.value, 10));
    setPage(0);
  };

  return (
    <Box maxWidth={"95%"} pl={2} pt={5}>
    <Typography variant="h4" component="h1" gutterBottom>
      館藏查詢
    </Typography>
    <TableContainer component={Paper}>
      <Table aria-label="collapsible table">

        <TableHead>
          <TableRow>
            <TableCell />
            <TableCell>
              <TableSortLabel
                active={sort.column === 'bookName'}
                direction={sort.column === 'bookName' ? sort.direction : 'asc'}
                onClick={() => handleSort('bookName')}
              >
                Book Name
              </TableSortLabel>
            </TableCell>
            <TableCell align="right">
              <TableSortLabel
                active={sort.column === 'author'}
                direction={sort.column === 'author' ? sort.direction : 'asc'}
                onClick={() => handleSort('author')}
              >
                Author
              </TableSortLabel>
            </TableCell>
            <TableCell align="right">
              <TableSortLabel
                active={sort.column === 'genre'}
                direction={sort.column === 'genre' ? sort.direction : 'asc'}
                onClick={() => handleSort('genre')}
              >
                Genre
              </TableSortLabel>
            </TableCell>
            <TableCell align="right">
              <TableSortLabel
                active={sort.column === 'status'}
                direction={sort.column === 'status' ? sort.direction : 'asc'}
                onClick={() => handleSort('status')}
              >
                Status
              </TableSortLabel>
            </TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
        {books
            .sort((a, b) => {
              if (a[sort.column] < b[sort.column]) {
                return sort.direction === 'asc' ? -1 : 1;
              }
              if (a[sort.column] > b[sort.column]) {
                return sort.direction === 'asc' ? 1 : -1;
              }
              return 0;
            })
            .filter(book => book.status !== 2 && book.status !== 3)
            .slice(page * rowsPerPage, page * rowsPerPage + rowsPerPage)
            .map((book) => (
              <Row key={book.id} row={book} />
            ))}
        </TableBody>
      </Table>
      <TablePagination
        rowsPerPageOptions={[5, 10, 15]}
        component="div"
        count={books.length}
        rowsPerPage={rowsPerPage}
        page={page}
        onPageChange={handleChangePage}
        onRowsPerPageChange={handleChangeRowsPerPage}
      />
    </TableContainer>
    </Box>
  );
}

function Row(props) {
  const { row } = props;
  const [open, setOpen] = React.useState(false);
  const navigate = useNavigate();

  const statusVal = Status[row.status];
  const navigateToBook = () => {
    navigate(`/book/${row.id}`);
  }
  return (
    <React.Fragment>
      <TableRow sx={{ '& > *': { borderBottom: 'unset' } }}>
        <TableCell>
          <IconButton
            aria-label="expand row"
            size="small"
            onClick={() => setOpen(!open)}
          >
            {open ? <KeyboardArrowUpIcon /> : <KeyboardArrowDownIcon />}
          </IconButton>
        </TableCell>
        <TableCell component="th" scope="row">
          {row.book_name}
        </TableCell>
        <TableCell align="right">{row.author}</TableCell>
        <TableCell align="right">{row.genre}</TableCell>
        <TableCell align="right">{statusVal}</TableCell>
      </TableRow>
      <TableRow>
        <TableCell style={{ paddingBottom: 0, paddingTop: 0 }} colSpan={6}>
          <Collapse in={open} timeout="auto" unmountOnExit>
            <Box sx={{ margin: 1 }}>
              {/* <Typography variant="h6" gutterBottom component="div">
                Time Added to Library
                <Typography>{row.added_to_library}</Typography>
              </Typography> */}
              {row.expected_return_time && (
                <Typography variant="h6" gutterBottom component="div">
                  Expected Return Time 
                  <Typography>{row.expected_return_time}</Typography>
                </Typography>
              )}
              
              {/* {row.comments && ( */}
              <Typography variant="h6" gutterBottom component="div" onClick={navigateToBook()}>
                Comments
                <Typography>{row.comments ? row.comments : "None"}</Typography>
              </Typography>
              {/* )} */}

            </Box>
          </Collapse>
        </TableCell>
      </TableRow>
    </React.Fragment>
  );
}

Row.propTypes = {
  row: PropTypes.shape({
    book_name: PropTypes.string.isRequired,
    author: PropTypes.string.isRequired,
    genre: PropTypes.string.isRequired,
    status: PropTypes.number.isRequired,
    added_to_library: PropTypes.string.isRequired,
    comments: PropTypes.string,
  }).isRequired,
};

export default CollapsibleTable;