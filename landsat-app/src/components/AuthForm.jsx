import React, { useState } from 'react';
import { LoadScript, GoogleMap, Marker, Autocomplete } from '@react-google-maps/api';
import { validateEmail } from '../utils/validation';

const AuthForm = ({ formType }) => {
  const [selectedLocation, setSelectedLocation] = useState(null);
  const [mapCenter, setMapCenter] = useState({ lat: -34.397, lng: 150.644 });
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [email, setEmail] = useState('');
  const autocompleteRef = React.useRef(null);

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

  const handleSubmit = (event) => {
    event.preventDefault();
    
    if (formType === 'signIn') {
      if (!username || !password || !email || !validateEmail(email)) {
        alert("Por favor, completa todos los campos y asegúrate de que el correo es válido.");
        return;
      }
      // Lógica para Sign In
    }

    if (formType === 'signUp') {
      if (!username || !password || !validateEmail(email)) {
        alert("Por favor, completa todos los campos y asegúrate de que el correo es válido.");
        return;
      }
      // Lógica para Sign Up
    }

    if (formType === 'guest') {
      if (!email || !validateEmail(email) || !selectedLocation) {
        alert("Por favor, completa todos los campos, asegúrate de que el correo es válido y selecciona una ubicación.");
        return;
      }
      // Lógica para Guest
    }

    alert("Formulario enviado correctamente!");
    // Limpiar los campos
    setUsername('');
    setPassword('');
    setEmail('');
    setSelectedLocation(null);
  };

  return (
    <form className="space-y-4" onSubmit={handleSubmit}>
      {formType === 'signIn' && (
        <>
          <div>
            <label className="block mb-1 font-bold text-gray-700">Username</label>
            <input type="text" value={username} onChange={(e) => setUsername(e.target.value)} className="w-full p-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-500" placeholder="Enter your username" />
          </div>
          <div>
            <label className="block mb-1 font-bold text-gray-700">Password</label>
            <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} className="w-full p-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-500" placeholder="Enter your password" />
          </div>
          <div>
            <label className="block mb-1 font-bold text-gray-700">Correo</label>
            <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} className="w-full p-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-500" placeholder="Enter your email" />
          </div>
          <button type="submit" className="w-full bg-blue-500 text-white p-2 rounded hover:bg-blue-600 transition duration-300">Sign In</button>
        </>
      )}

      {formType === 'signUp' && (
        <>
          <div>
            <label className="block mb-1 font-bold text-gray-700">Correo/Username</label>
            <input type="text" value={username} onChange={(e) => setUsername(e.target.value)} className="w-full p-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-500" placeholder="Enter your email or username" />
          </div>
          <div>
            <label className="block mb-1 font-bold text-gray-700">Password</label>
            <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} className="w-full p-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-500" placeholder="Enter your password" />
          </div>
          <button type="submit" className="w-full bg-blue-500 text-white p-2 rounded hover:bg-blue-600 transition duration-300">Sign Up</button>
        </>
      )}

      {formType === 'guest' && (
        <>
          <div>
            <label className="block mb-1 font-bold text-gray-700">Correo</label>
            <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} className="w-full p-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-500" placeholder="Enter your email" />
          </div>
          <div>
            <label className="block mb-1 font-bold text-gray-700">Ubicación Exacta</label>
            <LoadScript googleMapsApiKey="AIzaSyDFlAmQasoDZSQmjLbLnbjPxNeufX1kLT4" libraries={["places"]}>
              <Autocomplete onLoad={ref => (autocompleteRef.current = ref)} onPlaceChanged={onPlaceChanged}>
                <input type="text" className="w-full p-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-500" placeholder="Buscar ubicación" />
              </Autocomplete>

              <GoogleMap id="example-map" mapContainerStyle={{ height: "400px", width: "100%" }} zoom={10} center={mapCenter} onClick={onMapClick}>
                {selectedLocation && <Marker position={selectedLocation} />}
              </GoogleMap>
            </LoadScript>
          </div>
          <button type="submit" className="w-full bg-blue-500 text-white p-2 rounded hover:bg-blue-600 transition duration-300">Entrar como Invitado</button>
        </>
      )}
    </form>
  );
};

export default AuthForm;
