import { useEffect } from "react";
import { useNavigate } from "react-router-dom";
import TypewriterText from "./TypewriterText";

const WelcomeScreen = () => {
  const navigate = useNavigate();

  useEffect(() => {
    const timer = setTimeout(() => {
      navigate("/home");
    }, 300000);

    return () => clearTimeout(timer);
  }, [navigate]);

  const handleGetStarted = () => {
    navigate("/home");
  };

  return (
    <div className="relative h-screen w-full overflow-hidden">
      {/* 🎥 ВИДЕО-ФОН */}
      <video
        autoPlay
        loop
        muted
        playsInline
        className="absolute top-0 left-0 w-full h-full object-cover z-0"
      >
        <source src="/bg_video.mp4" type="video/mp4" />
        Your browser does not support the video tag.
      </video>

      {/* 💨 Плавающие частицы */}
      <div className="absolute inset-0 z-10">
        {[...Array(20)].map((_, i) => (
          <div
            key={i}
            className="absolute w-2 h-2 bg-white/20 rounded-full animate-float"
            style={{
              left: `${Math.random() * 100}%`,
              top: `${Math.random() * 100}%`,
              animationDelay: `${Math.random() * 5}s`,
              animationDuration: `${5 + Math.random() * 10}s`
            }}
          />
        ))}
      </div>

      {/* Контент */}
      <div className="relative z-20 h-full w-full flex flex-col items-center justify-center">
        <div className="text-center transform transition-all duration-1000 animate-fadeIn">
          <h1 className="text-7xl font-bold text-white tracking-tight">
            <TypewriterText 
              text="AITilchi'ге кош келиңиз!"
              highlightWord="AI"
              className="text-7xl font-bold text-white tracking-tight"
            />
          </h1>
          <p className="mt-4 text-xl text-gray-300 animate-pulse">
            <TypewriterText 
              text="Кыргыз грамматикасына багытталган биринчи тилдик AI" 
              className="inline-block font-bold"
              delay={40}
            />
          </p>
          <button
            onClick={handleGetStarted}
            className="mt-8 px-8 py-3 bg-red-600 text-white rounded-full 
                     transform transition-all duration-300 
                     hover:bg-red-500 hover:scale-105 
                     focus:outline-none focus:ring-2 focus:ring-red-500 focus:ring-opacity-50
                     shadow-lg hover:shadow-red-500/25 text-xl font-bold"
          >
            Баштоо
          </button>
        </div>
      </div>
    </div>
  );
};

export default WelcomeScreen;
