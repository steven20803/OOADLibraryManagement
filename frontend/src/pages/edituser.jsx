import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';

function EditUser() {
    const { userId } = useParams();
    const [user, setUser] = useState(null);
    const [loading, setLoading] = useState(true);
  
    useEffect(() => {
      // Fetch the user's data from the server when the component mounts
      fetch(`http://localhost:8000/user/${userId}`)
        .then(response => response.json())
        .then(data => {
          setUser(data);
          setLoading(false);
        });
    }, [userId]);

  const handleChange = (event) => {
    setUser({
      ...user,
      [event.target.name]: event.target.value,
    });
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    // Make an API call to update the user
    fetch(`http://localhost:8000/user/${userId}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(user),
    });
  };

  if (loading) {
    return <div>Loading...</div>;
  }

  return (
    <form onSubmit={handleSubmit}>
      <h2>Edit User</h2>
      <ul style={{ listStyleType: 'none', backgroundColor: '#f6f6f6', padding: '10px' }}>
        <li>
          <label>
            Name:
            <input type="text" name="name" value={user.name} onChange={handleChange} />
          </label>
        </li>
        <li>
          <label style={{textAlign: 'left'}}>
            Role:
            <select name="role" value={user.role} onChange={handleChange}>
              <option value={0}>Admin</option>
              <option value={1}>User</option>
            </select>
          </label>
        </li>
        <li>
          <label>
            Birthdate:
            <input type="date" name="birthdate" value={user.birthdate} onChange={handleChange} />
          </label>
        </li>
        <li>
          <label>
            Status:
            <input type="checkbox" name="status" checked={user.status} onChange={handleChange} />
          </label>
        </li>
      </ul>
      <button type="submit">Update</button>
    </form>
  );
}

export default EditUser;