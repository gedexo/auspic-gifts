

// Predefined arrays for toast messages and types
const toastArray = ['Message One', 'Message Two', 'Message Three', 'Message Four', 'Message Five'];
const types = ['info', 'warning', 'success', 'error'];
function createNotification(message = null, type = null) {
    // Create a new div element for the toast notification
    const notIf = document.createElement('div');
    notIf.classList.add('toast'); // Add the 'toast' class for styling
    notIf.classList.add(type ? type : getRandomTypes()); // Add a type class (random if not provided)

    // Set the text content of the toast (random message if not provided)
    notIf.innerText = message ? message : getRandomMessage();
    toasts.appendChild(notIf); // Append the toast to the toast container

    // Remove the toast after 3 seconds
    setTimeout(() => {
        notIf.remove();
    }, 3000);
}