import axios from 'axios';
import { TEST_DATA } from '../app/utils/constants';

const BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:5000';
export default async function getStatsWithLeagueID(leagueID, useTestData = false) {
  if (useTestData) return (
    { status: 200, data: TEST_DATA.api_stat }
  );

  try {
    const response = await axios.get(
      `${BASE_URL}/leagueID`, {
      params: { leagueID }, 
      headers: { 'Content-Type': 'application/json' }
    });
    return response;
  } catch (error) {
    console.error('Error fetching stats:', error);
    throw error;
  }
}