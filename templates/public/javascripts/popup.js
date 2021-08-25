// Get the modal
var popup = document.getElementById("popup");

// Get the button that opens the modal
var btn = document.getElementById("btn-search");

// Get the <span> element that closes the modal
var span = document.getElementsByClassName("close")[0];

// When the user clicks the button, open the modal
btn.onclick = function() {
    popup.style.display = "block";
}

// When the user clicks on <span> (x), close the modal
span.onclick = function() {
    popup.style.display = "none";
}

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
    if (event.target == popup) {
       popup.style.display = "none";
    }
}
