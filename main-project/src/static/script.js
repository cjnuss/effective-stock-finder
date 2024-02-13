function replaceButtonWithText() {
    var contentContainer = document.querySelector('.content');
    var newTextElement = document.createElement('p');
    // newTextElement.textContent = flaskText2; // passed from HTML
    newTextElement.textContent = "test test blah blah";
    var buttonElement = document.querySelector('button');
    buttonElement.remove();
    contentContainer.appendChild(newTextElement);
}

function stockRec() {
    document.getElementById("stock_rec").submit();
}

window.addEventListener('beforeunload', function() {
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/refresh');
    xhr.send();
});
