import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Progress } from '@/components/ui/progress';
import { calculateAutismRisk } from './api';

const questions = [
  { id: 'name_response', text: 'Does your child look at you when you call his/her name?', options: ['always', 'usually', 'sometimes', 'rarely', 'never'] },
  // Add other questions here as needed
];

export default function AutismScreeningTool() {
  const [currentQuestion, setCurrentQuestion] = useState(0);
  const [answers, setAnswers] = useState({});
  const [screeningComplete, setScreeningComplete] = useState(false);
  const [results, setResults] = useState(null);

  const handleAnswer = async (answer) => {
    setAnswers(prev => ({ ...prev, [questions[currentQuestion].id]: answer }));
    if (currentQuestion < questions.length - 1) {
      setCurrentQuestion(currentQuestion + 1);
    } else {
      setScreeningComplete(true);
      const result = await calculateAutismRisk(answers);
      setResults(result);
    }
  };

  return (
    <div className="container">
      {screeningComplete ? (
        <div>Risk Level: {results?.risk_level}</div>
      ) : (
        <div>
          <Progress value={(currentQuestion / questions.length) * 100} />
          <p>{questions[currentQuestion].text}</p>
          {questions[currentQuestion].options.map(option => (
            <Button key={option} onClick={() => handleAnswer(option)}>
              {option}
            </Button>
          ))}
        </div>
      )}
    </div>
  );
}
