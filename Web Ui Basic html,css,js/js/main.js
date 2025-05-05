//switch light and dark mode
const toggleLightDark=()=>{
    const body=document.querySelector('body')
    body.classList.toggle('light')
};
let imgBx = document.querySelectorAll('.imgBx');
let contentBx = document.querySelectorAll('.contentBx');

for (let i = 0; i < imgBx.length; i++) {
    imgBx[i].addEventListener('click', function () {
        for (let j = 0; j < contentBx.length; j++) {
            contentBx[j].classList.remove('active');
        }

        const targetContent = document.getElementById(this.dataset.id);
        if (targetContent) {
            targetContent.classList.add('active');
            updateBorderColors(this.dataset.id);
        }

        for (let j = 0; j < imgBx.length; j++) {
            imgBx[j].classList.remove('active');
        }

        this.classList.add('active');
    });
}



document.addEventListener("DOMContentLoaded", function() {
    const popupButton = document.getElementById("popup-button");
    const popupMenu = document.getElementById("popup-menu");
    const closeButton = document.getElementById("close-button");
  
    // Show popup menu when the button is clicked
    popupButton.addEventListener("click", function() {
      popupMenu.classList.add("active");
      // Apply blur to the background when the popup is active

    });
  
    // Close the popup menu when the close button is clicked
    closeButton.addEventListener("click", function() {
      popupMenu.classList.remove("active");
      // Remove the blur from the background
      document.body.style.filter = "none";
    });
  });
  
  let currentIconIndex = 0;

  function cycleIcons() {
      // Remove active class from all icons
      imgBx.forEach(icon => icon.classList.remove('active'));
      contentBx.forEach(content => content.classList.remove('active'));
  
      // Set the next icon as active
      imgBx[currentIconIndex].classList.add('active');
      const contentId = imgBx[currentIconIndex].dataset.id;
      const targetContent = document.getElementById(contentId);
      if (targetContent) {
          targetContent.classList.add('active');
          updateBorderColors(contentId);
      }
  
      // Increment index and reset to 0 if it exceeds the length
      currentIconIndex = (currentIconIndex + 1) % 4;
      console.log(currentIconIndex)
  }
  
  // Start cycling every 4 seconds
  setInterval(cycleIcons, 3000);
  function updateTransformOrigin() {
    const container = document.querySelector('.ring');
    const icons = document.querySelectorAll('.container .icon .imgBx');
    const containerWidth = container.offsetWidth;

    // Calculate the transform-origin dynamically
    const transformOriginValue = containerWidth / 1.7;

    // Check if media query condition is met
    if (window.matchMedia('(max-width: 768px)').matches) {
        // Disable dynamic transform-origin for small screens
        icons.forEach((icon) => {
            icon.style.transformOrigin = '165px';
            console.log('Disabled dynamic transform-origin on small screen');
        });
    } else {
        // Apply dynamic transform-origin for larger screens
        icons.forEach((icon) => {
            icon.style.transformOrigin = `${transformOriginValue}px`;
            console.log('Dynamic Transform Origin:', transformOriginValue);
        });
    }
}

// Run on load
updateTransformOrigin();

// Add resize event listener
window.addEventListener('resize', updateTransformOrigin);



// Open Chat Popup with transition
function openChatPopup() {
    const popup = document.getElementById('chat-popup');
    popup.classList.add('open');
}

// Close Chat Popup with transition
function closeChatPopup() {
    const popup = document.getElementById('chat-popup');
    popup.classList.remove('open');
}

// Send message function
function sendMessage() {
    const input = document.getElementById('user-input');
    const messageContainer = document.getElementById('message-container');

    if (input.value.trim() !== "") {
        // Add user message
        const userMessage = document.createElement('div');
        userMessage.classList.add('message', 'user');
        userMessage.innerText = input.value;
        messageContainer.appendChild(userMessage);

        // Clear input field
        input.value = "";

        // Simulate server response (can be replaced with actual Fetch request)
        setTimeout(() => {
            const botMessage = document.createElement('div');
            botMessage.classList.add('message', 'bot');
            botMessage.innerText = "This is a bot reply!";
            messageContainer.appendChild(botMessage);
        }, 1000);
    }
}



function updateBorderColors(contentId) {
    const borderColors = {
        content1: { before: '#2196f3', after: '#f32121' }, // Instagram
        content2: { before: '#25d366', after: '#34B7F1' }, // WhatsApp
        content3: { before: '#1da1f2', after: '#657786' }, // X (formerly Twitter)
        content4: { before: '#4267B2', after: '#1877F2' }  // Facebook
    };
    console.log(contentId)


    const selectedColors = borderColors[contentId];
    console.log('Selected Colors:', selectedColors);

    // Update CSS variables dynamically
    document.documentElement.style.setProperty('--border-before-color', selectedColors.before);
    document.documentElement.style.setProperty('--border-after-color', selectedColors.after);
}


