import React from 'react';
import Link from 'next/link';

const LandingPage = () => {
  return (
    <div className="min-h-screen bg-green-50">
      <header className="bg-green-600 text-white p-4">
        <div className="container mx-auto flex justify-between items-center">
          <h1 className="text-2xl font-bold">Smart Agriculture</h1>
          <nav>
            <Link href="#features" className="mx-2">Features</Link>
            <Link href="#about" className="mx-2">About</Link>
            <Link href="#contact" className="mx-2">Contact</Link>
          </nav>
        </div>
      </header>

      <main className="container mx-auto mt-8 p-4">
        <section className="text-center mb-12">
          <h2 className="text-4xl font-bold mb-4">Revolutionize Your Farming with Satellite and IoT Insights</h2>
          <p className="text-xl mb-6">Harness the power of Landsat data and local IoT sensors for smarter agricultural decisions.</p>
          <Link href="/onboarding">
          <button className="bg-green-500 text-white px-6 py-2 rounded-full text-lg">Get Started</button>
</Link>

        </section>

        <section id="features" className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-12">
          <div className="bg-white p-6 rounded-lg shadow">
            <h3 className="text-xl font-semibold mb-2">Satellite Data Integration</h3>
            <p>Access Landsat imagery for broad-scale crop health monitoring and analysis.</p>
          </div>
          <div className="bg-white p-6 rounded-lg shadow">
            <h3 className="text-xl font-semibold mb-2">IoT Sensor Network</h3>
            <p>Integrate local sensor data for real-time, precise farm condition monitoring.</p>
          </div>
          <div className="bg-white p-6 rounded-lg shadow">
            <h3 className="text-xl font-semibold mb-2">Comprehensive Insights</h3>
            <p>Get actionable recommendations based on combined satellite and local data analysis.</p>
          </div>
        </section>

        <section id="about" className="bg-white p-8 rounded-lg shadow mb-12">
          <h2 className="text-3xl font-bold mb-4">About Smart Agriculture</h2>
          <p>Smart Agriculture combines cutting-edge satellite technology with local IoT sensors to provide a comprehensive view of your farm. Our platform offers timely, accurate, and actionable insights to optimize farming practices and increase productivity.</p>
        </section>

        <section id="contact" className="text-center">
          <h2 className="text-3xl font-bold mb-4">Ready to Transform Your Farm?</h2>
          <p className="mb-4">Sign up for a free account or try our demo to see how Smart Agriculture can work for you.</p>
          <button className="bg-green-500 text-white px-6 py-2 rounded-full text-lg mr-4">Sign Up</button>
          <button className="bg-blue-500 text-white px-6 py-2 rounded-full text-lg">Try Demo</button>
        </section>
      </main>

      <footer className="bg-green-600 text-white p-4 mt-12">
        <div className="container mx-auto text-center">
          <p>&copy; 2024 Smart Agriculture. All rights reserved.</p>
        </div>
      </footer>
    </div>
  );
};

export default LandingPage;