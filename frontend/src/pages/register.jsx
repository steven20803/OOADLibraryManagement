import { Cookie } from '@mui/icons-material';
import axios from 'axios';
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

const RegisterPage = () => {
    const navigate = useNavigate();
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');

    const handleUsernameChange = (e) => {
        setUsername(e.target.value);
    };

    const handlePasswordChange = (e) => {
        setPassword(e.target.value);
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        fetch(`http://localhost:8000/user/register?username=${username}&set_password=${password}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
        })
            .then((res) => res.json())
            .then((data) => {
                console.log(data);
                alert('Register success');
                navigate('/');
            });
        
    };

    return (
        <div>
            <h2>Register</h2>
            <form>
                <div>
                    <label>Username:</label>
                    <input type="text" value={username} onChange={handleUsernameChange} />
                </div>
                <div>
                    <label>Password:</label>
                    <input type="password" value={password} onChange={handlePasswordChange} />
                </div>
                <button type="submit" onClick={handleSubmit}>Register</button>
            </form>
        </div>
    );
};

export default RegisterPage;