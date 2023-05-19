// Start of pricing script 
function getCountryCode() {
    var theUrl = 'https://pro.ip-api.com/json?key=mABwd9BINggwJrN&fields=countryCode';
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open("GET", theUrl, false); // false for synchronous request
    xmlHttp.send(null);
    var response = JSON.parse(xmlHttp.responseText);
    return response.countryCode;
}

function getCurrencyInfo(countryCode) {
    var theUrl = `https://kyte-prices.azurewebsites.net/plans/${countryCode}`;
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open("GET", theUrl, false); // false for synchronous request
    xmlHttp.send(null);
    var response = JSON.parse(xmlHttp.responseText);
    return response;
};

const countryCode = getCountryCode();
const currencyGroup = getCurrencyInfo(countryCode);


// set values on DOM
document.getElementById("pro-monthly").innerHTML = currencyGroup.pro.monthly;
document.getElementById("pro-yearly").innerHTML = currencyGroup.pro.yearly;
document.getElementById("grow-monthly").innerHTML = currencyGroup.grow.monthly;
document.getElementById("grow-yearly").innerHTML = currencyGroup.grow.yearly;
document.getElementById("prime").innerHTML = currencyGroup.prime.yearly;
document.getElementById("prime-yearly").innerHTML = currencyGroup.prime.yearly;

// End of pricing script 
