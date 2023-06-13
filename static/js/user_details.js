// Fetch user data from Flask route
fetch('/user_details')
  .then(response => response.json())
  .then(data => {
    // Get the table body element
    const tableBody = document.querySelector('#user-table tbody');
    
    // Clear any existing rows in the table
    tableBody.innerHTML = '';
    
    // Loop through the fetched data and create table rows
    data.users.forEach(user => {
      const row = document.createElement('tr');
      
      // Create table cells for each user property
      const userIdCell = document.createElement('td');
      userIdCell.textContent = user.user_id;
      
      const userNameCell = document.createElement('td');
      userNameCell.textContent = user.user_name;
      
      const emailCell = document.createElement('td');
      emailCell.textContent = user.email;
      
      const passwordCell = document.createElement('td');
      passwordCell.textContent = user.password;
      
      // Append table cells to the row
      row.appendChild(userIdCell);
      row.appendChild(userNameCell);
      row.appendChild(emailCell);
      row.appendChild(passwordCell);
      
      // Append the row to the table body
      tableBody.appendChild(row);
    });
  })
  .catch(error => console.error(error));
