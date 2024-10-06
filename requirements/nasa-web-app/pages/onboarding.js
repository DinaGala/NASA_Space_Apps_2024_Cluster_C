import React from 'react';

const OnboardingPage = () => {
  const farmTypes = [
    { id: 'crop', label: 'Crop Farming' },
    { id: 'livestock', label: 'Livestock' },
    { id: 'mixed', label: 'Mixed Farming' },
    { id: 'organic', label: 'Organic Farming' },
    { id: 'greenhouse', label: 'Greenhouse' },
    { id: 'orchard', label: 'Orchard' },
  ];

  const indicators = [
    { id: 'ndvi', label: 'NDVI (Vegetation Health)' },
    { id: 'lai', label: 'LAI (Leaf Area Index)' },
    { id: 'evi', label: 'EVI (Enhanced Vegetation Index)' },
    { id: 'ndwi', label: 'NDWI (Water Content)' },
    { id: 'soil_moisture', label: 'Soil Moisture' },
    { id: 'temperature', label: 'Surface Temperature' },
    { id: 'chlorophyll', label: 'Chlorophyll Content' },
    { id: 'nitrogen', label: 'Nitrogen Content' },
  ];

  return (
    <div className="container mx-auto p-4 max-w-2xl">
      <h1 className="text-3xl font-bold mb-6 text-center text-green-700">Welcome to Smart Agriculture</h1>
      
      <div className="bg-white p-6 rounded-lg shadow-md mb-6">
        <h2 className="text-2xl font-semibold mb-4 text-green-600">Tell us about your farm</h2>
        <p className="mb-4">Select your primary farming type:</p>
        <div className="grid grid-cols-2 gap-4 mb-6">
          {farmTypes.map(type => (
            <div key={type.id} className="flex items-center">
              <input type="radio" id={type.id} name="farmType" className="mr-2" />
              <label htmlFor={type.id}>{type.label}</label>
            </div>
          ))}
        </div>
      </div>

      <div className="bg-white p-6 rounded-lg shadow-md mb-6">
        <h2 className="text-2xl font-semibold mb-4 text-green-600">Choose indicators to monitor</h2>
        <p className="mb-4">Select the indicators most relevant to your farm:</p>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {indicators.map(indicator => (
            <div key={indicator.id} className="flex items-center">
              <input type="checkbox" id={indicator.id} className="mr-2" />
              <label htmlFor={indicator.id}>{indicator.label}</label>
            </div>
          ))}
        </div>
      </div>

      <div className="bg-white p-6 rounded-lg shadow-md mb-6">
        <h2 className="text-2xl font-semibold mb-4 text-green-600">Set your farm location</h2>
        <p className="mb-4">Enter your farm's address or coordinates:</p>
        <input type="text" placeholder="Enter address or coordinates" className="w-full p-2 border rounded mb-4" />
        <div className="h-40 bg-gray-200 rounded flex items-center justify-center mb-4">
          [Map preview would be displayed here]
        </div>
        <button className="bg-green-500 text-white p-2 rounded w-full">Confirm Location</button>
      </div>

      <div className="bg-white p-6 rounded-lg shadow-md mb-6">
        <h2 className="text-2xl font-semibold mb-4 text-green-600">Notification preferences</h2>
        <p className="mb-4">How often would you like to receive farm insights?</p>
        <select className="w-full p-2 border rounded mb-4">
          <option>Daily</option>
          <option>Weekly</option>
          <option>Bi-weekly</option>
          <option>Monthly</option>
        </select>
      </div>

      <button className="bg-green-600 text-white p-3 rounded w-full text-lg font-semibold hover:bg-green-700">
        Complete Setup and View Your Farm Dashboard
      </button>
    </div>
  );
};

export default OnboardingPage;
