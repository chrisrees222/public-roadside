
// Get Stripe publishable key
fetch("/config/")
  .then((result) => result.json())
  .then((data) => {
    // Initialize Stripe.js
    const stripe = Stripe(data.publicKey);

    // Event Handler for when button is pressed    
      let sixtySubmit = document.querySelector("#sixtySubmit");
      if (sixtySubmit != null) {
        sixtySubmit.addEventListener("click", () => {
          // Get Checkout Session ID
          fetch("/create-checkout-session-sixty/")
            .then((result) => {
              return result.json();
            })
            .then((data) => {
              console.log(data);
              // Redirect to Stripe Checkout
              return stripe.redirectToCheckout({ sessionId: data.sessionId });
            })
            .then((res) => {
              console.log(res);
            });
          }); 
        };
        let thirtySubmit = document.querySelector("#thirtySubmit");
        if (thirtySubmit != null) {
          thirtySubmit.addEventListener("click", () => {
          // Get Checkout Session ID
            fetch("/create-checkout-session-thirty/")
              .then((result) => {
                return result.json();
              })
              .then((data) => {
               console.log(data);
              // Redirect to Stripe Checkout
                return stripe.redirectToCheckout({ sessionId: data.sessionId });
             })
              .then((res) => {
               console.log(res);
             });
            }); 
          }; 
          let ninetySubmit = document.querySelector("#ninetySubmit");
          if (ninetySubmit != null) {
            ninetySubmit.addEventListener("click", () => {
            // Get Checkout Session ID
              fetch("/create-checkout-session-ninety/")
                .then((result) => {
                  return result.json();
                })
                .then((data) => {
                 console.log(data);
                // Redirect to Stripe Checkout
                  return stripe.redirectToCheckout({ sessionId: data.sessionId });
               })
                .then((res) => {
                 console.log(res);
               });
              }); 
            };       
      }) 

// for when button selected, expands sub menu in profile.
let subMenu = document.getElementById("profile-subMenu") 

function toggleMenu() {
    subMenu.classList.toggle("open-menu")
}

// input for getting postcode.
function f() {
    var t = document.getElementById("input").value;
    getLatLongFromPostcode(t);
}

 //initialises the map by getting the html geolocation.
 (() => {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(success, error);
        } else {
            alert("Geolocation is not supported by this browser");
        }
    }
)();

// to display the location coordinates set functions.
const x = document.getElementById("get_coords");

function getLocation() {
    if (navigator.geolocation) {
        navigator.geolocation.watchPosition(showPosition);
        } else {
            x.innerHTML = "Geolocation is not supported by this browser.";
            }
}

function showPosition(position) {
    //x.innerHTML="Latitude: " + position.coords.latitude +              //show the latitude given
    //"<br>Longitude: " + position.coords.longitude;                     // show the longitude.
    getMap(position.coords.latitude, position.coords.longitude)
}

// End of section to display the coordinates when button clicked.
function success(position) {
    const latitude = position.coords.latitude;
    const longitude = position.coords.longitude;
    getMap(latitude, longitude);
}

// for handling error of failed location.
function error() {
    alert("Unable to retrieve location");
    }

// get the latitude and longitude coordinates from api.postcodes.io.
function getLatLongFromPostcode(postcode) {
    fetch(`https://api.postcodes.io/postcodes/${postcode}`)
    .then(response => response.json())
    .then(data => getMap(data.result.latitude,data.result.longitude))        
}

// displays lat lon in profile when post code is entered and the API is used.
function storeLatLongModel() {
    var a = document.getElementById("postcode").value;
    fetch(`https://api.postcodes.io/postcodes/${a}`)
    .then(response => response.json())
    .then(data => {lat = data.result.latitude, lon = data.result.longitude ;})             
    document.getElementById("latitude").value=lat
    document.getElementById("longitude").value=lon     
}
