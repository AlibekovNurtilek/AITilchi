import { useState, useEffect } from 'react';

const TypewriterText = ({ text, highlightWord = "", className = "", delay = 80 }) => {
  const [currentIndex, setCurrentIndex] = useState(0);

  useEffect(() => {
    if (currentIndex < text.length) {
      const timer = setTimeout(() => {
        setCurrentIndex(prev => prev + 1);
      }, delay);
      return () => clearTimeout(timer);
    }
  }, [currentIndex, delay, text.length]);

  const renderChar = (char, i) => {
    const isVisible = i <= currentIndex;
    const content = char === " " ? "\u00A0" : char;

    // Проверка, входит ли буква в highlightWord
    const inHighlight =
      highlightWord &&
      i >= text.indexOf(highlightWord) &&
      i < text.indexOf(highlightWord) + highlightWord.length;

    return (
      <span
        key={i}
        className={`inline-block transition-opacity duration-300 ${
          isVisible ? "opacity-100" : "opacity-0"
        } ${inHighlight ? "text-red-500 hover:text-red-400 hover:scale-110" : ""}`}
      >
        {content}
      </span>
    );
  };

  return (
    <span className={className}>
      {text.split("").map((char, i) => renderChar(char, i))}
    </span>
  );
};

export default TypewriterText;
