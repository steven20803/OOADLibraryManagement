import React, { useEffect, useState } from 'react';
import Cookies from 'js-cookie';

const Profile = () => {
    const userId = Cookies.get('userId');
    const user = Cookies.get('user');
    const role = Cookies.get('role');

    const [userInfo, setUserInfo] = useState({});
    var [borrowHistory, setBorrowHistory] = useState([]);

    const roleNames = {
        0: 'Admin',
        1: 'User',
        2: 'Guest',
    };

    useEffect(() => {
        // Fetch user info and borrow history from API
        const fetchUserData = async () => {
            try {
                // Make API call to fetch user info
                const userInfoResponse = await fetch('http://localhost:8000/user/' + userId);
                const userInfoData = await userInfoResponse.json();
                setUserInfo(userInfoData);

                // Make API call to fetch borrow history
                const borrowHistoryResponse = await fetch('/api/borrow-history');
                const borrowHistoryData = await borrowHistoryResponse.json();
                setBorrowHistory(borrowHistoryData);
            } catch (error) {
                console.error('Error fetching user data:', error);
            }
        };

        fetchUserData();
    }, []);      
    
    useEffect(() => {
        const fetchHistoryData = async () => {
            try {
                // Make API call to fetch user info
                const userInfoResponse = await fetch('http://localhost:8000/user/' + userId);
                const userInfoData = await userInfoResponse.json();
                setUserInfo(userInfoData);

                // Make API call to fetch borrow history
                var borrowHistoryResponse = await fetch(`http://localhost:8000/record/Records`);
                var borrowHistoryData = await borrowHistoryResponse.json();
                borrowHistory = borrowHistoryData.filter((record) => record.user_id === userId);

                console.log(borrowHistoryData);
                setBorrowHistory(borrowHistoryData);
            } catch (error) {
                console.error('Error fetching user data:', error);
            }
        };

        fetchHistoryData();
    }, []);

    const returnBook = async (bookId) => {
        try {
            const response = await fetch(`http://localhost:8000/user/${userId}/returnBook/${bookId}`, {
                method: 'POST',
            });
            const data = await response.json();
    
            if (!response.ok) {
                throw new Error(data.message || 'Could not return book.');
            }
    
            // Refresh borrow history after returning book
            window.location.reload();
        } catch (error) {
            console.error('Error returning book:', error);
        }
    };
        
    return (
        <div>
            <h1>User Info</h1>
            <p>Name: {userInfo.name}</p>
            <p>BirthDate: {userInfo.birthdate}</p>
            <p>Role: {roleNames[userInfo.role]}</p>
            {/* Render other user info fields here */}

            <h1>Borrow History</h1>
            <ul>
                {borrowHistory.map((historyItem) => (
                    <li key={historyItem.id} style={{listStyleType: "none"}}>
                        Book ID: {historyItem.book_id}, {new Date(historyItem.borrowed_time).toLocaleDateString()} ~ {new Date(historyItem.expected_return_time).toLocaleDateString()}
                        {
                            historyItem.expected_return_time < new Date() &&
                            <button onClick={() => returnBook(historyItem.book_id)}>Return Book</button>
                        }
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default Profile;