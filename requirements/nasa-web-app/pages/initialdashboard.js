import { useState, useEffect } from 'react'; // No need for 'React' import in Next.js 13+
import Link from 'next/link';
const InitialPassDashboard = () => {
  const [countdown, setCountdown] = useState({
    days: 1,
    hours: 2,
    minutes: 24,
    seconds: 28,
  });

  const [sensorData, setSensorData] = useState({
    soilMoisture: '',
    temperature: '',
    cropHeight: '',
  });

  useEffect(() => {
    const totalSeconds =
      countdown.days * 86400 +
      countdown.hours * 3600 +
      countdown.minutes * 60 +
      countdown.seconds;
    let secondsLeft = totalSeconds;

    const timer = setInterval(() => {
      if (secondsLeft > 0) {
        secondsLeft--;
        const d = Math.floor(secondsLeft / 86400);
        const h = Math.floor((secondsLeft % 86400) / 3600);
        const m = Math.floor((secondsLeft % 3600) / 60);
        const s = secondsLeft % 60;

        setCountdown({ days: d, hours: h, minutes: m, seconds: s });
      } else {
        clearInterval(timer);
        // Handle countdown finished
      }
    }, 1000);

    return () => clearInterval(timer);
  }, [countdown]);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setSensorData((prevData) => ({
      ...prevData,
      [name]: value,
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log('Submitting sensor data:', sensorData);
    // Here you would typically send the data to your backend
  };

  return (
    <div className="container mx-auto p-4 max-w-4xl">
      <h1 className="text-3xl font-bold mb-6 text-green-700">
        Welcome to Your Smart Farm Dashboard
      </h1>

      <div
        className="bg-blue-100 border-l-4 border-blue-500 text-blue-700 p-4 mb-8"
        role="alert"
      >
        <h2 className="font-bold text-xl mb-2">First Satellite Pass Coming Up!</h2>
        <p className="mb-2">
          Prepare for your farm's first satellite data collection. This initial
          pass is crucial for establishing baseline data for your fields.
        </p>
        <p>
          <strong>Estimated Time:</strong> June 15, 2024, 10:30 AM (Local Time)
        </p>
      </div>

      <div className="bg-gray-100 p-4 rounded-lg mb-8">
        <h2 className="text-2xl font-semibold mb-4 text-center">
          Next Satellite Pass
        </h2>
        <div className="flex justify-center space-x-4">
          {Object.entries(countdown).map(([unit, value]) => (
            <div key={unit} className="text-center">
              <div className="bg-white rounded-lg shadow-md p-3 mb-2">
                <span className="text-4xl font-bold text-green-600 countdown-animation">
                  {value.toString().padStart(2, '0')}
                </span>
              </div>
              <span className="text-sm text-gray-600">{unit}</span>
            </div>
          ))}
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-8 mb-8">
        <div className="bg-white p-6 rounded-lg shadow-md">
          <h2 className="text-2xl font-semibold mb-4 text-green-600">
            Why This is Important
          </h2>
          <ul className="list-disc pl-5 space-y-2">
            <li>Establishes a baseline for future comparisons</li>
            <li>Helps calibrate satellite data with ground conditions</li>
            <li>Enables more accurate crop health monitoring</li>
            <li>Initiates personalized insights for your farm</li>
          </ul>
        </div>
        <div className="bg-white p-6 rounded-lg shadow-md">
          <h2 className="text-2xl font-semibold mb-4 text-green-600">
            Preparation Checklist
          </h2>
          <ul className="space-y-2">
            <li>
              <input type="checkbox" id="sensors" className="mr-2" />
              <label htmlFor="sensors">Ensure all ground sensors are operational</label>
            </li>
            <li>
              <input type="checkbox" id="fields" className="mr-2" />
              <label htmlFor="fields">Confirm field boundaries in the app</label>
            </li>
            <li>
              <input type="checkbox" id="crops" className="mr-2" />
              <label htmlFor="crops">Update crop types for each field</label>
            </li>
            <li>
              <input type="checkbox" id="weather" className="mr-2" />
              <label htmlFor="weather">Check weather forecast for clear skies</label>
            </li>
          </ul>
        </div>
      </div>

      <div className="bg-white p-6 rounded-lg shadow-md mb-8">
        <h2 className="text-2xl font-semibold mb-4 text-green-600">
          Input Initial Sensor Data
        </h2>
        <p className="mb-4 text-gray-600">
          Please enter the following data on the day of the satellite pass:
        </p>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label
              htmlFor="soilMoisture"
              className="block text-sm font-medium text-gray-700"
            >
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
            <label
              htmlFor="temperature"
              className="block text-sm font-medium text-gray-700"
            >
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
            <label
              htmlFor="cropHeight"
              className="block text-sm font-medium text-gray-700"
            >
              Avg. Crop Height (cm)
            </label>
            <input
              type="number"
              id="cropHeight"
              name="cropHeight"
              value={sensorData.cropHeight}
              onChange={handleInputChange}
              className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-green-500 focus:ring focus:ring-green-200"
              required
            />
          </div>
          <Link href="activedashboard">
          <button
            type="submit"
            className="w-full bg-green-600 text-white py-2 px-4 rounded-md hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-green-500 focus:ring-opacity-50"
          >
            Submit Initial Data
          </button>
          </Link>
        </form>
      </div>

      <div className="bg-white p-6 rounded-lg shadow-md mb-8">
        <h2 className="text-2xl font-semibold mb-4 text-green-600">
          What Happens Next?
        </h2>
        <ol className="list-decimal pl-5 space-y-2">
          <li>Our satellites will capture detailed imagery of your farm.</li>
          <li>
            We'll process the data and combine it with your ground sensor
            readings.
          </li>
          <li>
            Within 48 hours, you'll receive your first comprehensive farm health
            report.
          </li>
          <li>
            Our system will start generating personalized insights and
            recommendations.
          </li>
        </ol>
      </div>

      <div className="text-center">
        <button className="bg-green-600 text-white px-6 py-2 rounded-full text-lg hover:bg-green-700">
          Learn More About Satellite Monitoring
        </button>
      </div>

      <style jsx>{`
        .countdown-animation {
          animation: pulse 1s infinite alternate;
        }
        @keyframes pulse {
          from {
            transform: scale(1);
          }
          to {
            transform: scale(1.05);
          }
        }
      `}</style>
    </div>
  );
};
export default InitialPassDashboard;
