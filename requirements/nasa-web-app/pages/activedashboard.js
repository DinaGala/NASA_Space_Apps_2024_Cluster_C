import React, { useState } from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import Link from "next/link"
const Dashboard = () => {
  const [sensorData, setSensorData] = useState({
    soilMoisture: '',
    temperature: '',
    humidity: '',
  });

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setSensorData((prevData) => ({
      ...prevData,
      [name]: value,
    }));
  };

  const handleSubmitSensorData = (e) => {
    e.preventDefault();
    console.log('Submitting sensor data:', sensorData);
    alert('Sensor data submitted successfully!');
    setSensorData({ soilMoisture: '', temperature: '', humidity: '' });
  };

  const mockData = [
    { name: 'Field A', ndvi: 0.8, soilMoisture: 0.3 },
    { name: 'Field B', ndvi: 0.7, soilMoisture: 0.25 },
    { name: 'Field C', ndvi: 0.75, soilMoisture: 0.28 },
    { name: 'Field D', ndvi: 0.85, soilMoisture: 0.32 },
  ];

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-3xl font-bold mb-6 text-green-700">Farm Dashboard</h1>

      <div className="bg-green-100 border-l-4 border-green-500 text-green-700 p-4 mb-8" role="alert">
        <div className="flex items-center">
          <div className="py-1">
            <svg
              className="fill-current h-6 w-6 text-green-500 mr-4"
              xmlns="http://www.w3.org/2000/svg"
              viewBox="0 0 20 20"
            >
              <path d="M2.93 17.07A10 10 0 1 1 17.07 2.93 10 10 0 0 1 2.93 17.07zm12.73-1.41A8 8 0 1 0 4.34 4.34a8 8 0 0 0 11.32 11.32zM9 11V9h2v6H9v-4zm0-6h2v2H9V5z" />
            </svg>
          </div>
          <div>
            <p className="font-bold">Satellite Pass Active</p>
            <p className="text-sm">Current pass window: Next 20 minutes</p>
          </div>
        </div>
      </div>

      <div className="bg-white p-6 rounded-lg shadow-md mb-8">
        <h2 className="text-2xl font-semibold mb-4 text-green-600">Add Sensor Data</h2>
        <form onSubmit={handleSubmitSensorData} className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div>
              <label htmlFor="soilMoisture" className="block text-sm font-medium text-gray-700">
                Soil Moisture (%)
              </label>
              <input
                type="number"
                id="soilMoisture"
                name="soilMoisture"
                value={sensorData.soilMoisture}
                onChange={handleInputChange}
                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-green-500 focus:ring focus:ring-green-200"
                required
              />
            </div>
            <div>
              <label htmlFor="temperature" className="block text-sm font-medium text-gray-700">
                Temperature (°C)
              </label>
              <input
                type="number"
                id="temperature"
                name="temperature"
                value={sensorData.temperature}
                onChange={handleInputChange}
                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-green-500 focus:ring focus:ring-green-200"
                required
              />
            </div>
            <div>
              <label htmlFor="humidity" className="block text-sm font-medium text-gray-700">
                Humidity (%)
              </label>
              <input
                type="number"
                id="humidity"
                name="humidity"
                value={sensorData.humidity}
                onChange={handleInputChange}
                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-green-500 focus:ring focus:ring-green-200"
                required
              />
            </div>
          </div>
          <Link href = "addsensor">
          <button
            type="submit"
            className="w-full bg-green-600 text-white py-2 px-4 rounded-md hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-green-500 focus:ring-opacity-50"
          >
            Submit Sensor Data
          </button>
          </Link>
        </form>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
        <div className="bg-white p-4 rounded-lg shadow">
          <h2 className="text-xl font-semibold mb-2 text-green-600">Average NDVI</h2>
          <p className="text-3xl font-bold">0.75</p>
          <p className="text-sm text-gray-500">Healthy vegetation</p>
        </div>
        <div className="bg-white p-4 rounded-lg shadow">
          <h2 className="text-xl font-semibold mb-2 text-green-600">Soil Moisture</h2>
          <p className="text-3xl font-bold">28%</p>
          <p className="text-sm text-gray-500">Optimal range</p>
        </div>
        <div className="bg-white p-4 rounded-lg shadow">
          <h2 className="text-xl font-semibold mb-2 text-green-600">Temperature</h2>
          <p className="text-3xl font-bold">22°C</p>
          <p className="text-sm text-gray-500">Current reading</p>
        </div>
      </div>

      <div className="bg-white p-4 rounded-lg shadow mb-8">
        <h2 className="text-2xl font-semibold mb-4 text-green-600">Field Overview</h2>
        <ResponsiveContainer width="100%" height={300}>
          <BarChart data={mockData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="name" />
            <YAxis yAxisId="left" orientation="left" stroke="#8884d8" />
            <YAxis yAxisId="right" orientation="right" stroke="#82ca9d" />
            <Tooltip />
            <Legend />
            <Bar yAxisId="left" dataKey="ndvi" fill="#8884d8" name="NDVI" />
            <Bar yAxisId="right" dataKey="soilMoisture" fill="#82ca9d" name="Soil Moisture" />
          </BarChart>
        </ResponsiveContainer>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-8">
        <div className="bg-white p-4 rounded-lg shadow">
          <h2 className="text-xl font-semibold mb-2 text-green-600">Recent Alerts</h2>
          <ul className="space-y-2">
            <li className="text-red-500">Low soil moisture detected in Field B</li>
            <li className="text-yellow-500">Potential pest infestation in Field C</li>
            <li className="text-green-500">Optimal conditions for harvesting in Field A</li>
          </ul>
        </div>
        <div className="bg-white p-4 rounded-lg shadow">
          <h2 className="text-xl font-semibold mb-2 text-green-600">Recommendations</h2>
          <ul className="space-y-2">
            <li>Increase irrigation in Field B</li>
            <li>Schedule pest inspection for Field C</li>
            <li>Prepare harvesting equipment for Field A</li>
          </ul>
        </div>
      </div>

      <div className="text-center">
        <Link href = "/historical-data">
        <button className="bg-green-600 text-white px-6 py-2 rounded-full text-lg hover:bg-green-700">
          View Detailed Reports
        </button>
        </Link>
      </div>
    </div>
  );
};

export default Dashboard;
