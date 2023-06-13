const sideMenu = document.querySelector("aside");
const menuBtn = document.querySelector("#menu-btn");
const closeBtn = document.querySelector("#close-btn");
const themeToggler = document.querySelector(".theme-toggler");
const sidebarLinks = document.querySelectorAll('aside .sidebar a');
const dateInput = document.getElementById('dateInput');
const currentDate = new Date().toISOString().split('T')[0];

// show sidebar
menuBtn.addEventListener("click", () => {
    sideMenu.style.display = "block";
})

// close sidebar
closeBtn.addEventListener("click", () => {
    sideMenu.style.display = "none";
})

// change theme
themeToggler.addEventListener("click", () => {
    document.body.classList.toggle('dark-theme-variables');
    themeToggler.querySelector('span:nth-child(1)').classList.toggle('active');
    themeToggler.querySelector('span:nth-child(2)').classList.toggle('active');
})

// Change active state of links
sidebarLinks.forEach(link => {
  link.addEventListener('click', (event) => {
    event.preventDefault();
    sidebarLinks.forEach(link => {
      link.classList.remove('active');
    });
    link.classList.add('active');
  });
});

// Fetch Date
dateInput.value = currentDate;
dateInput.addEventListener('change', (event) => {
  const selectedDate = event.target.value;
  console.log('Selected date:', selectedDate);
});

// Logout
const logoutBtn = document.querySelector('a[href="/logout"]'); // Update selector to match your HTML structure
logoutBtn.addEventListener("click", () => {
    window.location.href = "/logout"; // Update the URL to match your Flask logout route
});