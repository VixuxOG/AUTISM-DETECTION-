const API_URL = 'http://localhost:5000';

export async function calculateAutismRisk(answers) {
  try {
    const response = await fetch(`${API_URL}/predict`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ answers })
    });
    if (!response.ok) throw new Error('Error with API response');
    return await response.json();
  } catch (error) {
    console.error('Error calculating autism risk:', error);
    return { risk_level: 'Error', risk_score: 0 };
  }
}
