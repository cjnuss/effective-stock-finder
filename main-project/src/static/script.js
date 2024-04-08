//Submits the form to load the page with information about the current best stock to buy
function stockRec() {
    document.getElementById("stock_rec").submit();
}

//Variables that store stocks that are up, down and no change
var plusStock = document.querySelectorAll("#plus-stock, #plus-index");
var noChangeStock = document.querySelectorAll("#no-change-stock, #no-change-index");
var minusStock = document.querySelectorAll("#minus-stock, #minus-index");

//Gives green left border to stocks that are up 
plusStock.forEach(function(x) {
    x.style.backgroundColor = "#31cc5a";
});

//Gives grey left border to stocks that didn't change
noChangeStock.forEach(function(x) {
    x.style.backgroundColor = "grey";
});

//Gives red left border to stocks that are down 
minusStock.forEach(function(x) {
    x.style.backgroundColor = "#c73e43";
});

//Goes back to the home page when back button is clicked
function goBack() {
    window.location.href = "/";
}

//Changes the mode between light and dark on button click
function toggleMode() {
    var body = document.body;
    var darkModeButton = document.getElementById('dark-mode-button');
    var isDarkMode = body.classList.toggle('dark-mode');
    //Changes the text of the button if it has been clicked
    if (isDarkMode) {
        darkModeButton.textContent = 'Light Mode';
    } else {
        darkModeButton.textContent = 'Dark Mode';
    }
    //Makes sure the setting is saved locally so next time you load the website the mode is set to what you last set
    localStorage.setItem('isDarkMode', isDarkMode);
}

//Changes the mode to dark mode if you changed it to dark mode last time you used the website
function loadMode() {
    var isDarkMode = localStorage.getItem('isDarkMode');
    if (isDarkMode === 'true') {
        document.body.classList.add('dark-mode');
        document.getElementById('dark-mode-button').textContent = 'Light Mode';
    }
}

//Calls the loadMode function once the page loads
window.addEventListener('load', loadMode);

//Creates the plot for the best stock based on the data
function initializePlot() {
    //Gets the data and the color for the line
    var plotData = JSON.parse(document.getElementById("plot").getAttribute('data-plot'));
    var color = document.getElementById("plot").getAttribute('color')
    //Styles the data and makes the points pop up when hovered over
    var data = {
        x: plotData.map(entry => entry.Date),
        y: plotData.map(entry => entry.Value),
        type: 'scatter',
        mode: 'lines+markers', 
        line: {
            color: color,
            width: 1
        },
        marker: {
            size: 5,
            opacity: 0 
        },
        hoverinfo: 'y', 
        hoveron: 'points'
    };

    //Styles the layout of the plot
    var layout = {
        title: {
                text: 'Stock Market Data',
                font: {
                    color: '#fff'  
                }
            },
        xaxis: {
            title: {
                text: 'Date',
                font: {
                    color: '#fff' 
                }
            },
            tickformat: '%Y-%m-%d',
            showgrid: true,
            gridcolor: '#222',  
            linecolor: '#fff', 
            linewidth: 1,
            ticks: 'inside',
            ticklen: 5,
            tickfont: {
                color: '#fff' 
            }
        },
        yaxis: {
            title: {
                text: 'Price',
                font: {
                    color: '#fff'  
                }
            },
            showgrid: true,
            gridcolor: '#444',  
            gridwidth: 1, 
            linecolor: '#fff',  
            linewidth: 0,  
            ticks: 'inside',
            ticklen: 5,
            tickfont: {
                color: '#fff'  
            }
        },
        hovermode: 'x',
        plot_bgcolor: '#222',  
        paper_bgcolor: '#111',  

        margin: {
            l: 75,  
            r: 75,  
            t: 75,  
            b: 75   
        }
    };

    Plotly.newPlot('plot', [data], layout);
}

//Calls the initializePlot function when the page is loaded
document.addEventListener("DOMContentLoaded", function() {
    initializePlot();
});