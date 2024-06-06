import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import Cookies from 'js-cookie';

const BookInfo = () => {
    const {id} = useParams();
    const [bookInfo, setBookInfo] = useState(null);
    const [loading, setLoading] = useState(true);
    const statusNames = {
        0: 'Borrowed',
        1: 'Available',
        2: 'Lost',
        3: 'Damaged',
      };

      const handleBorrow = () => {
        const user_id = Cookies.get('userId');
        if(Cookies.get('role') !== '1' && Cookies.get('role') !== '0'){
            alert('Please login first');
            return;
        }
        fetch(`http://localhost:8000/book/${id}/borrow?user_id=${user_id}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            }
        })
        .then((response) => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then((data) => {
            setBookInfo(data);
        })
        .catch((error) => {
            console.error('Error:', error);
            alert('An error occurred while borrowing the book. Please try again.');
        });
    }
    
    useEffect(() => {
        fetch(`http://localhost:8000/book/${id}`)
            .then((response) => response.json())
            .then((data) => {
                setBookInfo(data);
                setLoading(false);
            });
    }, [id]);

    if (!bookInfo) {
        return <div>Loading...</div>;
    }

    return (
        <div>
            <h1>{bookInfo.book_name}</h1>
            <p>Author: {bookInfo.author}</p>
            <p>Genre: {bookInfo.genre}</p>
            <p>Status: {statusNames[bookInfo.status]}</p>
            <p>Added to Library: {bookInfo.added_to_library}</p>
            <p>Note: {bookInfo.comments}</p>
            {statusNames[bookInfo.status] === 'Borrowed' && (
                <p>expected_return_time: {bookInfo.expected_return_time}</p>
            )}

            {statusNames[bookInfo.status] === 'Available' && (
                <button onClick={handleBorrow}>Borrow</button>
            )}
        </div>
    );
};

export default BookInfo;