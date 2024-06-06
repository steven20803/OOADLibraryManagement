import React, { useState, useEffect } from 'react';
import Cookies from 'js-cookie';

const Borrow = () => {
    const [isLoggedIn, setIsLoggedIn] = useState(false);
    const username = Cookies.get('userId');
    const role = Cookies.get('role');

    useEffect(() => {
        const checkLoginStatus = () => {
            const isLoggedIn = Cookies.get('role') === '1' || Cookies.get('role') === '0';
            setIsLoggedIn(isLoggedIn);
        };

        checkLoginStatus();
    }, []);

    return (
        <div>
            {isLoggedIn ? (
                <h1>歡迎借書</h1>
            ) : (
                <h1>請先登入再進行操作</h1>
            )}
        </div>
    );
};

export default Borrow;