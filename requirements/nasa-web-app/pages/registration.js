import React, { useState } from 'react';

const RegistrationPage = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [name, setName] = useState('');
  const [isSkippingRegistration, setIsSkippingRegistration] = useState(false);

  const handleSubmit = (e) => {
    e.preventDefault();
    // Handle registration or email subscription logic here
    console.log(isSkippingRegistration ? "Email subscription" : "Full registration", { email, name, password });
  };

  return (
    <div className="min-h-screen bg-green-50 flex items-center justify-center">
      <div className="bg-white p-8 rounded-lg shadow-md w-full max-w-md">
        <h1 className="text-3xl font-bold text-center mb-6">Join Smart Agriculture</h1>
        <form onSubmit={handleSubmit} className="space-y-4">
          {!isSkippingRegistration && (
            <div>
              <label htmlFor="name" className="block text-sm font-medium text-gray-700">Full Name</label>
              <input
                type="text"
                id="name"
                value={name}
                onChange={(e) => setName(e.target.value)}
                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-green-500 focus:ring focus:ring-green-200"
              />
            </div>
          )}
          <div>
            <label htmlFor="email" className="block text-sm font-medium text-gray-700">Email Address</label>
            <input
              type="email"
              id="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
              className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-green-500 focus:ring focus:ring-green-200"
            />
          </div>
          {!isSkippingRegistration && (
            <div>
              <label htmlFor="password" className="block text-sm font-medium text-gray-700">Password</label>
              <input
                type="password"
                id="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-green-500 focus:ring focus:ring-green-200"
              />
            </div>
          )}
          <button type="submit" className="w-full bg-green-500 text-white py-2 px-4 rounded-md hover:bg-green-600 focus:outline-none focus:ring-2 focus:ring-green-500 focus:ring-opacity-50">
            {isSkippingRegistration ? "Subscribe for Updates" : "Create Account"}
          </button>
        </form>
        <p className="mt-4 text-center text-sm text-gray-600">
          {isSkippingRegistration ? (
            <span>Want full access? <button onClick={() => setIsSkippingRegistration(false)} className="text-green-600 hover:text-green-500">Create an account</button></span>
          ) : (
            <span>Just want updates? <button onClick={() => setIsSkippingRegistration(true)} className="text-green-600 hover:text-green-500">Subscribe with email</button></span>
          )}
        </p>
      </div>
    </div>
  );
};

export default RegistrationPage;
