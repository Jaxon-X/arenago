document.addEventListener('DOMContentLoaded', function () {
    const locationInput = document.getElementById('id_location');

    if (locationInput) {
        const getLocationBtn = document.createElement('button');
        getLocationBtn.type = 'button';
        getLocationBtn.innerText = 'Mening Joylashuvim (GPS)';
        getLocationBtn.style.marginLeft = '10px';
        getLocationBtn.style.padding = '5px 10px';
        getLocationBtn.style.cursor = 'pointer';
        getLocationBtn.style.backgroundColor = '#417690'; // Django admin button color
        getLocationBtn.style.color = 'white';
        getLocationBtn.style.border = 'none';
        getLocationBtn.style.borderRadius = '4px';

        // Insert the button after the input field
        locationInput.parentNode.insertBefore(getLocationBtn, locationInput.nextSibling);

        getLocationBtn.addEventListener('click', function () {
            if (navigator.geolocation) {
                getLocationBtn.innerText = 'Joylashuv olinmoqda...';
                getLocationBtn.disabled = true;

                navigator.geolocation.getCurrentPosition(
                    function (position) {
                        const lat = position.coords.latitude;
                        const lon = position.coords.longitude;

                        // Format: POINT (longitude latitude)
                        const wkt = `POINT (${lon} ${lat})`;
                        locationInput.value = wkt;

                        // Trigger change event for OSMWidget or other listeners
                        // We need to use a native event dispatch because jQuery might not be available or used differently
                        // But Django admin usually has jQuery as django.jQuery

                        // Try standard event
                        const event = new Event('change', { bubbles: true });
                        locationInput.dispatchEvent(event);

                        getLocationBtn.innerText = 'Mening Joylashuvim (GPS)';
                        getLocationBtn.disabled = false;

                        if (confirm(`Joylashuv aniqlandi:\nKenglik: ${lat}\nUzunlik: ${lon}\n\nGoogle Maps-da ko'rishni xohlaysizmi?`)) {
                            window.open(`https://www.google.com/maps?q=${lat},${lon}`, '_blank');
                        }
                    },
                    function (error) {
                        console.error('Error getting location:', error);
                        let errorMsg = 'Joylashuvni olishda xatolik yuz berdi.';
                        switch (error.code) {
                            case error.PERMISSION_DENIED:
                                errorMsg = "Joylashuvni olishga ruxsat berilmadi.";
                                break;
                            case error.POSITION_UNAVAILABLE:
                                errorMsg = "Joylashuv ma'lumotlari mavjud emas.";
                                break;
                            case error.TIMEOUT:
                                errorMsg = "So'rov vaqti tugadi.";
                                break;
                            case error.UNKNOWN_ERROR:
                                errorMsg = "Noma'lum xatolik yuz berdi.";
                                break;
                        }
                        alert(errorMsg);
                        getLocationBtn.innerText = 'Mening Joylashuvim (GPS)';
                        getLocationBtn.disabled = false;
                    },
                    {
                        enableHighAccuracy: true,
                        timeout: 10000,
                        maximumAge: 0
                    }
                );
            } else {
                alert('Sizning brauzeringiz Geolocation-ni qo\'llab-quvvatlamaydi.');
            }
        });
    }
});
