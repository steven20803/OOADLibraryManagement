import React, { useState, useEffect } from 'react';
import Cookies from 'js-cookie';
import { useNavigate } from 'react-router-dom';

const Dashboard = () => {
    const [users, setUsers] = useState([]);
    const [books, setBooks] = useState([]);
    const [isLoggedIn, setIsLoggedIn] = useState(false);
    const username = Cookies.get('user');
    const role = Cookies.get('role');
    const navigate = useNavigate();

    useEffect(() => {
        const checkLoginStatus = () => {
            const isLoggedIn = Cookies.get('role') === '0';
            setIsLoggedIn(isLoggedIn);
        };

        checkLoginStatus();
    }, []);

    useEffect(() => {
        // Fetch users and books data from API or database
        // and update the state variables
        fetchUsers();
        fetchBooks();
    }, []);

    const fetchUsers = async () => {
        try {
            // Make an API call to fetch users data
            const response = await fetch('http://localhost:8000/user');
            const data = await response.json();
            setUsers(data);
        } catch (error) {
            console.error('Error fetching users:', error);
        }
    };

    const fetchBooks = async () => {
        try {
            // Make an API call to fetch books data
            const response = await fetch('/api/books');
            const data = await response.json();
            setBooks(data);
        } catch (error) {
            console.error('Error fetching books:', error);
        }
    };

    const handleDelete = async (id) => {
        try {
            // Make an API call to delete a user
            await fetch(`http://localhost:8000/user/${id}`, {
                method: 'DELETE',
            });
            fetchUsers();
        } catch (error) {
            console.error('Error deleting user:', error);
        }
    }

    const handleEditBook = (id) => {
        navigate(`/editbook/${id}`);
    }

    const handleEditUser = (id) => {
        navigate(`/edituser/${id}`);
    }


    return (
        <div>
        {isLoggedIn ? (
        <div>
            <h1>Dashboard</h1>

            <h2>Users</h2>
            <ul>
                {users.map((user, index) => (
                    <li key={user.id} style={{ listStyleType: "none", backgroundColor: index % 2 === 0 ? '#f6f6f6' : '#e9e9e9' }}>
                    <div style={{ display: 'flex', justifyContent: 'space-between', padding: '10px' }}>
                    <div style={{textAlign: 'left'}}>
                        <p>Name: {user.name}</p>
                        <p>Role: {user.role}</p>
                        <p>Birthdate: {user.birthdate}</p>
                        <p>Status: {user.status ? 'Active' : 'Inactive'}</p>
                        </div>
                        <button onClick={() => handleEditUser(user.id)}>Edit</button>
                        {/* <button onClick={() => handleDelete(user.id)}>Delete</button> */}
                    </div>
                    </li>
                ))}
            </ul>
        </div>
        ) : (
            <h1>Unauthorized</h1>
        )}
        </div>
    );
};

export default Dashboard;