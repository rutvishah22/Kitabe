document.addEventListener('DOMContentLoaded', function() {
    const locationBtn = document.getElementById('location-btn');
    const cityInput = document.getElementById('city-input');
    
    if (locationBtn && cityInput) {
        locationBtn.addEventListener('click', function() {
            if (navigator.geolocation) {
                locationBtn.textContent = 'Getting location...';
                locationBtn.disabled = true;
                
                navigator.geolocation.getCurrentPosition(
                    function(position) {
                        // In a real app, you would use a geocoding service to get the city name
                        // For this example, we'll simulate it
                        getCityFromCoordinates(position.coords.latitude, position.coords.longitude)
                            .then(function(city) {
                                cityInput.value = city;
                                locationBtn.textContent = 'Use My Location';
                                locationBtn.disabled = false;
                                
                                // Auto-submit the form
                                cityInput.form.submit();
                            })
                            .catch(function(error) {
                                console.error('Error getting city:', error);
                                locationBtn.textContent = 'Use My Location';
                                locationBtn.disabled = false;
                                alert('Could not determine your city. Please enter it manually.');
                            });
                    },
                    function(error) {
                        console.error('Geolocation error:', error);
                        locationBtn.textContent = 'Use My Location';
                        locationBtn.disabled = false;
                        
                        if (error.code === error.PERMISSION_DENIED) {
                            alert('Location access denied. Please enter your city manually.');
                        } else {
                            alert('Could not get your location. Please enter your city manually.');
                        }
                    }
                );
            } else {
                alert('Geolocation is not supported by your browser. Please enter your city manually.');
            }
        });
    }
    
    // Simulate getting city from coordinates
    // In a real app, you would use a geocoding service like Google Maps API
    function getCityFromCoordinates(latitude, longitude) {
        return new Promise(function(resolve, reject) {
            // Simulate API call delay
            setTimeout(function() {
                // For demo purposes, return a random city
                const cities = ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix', 'Philadelphia', 'San Antonio', 'San Diego', 'Dallas', 'San Jose'];
                const randomCity = cities[Math.floor(Math.random() * cities.length)];
                resolve(randomCity);
            }, 1000);
        });
    }
});