import React, { useState } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

const HistoricalDataView = () => {
  const [dataSource, setDataSource] = useState('all');
  const [timeRange, setTimeRange] = useState('1month');
  const [metric, setMetric] = useState('ndvi');

  // Mock data - in a real app, this would be fetched from an API
  const mockData = [
    { date: '2024-04-01', ndvi: 0.65, soilMoisture: 0.28, temperature: 18, satellitePass: true },
    { date: '2024-04-08', ndvi: 0.68, soilMoisture: 0.30, temperature: 20, satellitePass: false },
    { date: '2024-04-15', ndvi: 0.72, soilMoisture: 0.32, temperature: 22, satellitePass: true },
    { date: '2024-04-22', ndvi: 0.75, soilMoisture: 0.29, temperature: 24, satellitePass: false },
    { date: '2024-04-29', ndvi: 0.78, soilMoisture: 0.27, temperature: 26, satellitePass: true },
  ];

  const filteredData = dataSource === 'satellite' 
    ? mockData.filter(item => item.satellitePass)
    : mockData;

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-3xl font-bold mb-6 text-green-700">Historical Farm Data</h1>

      <div className="mb-4 flex justify-between items-center">
        <div>
          <label htmlFor="dataSource" className="mr-2">Data Source:</label>
          <select
            id="dataSource"
            value={dataSource}
            onChange={(e) => setDataSource(e.target.value)}
            className="border rounded p-1"
          >
            <option value="all">All Sources</option>
            <option value="satellite">Satellite Only</option>
            <option value="iot">IoT Sensors Only</option>
          </select>
        </div>
        <div>
          <label htmlFor="timeRange" className="mr-2">Time Range:</label>
          <select
            id="timeRange"
            value={timeRange}
            onChange={(e) => setTimeRange(e.target.value)}
            className="border rounded p-1"
          >
            <option value="1month">Last Month</option>
            <option value="3months">Last 3 Months</option>
            <option value="6months">Last 6 Months</option>
            <option value="1year">Last Year</option>
          </select>
        </div>
        <div>
          <label htmlFor="metric" className="mr-2">Metric:</label>
          <select
            id="metric"
            value={metric}
            onChange={(e) => setMetric(e.target.value)}
            className="border rounded p-1"
          >
            <option value="ndvi">NDVI</option>
            <option value="soilMoisture">Soil Moisture</option>
            <option value="temperature">Temperature</option>
          </select>
        </div>
      </div>

      <div className="bg-white p-4 rounded-lg shadow mb-8">
        <h2 className="text-2xl font-semibold mb-4 text-green-600">{metric.toUpperCase()} Trend</h2>
        <ResponsiveContainer width="100%" height={400}>
          <LineChart data={filteredData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="date" />
            <YAxis />
            <Tooltip />
            <Legend />
            <Line type="monotone" dataKey={metric} stroke="#8884d8" name={metric.toUpperCase()} />
          </LineChart>
        </ResponsiveContainer>
      </div>

      <div className="bg-white p-4 rounded-lg shadow mb-8">
        <h2 className="text-2xl font-semibold mb-4 text-green-600">Data Records</h2>
        <div className="overflow-x-auto">
          <table className="min-w-full bg-white">
            <thead className="bg-green-100">
              <tr>
                <th className="px-4 py-2 text-left">Date</th>
                <th className="px-4 py-2 text-left">NDVI</th>
                <th className="px-4 py-2 text-left">Soil Moisture</th>
                <th className="px-4 py-2 text-left">Temperature (°C)</th>
                <th className="px-4 py-2 text-left">Satellite Pass</th>
                <th className="px-4 py-2 text-left">Actions</th>
              </tr>
            </thead>
            <tbody>
              {filteredData.map((row, index) => (
                <tr key={index} className={index % 2 === 0 ? 'bg-gray-50' : ''}>
                  <td className="px-4 py-2">{row.date}</td>
                  <td className="px-4 py-2">{row.ndvi.toFixed(2)}</td>
                  <td className="px-4 py-2">{row.soilMoisture.toFixed(2)}</td>
                  <td className="px-4 py-2">{row.temperature}</td>
                  <td className="px-4 py-2">{row.satellitePass ? 'Yes' : 'No'}</td>
                  <td className="px-4 py-2">
                    <button className="bg-blue-500 text-white px-2 py-1 rounded text-sm">View Details</button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      <div className="text-center">
        <button className="bg-green-600 text-white px-6 py-2 rounded-full text-lg hover:bg-green-700 mr-4">
          Download Report
        </button>
        <button className="bg-blue-600 text-white px-6 py-2 rounded-full text-lg hover:bg-blue-700">
          Export Raw Data
        </button>
      </div>
    </div>
  );
};

export default HistoricalDataView;
