// Define the base API URL, assuming the frontend will communicate with the backend API here.
const API_URL = 'http://localhost:5000';

/**
 * Calculates autism risk by making a POST request to the `/predict` endpoint.
 * @param {Object} answers - An object containing the answers to the screening questions.
 * @returns {Object} - Risk level and risk score calculated by the backend.
 */
export async function calculateAutismRisk(answers) {
  try {
    const response = await fetch(`${API_URL}/predict`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ answers }),
    });
    
    if (!response.ok) {
      throw new Error('Network response was not ok');
    }
    
    return await response.json();
  } catch (error) {
    console.error('Error calculating autism risk:', error);
    throw error;
  }
}

export default calculateAutismRisk;
