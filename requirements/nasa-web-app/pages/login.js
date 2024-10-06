import { useState } from 'react'; // No need for React import in Next.js 13+

const LoginPage = () => {
  const [isLogin, setIsLogin] = useState(true);
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [name, setName] = useState('');
  const [isSubscription, setIsSubscription] = useState(false);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (isSubscription) {
      console.log("Email subscription", { email });
      // Handle subscription logic
    } else if (isLogin) {
      console.log("Login attempt", { email, password });
      // Handle login logic
      // If successful, you might want to update app state or redirect
    } else {
      console.log("Registration attempt", { name, email, password });
      // Handle registration logic
      // If successful, you might want to update app state or redirect
    }
  };

  return (
    <div className="min-h-screen bg-green-50 flex items-center justify-center">
      <div className="bg-white p-8 rounded-lg shadow-md w-full max-w-md">
        <h1 className="text-3xl font-bold text-center mb-6">
          {isLogin ? 'Login to' : 'Join'} Smart Agriculture
        </h1>
        <form onSubmit={handleSubmit} className="space-y-4">
          {!isLogin && !isSubscription && (
            <div>
              <label htmlFor="name" className="block text-sm font-medium text-gray-700">Full Name</label>
              <input
                type="text"
                id="name"
                value={name}
                onChange={(e) => setName(e.target.value)}
                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-green-500 focus:ring focus:ring-green-200"
                required={!isLogin && !isSubscription}
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
              className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-green-500 focus:ring focus:ring-green-200"
              required
            />
          </div>
          {!isSubscription && (
            <div>
              <label htmlFor="password" className="block text-sm font-medium text-gray-700">Password</label>
              <input
                type="password"
                id="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-green-500 focus:ring focus:ring-green-200"
                required={!isSubscription}
              />
            </div>
          )}
          <button
            type="submit"
            className="w-full bg-green-500 text-white py-2 px-4 rounded-md hover:bg-green-600 focus:outline-none focus:ring-2 focus:ring-green-500 focus:ring-opacity-50"
          >
            {isSubscription ? "Subscribe for Updates" : (isLogin ? "Login" : "Create Account")}
          </button>
        </form>
        <div className="mt-4 text-center text-sm text-gray-600">
          {isSubscription ? (
            <p>
              Want full access?{' '}
              <button onClick={() => setIsSubscription(false)} className="text-green-600 hover:text-green-500">
                {isLogin ? "Login" : "Create an account"}
              </button>
            </p>
          ) : (
            <>
              <p>
                {isLogin ? "Don't have an account?" : "Already have an account?"}{' '}
                <button onClick={() => setIsLogin(!isLogin)} className="text-green-600 hover:text-green-500">
                  {isLogin ? "Sign up" : "Login"}
                </button>
              </p>
              <p className="mt-2">
                Just want updates?{' '}
                <button onClick={() => setIsSubscription(true)} className="text-green-600 hover:text-green-500">
                  Subscribe with email
                </button>
              </p>
            </>
          )}
        </div>
      </div>
    </div>
  );
};

export default LoginPage;
