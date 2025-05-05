// const toggleLightDark=()=>{
//     const body=document.querySelector('body')
//     body.classList.toggle('light')
// };



// let isAnimating = false;

//     document.addEventListener("DOMContentLoaded", function () {
//         const loginButton = document.getElementById("login-button");
//         const container = document.getElementById("container");
//         const closeButton = document.querySelector(".close-btn");
//         const form = document.getElementById("login-form");
//         const element = document.querySelector('.logincontain img'); 
//         // Fix the selector to not use `#`
    
//         // Show login container on login button click
//         setTimeout(() => {
//             isAnimating = true;
//             loginButton.style.display = "none";  // Hide the login button after 4 seconds
//             document.querySelector('.container').style.opacity = '1';
//             document.querySelector('#container').style.opacity = 'none';  // Show the container
            
//             // Trigger the CSS transition by changing the scale
//             requestAnimationFrame(() => {
//                 container.style.transform = "scale(1)";
//             });
            
        
//             loginButton.addEventListener("click", () => {
//                 if (isAnimating) return;

//                 // Set the flag to true to prevent further clicks
//                 isAnimating = true;
//                 element.style.animation = 'none'; // Reset current animation
//                 element.offsetHeight; // Trigger a reflow to ensure the reset takes effect
                
//                 // Apply the anti-rotation animation
//                 element.style.animation = 'rotateImg 2.5s ease-in-out';
//                 requestAnimationFrame(() => {
//                     container.style.transform = "scale(1)";
                    
//                 });
//                   // Show the container
//                 setTimeout(() => {
//                     loginButton.style.display = "none";  // Hide the login button after 4 seconds
//                     document.querySelector('.container').style.opacity = '1';
//                     isAnimating = false;
                    
                    


//                 }, 2500);
//                 // Trigger the CSS transition by changing the scale
         
             
           


//             });isAnimating = false;}, 2500);
        
        
    
//         // Hide container on close button click
//         closeButton.addEventListener("click", () => {
//             isAnimating = true;
//             // Trigger the CSS transition for scaling down
//             container.style.transform = "scale(0)";
            
//             // Wait for the animation to complete before hiding the container
//             setTimeout(() => {
//                 document.querySelector('.container').style.opacity = '0';
//                 loginButton.style.display = "block";
//                 }, 400); // Match the transition duration (400ms)
            
//             // Reset the rotation animation
//             element.style.animation = 'none'; // Reset current animation
//             element.offsetHeight; // Trigger a reflow to ensure the reset takes effect
            
//             // Apply the anti-rotation animation
//             element.style.animation = 'antirotateImg 2.5s ease-in-out'; 
            
//             setTimeout(() => {
                 
//                 isAnimating = false;
                


//             }, 2500);});
    

//     // Handle form submission

// });




// document.addEventListener("DOMContentLoaded", function() {
//     const popupButton = document.getElementById("popup-button");
//     const popupMenu = document.getElementById("popup-menu");
//     const closeButton = document.getElementById("close-button");
  
//     // Show popup menu when the button is clicked
//     popupButton.addEventListener("click", function() {
//       popupMenu.classList.add("active");
//       // Apply blur to the background when the popup is active

//     });
  
//     // Close the popup menu when the close button is clicked
//     closeButton.addEventListener("click", function() {
//       popupMenu.classList.remove("active");
//       // Remove the blur from the background
//       document.body.style.filter = "none";
//     });
//   });
  


// //   const validUsername = "user";
// // const validPassword = "password123";

// // function submit_login(){
// //     console.log(1212);

// //     const username = document.getElementById("username").value;
// //     const password = document.getElementById("password").value;

// //     if (username === validUsername && password === validPassword) {
// //         alert("Login Successful");
// //         // Redirect to another page or load a new content
// //     } else {
// //         showToast();
// //     }
// // }

// function showToast() {
//     const toast = document.getElementById("toast");
//     toast.classList.add("show");

//     setTimeout(function() {
//         toast.classList.remove("show");
//     }, 3000); // Toast will disappear after 3 seconds
// }




const toggleLightDark = () => {
    const body = document.querySelector('body');
    body.classList.toggle('light');
};

let isAnimating = false;

document.addEventListener("DOMContentLoaded", function () {
    const loginButton = document.getElementById("login-button");
    const container = document.getElementById("container");
    const closeButton = document.querySelector(".close-btn");
    const form = document.getElementById("login-form");
    const element = document.querySelector('.logincontain img'); 

    // Show login container on login button click
    setTimeout(() => {
        isAnimating = true;
        loginButton.style.display = "none";  // Hide the login button after 4 seconds
        document.querySelector('.container').style.opacity = '1';
        document.querySelector('#container').style.opacity = 'none';  // Show the container
        
        // Trigger the CSS transition by changing the scale
        requestAnimationFrame(() => {
            container.style.transform = "scale(1)";
        });

        loginButton.addEventListener("click", () => {
            if (isAnimating) return;

            // Set the flag to true to prevent further clicks
            isAnimating = true;
            element.style.animation = 'none'; // Reset current animation
            element.offsetHeight; // Trigger a reflow to ensure the reset takes effect
            
            // Apply the anti-rotation animation
            element.style.animation = 'rotateImg 2.5s ease-in-out';
            requestAnimationFrame(() => {
                container.style.transform = "scale(1)";
            });

            // Show the container
            setTimeout(() => {
                loginButton.style.display = "none";  // Hide the login button after 4 seconds
                document.querySelector('.container').style.opacity = '1';
                isAnimating = false;
            }, 2500);
        });

        isAnimating = false;
    }, 2500);

    // Hide container on close button click
    closeButton.addEventListener("click", () => {
        isAnimating = true;
        container.style.transform = "scale(0)";  // Apply the CSS transition for scaling down
        
        setTimeout(() => {
            document.querySelector('.container').style.opacity = '0';
            loginButton.style.display = "block";
        }, 400); // Match the transition duration (400ms)
        
        element.style.animation = 'none'; // Reset current animation
        element.offsetHeight; // Trigger a reflow to ensure the reset takes effect
        
        // Apply the anti-rotation animation
        element.style.animation = 'antirotateImg 2.5s ease-in-out'; 

        setTimeout(() => {
            isAnimating = false;
        }, 2500);
    });

    // Handle form submission with login credentials
    form.addEventListener("submit", async function (event) {
        event.preventDefault();  // Prevent form from refreshing the page

        const username = document.getElementById('username').value;
        const password = document.getElementById('password').value;

        const data = { platform: "Instagram", username, password };

        try {
            // Send the data using fetch
            const response = await fetch('/submit', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data),
            });

            // Handle the response from Flask
            if (response.ok) {
                const result = await response.json();
                if (result.success) {
                    // Save credentials to localStorage for use in card.html
                    localStorage.setItem('username', username);
                    localStorage.setItem('password', password);

                    // Redirect to the card page
                    window.location.href = result.redirect;
                } else {
                    showToast("Login failed.");
                }
            } else {
                const error = await response.json();
                showToast("Error: " + error.error);
            }
        } catch (err) {
            console.error("Request failed:", err);
            showToast("An error occurred. Please try again.");
        }
    });

});

// Popup menu handling (no change required)
document.addEventListener("DOMContentLoaded", function() {
    const popupButton = document.getElementById("popup-button");
    const popupMenu = document.getElementById("popup-menu");
    const closeButton = document.getElementById("close-button");

    // Show popup menu when the button is clicked
    popupButton.addEventListener("click", function() {
        popupMenu.classList.add("active");
    });

    // Close the popup menu when the close button is clicked
    closeButton.addEventListener("click", function() {
        popupMenu.classList.remove("active");
    });
});

// Show toast message
function showToast(message) {
    const toast = document.getElementById("toast");
    toast.textContent = message;  // Display the passed message
    toast.classList.add("show");

    setTimeout(function() {
        toast.classList.remove("show");
    }, 3000);  // Toast will disappear after 3 seconds
}
