function initMap() {
    const myLatlng = { lat: 39.5, lng: -98.35 };
    const map = new google.maps.Map(document.getElementById("map"), {
      zoom: 4,
      center: myLatlng,
    });
    // Create the initial InfoWindow.
    let infoWindow = new google.maps.InfoWindow({
      content: "Click the map to get Lat/Lng!",
      position: myLatlng,
    });
    infoWindow.open(map);
    // Configure the click listener.
    map.addListener("click", (mapsMouseEvent) => {
      // Close the current InfoWindow.
      infoWindow.close();
      // Create a new InfoWindow.
      infoWindow = new google.maps.InfoWindow({
        position: mapsMouseEvent.latLng,
      });      
      let thisobject = mapsMouseEvent.latLng
      
      infoWindow.setContent(
        JSON.stringify(mapsMouseEvent.latLng.toJSON(), null, 2)
        
      ); $('#latbox').val(thisobject.lat())
      $('#lngbox').val(thisobject.lng())
      infoWindow.open(map);
    });
  }