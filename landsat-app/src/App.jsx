import React, { useState, useRef } from 'react';
import { LoadScript, GoogleMap, Marker, Autocomplete } from '@react-google-maps/api';

function App() {
  const [formType, setFormType] = useState('signIn');
  const [selectedLocation, setSelectedLocation] = useState(null);
  const [mapCenter, setMapCenter] = useState({ lat: -34.397, lng: 150.644 }); // Coordenadas iniciales
  const autocompleteRef = useRef(null);

  // Maneja el cambio de lugar seleccionado del Autocomplete
  const onPlaceChanged = () => {
    if (autocompleteRef.current) {
      const place = autocompleteRef.current.getPlace();
      if (place.geometry && place.geometry.location) {
        setSelectedLocation({
          lat: place.geometry.location.lat(),
          lng: place.geometry.location.lng(),
        });
        setMapCenter({
          lat: place.geometry.location.lat(),
          lng: place.geometry.location.lng(),
        });
      }
    }
  };

  // Maneja el clic en el mapa para seleccionar una ubicación
  const onMapClick = (event) => {
    setSelectedLocation({
      lat: event.latLng.lat(),
      lng: event.latLng.lng(),
    });
    setMapCenter({
      lat: event.latLng.lat(),
      lng: event.latLng.lng(),
    });
  };

  return (
    <div className="flex justify-center items-center min-h-screen bg-gray-100">
      <div className="bg-white p-8 rounded-lg shadow-lg w-full max-w-md">
        <h1 className="text-2xl font-bold mb-6 text-center">LandsatClusterC</h1>

        <div className="flex justify-around mb-4">
          <button
            className={`px-4 py-2 rounded ${formType === 'signIn' ? 'bg-blue-500 text-white' : 'bg-gray-200'}`}
            onClick={() => setFormType('signIn')}
          >
            Sign In
          </button>
          <button
            className={`px-4 py-2 rounded ${formType === 'signUp' ? 'bg-blue-500 text-white' : 'bg-gray-200'}`}
            onClick={() => setFormType('signUp')}
          >
            Sign Up
          </button>
          <button
            className={`px-4 py-2 rounded ${formType === 'guest' ? 'bg-blue-500 text-white' : 'bg-gray-200'}`}
            onClick={() => setFormType('guest')}
          >
            Guest
          </button>
        </div>

        <div className="bg-gray-50 p-6 rounded-lg shadow-md">
          {/* Renderizar el formulario basado en el tipo seleccionado */}
          {formType === 'signIn' && (
            <form className="space-y-4">
              <div>
                <label className="block mb-1 font-bold text-gray-700">Username</label>
                <input type="text" className="w-full p-2 border border-gray-300 rounded" placeholder="Enter your username" required />
              </div>
              <div>
                <label className="block mb-1 font-bold text-gray-700">Password</label>
                <input type="password" className="w-full p-2 border border-gray-300 rounded" placeholder="Enter your password" required />
              </div>
              <div>
                <label className="block mb-1 font-bold text-gray-700">Correo</label>
                <input type="email" className="w-full p-2 border border-gray-300 rounded" placeholder="Enter your email" required />
              </div>
              <button className="w-full bg-blue-500 text-white p-2 rounded">Sign In</button>
            </form>
          )}

          {formType === 'signUp' && (
            <form className="space-y-4">
              <div>
                <label className="block mb-1 font-bold text-gray-700">Correo/Username</label>
                <input type="text" className="w-full p-2 border border-gray-300 rounded" placeholder="Enter your email or username" required />
              </div>
              <div>
                <label className="block mb-1 font-bold text-gray-700">Password</label>
                <input type="password" className="w-full p-2 border border-gray-300 rounded" placeholder="Enter your password" required />
              </div>
              <button className="w-full bg-blue-500 text-white p-2 rounded">Sign Up</button>
            </form>
          )}

          {formType === 'guest' && (
            <form className="space-y-4">
              <div>
                <label className="block mb-1 font-bold text-gray-700">Correo</label>
                <input type="email" className="w-full p-2 border border-gray-300 rounded" placeholder="Enter your email" required />
              </div>
              <div>
                <label className="block mb-1 font-bold text-gray-700">Ubicación Exacta</label>

                {/* Google Maps Autocomplete para la ubicación */}
                <LoadScript googleMapsApiKey="AIzaSyDFlAmQasoDZSQmjLbLnbjPxNeufX1kLT4" libraries={["places"]}>
                  <Autocomplete
                    onLoad={ref => (autocompleteRef.current = ref)}
                    onPlaceChanged={onPlaceChanged}
                  >
                    <input
                      type="text"
                      className="w-full p-2 border border-gray-300 rounded"
                      placeholder="Buscar ubicación"
                      required
                    />
                  </Autocomplete>

                  {/* Mostrar el mapa */}
                  <GoogleMap
                    id="example-map"
                    mapContainerStyle={{
                      height: "300px",
                      width: "100%",
                    }}
                    zoom={10}
                    center={mapCenter}
                    onClick={onMapClick} // Manejar clic en el mapa
                  >
                    {/* Mostrar el marcador en la ubicación seleccionada */}
                    {selectedLocation && <Marker position={selectedLocation} />}
                  </GoogleMap>
                </LoadScript>

                {/* Mostrar la ubicación seleccionada */}
                {selectedLocation && (
                  <p className="mt-2 text-sm text-gray-500">
                    Ubicación seleccionada: {`Lat: ${selectedLocation.lat}, Lng: ${selectedLocation.lng}`}
                  </p>
                )}
              </div>
              <button className="w-full bg-blue-500 text-white p-2 rounded">Submit</button>
            </form>
          )}
        </div>
      </div>
    </div>
  );
}

export default App;
