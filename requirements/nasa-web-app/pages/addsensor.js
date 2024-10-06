import { useState } from 'react';

const AddSensorData = () => {
  const [formData, setFormData] = useState({
    soilMoisture: '',
    temperature: '',
    humidity: '',
    soilpH: '',
    nitrogen: '',
    phosphorus: '',
    potassium: '',
  });

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prevData => ({
      ...prevData,
      [name]: value
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    // Here you would typically send the data to your backend
    console.log('Submitting sensor data:', formData);
    // Reset form or show success message
  };

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-3xl font-bold mb-6 text-green-700">Add Sensor Data for Satellite Pass</h1>
      
      <div className="bg-yellow-100 border-l-4 border-yellow-500 text-yellow-700 p-4 mb-8" role="alert">
        <p className="font-bold">Important</p>
        <p>Please ensure all sensor readings are taken within 30 minutes of the satellite pass for optimal data correlation.</p>
      </div>

      <form onSubmit={handleSubmit} className="bg-white p-6 rounded-lg shadow-md">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <label htmlFor="soilMoisture" className="block text-sm font-medium text-gray-700">Soil Moisture (%)</label>
            <input
              type="number"
              id="soilMoisture"
              name="soilMoisture"
              value={formData.soilMoisture}
              onChange={handleInputChange}
              className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-green-500 focus:ring focus:ring-green-200"
              required
            />
          </div>
          <div>
            <label htmlFor="temperature" className="block text-sm font-medium text-gray-700">Temperature (°C)</label>
            <input
              type="number"
              id="temperature"
              name="temperature"
              value={formData.temperature}
              onChange={handleInputChange}
              className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-green-500 focus:ring focus:ring-green-200"
              required
            />
          </div>
          <div>
            <label htmlFor="humidity" className="block text-sm font-medium text-gray-700">Humidity (%)</label>
            <input
              type="number"
              id="humidity"
              name="humidity"
              value={formData.humidity}
              onChange={handleInputChange}
              className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-green-500 focus:ring focus:ring-green-200"
              required
            />
          </div>
          <div>
            <label htmlFor="soilpH" className="block text-sm font-medium text-gray-700">Soil pH</label>
            <input
              type="number"
              id="soilpH"
              name="soilpH"
              value={formData.soilpH}
              onChange={handleInputChange}
              className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-green-500 focus:ring focus:ring-green-200"
              step="0.1"
              required
            />
          </div>
          <div>
            <label htmlFor="nitrogen" className="block text-sm font-medium text-gray-700">Nitrogen (ppm)</label>
            <input
              type="number"
              id="nitrogen"
              name="nitrogen"
              value={formData.nitrogen}
              onChange={handleInputChange}
              className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-green-500 focus:ring focus:ring-green-200"
              required
            />
          </div>
          <div>
            <label htmlFor="phosphorus" className="block text-sm font-medium text-gray-700">Phosphorus (ppm)</label>
            <input
              type="number"
              id="phosphorus"
              name="phosphorus"
              value={formData.phosphorus}
              onChange={handleInputChange}
              className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-green-500 focus:ring focus:ring-green-200"
              required
            />
          </div>
          <div>
            <label htmlFor="potassium" className="block text-sm font-medium text-gray-700">Potassium (ppm)</label>
            <input
              type="number"
              id="potassium"
              name="potassium"
              value={formData.potassium}
              onChange={handleInputChange}
              className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-green-500 focus:ring focus:ring-green-200"
              required
            />
          </div>
        </div>
        <div className="mt-6">
          <button type="submit" className="w-full bg-green-600 text-white py-2 px-4 rounded-md hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-green-500 focus:ring-opacity-50">
            Submit Sensor Data
          </button>
        </div>
      </form>
    </div>
  );
};

export default AddSensorData;
