import { create } from 'zustand';

export const useStatsStore = create((set) => ({
  apiStats: null,
  setApiStats: (data) => set({ apiStats: data }),
}));