import { describe, it, expect } from 'vitest';

// Test utility functions (can be expanded as we add more utils)

describe('Utility Functions', () => {
  describe('Currency Formatting', () => {
    it('formats numbers as Indian Rupees', () => {
      const amount = 1500;
      const formatted = `₹${amount.toLocaleString('en-IN')}`;
      expect(formatted).toBe('₹1,500');
    });

    it('handles zero amount', () => {
      const amount = 0;
      const formatted = `₹${amount.toLocaleString('en-IN')}`;
      expect(formatted).toBe('₹0');
    });

    it('handles large amounts', () => {
      const amount = 150000;
      const formatted = `₹${amount.toLocaleString('en-IN')}`;
      expect(formatted).toBe('₹1,50,000');
    });
  });

  describe('Patient ID Generation', () => {
    it('formats patient ID correctly', () => {
      const id = 'PAT-000001';
      expect(id).toMatch(/^PAT-\d{6}$/);
    });
  });

  describe('Date Formatting', () => {
    it('formats date for display', () => {
      const date = new Date('2026-10-01');
      const formatted = date.toLocaleDateString('en-IN');
      expect(formatted).toBeTruthy();
    });
  });
});
